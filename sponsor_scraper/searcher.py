"""
從 Google 搜尋關鍵字，取回潛在贊助商的網址清單。
若 Google 限速，自動切換為讀取本地 urls.txt。
"""

import time
import random
import re
from urllib.parse import urlparse
from config import SEARCH_RESULTS_PER_KEYWORD, REQUEST_DELAY_MIN, REQUEST_DELAY_MAX

# 過濾掉常見的非贊助商網域
_SKIP_DOMAINS = {
    "google", "facebook", "youtube", "instagram", "twitter", "linkedin",
    "wikipedia", "wikimedia", "pinterest", "tiktok", "amazon", "shopee",
    "pchome", "momo", "yahoo", "bing", "baidu", "line",
}


def _is_valid_domain(url: str) -> bool:
    try:
        host = urlparse(url).netloc.lower().replace("www.", "")
        root = host.split(".")[0]
        return root not in _SKIP_DOMAINS
    except Exception:
        return False


def search_by_keywords(keywords: list[str], count: int = SEARCH_RESULTS_PER_KEYWORD) -> list[dict]:
    """
    對每個關鍵字執行 Google 搜尋，回傳去重後的網址列表。
    每項格式：{"url": str, "source_keyword": str}
    """
    try:
        from googlesearch import search as google_search
    except ImportError:
        print("[警告] 找不到 googlesearch-python，請執行: pip install googlesearch-python")
        return []

    results = []
    seen_domains = set()

    for kw in keywords:
        print(f"[搜尋] 關鍵字：{kw}")
        try:
            for url in google_search(kw, num_results=count, lang="zh-tw", sleep_interval=2):
                if not _is_valid_domain(url):
                    continue
                domain = urlparse(url).netloc.lower()
                if domain in seen_domains:
                    continue
                seen_domains.add(domain)
                # 只保留首頁
                base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
                results.append({"url": base_url, "source_keyword": kw})
            delay = random.uniform(REQUEST_DELAY_MIN, REQUEST_DELAY_MAX)
            time.sleep(delay)
        except Exception as e:
            print(f"[錯誤] 搜尋關鍵字「{kw}」失敗：{e}")
            print("[提示] 若 Google 封鎖，請改用 --urls 參數指定 urls.txt")

    print(f"[搜尋完成] 共取得 {len(results)} 個不重複網域")
    return results


def load_from_file(filepath: str) -> list[dict]:
    """
    從 txt 或 csv 讀取 URL 清單（每行一個 URL）。
    回傳格式與 search_by_keywords 相同。
    """
    results = []
    seen = set()
    url_pattern = re.compile(r"https?://[^\s,]+")

    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # 支援 csv（取第一欄）或純 txt
            match = url_pattern.search(line)
            raw = match.group(0) if match else line.split(",")[0].strip()
            if not raw.startswith("http"):
                raw = "https://" + raw
            domain = urlparse(raw).netloc.lower()
            if domain in seen or not domain:
                continue
            seen.add(domain)
            base_url = f"{urlparse(raw).scheme}://{urlparse(raw).netloc}"
            results.append({"url": base_url, "source_keyword": "manual"})

    print(f"[讀取] 從 {filepath} 載入 {len(results)} 個網址")
    return results
