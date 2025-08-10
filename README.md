<div align="center">

# Discord X Bot - Twitter 通知與翻譯機器人

[![](https://img.shields.io/badge/python-3.11+-blue?logo=python&logoColor=white)](https://www.python.org/downloads/)

一個功能豐富的 Discord 機器人，提供 Twitter 追蹤通知和自動翻譯功能

本專案基於以下開源專案開發：

## 原始專案
**專案名稱**: [Tweetcord]
**作者**: [Yuuzi261]
**原始碼**: [[GitHub 連結](https://github.com/Yuuzi261/Tweetcord)]

</div>

## � 簡介

Discord X Bot 是一個多功能的 Discord 機器人，主要功能包括：

1. **Twitter 追蹤通知** - 自動將指定 Twitter 用戶的推文轉發到 Discord 頻道
2. **自動翻譯功能** - 使用 Google Gemini API 自動翻譯推文到指定語言
3. **頻道管理** - 支援多頻道、多語言的翻譯映射

## ✨ 主要功能

### 🐦 Twitter 追蹤功能
- 即時追蹤指定 Twitter 用戶的推文
- 支援轉推、引用推文的通知
- 自定義通知訊息格式
- 多媒體內容支援（圖片、影片）

### 🌍 翻譯功能
- 自動翻譯 Twitter 連結中的推文
- 支援多種語言翻譯
- 頻道映射功能（不同頻道翻譯到不同語言）
- 手動翻譯指令

### 📱 Discord 指令

#### Twitter 追蹤指令
- `/add notifier` - 添加 Twitter 用戶追蹤
- `/remove notifier` - 移除 Twitter 用戶追蹤
- `/list users` - 列出所有追蹤的用戶
- `/sync` - 同步資料庫與 Discord 命令

#### 翻譯指令
- `/translate [url]` - 手動翻譯 Twitter 連結
- `/清除快取` - 清除翻譯快取
- `/重載設定` - 重新載入設定檔

## � 快速開始

### 1. 環境需求
- Python 3.11+
- Docker & Docker Compose（推薦）
- Discord Bot Token
- Google Gemini API Key
- Twitter Auth Token（用於追蹤功能）

### 2. 設定環境變數

創建 `.env` 檔案：

```env
# Discord Bot Token
BOT_TOKEN=your_discord_bot_token

# Google Gemini API Key（用於翻譯功能）
GEMINI_API_KEY=your_gemini_api_key

# Twitter Auth Token（用於追蹤功能，可選）
TWITTER_TOKEN=Account1:your_twitter_auth_token

# 資料路徑
DATA_PATH=./data
```

### 3. 設定機器人配置

編輯 `configs.yml`：

```yaml
# 基本設定
prefix: "!"
activity_name: "Twitter & Translation Bot"
activity_type: "watching"

# 翻譯功能設定
auto_translate_channels:
  - 1234567890123456789  # 自動翻譯的頻道 ID

channel_mapping:
  1234567890123456789: "zh-TW"  # 頻道 ID: 目標語言

translation_mode: "gemini"  # 翻譯引擎

# Twitter 追蹤設定
tweets_check_period: 18
tweets_updater_retry_delay: 5
auth_max_attempts: 3

# 嵌入樣式
embed:
  type: "built_in"
  built_in:
    fx_image: true
    video_link_button: true
    legacy_logo: false

# 預設訊息格式
default_message: "{mention} **{author}** just {action}:\n{url}"
```

### 4. 啟動機器人

#### 使用 Docker（推薦）

```bash
# 啟動服務（背景運行）
docker compose up -d

# 查看日誌
docker compose logs -f

# 重啟服務
docker compose restart

# 停止服務
docker compose down
```

#### 本地運行

```bash
# 安裝依賴
pip install -r requirements.txt

# 啟動機器人
python bot.py
```

## 🔧 詳細配置

### Discord Bot 權限設定

權限整數：`2147666944`

必要權限：
- ✔️ 讀取訊息/查看頻道
- ✔️ 發送訊息
- ✔️ 嵌入連結
- ✔️ 附加檔案
- ✔️ 提及所有身分組
- ✔️ 使用應用程式命令

特權意圖：
- ✔️ 訊息內容意圖（Message Content Intent）

### 翻譯功能配置

在 `configs.yml` 中設定翻譯功能：

```yaml
# 自動翻譯的頻道
auto_translate_channels:
  - channel_id_1
  - channel_id_2

# 頻道語言映射
channel_mapping:
  channel_id_1: "zh-TW"  # 翻譯成繁體中文
  channel_id_2: "en"     # 翻譯成英文
  channel_id_3: "ja"     # 翻譯成日文

# 翻譯引擎
translation_mode: "gemini"  # 或 "google"
```

### Twitter 追蹤配置

```yaml
# 檢查推文頻率（秒）
tweets_check_period: 18  # 建議值，避免速率限制

# 自動行為
auto_change_client: true
auto_turn_off_notification: true
auto_unfollow: false

# 資料庫自動修復
auto_repair_mismatched_clients: true
```

## 📋 使用範例

### 1. 設定 Twitter 追蹤

```
/add notifier username:elonmusk channel:#twitter-updates mention:@everyone type:all media_type:all account_used:Account1
```

### 2. 手動翻譯推文

```
/translate https://twitter.com/elonmusk/status/1234567890
```

### 3. 自動翻譯

在設定的 `auto_translate_channels` 中貼上任何 Twitter/X 連結，機器人會自動翻譯。

## 🛠️ 管理指令

### 一鍵修復腳本

```bash
# 修復配置和重啟服務
./fix-cloud-vm.sh
```

### 更新機器人

```bash
# 更新到最新版本
./update-bot.sh
```

### 健康檢查

```bash
# 檢查服務狀態
./health-check.sh
```

## � 故障排除

### 常見問題

1. **Bot 無法連線**
   ```bash
   # 檢查 Token 是否正確
   docker compose logs | grep "token"
   ```

2. **翻譯功能無效**
   ```bash
   # 檢查 Gemini API Key
   docker compose logs | grep -i "gemini\|api"
   ```

3. **Twitter 追蹤失效**
   ```bash
   # 檢查 Twitter Token
   docker compose logs | grep -i "twitter\|auth"
   ```

### 重建服務

```bash
# 完全重建
docker compose down
docker compose up -d --build
```

## � 專案結構

```
├── bot.py                    # 主程式
├── docker-compose.yml        # Docker 配置
├── .env                     # 環境變數
├── configs.yml              # Bot 設定
├── requirements.txt         # Python 套件
├── cogs/                    # Discord 功能模組
│   ├── translation.py       # 翻譯功能
│   ├── auto_translation.py  # 自動翻譯
│   ├── notification.py      # Twitter 通知
│   └── ...
├── src/                     # 核心程式
│   ├── translation/         # 翻譯引擎
│   ├── notification/        # Twitter 追蹤
│   └── ...
└── data/                    # 資料庫檔案
```

## 🌐 部署建議

### 雲端 VM 部署

推薦使用以下服務：
- **Google Cloud Platform**
- **AWS EC2**
- **Azure VM**
- **DigitalOcean Droplet**

### 24/7 運行

使用 Docker Compose 的分離模式：

```bash
# 背景運行，即使 SSH 斷線也會繼續執行
docker compose up -d
```

## � 支援與貢獻

如有問題或建議，歡迎開啟 Issue 或提交 Pull Request。

## � 授權

本專案採用 MIT 授權條款。

- 即時監控指定 Twitter 用戶的推文
- 自動轉發到指定的 Discord 頻道
- 支援圖片、影片等多媒體內容
- 靈活的通知設置與管理

### 🌍 推文翻譯功能

- 手動翻譯任何推文連結
- 使用 Gemini AI 提供高品質翻譯
- 提供雙重翻譯風格（直接翻譯 + 自然翻譯）
- 詳細的詞彙解說與文化背景說明

### 🤖 自動翻譯功能

- 在指定頻道自動檢測推文連結
- 無需手動指令即可自動翻譯
- 美觀的格式化顯示
- 管理員友善的設置介面

### ⚙️ 管理功能

- 簡單的指令介面
- 靈活的權限控制
- 詳細的使用統計
- 完善的錯誤處理

## 🆘 需要幫助？

如果您在使用過程中遇到任何問題：

1. **查看對應的指南文件** - 大部分問題都能在文件中找到解答
2. **檢查終端錯誤訊息** - 通常會提供具體的錯誤原因
3. **查看 console.log** - 詳細的執行日誌
4. **確認配置正確** - 檢查 configs.yml 和環境變數設置

---

**開始您的 X Bot trnaslation 之旅吧！** 🎉
