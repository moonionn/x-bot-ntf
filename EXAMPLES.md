# 🎯 功能展示與使用範例

## 📱 自動翻譯功能展示

### 設置過程

1. **啟用自動翻譯**
   ```
   /autotranslate add_channel #推文翻譯
   ```
2. **檢查狀態**

   ```
   /autotranslate status
   ```

   ![狀態顯示](images/md/status_example.png)

3. **查看已啟用的頻道**
   ```
   /autotranslate list_channels
   ```

### 實際使用效果

**用戶操作:** 在已啟用的頻道中貼上推文連結

```
https://twitter.com/elonmusk/status/1234567890
```

**Bot 自動回覆:**

---

📝 **原文**

> Just had a great meeting about the future of sustainable transport. Exciting times ahead! 🚗⚡

🌏 **翻譯結果**

> **翻譯一（直接翻譯）**
> 剛剛開了一個關於永續交通未來的精彩會議。令人興奮的時代即將到來！🚗⚡
>
> **翻譯二（自然翻譯）**  
> 剛才開了個超棒的會，討論未來的環保交通。好期待接下來的發展！🚗⚡

📚 **詞句詳細解說**
• **sustainable transport**: 永續交通，指的是對環境影響較小的交通方式，如電動車、公共運輸等
• **Exciting times ahead**: 英語慣用語，表示「未來充滿令人期待的事情」，常用於預告好消息或重大發展

---

## 🐦 Twitter 追蹤功能展示

### 添加追蹤

```
.add @elonmusk #推文通知
```

**成功回應:**
✅ 已開始追蹤 @elonmusk 的推文，將通知到 #推文通知

### 推文通知效果

當被追蹤的用戶發推時，Bot 會自動發送通知：

---

🔔 **@Ping\_推文通知 Elon Musk** just **tweeted** here:
https://twitter.com/elonmusk/status/1234567890

[嵌入式推文預覽，包含圖片/影片]

---

## 🎨 翻譯格式範例

### 日語推文翻譯

**原文:**

> 今日はとても楽しい一日でした！新しいプロジェクトが始まります。みんなで頑張りましょう！🎉

**翻譯結果:**

> **翻譯一（直接翻譯）**
> 今天是非常快樂的一天！新的專案開始了。大家一起努力吧！🎉
>
> **翻譯二（自然翻譯）**
> 今天過得超開心的！新專案要開跑了，大家一起加油！🎉

**詞句解說:**
• **楽しい一日**: 快樂的一天，日語中表達愉快心情的常用說法
• **プロジェクト**: 來自英語 project 的外來語，在日語中廣泛使用
• **みんなで頑張りましょう**: 日語敬語表達，「大家一起努力」的禮貌說法

### 英語推文翻譯

**原文:**

> Breaking: Major breakthrough in AI research! This could change everything we know about machine learning. Thread below 🧵

**翻譯結果:**

> **翻譯一（直接翻譯）**
> 突發：AI 研究重大突破！這可能會改變我們對機器學習的所有認知。下方串文 🧵
>
> **翻譯二（自然翻譯）**
> 爆料：AI 研究有重大進展！這可能顛覆我們對機器學習的理解。詳情請看下面的連續推文 🧵

**詞句解說:**
• **Breaking**: 新聞用語，表示「突發新聞」或「最新消息」
• **Major breakthrough**: 重大突破，指具有重要意義的發現或進展
• **Thread below**: Twitter 特有用語，指「下方的連續推文」，用於發表長篇內容

## ⚙️ 管理功能展示

### 查看追蹤列表

```
.list
```

**回應範例:**

```
📋 追蹤清單 (共 3 個帳號)

🐦 @elonmusk → #推文通知
🐦 @openai → #科技新聞
🐦 @github → #開發者頻道

使用 .remove @username #channel 來移除追蹤
```

### 自動翻譯狀態檢查

```
/autotranslate status
```

**回應範例:**

```
🌍 自動翻譯功能狀態

✅ Gemini API: 已配置且可用
✅ 翻譯功能: 正常運作
📊 已啟用頻道: 2 個
🎯 目標語言: 繁體中文

最近 24 小時翻譯次數: 15 次
```

## 🛠️ 錯誤處理展示

### 翻譯失敗

當翻譯失敗時，Bot 會：

1. 在原訊息上添加 ❌ 反應
2. 在終端記錄詳細錯誤信息
3. 不會發送不完整的翻譯結果

### 追蹤失敗

```
.add @nonexistentuser #channel
```

**回應:**
❌ 找不到用戶 @nonexistentuser，請檢查用戶名稱是否正確

### 權限不足

當用戶沒有管理權限時：

```
/autotranslate add_channel #test
```

**回應:**
🔒 您需要「管理頻道」權限才能設置自動翻譯功能

## 🎨 視覺效果特色

### 嵌入式訊息設計

- 🎨 美觀的色彩配置
- 📱 響應式設計
- 🖼️ 支援圖片預覽
- 🎥 支援影片連結
- 👤 顯示用戶頭像

### 翻譯結果格式化

- 📝 清晰的段落區分
- 🔵 藍色引用線突出翻譯內容
- 📚 分層式詞彙解說
- ✨ 表情符號增強視覺效果

## 💡 使用技巧

### 1. 批量設置

```bash
# 一次添加多個帳號
.add @user1 #channel
.add @user2 #channel
.add @user3 #channel
```

### 2. 多語言支援

翻譯功能自動識別推文語言，支援：

- 🇯🇵 日語 → 繁體中文
- 🇺🇸 英語 → 繁體中文
- 🇰🇷 韓語 → 繁體中文
- 🇫🇷 法語 → 繁體中文
- 🇩🇪 德語 → 繁體中文

### 3. 效率使用

- 使用 `/autotranslate list_channels` 快速查看配置
- 定期使用 `/autotranslate status` 檢查功能狀態
- 利用 `.list` 管理追蹤清單

---

**這些範例展示了 X Bot NTF 的強大功能和用戶友善的設計！** 🎉
