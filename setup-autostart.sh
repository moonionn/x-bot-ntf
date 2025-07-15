#!/bin/bash

# 創建系統服務讓 X Bot 自動啟動
# 在 VM 上執行此腳本

echo "🔧 設置 X Bot 自動啟動服務..."

# 創建 systemd 服務文件
sudo tee /etc/systemd/system/x-bot.service > /dev/null << EOF
[Unit]
Description=X Bot Notification System
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/$USER/x-bot-ntf
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
User=$USER
Group=$USER

[Install]
WantedBy=multi-user.target
EOF

# 重新載入 systemd
sudo systemctl daemon-reload

# 啟用服務（開機自動啟動）
sudo systemctl enable x-bot.service

# 啟動服務
sudo systemctl start x-bot.service

echo "✅ X Bot 自動啟動服務已設置完成！"
echo ""
echo "🔧 管理命令："
echo "  查看狀態: sudo systemctl status x-bot"
echo "  啟動服務: sudo systemctl start x-bot"
echo "  停止服務: sudo systemctl stop x-bot"
echo "  重啟服務: sudo systemctl restart x-bot"
echo "  查看日誌: sudo journalctl -u x-bot -f"
