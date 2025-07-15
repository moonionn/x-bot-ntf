#!/bin/bash

# 雲端 VM 配置修復腳本
# 修復本地與雲端配置不同步的問題

echo "🔧 雲端 VM 配置修復腳本"
echo "=========================="

# 檢查是否在正確的目錄
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ 錯誤：請在 x-bot-ntf 專案目錄中執行此腳本"
    exit 1
fi

# 備份現有配置
echo "💾 備份現有配置..."
cp configs.yml configs.yml.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null || echo "configs.yml 不存在，將創建新的"
cp .env .env.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null || echo ".env 不存在，將創建新的"

# 修復 configs.yml
echo "📝 修復 configs.yml 配置..."
cat > configs.yml << 'EOF'
activity_name: "{count} accounts"
activity_type: watching
auth_max_attempts: 2
auto_change_client: false
auto_repair_mismatched_clients: false
auto_turn_off_notification: true
auto_unfollow: true
default_message: "{mention}**{author}** just {action} here: \n{url}\n"
embed:
  built_in:
    fx_image: true
    legacy_logo: true
    video_link_button: false
  fx_twitter:
    domain_name: fxtwitter
    original_url_button: true
  type: built_in
emoji_auto_format: true
prefix: .
tasks_monitor_check_period: 60
tasks_monitor_log_period: 14400
translation:
  auto_translate_channels:
    - 1394029482272358490 # x更新通知頻道
    - 1394268004044247093 # 我翻好了頻道
  default_target_language: 繁體中文
  # 頻道映射設置：通知頻道 -> 翻譯頻道
  channel_mapping:
    1394029482272358490: 1394268004044247093 # x更新通知 -> 我翻好了
  # 設置模式：'reply' = 在原頻道回覆, 'separate' = 發送到指定翻譯頻道
  translation_mode: "separate"
tweets_check_period: 10
tweets_updater_retry_delay: 300
users_list_page_counter_position: title
users_list_pagination_size: 8
EOF

echo "✅ configs.yml 已更新為正確的翻譯配置"

# 檢查並修復 .env 文件
echo "🔍 檢查 .env 文件..."
if [ ! -f ".env" ]; then
    echo "📝 創建 .env 文件..."
    cat > .env << 'EOF'
BOT_TOKEN=請填入您的Discord_Bot_Token
GEMINI_API_KEY=請填入您的Gemini_API_Key
DATA_PATH=./data
TWITTER_TOKEN=DummyAccount:dummy_token_placeholder
EOF
    echo "⚠️  請編輯 .env 文件並填入正確的 API 金鑰"
else
    # 檢查是否有 TWITTER_TOKEN
    if ! grep -q "TWITTER_TOKEN" .env; then
        echo "🔧 添加 TWITTER_TOKEN 以避免啟動錯誤..."
        echo "TWITTER_TOKEN=DummyAccount:dummy_token_placeholder" >> .env
    fi
    
    # 檢查是否有 DATA_PATH
    if ! grep -q "DATA_PATH" .env; then
        echo "🔧 添加 DATA_PATH..."
        echo "DATA_PATH=./data" >> .env
    fi
fi

# 清理可能存在的問題資料庫記錄
echo "🗑️ 清理資料庫中的假帳戶..."
if [ -f "data/tracked_accounts.db" ]; then
    # 使用 Docker 來清理資料庫
    docker compose run --rm x-bot python -c "
import sqlite3
import os
try:
    if os.path.exists('/app/data/tracked_accounts.db'):
        conn = sqlite3.connect('/app/data/tracked_accounts.db')
        cursor = conn.cursor()
        
        # 刪除 DummyAccount 相關記錄
        cursor.execute('DELETE FROM user WHERE client_used = \"DummyAccount\"')
        cursor.execute('DELETE FROM accounts WHERE name = \"DummyAccount\"')
        
        conn.commit()
        conn.close()
        print('✅ 已清理資料庫中的假帳戶記錄')
    else:
        print('ℹ️ 資料庫文件不存在，將自動創建')
except Exception as e:
    print(f'資料庫清理失敗: {e}')
" 2>/dev/null || echo "資料庫清理將在服務啟動時處理"
fi

# 確保數據目錄存在
mkdir -p data

# 停止現有服務
echo "⏹️ 停止現有服務..."
docker compose down

# 清理 Docker 緩存
echo "🧹 清理 Docker 緩存..."
docker system prune -f >/dev/null 2>&1

# 重新構建並啟動服務
echo "🔨 重新構建並啟動服務..."
docker compose build --no-cache
docker compose up -d

# 等待服務啟動
echo "⏳ 等待服務啟動..."
sleep 15

# 檢查服務狀態
echo "🔍 檢查服務狀態..."
docker compose ps

# 顯示最新日誌
echo ""
echo "📋 最新啟動日誌："
docker compose logs --tail=30

echo ""
echo "✅ 修復完成！"
echo ""
echo "📋 驗證步驟："
echo "1. 檢查日誌中是否出現：'auto_translate_channels: [1394029482272358490, 1394268004044247093]'"
echo "2. 檢查是否出現：'translation_mode: separate'"
echo "3. 確認沒有 DummyAccount 認證錯誤"
echo "4. 在 Discord 頻道中發送 Twitter 連結測試翻譯功能"
echo ""
echo "🔧 有用的指令："
echo "  查看即時日誌: docker compose logs -f"
echo "  重啟服務: docker compose restart"
echo "  查看配置: cat configs.yml"
echo ""
echo "⚠️ 如果仍有問題，請檢查 .env 文件中的 API 金鑰是否正確："
echo "  nano .env"
