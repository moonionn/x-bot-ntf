#!/bin/bash

# X Bot 一鍵更新腳本
# 在 VM 上執行此腳本來更新 Bot 到最新版本

echo "🔄 開始更新 X Bot 通知系統..."

# 檢查是否在正確的目錄
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ 錯誤：請在 x-bot-ntf 目錄中執行此腳本"
    exit 1
fi

# 備份當前配置
echo "💾 備份配置文件..."
cp configs.yml configs.yml.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null
cp .env .env.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null

# 備份資料庫
if [ -d "data" ]; then
    echo "💾 備份資料庫..."
    tar -czf "data_backup_$(date +%Y%m%d_%H%M%S).tar.gz" data/
fi

# 拉取最新代碼
echo "📥 拉取最新代碼..."
git stash  # 暫存本地修改
git pull origin main

if [ $? -ne 0 ]; then
    echo "❌ Git 拉取失敗，請檢查網路連線或解決衝突"
    exit 1
fi

# 恢復配置文件（如果被覆蓋）
echo "🔧 檢查配置文件..."

# 檢查 configs.yml 是否存在，不存在才恢復備份
if [ ! -f "configs.yml" ]; then
    config_backups=$(ls configs.yml.backup.* 2>/dev/null | wc -l)
    if [ "$config_backups" -gt 0 ]; then
        latest_config=$(ls -t configs.yml.backup.* | head -1)
        cp "$latest_config" configs.yml
        echo "✅ 已恢復配置文件: $latest_config"
    fi
else
    echo "ℹ️  使用新版本的配置文件"
fi

# 檢查 .env 是否存在，不存在才恢復備份
if [ ! -f ".env" ]; then
    env_backups=$(ls .env.backup.* 2>/dev/null | wc -l)
    if [ "$env_backups" -gt 0 ]; then
        latest_env=$(ls -t .env.backup.* | head -1)
        cp "$latest_env" .env
        echo "✅ 已恢復環境變數文件: $latest_env"
    fi
else
    echo "ℹ️  使用新版本的環境變數文件"
fi

# 重新構建 Docker 映像
echo "🔨 重新構建 Docker 映像..."
docker compose build --no-cache

if [ $? -ne 0 ]; then
    echo "❌ Docker 構建失敗"
    exit 1
fi

# 重新啟動服務
echo "🚀 重新啟動服務..."
docker compose down
docker compose up -d

# 等待服務啟動
echo "⏳ 等待服務啟動..."
sleep 10

# 檢查服務狀態
echo "🔍 檢查服務狀態..."
docker compose ps

# 顯示日誌
echo ""
echo "📋 最新日誌："
docker compose logs --tail 20

echo ""
echo "✅ 更新完成！"
echo ""
echo "🔧 有用的命令："
echo "  查看即時日誌: docker compose logs -f"
echo "  查看服務狀態: docker compose ps"
echo "  重啟服務: docker compose restart"
echo ""
echo "💾 備份文件位置："
ls -la *.backup.* data_backup_*.tar.gz 2>/dev/null || echo "  無備份文件"
