# Twitter API 速率限制處理

## 概述

此文件說明 x_bot_ntf 如何處理 Twitter API 的速率限制問題，以及相關的監控和管理功能。

## 新增功能

### 1. 智能速率限制處理

- **自動檢測**: 自動識別 Twitter API 速率限制錯誤
- **指數退避**: 使用指數退避策略處理連續的速率限制錯誤
- **動態延遲**: 根據錯誤頻率動態調整重試間隔

### 2. 速率限制管理器 (`src/notification/rate_limiter.py`)

#### 主要功能

- **錯誤追蹤**: 記錄每個帳戶的速率限制歷史
- **退避策略**: 15分鐘 → 30分鐘 → 1小時 → 2小時 → 5小時
- **狀態監控**: 提供詳細的速率限制狀態報告
- **自動恢復**: 成功請求後自動重置連續錯誤計數

#### 退避時間表

| 連續錯誤次數 | 等待時間 |
|-------------|----------|
| 第1次       | 15分鐘   |
| 第2次       | 30分鐘   |
| 第3次       | 1小時    |
| 第4次       | 2小時    |
| 第5次+      | 5小時    |

### 3. 管理員指令 (`/ratelimit`)

#### 可用指令

- `/ratelimit status` - 查看所有帳戶的速率限制狀態
- `/ratelimit reset <account_name>` - 重置指定帳戶的速率限制記錄

#### 使用範例

```
/ratelimit status
```
顯示所有追蹤帳戶的速率限制狀態，包括：
- 連續錯誤次數
- 最後錯誤時間
- 總速率限制次數

```
/ratelimit reset Account1
```
重置 Account1 的速率限制記錄，讓它立即恢復正常檢查頻率。

## 配置調整

### `configs.yml` 更新

```yaml
# 增加推文檢查間隔，降低 API 請求頻率
tweets_check_period: 30  # 從 10 秒改為 30 秒

# 其他錯誤的重試延遲保持不變
tweets_updater_retry_delay: 300
```

### 建議設定

對於經常遇到速率限制的情況，建議：

1. **增加檢查間隔**: 將 `tweets_check_period` 設為 60-120 秒
2. **減少追蹤帳戶**: 暫時停用部分不重要的追蹤帳戶
3. **使用多個 Twitter 帳戶**: 分散 API 請求負載

## 日誌監控

### 正常運作日誌

```
[INFO] Rate limit status:
  Account1: OK (total rate limits: 0)
  Account2: OK (total rate limits: 2)
```

### 速率限制警告

```
[WARNING] Rate limit hit for account 'Account1' (consecutive: 1, total: 3). Will wait 15 minutes before retry.
```

### 持續性問題

```
[WARNING] Skipping tweets update for Account1 due to persistent rate limiting
```

## 故障排除

### 常見問題

1. **持續速率限制**
   - 檢查是否有其他程式同時使用相同的 Twitter 帳戶
   - 考慮增加 `tweets_check_period`
   - 使用 `/ratelimit reset` 清除錯誤記錄

2. **部分帳戶無法更新**
   - 使用 `/ratelimit status` 檢查狀態
   - 查看日誌中的詳細錯誤訊息
   - 考慮重新驗證 Twitter 帳戶

3. **推文延遲通知**
   - 這是正常現象，速率限制會導致更新延遲
   - 檢查 `tweets_check_period` 設定是否過高

### 手動介入

如果速率限制問題持續：

1. 使用 `/ratelimit reset <account_name>` 重置問題帳戶
2. 暫時停用有問題的追蹤帳戶
3. 聯繫 Twitter API 支援（如果是帳戶級別的限制）

## 最佳實踐

1. **監控日誌**: 定期檢查速率限制狀態日誌
2. **適度使用**: 避免過度頻繁的 API 請求
3. **負載平衡**: 使用多個 Twitter 帳戶分散負載
4. **及時調整**: 根據實際使用情況調整檢查間隔

## 技術細節

### 錯誤識別

系統會檢查以下關鍵字來識別速率限制錯誤：
- `rate limit`
- `too many requests`
- `429`
- `rate_limit_exceeded`
- `quota exceeded`
- `requests per`
- `limit reached`

### 狀態持久化

速率限制狀態儲存在記憶體中，重啟機器人會重置所有記錄。這是設計考量，確保重啟後能快速恢復正常運作。

### 安全機制

- 最長等待時間限制為 6 小時
- 自動跳過持續性問題帳戶
- 成功請求後立即重置連續錯誤計數
