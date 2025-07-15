# 快速啟動指南

## 🚀 5 分鐘快速設置

如果您想要快速開始使用 X Bot NTF，請按照以下步驟：

### 1. 準備工作 (2 分鐘)

**必需的資料:**

- Discord Bot Token ([如何獲取](https://discord.com/developers/applications))
- Twitter/X 帳號 (用戶名稱和密碼)
- Gemini API Key ([如何獲取](https://aistudio.google.com/app/apikey))

### 2. 安裝與配置 (2 分鐘)

```bash
# 1. 安裝相依套件
pip install -r requirements.txt

# 2. 複製配置檔案
cp configs.example.yml configs.yml

# 3. 編輯 configs.yml，填入您的資料
# translation:
#   gemini_api_key: "你的_Gemini_API_金鑰"
```

### 3. 設置環境變數 (1 分鐘)

建立 `.env` 檔案或直接設置：

```bash
export DISCORD_TOKEN="你的_Discord_Bot_Token"
export TWITTER_USERNAME="你的_Twitter_帳號"
export TWITTER_PASSWORD="你的_Twitter_密碼"
export GEMINI_API_KEY="你的_Gemini_API_金鑰"
```

### 4. 啟動 Bot

```bash
python bot.py
```

---

## 🎯 立即使用

### 基本功能測試

1. **測試追蹤功能**

   ```
   .add @elonmusk #general
   ```

2. **測試翻譯功能**

   ```
   /translate https://twitter.com/username/status/1234567890
   ```

3. **設置自動翻譯**
   ```
   /autotranslate add_channel #general
   ```

### 驗證功能是否正常

- ✅ Bot 出現在 Discord 服務器中
- ✅ 使用 `.list` 可以看到追蹤列表
- ✅ 使用 `/autotranslate status` 看到綠色勾號
- ✅ 在頻道中貼上推文連結會自動翻譯

---

## 🔧 進階配置

想要詳細了解所有功能嗎？請查看 [完整使用指南](USAGE_GUIDE.md)

### 常用指令一覽

```bash
# 追蹤管理
.add @username #channel      # 添加追蹤
.remove @username #channel   # 移除追蹤
.list                       # 查看追蹤清單

# 翻譯功能
/translate <推文連結>        # 手動翻譯
/autotranslate add_channel  # 設置自動翻譯
/autotranslate status       # 檢查翻譯狀態

# 系統管理
/sync                       # 同步指令
/list_users                 # 管理用戶列表
```

---

## ❗ 常見問題

**Q: Bot 啟動後沒有反應？**
A: 檢查 Discord Token 是否正確，確認 Bot 已被邀請到服務器

**Q: 無法追蹤 Twitter 帳號？**
A: 檢查 Twitter 帳號密碼是否正確，確認帳號沒有被限制

**Q: 翻譯功能不工作？**
A: 確認 Gemini API Key 正確，使用 `/autotranslate status` 檢查狀態

**Q: 自動翻譯沒有觸發？**
A: 確認頻道已加入自動翻譯列表：`/autotranslate list_channels`

---

**需要更詳細的說明？請查看 [完整使用指南](USAGE_GUIDE.md) 📖**
