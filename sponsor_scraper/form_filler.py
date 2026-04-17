"""
使用 Playwright 自動填寫並送出網站聯絡表單。
欄位辨識邏輯：以 name / placeholder / label / id 屬性關鍵字推斷欄位用途。
"""

import time
import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

from config import USER_INFO, PLAYWRIGHT_HEADLESS, FORM_FILL_DELAY

# 欄位用途關鍵字對應表（中英文）
_FIELD_HINTS = {
    "name": ["name", "姓名", "名字", "full_name", "your_name", "fullname", "contact_name"],
    "company": ["company", "organization", "org", "公司", "組織", "機構", "firm"],
    "email": ["email", "mail", "e-mail", "信箱", "電子郵件", "電郵"],
    "phone": ["phone", "tel", "mobile", "電話", "手機", "聯絡電話"],
    "subject": ["subject", "title", "主旨", "標題", "主題"],
    "message": ["message", "body", "content", "comment", "內容", "訊息", "留言", "備註"],
}


def _guess_field_type(attrs: dict) -> str | None:
    combined = " ".join(str(v) for v in attrs.values()).lower()
    for field_type, hints in _FIELD_HINTS.items():
        if any(h in combined for h in hints):
            return field_type
    return None


async def _fill_form(page, form_url: str) -> str:
    """
    在指定頁面嘗試填寫並送出表單。
    回傳狀態字串：'已填表單' / '需手動處理' / '填表失敗'
    """
    try:
        await page.goto(form_url, timeout=20000, wait_until="domcontentloaded")
    except PlaywrightTimeout:
        return "填表失敗"

    # 偵測 CAPTCHA
    content = await page.content()
    if any(kw in content.lower() for kw in ["recaptcha", "hcaptcha", "captcha", "turnstile"]):
        print(f"  [CAPTCHA] {form_url} — 需手動處理")
        return "需手動處理"

    # 找表單
    form = page.locator("form").first
    try:
        await form.wait_for(timeout=5000)
    except PlaywrightTimeout:
        return "填表失敗"

    filled_any = False

    # 處理 input 和 textarea
    for tag in ["input", "textarea"]:
        elements = await page.locator(f"form {tag}").all()
        for el in elements:
            try:
                input_type = (await el.get_attribute("type") or "text").lower()
                if input_type in ("hidden", "submit", "button", "reset", "checkbox", "radio", "file"):
                    continue
                if not await el.is_visible():
                    continue

                attrs = {
                    "name": await el.get_attribute("name") or "",
                    "id": await el.get_attribute("id") or "",
                    "placeholder": await el.get_attribute("placeholder") or "",
                    "class": await el.get_attribute("class") or "",
                }
                # 嘗試找對應 label
                el_id = attrs["id"]
                if el_id:
                    label_el = page.locator(f'label[for="{el_id}"]')
                    if await label_el.count() > 0:
                        attrs["label"] = await label_el.first.inner_text()

                field_type = _guess_field_type(attrs)
                value = USER_INFO.get(field_type or "", "")

                if not value and tag == "textarea":
                    value = USER_INFO["message"]

                if value:
                    await el.fill(str(value))
                    filled_any = True
                    await asyncio.sleep(FORM_FILL_DELAY)

            except Exception:
                continue

    if not filled_any:
        return "填表失敗"

    # 找送出按鈕
    submit = None
    for selector in [
        'form button[type="submit"]',
        'form input[type="submit"]',
        'form button:not([type="button"])',
        'button:has-text("送出")', 'button:has-text("submit")',
        'button:has-text("傳送")', 'button:has-text("send")',
    ]:
        loc = page.locator(selector).first
        if await loc.count() > 0 and await loc.is_visible():
            submit = loc
            break

    if submit is None:
        return "需手動處理"

    try:
        await submit.click()
        await asyncio.sleep(2)  # 等候送出後的頁面回應
        print(f"  ✓ 表單已送出：{form_url}")
        return "已填表單"
    except Exception as e:
        print(f"  [錯誤] 無法送出表單 {form_url}：{e}")
        return "填表失敗"


async def fill_forms_async(pending: list[dict]) -> list[dict]:
    """
    對所有 status='待填表單' 的條目執行 form_filler。
    直接修改並回傳同一份 list。
    """
    if not pending:
        return pending

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=PLAYWRIGHT_HEADLESS)
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )
        page = await context.new_page()

        for entry in pending:
            form_url = entry.get("contact_form_url")
            if not form_url:
                entry["status"] = "無聯絡方式"
                continue
            print(f"[填表單] {entry['url']}")
            status = await _fill_form(page, form_url)
            entry["status"] = status
            await asyncio.sleep(2)

        await browser.close()

    return pending


def fill_forms(pending: list[dict]) -> list[dict]:
    """同步包裝，供 main.py 直接呼叫。"""
    return asyncio.run(fill_forms_async(pending))
