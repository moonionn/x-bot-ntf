# 🌟 x_bot_ntf 翻譯功能設置指南

x_bot_ntf 現在支援使用 Gemini API 進行推文翻譯功能。這個簡潔的解決方案讓你能夠輕鬆翻譯 Twitter 推文內容。

## 🚀 快速設置

### 1. 獲取 Gemini API 金鑰

1. 前往 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 登入你的 Google 帳戶
3. 創建新的 API 金鑰
4. 複製 API 金鑰備用

### 2. 配置 API 金鑰

**方法 A: 在 configs.yml 中設置（推薦）**
```yaml
translation:
  gemini_api_key: "your-gemini-api-key-here"
  default_target_language: "繁體中文"
```

**方法 B: 使用環境變數**
```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
```

或在 `.env` 文件中添加：
```env
GEMINI_API_KEY=your-gemini-api-key-here
```

### 3. 安裝依賴套件（如果尚未安裝）

```bash
pip install google-generativeai beautifulsoup4 aiohttp
```

## 📱 使用方法

### Discord 指令

在 Discord 中使用斜線指令：
```
/translate tweet https://twitter.com/username/status/1234567890
```

或
```
/translate tweet https://x.com/username/status/1234567890
```

### 支援的功能

✅ **智能內容提取**
- 自動從推文中提取純文字內容
- 移除 Twitter 界面元素和噪音
- 保留 emoji 和特殊字符

✅ **優化翻譯**
- 針對社群媒體內容優化的翻譯提示
- 保持原文語調和風格
- 專有名詞保持原文

✅ **多種來源支援**
- 支援 twitter.com 和 x.com 連結
- 自動嘗試多種抓取方法
- 智能錯誤處理和重試

## 🔧 進階設置

### 自訂翻譯語言

你可以在配置中修改預設翻譯語言：
```yaml
translation:
  default_target_language: "English"    # 英文
  # default_target_language: "日本語"    # 日文
  # default_target_language: "한국어"    # 韓文
```

### 程式碼中使用

```python
from src.translation.tweet_translator import TweetTranslator

# 初始化翻譯器
translator = TweetTranslator(gemini_api_key="your-api-key")

# 翻譯推文
result = await translator.translate_tweet("https://twitter.com/username/status/1234567890")

if result['success']:
    print(f"原文: {result['original_text']}")
    print(f"翻譯: {result['translated_text']}")
else:
    print(f"錯誤: {result['error']}")
```

## 🛠️ 故障排除

### 常見問題

1. **翻譯功能無法使用**
   - 檢查 API 金鑰是否正確設置
   - 確認 API 金鑰有效且有配額
   - 查看 bot 日誌中的錯誤信息

2. **推文無法抓取**
   - 確認推文是公開的（非私人帳戶）
   - 檢查推文連結格式是否正確
   - 推文可能已被刪除

3. **翻譯結果不理想**
   - 可能遇到 API 安全過濾器
   - 內容可能包含不支援的格式
   - 嘗試不同的推文進行測試

### 日誌檢查

查看 Discord bot 的日誌輸出：
```
[INFO] 初始化 Gemini API 翻譯器
[INFO] 正在爬取推文內容: https://...
[INFO] 成功獲取推文內容 (長度: 123): ...
[INFO] 翻譯完成: ...
```

如果看到錯誤：
```
[ERROR] Gemini API 翻譯器初始化失敗: ...
[WARNING] 未設定翻譯服務，翻譯功能將無法使用
```

請檢查 API 金鑰設置。

## 📊 功能特色

| 特性 | 說明 |
|------|------|
| 🚀 簡單設置 | 只需 Gemini API 金鑰即可使用 |
| 🧠 智能提取 | 自動清理推文內容，只翻譯核心文字 |
| 🌍 多語言支援 | 支援多種目標語言翻譯 |
| 😊 保留 Emoji | 完整保留原文中的 emoji 和特殊符號 |
| 🔗 多源支援 | 支援 fxtwitter、nitter 等多種抓取方式 |
| ⚡ 高性能 | 使用最新的 Gemini 模型，翻譯速度快 |

## 💡 使用建議

1. **API 金鑰安全**：不要在公開場所分享你的 API 金鑰
2. **配額管理**：注意 Gemini API 的使用配額限制
3. **測試推文**：先用簡單的推文測試功能是否正常
4. **備用方案**：如果遇到問題，可以嘗試複製推文文字直接翻譯

## 🆘 獲取支援

如果遇到問題：

1. 檢查日誌輸出
2. 確認 API 金鑰有效
3. 測試推文是否公開可見
4. 聯繫開發者或提交 issue

---

**享受你的多語言推文翻譯體驗！** 🎉
