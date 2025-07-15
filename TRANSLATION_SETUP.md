# 翻譯功能設定說明

## 功能概述
這個新增的翻譯功能可以：
1. 爬取推文網址的內容
2. 使用 Gemini API 翻譯推文內容
3. 將翻譯結果以美觀的 embed 形式回傳到 Discord

## 安裝步驟

### 1. 安裝所需套件
```bash
pip install -r translation_requirements.txt
```

### 2. 獲取 Gemini API 金鑰
1. 前往 Google AI Studio: https://makersuite.google.com/app/apikey
2. 創建新的 API 金鑰
3. 複製 API 金鑰

### 3. 設定環境變數
在 `.env` 檔案中添加：
```
GEMINI_API_KEY=你的_Gemini_API_金鑰
```

### 4. 啟用翻譯功能
在 `cogs/translation.py` 中：
1. 取消註釋第 12 行：`from src.translation.tweet_translator import TweetTranslator`
2. 取消註釋第 18-23 行的初始化代碼

## 使用方法

### Discord 指令
1. **翻譯推文**: `/translate tweet url:推文網址 language:目標語言`
   - 範例: `/translate tweet url:https://twitter.com/username/status/1234567890 language:繁體中文`

2. **翻譯文字**: `/translate text text:要翻譯的文字 language:目標語言`
   - 範例: `/translate text text:Hello World language:繁體中文`

### 支援的語言
- 繁體中文 (預設)
- 簡體中文
- 英文
- 日文
- 韓文
- 法文
- 德文
- 西班牙文
- 等等（支援 Gemini 能理解的所有語言）

## 功能特色

### 1. 智能爬蟲
- 使用多種方法提取推文內容
- 支援 fxtwitter 和原生 Twitter 網址
- 自動處理反爬蟲機制

### 2. 智能翻譯
- 自動檢測是否為中文，避免不必要的翻譯
- 保持原文語調和意思
- 支援長文本翻譯

### 3. 用戶友好界面
- 美觀的 Discord Embed 顯示
- 按鈕操作界面
- 私人回應保護隱私
- 可選擇公開分享翻譯結果

### 4. 錯誤處理
- 完整的錯誤捕獲和處理
- 用戶友好的錯誤訊息
- 詳細的日誌記錄

## 安全考量
- API 金鑰安全存儲在環境變數中
- 翻譯結果預設為私人回應
- 用戶可選擇是否公開分享結果

## 限制
- 需要有效的 Gemini API 金鑰
- 受到 Twitter 反爬蟲機制限制
- 翻譯品質依賴於 Gemini API

## 故障排除

### 常見問題
1. **翻譯功能無法使用**
   - 檢查是否設定了 `GEMINI_API_KEY`
   - 確認 API 金鑰是否有效
   - 檢查是否安裝了所需套件

2. **無法爬取推文內容**
   - 確認網址格式正確
   - 檢查網路連線
   - 嘗試使用 fxtwitter 格式的網址

3. **翻譯結果不準確**
   - Gemini API 偶爾可能產生不準確的翻譯
   - 可以嘗試重新翻譯
   - 檢查原文是否完整獲取

## 擴展功能建議
1. 添加更多語言選項的快速按鈕
2. 支援批量翻譯
3. 添加翻譯歷史記錄
4. 支援自訂翻譯風格（正式/非正式）
5. 整合到現有的推文通知系統中
