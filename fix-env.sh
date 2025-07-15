#!/bin/bash

# 修復 X Bot NTF 環境變數問題腳本
# 此腳本會檢查並修復常見的環境變數配置問題

echo "🔧 X Bot NTF 環境變數修復腳本"
echo "================================"

# 檢查是否在專案目錄中
if [ ! -f "bot.py" ]; then
    echo "❌ 錯誤：請在 x-bot-ntf 專案根目錄中執行此腳本"
    exit 1
fi

# 檢查 .env 文件是否存在
if [ ! -f ".env" ]; then
    echo "📝 創建 .env 文件..."
    cp .env.example .env 2>/dev/null || cat << 'EOF' > .env
# Discord Bot Token (必需)
BOT_TOKEN=你的_Discord_Bot_Token

# Gemini AI API Key (翻譯功能必需)
GEMINI_API_KEY=你的_Gemini_API_Key

# 數據存儲路徑 (必需)
DATA_PATH=./data

# Twitter/X Token (翻譯模式可設為假值避免啟動警告)
TWITTER_TOKEN=DummyAccount:dummy_token_placeholder
EOF
    echo "✅ 已創建 .env 文件，請編輯並填入正確的值"
else
    echo "📁 發現現有 .env 文件"
fi

# 檢查必需的環境變數
echo ""
echo "🔍 檢查環境變數配置..."

# 讀取 .env 文件
source .env 2>/dev/null

# 檢查 BOT_TOKEN
if [ -z "$BOT_TOKEN" ] || [ "$BOT_TOKEN" = "你的_Discord_Bot_Token" ]; then
    echo "⚠️  警告：BOT_TOKEN 未設置或為默認值"
    echo "   請在 .env 文件中設置正確的 Discord Bot Token"
fi

# 檢查 GEMINI_API_KEY
if [ -z "$GEMINI_API_KEY" ] || [ "$GEMINI_API_KEY" = "你的_Gemini_API_Key" ]; then
    echo "⚠️  警告：GEMINI_API_KEY 未設置或為默認值"
    echo "   請在 .env 文件中設置正確的 Gemini AI API Key"
fi

# 檢查 TWITTER_TOKEN
if [ -z "$TWITTER_TOKEN" ]; then
    echo "🔧 添加默認 TWITTER_TOKEN 以避免啟動警告..."
    echo "TWITTER_TOKEN=DummyAccount:dummy_token_placeholder" >> .env
    echo "✅ 已添加默認 TWITTER_TOKEN"
fi

# 檢查 DATA_PATH
if [ -z "$DATA_PATH" ]; then
    echo "🔧 添加 DATA_PATH..."
    echo "DATA_PATH=./data" >> .env
    echo "✅ 已添加 DATA_PATH"
fi

# 檢查 configs.yml
echo ""
echo "🔍 檢查 configs.yml 配置..."

if [ ! -f "configs.yml" ]; then
    if [ -f "configs.example.yml" ]; then
        echo "📝 從示例文件創建 configs.yml..."
        cp configs.example.yml configs.yml
        echo "✅ 已創建 configs.yml，請檢查翻譯相關設置"
    else
        echo "❌ 錯誤：找不到 configs.yml 或 configs.example.yml"
        exit 1
    fi
fi

# 檢查翻譯配置
if grep -q "auto_translate_channels" configs.yml; then
    echo "✅ 發現翻譯配置"
else
    echo "⚠️  警告：未發現翻譯配置，請檢查 configs.yml 中的 translation 區段"
fi

# 創建數據目錄
if [ ! -d "data" ]; then
    echo "📁 創建數據目錄..."
    mkdir -p data
    echo "✅ 已創建 data 目錄"
fi

echo ""
echo "🐳 重新啟動 Docker 容器..."

# 檢查使用哪個 docker compose 指令
if command -v docker-compose >/dev/null 2>&1; then
    DOCKER_COMPOSE_CMD="docker-compose"
elif docker compose version >/dev/null 2>&1; then
    DOCKER_COMPOSE_CMD="docker compose"
else
    echo "❌ 錯誤：找不到 docker-compose 或 docker compose 指令"
    echo "請確保 Docker 已正確安裝"
    echo "📖 安裝指南: https://docs.docker.com/engine/install/"
    exit 1
fi

echo "🔍 使用 Docker Compose 指令: $DOCKER_COMPOSE_CMD"

# 停止現有容器
$DOCKER_COMPOSE_CMD down 2>/dev/null

# 重新構建並啟動
$DOCKER_COMPOSE_CMD up -d --build

echo ""
echo "✅ 修復完成！"
echo ""
echo "📋 接下來的步驟："
echo "1. 編輯 .env 文件，填入正確的 Discord Bot Token 和 Gemini API Key"
echo "2. 檢查 configs.yml 中的翻譯頻道設置"
echo "3. 使用以下指令管理服務："
echo ""
echo "🔗 查看日誌: docker compose logs -f"
echo "🔄 重啟服務: docker compose restart"
echo "⏹️  停止服務: docker compose down"
echo "🚀 啟動服務: docker compose up -d"
