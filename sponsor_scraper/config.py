# 使用者資訊設定 — 填寫聯絡表單時使用
USER_INFO = {
    "name": "王小明",           # 姓名
    "company": "XX 活動公司",   # 公司/組織名稱
    "email": "contact@example.com",  # 你的 email（收回覆用）
    "phone": "0912-345-678",   # 電話（選填）
    "subject": "贊助合作洽詢", # 信件主旨
    "message": (
        "您好，\n\n"
        "我們正在籌辦一項活動，希望能與貴公司洽談贊助合作事宜。\n"
        "請問是否有機會進一步討論？\n\n"
        "期待您的回覆，謝謝！\n\n"
        "敬祝商祺"
    ),
}

# 搜尋設定
SEARCH_RESULTS_PER_KEYWORD = 20   # 每個關鍵字最多取幾筆搜尋結果
REQUEST_DELAY_MIN = 1.5           # 請求間最小延遲（秒）
REQUEST_DELAY_MAX = 4.0           # 請求間最大延遲（秒）
MAX_SCRAPER_WORKERS = 5           # 並發抓取 email 的執行緒數

# HTTP 請求設定
REQUEST_TIMEOUT = 10              # 單次請求逾時（秒）
REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
}

# Playwright 設定
PLAYWRIGHT_HEADLESS = True        # True = 不顯示瀏覽器視窗
FORM_FILL_DELAY = 0.3             # 填欄位之間的延遲（秒）

# 輸出設定
OUTPUT_DIR = "output"
