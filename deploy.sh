#!/bin/bash

# X Bot 部署腳本
# 適用於 Google Cloud VM 部署

set -e

echo "🚀 開始部署 X Bot 通知系統..."

# 檢查是否安裝 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ 未安裝 Docker，正在安裝..."
    
    # 更新系統
    sudo apt-get update
    
    # 安裝必要的依賴
    sudo apt-get install -y \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    
    # 檢測 Linux 發行版
    if [ -f /etc/debian_version ]; then
        DISTRO="debian"
        CODENAME=$(lsb_release -cs)
    elif [ -f /etc/lsb-release ]; then
        DISTRO="ubuntu"
        CODENAME=$(lsb_release -cs)
    else
        echo "❌ 不支援的 Linux 發行版"
        exit 1
    fi
    
    echo "🔍 檢測到系統: $DISTRO $CODENAME"
    
    # 添加 Docker 官方 GPG 密鑰
    sudo mkdir -m 0755 -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/${DISTRO}/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    
    # 設置穩定版本倉庫
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/${DISTRO} \
      ${CODENAME} stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # 安裝 Docker
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    # 啟動 Docker 服務
    sudo systemctl start docker
    sudo systemctl enable docker
    
    # 將當前用戶添加到 docker 組
    sudo usermod -aG docker $USER
    
    echo "✅ Docker 安裝完成"
fi

# 檢查是否安裝 Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "⚠️  未找到 docker-compose，嘗試使用 docker compose..."
    if ! docker compose version &> /dev/null; then
        echo "❌ Docker Compose 不可用，請手動安裝"
        exit 1
    fi
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

# 創建必要的目錄
mkdir -p data
mkdir -p logs

# 檢查必要的配置文件
if [ ! -f "configs.yml" ]; then
    echo "⚠️  未找到 configs.yml，正在從範例複製..."
    if [ -f "configs.example.yml" ]; then
        cp configs.example.yml configs.yml
        echo "📝 請編輯 configs.yml 文件設置您的配置"
    else
        echo "❌ 未找到配置範例文件"
        exit 1
    fi
fi

if [ ! -f ".env" ]; then
    echo "⚠️  未找到 .env 文件，正在創建範例..."
    cat > .env << EOF
# Discord Bot Token
BOT_TOKEN=your_discord_bot_token_here

# X/Twitter API 配置 (需要至少一組)
CLIENT_1_BEARER_TOKEN=your_bearer_token_here
CLIENT_1_API_KEY=your_api_key_here
CLIENT_1_API_SECRET=your_api_secret_here

# Gemini AI API Key (用於翻譯功能)
GEMINI_API_KEY=your_gemini_api_key_here

# 資料路徑
DATA_PATH=/app/data
EOF
    echo "📝 請編輯 .env 文件設置您的環境變數"
fi

# 設置正確的權限
chmod 600 .env
chmod 644 configs.yml

echo "🔨 構建 Docker 映像..."
$DOCKER_COMPOSE build

echo "🚀 啟動服務..."
$DOCKER_COMPOSE up -d

echo "✅ 部署完成！"
echo ""
echo "📋 有用的命令："
echo "  查看日誌: $DOCKER_COMPOSE logs -f"
echo "  停止服務: $DOCKER_COMPOSE down"
echo "  重啟服務: $DOCKER_COMPOSE restart"
echo "  更新代碼: git pull && $DOCKER_COMPOSE build && $DOCKER_COMPOSE up -d"
echo ""
echo "🔧 配置提醒："
echo "  - 請確保已正確設置 .env 文件中的 API 金鑰"
echo "  - 請確保已正確設置 configs.yml 文件中的配置"
echo "  - 建議設置防火牆規則保護您的服務"
