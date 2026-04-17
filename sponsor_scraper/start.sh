#!/bin/bash
# 啟動贊助商蒐集工具網頁介面 + 公開 Tunnel
# 用法：
#   bash start.sh                          # port 5000，自動 quick tunnel
#   bash start.sh 5000 <CF_TUNNEL_TOKEN>   # 使用 Cloudflare 命名 tunnel

PORT=${1:-5000}
CF_TOKEN="${2:-${CF_TUNNEL_TOKEN:-}}"     # 可由參數或環境變數 CF_TUNNEL_TOKEN 傳入
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "======================================"
echo "  贊助商聯絡蒐集工具  v1.0"
echo "======================================"
cd "$SCRIPT_DIR"

# ── 1. 安裝 Python 依賴 ────────────────────────────────────────
echo "[1/3] 檢查 Python 依賴..."
pip install -r requirements.txt -q --ignore-installed 2>/dev/null || \
pip install -r requirements.txt -q 2>/dev/null

# ── 2. 啟動 Flask ──────────────────────────────────────────────
mkdir -p output
echo "[2/3] 啟動 Flask (port $PORT)..."
python3 app.py &
FLASK_PID=$!
sleep 2

# 確認 Flask 存活
if ! kill -0 $FLASK_PID 2>/dev/null; then
  echo "[錯誤] Flask 啟動失敗，請確認 port $PORT 未被占用"
  exit 1
fi

# 取得本機 IP（方便區網存取）
LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  本機網址（同一 WiFi/網路可用）："
echo "  http://${LOCAL_IP}:${PORT}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── 3. 嘗試建立公開 Tunnel ────────────────────────────────────
echo "[3/3] 嘗試建立公開 Tunnel..."

CF_PID=""
tunnel_started=false

# 方法 A：cloudflared 命名 tunnel（有 token，最穩定）
if command -v cloudflared &>/dev/null && [ -n "$CF_TOKEN" ]; then
  echo "  → 使用 Cloudflare 命名 Tunnel（token 模式）..."
  cloudflared tunnel run --token "$CF_TOKEN" 2>&1 | \
    grep --line-buffered -E "INF|ERR|Registered" &
  CF_PID=$!
  sleep 10
  if kill -0 $CF_PID 2>/dev/null; then
    tunnel_started=true
    echo ""
    echo "  ✓ Tunnel 已啟動！請至 Cloudflare Zero Trust Dashboard 查看公開網址"
    echo "  (dash.cloudflare.com → Zero Trust → Networks → Tunnels)"
  fi
fi

# 方法 B：cloudflared quick tunnel（免帳號）
if ! $tunnel_started && command -v cloudflared &>/dev/null; then
  echo "  → 使用 Cloudflare Quick Tunnel（免帳號）..."
  cloudflared tunnel --url "http://localhost:$PORT" --protocol http2 2>&1 | \
    grep --line-buffered -E "trycloudflare|quick Tunnel" &
  CF_PID=$!
  sleep 12
  if kill -0 $CF_PID 2>/dev/null; then
    tunnel_started=true
    echo ""
    echo "  公開網址如上方所示（https://xxxxx.trycloudflare.com）"
  fi
fi

# 方法 B：ngrok（需先 ngrok config add-authtoken <token>）
if ! $tunnel_started && command -v ngrok &>/dev/null; then
  echo "  → 嘗試 ngrok..."
  ngrok http $PORT --log=stdout 2>&1 &
  CF_PID=$!
  sleep 6
  PUBLIC_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | \
    python3 -c "import sys,json; d=json.load(sys.stdin); [print(t['public_url']) for t in d.get('tunnels',[]) if t.get('proto')=='https']" 2>/dev/null)
  if [ -n "$PUBLIC_URL" ]; then
    tunnel_started=true
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  公開網址（ngrok）："
    echo "  $PUBLIC_URL"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  fi
fi

if ! $tunnel_started; then
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  [提示] 公開 Tunnel 無法在此環境建立"
  echo "  （cloudflared 需要 port 7844 開通）"
  echo ""
  echo "  解決方法："
  echo "  1. 在自己的電腦/VPS 執行此腳本"
  echo "  2. 帶入 Cloudflare Tunnel token："
  echo "     bash start.sh 5000 <eyJ...token>"
  echo "  3. 或用 ngrok："
  echo "     ngrok config add-authtoken <token>"
  echo ""
  echo "  本機仍可使用：http://${LOCAL_IP}:${PORT}"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
fi

echo ""
echo "按 Ctrl+C 停止服務"

# ── 清理 ──────────────────────────────────────────────────────
cleanup() {
  echo ""
  echo "正在關閉..."
  [ -n "$CF_PID" ] && kill $CF_PID 2>/dev/null
  kill $FLASK_PID 2>/dev/null
  exit 0
}
trap cleanup INT TERM
wait $FLASK_PID
