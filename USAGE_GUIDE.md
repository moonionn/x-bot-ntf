# X Bot NTF 完整使用指南

## 📋 目錄

1. [系統需求與安裝](#系統需求與安裝)
2. [基本配置](#基本配置)
3. [Twitter 追蹤功能](#twitter-追蹤功能)
4. [翻譯功能](#翻譯功能)
5. [自動翻譯功能](#自動翻譯功能)
6. [管理指令](#管理指令)
7. [故障排除](#故障排除)
8. [更新與維護](#更新與維護)

---

## 🔧 系統需求與安裝

### 前置需求

- Python 3.8+
- Discord Bot Token
- Twitter/X 帳號 (用於追蹤功能)
- Gemini API Key (用於翻譯功能)

### 安裝步驟

1. **克隆/下載專案**

   ```bash
   # 如果有 git repository
   git clone <repository-url>
   cd x_bot_ntf
   ```

2. **建立虛擬環境**

   ```bash
   python -m venv .venv

   # 啟動虛擬環境
   # macOS/Linux:
   source .venv/bin/activate

   # Windows:
   .venv\Scripts\activate
   ```

3. **安裝相依套件**

   ```bash
   pip install -r requirements.txt
   ```

4. **配置設定檔**
   ```bash
   cp configs.example.yml configs.yml
   ```

---

## ⚙️ 基本配置

### 1. 編輯 `configs.yml`

```yaml
# Discord Bot 基本設置
prefix: "." # 指令前綴
activity_name: "{count} accounts" # Bot 狀態顯示
activity_type: "watching" # Bot 活動類型

# 推文檢查設置
tweets_check_period: 10 # 檢查推文間隔(秒)
tweets_updater_retry_delay: 5 # 重試延遲(秒)

# 自動化設置
auto_change_client: false # 自動更換客戶端
auto_turn_off_notification: true # 自動關閉通知
auto_unfollow: true # 自動取消追蹤

# 嵌入式訊息設置
embed:
  type: "built_in" # 或 'fx_twitter'
  built_in:
    fx_image: true # 顯示圖片
    video_link_button: false # 影片連結按鈕
    legacy_logo: true # 使用舊版 logo

# 翻譯功能設置
translation:
  default_target_language: "繁體中文" # 預設翻譯語言
  auto_translate_channels: [] # 自動翻譯頻道ID列表

# 注意：Gemini API Key 請設置在環境變數 GEMINI_API_KEY 中
```

### 2. 設置環境變數

建立 `.env` 檔案或設置系統環境變數：

```bash
# Discord
DISCORD_TOKEN=你的_Discord_Bot_Token

# Twitter/X (用於追蹤功能)
TWITTER_USERNAME=你的_Twitter_帳號
TWITTER_PASSWORD=你的_Twitter_密碼

# Gemini (用於翻譯功能)
GEMINI_API_KEY=你的_Gemini_API_金鑰
```

---

## 🐦 Twitter 追蹤功能

### 基本使用

1. **添加追蹤帳號**
   ```
   .add @username #channel
   ```
2. **移除追蹤帳號**

   ```
   .remove @username #channel
   ```

3. **查看追蹤列表**

   ```
   .list
   ```

4. **同步指令**
   ```
   /sync
   ```

### 進階功能

- **批量管理**: 使用 `/list_users` 查看並管理所有追蹤的用戶
- **自動取消追蹤**: 當 Twitter 帳號被停用時自動移除
- **錯誤恢復**: 自動重試失敗的追蹤請求

---

## 🌍 翻譯功能

### 手動翻譯

使用 `/translate` 指令翻譯推文：

```
/translate <推文連結>
```

**支援的連結格式:**

- `https://twitter.com/username/status/1234567890`
- `https://x.com/username/status/1234567890`
- `http://twitter.com/username/status/1234567890`
- `http://x.com/username/status/1234567890`

### 翻譯結果格式

翻譯會包含三個部分：

```
📝 原文
[原始推文內容]

🌏 翻譯結果
> **翻譯一（直接翻譯）**
> [保持原意的直接翻譯]
>
> **翻譯二（自然翻譯）**
> [自然、口語化的翻譯]

📚 詞句詳細解說
• 詞彙1: 解釋與文化背景
• 詞彙2: 解釋與文化背景
```

---

## 🤖 自動翻譯功能

### 設置自動翻譯

1. **添加頻道到自動翻譯列表**

   ```
   /autotranslate add_channel #your-channel
   ```

2. **移除頻道的自動翻譯**

   ```
   /autotranslate remove_channel #your-channel
   ```

3. **查看已啟用的頻道**

   ```
   /autotranslate list_channels
   ```

4. **檢查功能狀態**
   ```
   /autotranslate status
   ```

### 自動翻譯如何運作

自動翻譯功能有兩種工作模式：

1. **推文通知自動翻譯**（主要功能）

   - **觸發條件**: 機器人在已啟用的頻道中發送推文通知
   - **自動檢測**: Bot 會自動識別推文通知中的推文連結
   - **翻譯處理**: 自動爬取推文內容並使用 Gemini 進行翻譯
   - **結果回覆**: 以回覆形式發送格式化的翻譯結果到推文通知下方

2. **手動連結翻譯**（輔助功能）
   - **觸發條件**: 用戶在已啟用的頻道中發送包含 Twitter/X 連結的訊息
   - **自動檢測**: Bot 會自動識別訊息中的推文連結
   - **翻譯處理**: 自動爬取推文內容並使用 Gemini 進行翻譯
   - **結果回覆**: 以回覆形式發送格式化的翻譯結果

### 功能特色

- ✅ **智能檢測**: 自動識別推文通知和手動發送的推文連結
- ✅ **雙重翻譯**: 提供直接翻譯與自然翻譯兩種風格
- ✅ **詞彙解說**: 重要詞彙的詳細文化背景說明
- ✅ **格式美化**: 使用引用格式突出翻譯內容
- ✅ **錯誤處理**: 翻譯失敗時顯示 ❌ 反應
- ✅ **權限控制**: 需要管理頻道權限才能設置
- ✅ **通知翻譯**: 自動翻譯機器人發送的推文通知（主要功能）
- ✅ **手動翻譯**: 支援用戶手動發送的推文連結翻譯

---

## 🛠️ 管理指令

### 追蹤管理

```
.add @username #channel        # 添加追蹤
.remove @username #channel     # 移除追蹤
.list                         # 查看追蹤列表
/list_users                   # 批量管理用戶
```

### 翻譯管理

```
/translate <url>              # 手動翻譯
/autotranslate add_channel    # 添加自動翻譯頻道
/autotranslate remove_channel # 移除自動翻譯頻道
/autotranslate list_channels  # 查看自動翻譯頻道
/autotranslate status         # 檢查翻譯功能狀態
```

### 系統管理

```
/sync                         # 同步指令
/rate_limit_admin            # 速率限制管理
```

---

## 🔍 故障排除

### 常見問題

#### 1. Bot 無法啟動

**檢查項目:**

- ✅ Discord Token 是否正確
- ✅ Python 版本是否為 3.8+
- ✅ 相依套件是否安裝完成
- ✅ configs.yml 語法是否正確

**解決方法:**

```bash
# 檢查 Python 版本
python --version

# 重新安裝相依套件
pip install -r requirements.txt --upgrade

# 檢查配置檔案語法
python -c "import yaml; yaml.safe_load(open('configs.yml'))"
```

#### 2. 無法追蹤 Twitter 帳號

**檢查項目:**

- ✅ Twitter 帳號密碼是否正確
- ✅ Twitter 帳號是否被限制
- ✅ 網路連線是否正常

**解決方法:**

```bash
# 檢查 Twitter 登入狀態
# 查看 console.log 中的錯誤訊息
```

#### 3. 翻譯功能無法使用

**檢查項目:**

- ✅ Gemini API Key 是否正確
- ✅ API 配額是否足夠
- ✅ 推文連結格式是否正確
- ✅ 推文是否為公開狀態

**解決方法:**

```bash
# 測試 API Key
/autotranslate status

# 手動測試翻譯
/translate https://twitter.com/username/status/1234567890
```

#### 4. 自動翻譯不工作

**檢查項目:**

- ✅ 頻道是否已添加到自動翻譯列表
- ✅ Bot 是否有發送訊息權限
- ✅ 連結格式是否支援

**解決方法:**

```bash
# 檢查頻道列表
/autotranslate list_channels

# 重新添加頻道
/autotranslate add_channel #your-channel
```

### 日誌檢查

查看 `console.log` 文件以獲取詳細錯誤信息：

```bash
tail -f console.log
```

---

## 🔄 更新與維護

### 定期維護

1. **更新相依套件**

   ```bash
   pip install -r requirements.txt --upgrade
   ```

2. **清理日誌檔案**

   ```bash
   # 備份並清理日誌
   cp console.log console.log.backup
   > console.log
   ```

3. **資料庫維護**
   ```bash
   # 修復資料庫 (如果需要)
   python src/db_function/repair_db.py
   ```

### 備份重要檔案

建議定期備份以下檔案：

- `configs.yml` - 配置檔案
- `data/tracked_accounts.db` - 追蹤帳號資料庫
- `Account1.tw_session` - Twitter 登入狀態

### 版本更新

1. **備份當前版本**

   ```bash
   cp -r x_bot_ntf x_bot_ntf_backup
   ```

2. **下載新版本並覆蓋**
3. **恢復配置檔案**
   ```bash
   cp x_bot_ntf_backup/configs.yml x_bot_ntf/
   cp x_bot_ntf_backup/data/ x_bot_ntf/data/
   ```

---

## 📞 支援與社群

### 獲取幫助

- 📖 查看 [CHANGELOG.md](docs/CHANGELOG.md) 了解版本更新
- 🌍 多語言支援請參考 [翻譯指南](TRANSLATION_GUIDE.md)
- ⚡ 速率限制說明請參考 [RATE_LIMIT_GUIDE.md](RATE_LIMIT_GUIDE.md)

### 回報問題

如果遇到問題，請提供以下資訊：

1. 詳細的錯誤訊息
2. `console.log` 中的相關日誌
3. 系統環境（Python 版本、作業系統）
4. 重現問題的步驟

---

## ⚠️ 重要注意事項

1. **API 配額**: Gemini API 有使用限制，請注意配額管理
2. **Twitter 政策**: 遵守 Twitter 的使用條款和 API 政策
3. **隱私保護**: 不要在公開場所分享 API Key 或登入憑證
4. **效能考量**: 大量追蹤帳號可能影響效能，建議合理設置檢查間隔

---

**🎉 恭喜！您已完成 X Bot NTF 的完整設置。開始享受自動化的 Twitter 追蹤與翻譯功能吧！**
