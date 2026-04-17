"""
Flask 網頁伺服器 — 贊助商聯絡蒐集工具
提供：
  GET  /              → 主頁面
  POST /api/start     → 開始任務（關鍵字或上傳 URL 清單）
  GET  /api/stream/<job_id>  → SSE 即時進度
  GET  /api/results/<job_id> → 取得任務結果 JSON
  GET  /api/download/<job_id>→ 下載 Excel
"""

import os
import sys
import uuid
import json
import queue
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import Flask, request, jsonify, send_file, render_template, Response, stream_with_context

sys.path.insert(0, os.path.dirname(__file__))
import config

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB 上傳限制

# 全域任務狀態存儲
_jobs: dict[str, dict] = {}
_job_lock = threading.Lock()


def _new_job(job_id: str, total: int = 0) -> dict:
    return {
        "id": job_id,
        "status": "running",  # running | done | error
        "total": total,
        "done": 0,
        "results": [],
        "excel_path": None,
        "log_queue": queue.Queue(),
        "created_at": time.time(),
    }


def _emit(job: dict, msg_type: str, data: dict):
    """推送一筆 SSE 事件到該任務的 queue。"""
    job["log_queue"].put({"type": msg_type, "data": data})


# ─── 核心工作流程（在背景 thread 執行）────────────────────────────────────────

def _run_job(job_id: str, entries: list[dict], no_form: bool, workers: int):
    job = _jobs[job_id]

    def log(text: str):
        _emit(job, "log", {"text": text})

    try:
        log(f"開始處理 {len(job['total'])} ... ")

        # Step 1: 並發抓取 email
        results: list[dict] = []
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(_scrape_with_log, entry, job): entry for entry in entries}
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                with _job_lock:
                    job["done"] += 1
                    job["results"] = results[:]
                _emit(job, "progress", {
                    "done": job["done"],
                    "total": job["total"],
                    "latest": {
                        "url": result["url"],
                        "company": result["company_name"],
                        "emails": result["emails"],
                        "status": result["status"],
                    }
                })

        # Step 2: 填表單
        pending = [r for r in results if r["status"] == "待填表單"]
        if pending and not no_form:
            log(f"找到 {len(pending)} 個網站需填聯絡表單，開始自動填寫...")
            from form_filler import fill_forms
            fill_forms(pending)
            for r in pending:
                _emit(job, "form_done", {"url": r["url"], "status": r["status"]})

        # Step 3: 輸出 Excel
        from exporter import export_to_excel
        filepath = export_to_excel(results)
        with _job_lock:
            job["excel_path"] = filepath
            job["results"] = results
            job["status"] = "done"

        from collections import Counter
        counts = Counter(r["status"] for r in results)
        total_emails = sum(len(r.get("emails", [])) for r in results)
        _emit(job, "done", {
            "summary": dict(counts),
            "total_emails": total_emails,
            "excel_ready": True,
        })

    except Exception as e:
        with _job_lock:
            job["status"] = "error"
        _emit(job, "error", {"message": str(e)})
    finally:
        job["log_queue"].put(None)  # 結束訊號


def _scrape_with_log(entry: dict, job: dict) -> dict:
    from scraper import scrape_site
    result = scrape_site(entry)
    return result


# ─── Flask 路由 ──────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/start", methods=["POST"])
def start_job():
    from searcher import search_by_keywords, load_from_file

    mode = request.form.get("mode", "keywords")
    no_form = request.form.get("no_form", "false").lower() == "true"
    workers = min(int(request.form.get("workers", config.MAX_SCRAPER_WORKERS)), 10)
    count = min(int(request.form.get("count", config.SEARCH_RESULTS_PER_KEYWORD)), 100)

    if mode == "keywords":
        raw = request.form.get("keywords", "").strip()
        if not raw:
            return jsonify({"error": "請輸入搜尋關鍵字"}), 400
        keywords = [k.strip() for k in raw.splitlines() if k.strip()]
        entries = search_by_keywords(keywords, count=count)
    else:
        f = request.files.get("url_file")
        if not f:
            return jsonify({"error": "請上傳 URL 清單檔案"}), 400
        import tempfile
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="wb")
        f.save(tmp.name)
        tmp.close()
        entries = load_from_file(tmp.name)
        os.unlink(tmp.name)

    if not entries:
        return jsonify({"error": "未取得任何有效網址，請確認關鍵字或檔案內容"}), 400

    job_id = str(uuid.uuid4())
    job = _new_job(job_id, total=len(entries))
    job["total"] = len(entries)
    with _job_lock:
        _jobs[job_id] = job

    thread = threading.Thread(
        target=_run_job,
        args=(job_id, entries, no_form, workers),
        daemon=True,
    )
    thread.start()

    return jsonify({"job_id": job_id, "total": len(entries)})


@app.route("/api/stream/<job_id>")
def stream(job_id: str):
    job = _jobs.get(job_id)
    if not job:
        return jsonify({"error": "找不到任務"}), 404

    def generate():
        q = job["log_queue"]
        while True:
            try:
                msg = q.get(timeout=30)
                if msg is None:
                    yield "data: {\"type\":\"end\"}\n\n"
                    break
                yield f"data: {json.dumps(msg, ensure_ascii=False)}\n\n"
            except queue.Empty:
                yield "data: {\"type\":\"ping\"}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.route("/api/results/<job_id>")
def get_results(job_id: str):
    job = _jobs.get(job_id)
    if not job:
        return jsonify({"error": "找不到任務"}), 404
    results = [
        {k: v for k, v in r.items() if k != "log_queue"}
        for r in job.get("results", [])
    ]
    return jsonify({
        "status": job["status"],
        "done": job["done"],
        "total": job["total"],
        "results": results,
        "excel_ready": job["excel_path"] is not None,
    })


@app.route("/api/download/<job_id>")
def download(job_id: str):
    job = _jobs.get(job_id)
    if not job or not job.get("excel_path"):
        return jsonify({"error": "Excel 尚未產生"}), 404
    return send_file(
        job["excel_path"],
        as_attachment=True,
        download_name=os.path.basename(job["excel_path"]),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


if __name__ == "__main__":
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
