# 自動翻譯功能使用指南

## 功能概述

這個功能可以讓機器人在指定頻道中自動檢測並翻譯 Twitter/X 連結，無需手動使用翻譯指令。

## 設置步驟

### 1. 配置 API 金鑰

**推薦方式：使用環境變數**

在環境變數中設置 (更安全，不會洩露在配置檔案中)：

```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
```

**備用方式：配置檔案設置**

在 `configs.yml` 文件中的 translation 區塊：

```yaml
translation:
  default_target_language: "繁體中文"
  auto_translate_channels: []
```

**注意：**

- ✅ 優先推薦使用環境變數 `GEMINI_API_KEY`
- ⚠️ 請勿將 API 金鑰直接寫在配置檔案中，以免意外洩露

### 2. 啟用自動翻譯頻道

**方式一：單頻道模式（在同一頻道回覆）**

```
/autotranslate add_channel #your-channel-name
```

**方式二：雙頻道模式（分離通知和翻譯）**

1. 先添加兩個頻道到自動翻譯列表：

   ```
   /autotranslate add_channel #通知頻道
   /autotranslate add_channel #翻譯頻道
   ```

2. 設置頻道映射關係：
   ```
   /autotranslate set_mapping source_channel:#通知頻道 target_channel:#翻譯頻道
   ```

這樣設置後，當通知頻道收到推文通知時，翻譯結果會自動發送到指定的翻譯頻道。

### 3. 管理自動翻譯頻道

- **查看已啟用的頻道**：

  ```
  /autotranslate list_channels
  ```

- **查看頻道映射關係**：

  ```
  /autotranslate list_mappings
  ```

- **設置頻道映射**：

  ```
  /autotranslate set_mapping source_channel:#通知頻道 target_channel:#翻譯頻道
  ```

- **移除頻道的自動翻譯**：

  ```
  /autotranslate remove_channel #your-channel-name
  ```

- **檢查功能狀態**：
  ```
  /autotranslate status
  ```

## 使用方式

自動翻譯功能支援兩種使用模式：

### 🔀 分離模式（推薦）

- **通知頻道**: 專門接收推文通知
- **翻譯頻道**: 專門顯示翻譯結果
- **優點**: 保持頻道內容整潔，便於管理和查看

### 💬 回覆模式

- 翻譯結果直接在包含推文連結的消息下方回覆
- **適用**: 單頻道使用或希望保持對話連續性的場景

### 觸發方式

1. **推文通知自動翻譯**（主要功能）

   - 當機器人在已啟用的頻道中發送推文通知時
   - 系統會自動檢測通知中的推文連結並進行翻譯
   - 根據配置模式，翻譯結果發送到指定頻道或回覆原消息

2. **手動連結翻譯**（輔助功能）
   - 在已啟用自動翻譯的頻道中
   - 用戶手動發送包含 Twitter/X 連結的消息
   - 機器人會自動檢測連結並進行翻譯

## 功能特點

- ✅ 自動檢測 Twitter/X 連結 (支援 twitter.com 和 x.com)
- ✅ 多種翻譯格式（直接翻譯 + 自然翻譯 + 詞彙解說）
- ✅ 翻譯內容格式化顯示（引用格式突出翻譯文字）
- ✅ 錯誤處理（翻譯失敗時會顯示 ❌ 反應）
- ✅ 權限控制（需要「管理頻道」權限才能設置）

## 支援的連結格式

- `https://twitter.com/username/status/1234567890`
- `https://x.com/username/status/1234567890`
- `http://twitter.com/username/status/1234567890`
- `http://x.com/username/status/1234567890`

## 翻譯結果格式

翻譯結果會包含：

1. **📝 原文** - 推文的原始內容
2. **🌏 翻譯結果** - 包含兩種翻譯風格：
   - 翻譯一（直接翻譯，保留原意）
   - 翻譯二（最自然、口語的翻法）
3. **📚 詞句詳細解說** - 重要詞彙的文化背景和含義解釋

## 注意事項

- 需要有效的 Gemini API 金鑰
- 機器人需要在目標頻道有發送消息的權限
- 目前配置更改會在機器人重啟後重置，請聯繫管理員進行永久配置
- 翻譯功能使用 fxtwitter 服務爬取推文內容

## 故障排除

如果自動翻譯不工作，請檢查：

1. ✅ API 金鑰是否正確配置
2. ✅ 頻道是否已添加到自動翻譯列表
3. ✅ 機器人是否有足夠的權限
4. ✅ 推文連結格式是否正確
5. ✅ 推文是否為公開狀態

使用 `/autotranslate status` 指令可以快速檢查功能狀態。
