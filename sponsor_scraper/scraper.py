"""
對每個網站抓取 email 地址。
策略（依序執行）：
  1. 首頁全文 regex 搜尋
  2. 找聯絡頁面連結，遞迴抓取
  3. mailto: 連結
  4. footer / header 區塊
若找到任何 email 即停止，並回傳聯絡表單頁網址（供 form_filler 備用）。
"""

import re
import time
import random
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

from config import REQUEST_HEADERS, REQUEST_TIMEOUT, REQUEST_DELAY_MIN, REQUEST_DELAY_MAX

EMAIL_RE = re.compile(
    r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
)

# 不要的 email 前綴（常見圖示字型、範例地址）
_SKIP_EMAIL_PREFIXES = ("example", "test@", "user@", "noreply", "no-reply", "donotreply")
_SKIP_EMAIL_DOMAINS = ("example.com", "test.com", "sentry.io", "wixpress.com")

# 聯絡頁面的關鍵字（中英文）
_CONTACT_KEYWORDS = [
    "contact", "聯絡", "联系", "about", "關於", "关于",
    "support", "客服", "help", "service", "info",
]


def _is_valid_email(email: str) -> bool:
    email = email.lower()
    if any(email.startswith(p) for p in _SKIP_EMAIL_PREFIXES):
        return False
    domain = email.split("@")[-1]
    if any(domain == d for d in _SKIP_EMAIL_DOMAINS):
        return False
    # 過濾圖片副檔名誤判
    if domain.endswith((".png", ".jpg", ".gif", ".svg", ".css", ".js")):
        return False
    return True


def _fetch(url: str, session: requests.Session) -> BeautifulSoup | None:
    try:
        resp = session.get(url, timeout=REQUEST_TIMEOUT, headers=REQUEST_HEADERS)
        if resp.status_code == 200:
            return BeautifulSoup(resp.text, "lxml")
        if resp.status_code == 429:
            print(f"  [限速] {url}，等待 10 秒後重試")
            time.sleep(10)
            resp = session.get(url, timeout=REQUEST_TIMEOUT, headers=REQUEST_HEADERS)
            if resp.status_code == 200:
                return BeautifulSoup(resp.text, "lxml")
    except Exception as e:
        print(f"  [失敗] {url}：{e}")
    return None


def _extract_emails_from_soup(soup: BeautifulSoup) -> set[str]:
    emails = set()
    # mailto: 連結
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("mailto:"):
            addr = href[7:].split("?")[0].strip().lower()
            if EMAIL_RE.match(addr) and _is_valid_email(addr):
                emails.add(addr)
    # 全文 regex（去除 HTML 標籤後）
    text = soup.get_text(separator=" ")
    for m in EMAIL_RE.findall(text):
        if _is_valid_email(m.lower()):
            emails.add(m.lower())
    return emails


def _find_contact_links(soup: BeautifulSoup, base_url: str) -> list[str]:
    """找聯絡相關頁面的連結，回傳完整 URL 列表（最多 5 個）。"""
    links = []
    seen = set()
    base_domain = urlparse(base_url).netloc

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        text = (a.get_text() + " " + href).lower()
        if any(kw in text for kw in _CONTACT_KEYWORDS):
            full = urljoin(base_url, href)
            parsed = urlparse(full)
            # 只跟站內連結
            if parsed.netloc == base_domain and full not in seen:
                seen.add(full)
                links.append(full)
                if len(links) >= 5:
                    break
    return links


def _find_contact_form_url(soup: BeautifulSoup, base_url: str) -> str | None:
    """嘗試找出含表單的聯絡頁面網址。"""
    # 先看當前頁面有沒有 form
    if soup.find("form"):
        return base_url
    # 找聯絡頁連結
    for link in _find_contact_links(soup, base_url):
        return link  # 先回傳第一個，form_filler 自己驗證
    return None


def scrape_site(entry: dict) -> dict:
    """
    對單一網站執行 email 抓取。
    輸入：{"url": str, "source_keyword": str}
    輸出：{"url", "company_name", "emails", "contact_form_url", "status"}
    """
    url = entry["url"]
    result = {
        "url": url,
        "source_keyword": entry.get("source_keyword", ""),
        "company_name": urlparse(url).netloc.replace("www.", ""),
        "emails": [],
        "contact_form_url": None,
        "status": "處理中",
    }

    session = requests.Session()
    time.sleep(random.uniform(REQUEST_DELAY_MIN, REQUEST_DELAY_MAX))

    # Step 1: 首頁
    print(f"[抓取] {url}")
    soup = _fetch(url, session)
    if soup is None:
        result["status"] = "無法連線"
        return result

    # 嘗試從 <title> 或 og:site_name 取得公司名
    og_name = soup.find("meta", property="og:site_name")
    if og_name and og_name.get("content"):
        result["company_name"] = og_name["content"].strip()
    elif soup.title:
        result["company_name"] = soup.title.string.strip()[:60] if soup.title.string else result["company_name"]

    emails = _extract_emails_from_soup(soup)
    contact_form_url = _find_contact_form_url(soup, url)

    # Step 2: 追蹤聯絡頁面
    if not emails:
        for link in _find_contact_links(soup, url):
            time.sleep(0.8)
            sub_soup = _fetch(link, session)
            if sub_soup:
                emails |= _extract_emails_from_soup(sub_soup)
                if not contact_form_url and sub_soup.find("form"):
                    contact_form_url = link
            if emails:
                break

    result["emails"] = sorted(emails)
    result["contact_form_url"] = contact_form_url

    if emails:
        result["status"] = "已找到Email"
        print(f"  ✓ 找到 {len(emails)} 個 email：{', '.join(sorted(emails))}")
    elif contact_form_url:
        result["status"] = "待填表單"
        print(f"  → 無 email，找到聯絡表單：{contact_form_url}")
    else:
        result["status"] = "無聯絡方式"
        print(f"  ✗ 無 email 也無聯絡表單")

    return result
