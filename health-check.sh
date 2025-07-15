#!/bin/bash

# X Bot 健康檢查和自動重啟腳本
# 建議設置為 cron 任務每 5 分鐘執行一次

LOG_FILE="/home/$USER/x-bot-health.log"
BOT_DIR="/home/$USER/x-bot-ntf"

echo "$(date): 開始健康檢查..." >> $LOG_FILE

# 檢查是否在正確目錄
if [ ! -d "$BOT_DIR" ]; then
    echo "$(date): 錯誤 - 找不到 Bot 目錄: $BOT_DIR" >> $LOG_FILE
    exit 1
fi

cd "$BOT_DIR"

# 檢查容器狀態
CONTAINER_STATUS=$(docker compose ps --services --filter "status=running" | wc -l)

if [ "$CONTAINER_STATUS" -eq 0 ]; then
    echo "$(date): 警告 - X Bot 容器未運行，嘗試重新啟動..." >> $LOG_FILE
    
    # 嘗試重新啟動
    docker compose down
    sleep 5
    docker compose up -d
    
    # 等待啟動
    sleep 30
    
    # 再次檢查
    NEW_STATUS=$(docker compose ps --services --filter "status=running" | wc -l)
    
    if [ "$NEW_STATUS" -eq 0 ]; then
        echo "$(date): 錯誤 - X Bot 重啟失敗" >> $LOG_FILE
        # 可以在這裡添加通知邏輯，例如發送郵件或 Discord 訊息
    else
        echo "$(date): 成功 - X Bot 已重新啟動" >> $LOG_FILE
    fi
else
    echo "$(date): 正常 - X Bot 運行中" >> $LOG_FILE
fi

# 清理舊日誌（保留最近 100 行）
tail -n 100 $LOG_FILE > ${LOG_FILE}.tmp && mv ${LOG_FILE}.tmp $LOG_FILE
