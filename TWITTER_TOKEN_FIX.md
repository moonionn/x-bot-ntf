# 🔧 快速修復：TWITTER_TOKEN 環境變數錯誤

如果您在雲端 VM 上看到 `missing required environment variables: ['TWITTER_TOKEN']` 錯誤，這裡是快速解決方案。

## 🚀 一鍵修復（推薦）

在雲端 VM 上執行以下命令：

```bash
# 更新代碼
cd x-bot-ntf
git pull origin main

# 執行修復腳本
./fix-env.sh
```

## 🔍 問題原因

- Bot 原本設計用於 Twitter 監控 + 翻譯功能
- 如果只使用翻譯功能，不需要真實的 TWITTER_TOKEN
- 新版本支援「翻譯模式」，避免這個啟動錯誤

## 🛠️ 手動修復步驟

如果想要手動修復：

### 1. 檢查 .env 文件

```bash
nano .env
```

確保包含以下內容：
```env
BOT_TOKEN=你的_Discord_Bot_Token
GEMINI_API_KEY=你的_Gemini_API_Key
DATA_PATH=./data
# 翻譯模式：設為假值即可避免啟動錯誤
TWITTER_TOKEN=DummyAccount:dummy_token_placeholder
```

### 2. 重啟服務

```bash
docker-compose down
docker-compose up -d --build
```

### 3. 檢查日誌

```bash
docker-compose logs -f
```

現在應該會看到：
- ✅ `running in translation-only mode, TWITTER_TOKEN not required`
- ✅ `environment variables check passed`
- ✅ 沒有 TWITTER_TOKEN 錯誤

## 📋 驗證修復成功

啟動日誌中應該顯示：

```
INFO:bot:detected translation-only configuration, running in translation mode
INFO:src.checker:running in translation-only mode, TWITTER_TOKEN not required
INFO:src.checker:environment variables check passed
```

## 🤖 功能確認

修復後，翻譯功能應該正常工作：
- 自動翻譯指定頻道的訊息
- 支援手動 `/translate` 指令
- 結構化翻譯結果顯示（發文者、翻譯、詞句解說）

## 🆘 如果仍有問題

1. 檢查 Discord Bot Token 是否正確
2. 檢查 Gemini API Key 是否有效
3. 確認頻道 ID 設置正確
4. 查看完整日誌：`docker-compose logs -f`

---

**說明：** 這個修復保持向後兼容，如果以後要添加 Twitter 監控功能，只需要設置真實的 TWITTER_TOKEN 即可。
