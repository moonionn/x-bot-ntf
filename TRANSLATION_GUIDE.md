# x_bot_ntf 翻譯功能完整指南

這份指南涵蓋了 x_bot_ntf 的所有翻譯功能，包括多種翻譯方式的設置和使用。

## 🌟 翻譯方式概述

x_bot_ntf 支援三種翻譯方式：

1. **網頁版 Gemini** - 適合無法使用 API 但可以訪問 Gemini 網頁版的用戶
2. **Google Apps Script (GAS)** - 穩定的雲端翻譯解決方案
3. **Gemini API** - 官方 API，速度最快但可能有使用限制

## 📋 快速設置對照表

| 翻譯方式 | 配置方法 | 優點 | 缺點 | 推薦情況 |
|---------|----------|------|------|----------|
| 網頁版 Gemini | `use_web_gemini: true` | 無需 API 金鑰 | 較慢，需要瀏覽器 | API 受限但可訪問網頁版 |
| Google Apps Script | `gas_gemini_url: "your-url"` | 穩定，無瀏覽器依賴 | 需要設置 GAS | 長期穩定使用 |
| Gemini API | `gemini_api_key: "your-key"` | 最快，最穩定 | 可能有使用限制 | 有 API 訪問權限 |

## ⚙️ 配置方式

### 方式 1: 配置文件設置（推薦）

在 `configs.yml` 中設置：

```yaml
translation:
  # 選擇一種翻譯方式
  use_web_gemini: true          # 網頁版 Gemini
  # gas_gemini_url: "your-url"  # Google Apps Script
  # gemini_api_key: "your-key"  # Gemini API
  
  # 網頁版 Gemini 進階設置
  web_gemini:
    headless: true              # 無頭模式（不顯示瀏覽器）
    timeout: 60                 # 超時時間
  
  default_target_language: "繁體中文"
```

### 方式 2: 環境變數設置

在 `.env` 文件中設置：

```env
# 選擇一種翻譯方式
USE_WEB_GEMINI=true
# GAS_GEMINI_URL=your-gas-url
# GEMINI_API_KEY=your-api-key
```

## 🚀 各種翻譯方式的詳細設置

### 1. 網頁版 Gemini 設置

**優點：**
- 無需 API 金鑰
- 可以使用最新的 Gemini 模型
- 適合 API 受限的用戶

**缺點：**
- 需要安裝 Chrome 瀏覽器
- 速度較慢
- 消耗更多系統資源

**設置步驟：**

1. 安裝依賴：
```bash
pip install selenium webdriver-manager
```

2. 配置設置：
```yaml
translation:
  use_web_gemini: true
  web_gemini:
    headless: true    # 設為 false 可以看到瀏覽器操作（調試用）
    timeout: 60
```

3. 測試：
```bash
python test_web_gemini.py
```

### 2. Google Apps Script 設置

**詳細設置請參考：** `WEB_GEMINI_SETUP.md`

**優點：**
- 穩定可靠
- 無需本地瀏覽器
- 可以使用 Google Translate 作為備用

**設置步驟：**
1. 創建 Google Apps Script
2. 部署為網頁應用
3. 在配置中設置 URL

```yaml
translation:
  gas_gemini_url: "https://script.google.com/macros/s/your-script-id/exec"
```

### 3. Gemini API 設置

**最簡單的設置方式：**

```yaml
translation:
  gemini_api_key: "your-gemini-api-key"
```

## 🔧 故障排除

### 網頁版 Gemini 常見問題

1. **Chrome 找不到：**
   - macOS: 安裝 Chrome 瀏覽器
   - Ubuntu: `sudo apt install google-chrome-stable`
   - 或設置 Chrome 執行檔路徑

2. **Gemini 需要登入：**
   - 設置 `headless: false` 手動登入一次
   - 或使用其他翻譯方式

3. **翻譯超時：**
   - 增加 `timeout` 設置
   - 檢查網路連線

### 通用故障排除

1. **檢查日誌：**
```
[INFO] 初始化網頁版 Gemini 翻譯器
[ERROR] 翻譯器初始化失敗: ...
```

2. **測試翻譯器：**
```bash
python test_web_gemini.py
```

3. **備用方案：**
   - 設置多種翻譯方式
   - 系統會自動嘗試不同方式

## 📱 使用方法

### Discord 指令

```
/translate tweet https://twitter.com/username/status/1234567890
```

### 程式碼使用

```python
from src.translation.tweet_translator import TweetTranslator

# 網頁版 Gemini
translator = TweetTranslator(use_web_gemini=True)

# GAS
translator = TweetTranslator(gas_url="your-gas-url")

# API
translator = TweetTranslator(gemini_api_key="your-key")

# 翻譯
result = await translator.translate_tweet(tweet_url)
```

## 🎯 推薦配置

### 個人使用
```yaml
translation:
  use_web_gemini: true
  web_gemini:
    headless: true
    timeout: 60
```

### 伺服器部署
```yaml
translation:
  gas_gemini_url: "your-gas-url"
  # 備用方案
  gemini_api_key: "your-api-key"
```

### 開發測試
```yaml
translation:
  use_web_gemini: true
  web_gemini:
    headless: false  # 可以看到瀏覽器操作
    timeout: 120
```

## 📊 性能對比

| 特性 | 網頁版 Gemini | Google Apps Script | Gemini API |
|------|---------------|-------------------|------------|
| 設置難度 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| 穩定性 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 速度 | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 資源使用 | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 可用性 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

## 🔮 未來計畫

- [ ] 支援更多翻譯服務（OpenAI, Claude 等）
- [ ] 自動語言檢測
- [ ] 翻譯品質評估
- [ ] 批量翻譯功能
- [ ] 翻譯快取機制

---

**需要幫助？** 請查看相關文件或聯繫開發者。
