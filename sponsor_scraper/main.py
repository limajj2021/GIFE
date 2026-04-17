#!/usr/bin/env python3
"""
贊助商聯絡方式蒐集工具
用法：
  python main.py --keywords "台灣運動品牌 贊助" "飲料公司 贊助商" --count 20
  python main.py --urls urls.txt
  python main.py --keywords "品牌 贊助" --no-form     # 跳過表單自動填寫
  python main.py --keywords "品牌 贊助" --visible     # 開啟瀏覽器視窗（除錯用）
"""

import argparse
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# 確保可以 import 同目錄模組
sys.path.insert(0, os.path.dirname(__file__))

import config
from searcher import search_by_keywords, load_from_file
from scraper import scrape_site
from exporter import export_to_excel


def parse_args():
    parser = argparse.ArgumentParser(
        description="自動蒐集贊助商聯絡 Email，並整理成 Excel",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--keywords", "-k", nargs="+", metavar="關鍵字",
        help="搜尋關鍵字，可多個（以空格分隔）",
    )
    group.add_argument(
        "--urls", "-u", metavar="檔案路徑",
        help="從 txt/csv 檔案讀取 URL 清單（每行一個）",
    )
    parser.add_argument(
        "--count", "-n", type=int, default=config.SEARCH_RESULTS_PER_KEYWORD,
        help=f"每個關鍵字取幾筆結果（預設 {config.SEARCH_RESULTS_PER_KEYWORD}）",
    )
    parser.add_argument(
        "--no-form", action="store_true",
        help="跳過自動填寫聯絡表單（只收集 email）",
    )
    parser.add_argument(
        "--visible", action="store_true",
        help="填表單時顯示瀏覽器視窗（除錯用）",
    )
    parser.add_argument(
        "--workers", type=int, default=config.MAX_SCRAPER_WORKERS,
        help=f"並發抓取執行緒數（預設 {config.MAX_SCRAPER_WORKERS}）",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.visible:
        config.PLAYWRIGHT_HEADLESS = False

    # ── Step 1: 取得網址清單 ──────────────────────────────
    if args.keywords:
        entries = search_by_keywords(args.keywords, count=args.count)
    else:
        entries = load_from_file(args.urls)

    if not entries:
        print("[結束] 未取得任何網址，請確認關鍵字或網址檔案。")
        sys.exit(1)

    print(f"\n共 {len(entries)} 個網站待處理\n{'─' * 50}")

    # ── Step 2: 並發抓取 email ────────────────────────────
    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(scrape_site, entry): entry for entry in entries}
        for i, future in enumerate(as_completed(futures), start=1):
            result = future.result()
            results.append(result)
            print(f"  進度：{i}/{len(entries)}", end="\r")

    print(f"\n{'─' * 50}")

    # ── Step 3: 自動填表單（無 email 的網站）────────────────
    pending = [r for r in results if r["status"] == "待填表單"]
    if pending and not args.no_form:
        print(f"\n[填表單] 共 {len(pending)} 個網站需填寫聯絡表單")
        from form_filler import fill_forms
        fill_forms(pending)
        # pending 是 results 的子集（同一物件），狀態已就地更新
    elif pending and args.no_form:
        for r in pending:
            r["status"] = "待填表單（已跳過）"

    # ── Step 4: 輸出 Excel ───────────────────────────────
    filepath = export_to_excel(results)

    # ── 統計摘要 ─────────────────────────────────────────
    from collections import Counter
    counts = Counter(r["status"] for r in results)
    print("\n📊 執行結果統計：")
    for status, count in sorted(counts.items()):
        print(f"   {status:12s} {count} 筆")
    total_emails = sum(len(r.get("emails", [])) for r in results)
    print(f"\n   共蒐集到 {total_emails} 個 Email 地址")
    print(f"   結果檔案：{os.path.abspath(filepath)}\n")


if __name__ == "__main__":
    main()
