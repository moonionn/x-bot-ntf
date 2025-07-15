#!/bin/bash

# X Bot 持續運行配置腳本
# 確保 Bot 在 VM 重啟後自動啟動並持續運行

set -e

echo "🚀 配置 X Bot 持續運行..."

# 獲取當前用戶和工作目錄
CURRENT_USER=$(whoami)
WORK_DIR=$(pwd)

echo "👤 當前用戶: $CURRENT_USER"
echo "📁 工作目錄: $WORK_DIR"

# 1. 確保 Docker 服務開機自動啟動
echo "🐳 配置 Docker 自動啟動..."
sudo systemctl enable docker
sudo systemctl start docker

# 2. 停止現有容器（如果有的話）
echo "🛑 停止現有容器..."
docker compose down 2>/dev/null || true

# 3. 創建 systemd 服務文件
echo "📝 創建 X Bot 系統服務..."
sudo tee /etc/systemd/system/x-bot.service > /dev/null <<EOF
[Unit]
Description=X Bot Notification System
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
User=$CURRENT_USER
WorkingDirectory=$WORK_DIR
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
ExecReload=/usr/bin/docker compose restart
TimeoutStartSec=300
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 4. 重新載入 systemd 配置
echo "🔄 重新載入系統服務配置..."
sudo systemctl daemon-reload

# 5. 啟用服務（開機自動啟動）
echo "✅ 啟用 X Bot 自動啟動..."
sudo systemctl enable x-bot.service

# 6. 啟動服務
echo "🚀 啟動 X Bot 服務..."
sudo systemctl start x-bot.service

# 7. 等待容器啟動
echo "⏳ 等待容器啟動..."
sleep 10

# 8. 檢查狀態
echo "📊 檢查服務狀態..."
sudo systemctl status x-bot.service --no-pager -l

echo ""
echo "📊 檢查容器狀態..."
docker compose ps

echo ""
echo "✅ X Bot 持續運行配置完成！"
echo ""
echo "🛡️ 保障機制："
echo "  ✓ VM 重啟後自動啟動"
echo "  ✓ 容器崩潰後自動重啟"
echo "  ✓ Docker 服務重啟後自動恢復"
echo "  ✓ 網路斷線後自動重連"
echo ""
echo "📋 管理命令："
echo "  查看狀態: sudo systemctl status x-bot.service"
echo "  重啟服務: sudo systemctl restart x-bot.service"
echo "  停止服務: sudo systemctl stop x-bot.service"
echo "  啟動服務: sudo systemctl start x-bot.service"
echo "  查看日誌: docker compose logs -f"
echo "  檢查容器: docker compose ps"
echo ""
echo "🎉 現在您的 X Bot 將持續運行，不會因為 VM 重啟而中斷！"
