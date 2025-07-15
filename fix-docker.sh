#!/bin/bash

# 快速修復 Docker 安裝問題的腳本
# 專為 Debian 系統設計

echo "🔧 修復 Docker 安裝問題..."

# 移除可能有問題的 Docker 倉庫
sudo rm -f /etc/apt/sources.list.d/docker.list

# 清理 apt 快取
sudo apt-get clean
sudo apt-get update

# 重新添加正確的 Docker 倉庫 (Debian)
echo "📦 添加 Debian Docker 倉庫..."

# 添加 Docker 官方 GPG 密鑰
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 獲取 Debian 版本代號
CODENAME=$(lsb_release -cs)
echo "🔍 檢測到 Debian 版本: $CODENAME"

# 設置正確的 Debian Docker 倉庫
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $CODENAME stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 更新套件列表
sudo apt-get update

# 安裝 Docker
echo "🐳 安裝 Docker..."
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 啟動 Docker 服務
sudo systemctl start docker
sudo systemctl enable docker

# 將當前用戶添加到 docker 組
sudo usermod -aG docker $USER

echo "✅ Docker 安裝完成！"
echo "⚠️  請重新登錄或執行 'newgrp docker' 以應用群組變更"

# 檢查 Docker 版本
docker --version
docker compose version

echo ""
echo "🚀 現在可以繼續部署 X Bot："
echo "   ./deploy.sh"
