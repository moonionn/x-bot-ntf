# 安裝步驟說明

## 系統需求

- Python 3.8 或更高版本
- pip 套件管理器
- Discord Bot Token
- Twitter/X 帳號
- Gemini API Key (用於翻譯功能)

## 詳細安裝步驟

### 1. 下載專案

```bash
# 如果有 git repository
git clone <repository-url>
cd x_bot_ntf

# 或直接下載並解壓縮到目標資料夾
```

### 2. 建立虛擬環境 (建議)

```bash
# 建立虛擬環境
python -m venv .venv

# 啟動虛擬環境
# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate
```

### 3. 安裝相依套件

```bash
pip install -r requirements.txt
```

### 4. 配置設定檔

```bash
# 複製範例配置檔案
cp configs.example.yml configs.yml

# 使用您喜歡的編輯器編輯配置檔案
nano configs.yml
# 或
vim configs.yml
# 或使用 VS Code 等圖形化編輯器
```

### 5. 設置必要的配置項目

在 `configs.yml` 中設置：

```yaml
# 基本設置
prefix: "."

# 翻譯功能設置
translation:
  gemini_api_key: "您的_Gemini_API_金鑰"
  default_target_language: "繁體中文"
  auto_translate_channels: []
```

### 6. 設置環境變數

建立 `.env` 檔案：

```env
DISCORD_TOKEN=您的_Discord_Bot_Token
TWITTER_USERNAME=您的_Twitter_帳號
TWITTER_PASSWORD=您的_Twitter_密碼
GEMINI_API_KEY=您的_Gemini_API_金鑰
```

或在系統中設置環境變數：

```bash
# Windows (Command Prompt)
set DISCORD_TOKEN=您的_Discord_Bot_Token
set TWITTER_USERNAME=您的_Twitter_帳號
set TWITTER_PASSWORD=您的_Twitter_密碼
set GEMINI_API_KEY=您的_Gemini_API_金鑰

# Windows (PowerShell)
$env:DISCORD_TOKEN="您的_Discord_Bot_Token"
$env:TWITTER_USERNAME="您的_Twitter_帳號"
$env:TWITTER_PASSWORD="您的_Twitter_密碼"
$env:GEMINI_API_KEY="您的_Gemini_API_金鑰"

# macOS/Linux
export DISCORD_TOKEN="您的_Discord_Bot_Token"
export TWITTER_USERNAME="您的_Twitter_帳號"
export TWITTER_PASSWORD="您的_Twitter_密碼"
export GEMINI_API_KEY="您的_Gemini_API_金鑰"
```

### 7. 獲取必要的 API 金鑰

#### Discord Bot Token

1. 前往 [Discord Developer Portal](https://discord.com/developers/applications)
2. 建立新的應用程式
3. 在 "Bot" 頁面中建立 Bot 並複製 Token
4. 在 "OAuth2" > "URL Generator" 中選擇所需權限並產生邀請連結

#### Gemini API Key

1. 前往 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 建立新的 API 金鑰
3. 複製金鑰到配置檔案中

### 8. 設置 Discord Bot 權限

邀請 Bot 到您的伺服器時，請確保具有以下權限：

- ✅ 檢視頻道
- ✅ 發送訊息
- ✅ 嵌入連結
- ✅ 附加檔案
- ✅ 提及所有人
- ✅ 使用斜線指令

### 9. 啟動 Bot

```bash
# 確保虛擬環境已啟動
python bot.py
```

### 10. 驗證安裝

如果安裝成功，您應該會看到：

1. Bot 在終端中顯示啟動訊息
2. Bot 在 Discord 中顯示為線上狀態
3. 可以使用基本指令如 `.list`

## 疑難排解

### 常見問題

**Q: `ModuleNotFoundError` 錯誤**
A: 確保已安裝所有相依套件：`pip install -r requirements.txt`

**Q: Bot 無法啟動**
A: 檢查 Discord Token 是否正確設置

**Q: 無法追蹤 Twitter 帳號**
A: 檢查 Twitter 帳號密碼是否正確

**Q: 翻譯功能無法使用**
A: 確認 Gemini API Key 是否正確設置

### 獲取幫助

如果遇到問題，請：

1. 檢查終端中的錯誤訊息
2. 查看 `console.log` 檔案中的詳細日誌
3. 參考 [完整使用指南](USAGE_GUIDE.md)
4. 確認所有配置項目都已正確設置

## 下一步

安裝完成後，請參考：

- [快速啟動指南](QUICK_START.md) - 5 分鐘快速設置
- [完整使用指南](USAGE_GUIDE.md) - 詳細功能說明
- [自動翻譯指南](AUTO_TRANSLATION_GUIDE.md) - 自動翻譯功能設置
