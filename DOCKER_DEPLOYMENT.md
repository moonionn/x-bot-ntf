# Docker 部署指南

本指南將幫助您使用 Docker 部署 X Bot 通知系統到 Google Cloud VM 或其他 Linux 服務器。

## 快速部署

### 1. 克隆倉庫

```bash
git clone <您的倉庫URL>
cd x_bot_ntf
```

### 2. 自動部署（推薦）

執行自動部署腳本：

```bash
./deploy.sh
```

這個腳本會：
- 自動安裝 Docker（如果未安裝）
- 創建必要的配置文件
- 構建並啟動 Docker 容器

### 3. 手動部署

如果您更喜歡手動控制部署過程：

```bash
# 複製配置文件
cp configs.example.yml configs.yml

# 創建環境變數文件
cp .env.example .env  # 如果存在的話

# 編輯配置文件
nano configs.yml
nano .env

# 構建並啟動
docker-compose up -d
```

## 配置設置

### 環境變數文件 (.env)

```env
# Discord Bot Token
BOT_TOKEN=your_discord_bot_token_here

# X/Twitter API 配置
CLIENT_1_BEARER_TOKEN=your_bearer_token_here
CLIENT_1_API_KEY=your_api_key_here
CLIENT_1_API_SECRET=your_api_secret_here

# Gemini AI API Key (翻譯功能)
GEMINI_API_KEY=your_gemini_api_key_here

# 資料路徑
DATA_PATH=/app/data
```

### 配置文件 (configs.yml)

請參考 `configs.example.yml` 並根據您的需求進行配置。

## 常用命令

```bash
# 查看服務狀態
docker-compose ps

# 查看實時日誌
docker-compose logs -f

# 停止服務
docker-compose down

# 重啟服務
docker-compose restart

# 更新應用
git pull
docker-compose build
docker-compose up -d

# 進入容器內部（調試用）
docker-compose exec x-bot sh
```

## Google Cloud VM 部署

### 1. 創建 VM 實例

```bash
# 使用 gcloud CLI 創建實例
gcloud compute instances create x-bot-vm \
    --zone=asia-east1-a \
    --machine-type=e2-micro \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=20GB \
    --tags=http-server,https-server
```

### 2. 連接到 VM

```bash
gcloud compute ssh x-bot-vm --zone=asia-east1-a
```

### 3. 部署應用

在 VM 上執行：

```bash
# 更新系統
sudo apt update && sudo apt upgrade -y

# 安裝 Git
sudo apt install git -y

# 克隆項目
git clone <您的倉庫URL>
cd x_bot_ntf

# 執行部署
./deploy.sh
```

## 安全建議

1. **防火牆設置**：只開放必要的端口
2. **定期更新**：保持系統和 Docker 映像更新
3. **備份數據**：定期備份 `data/` 目錄
4. **監控日誌**：定期檢查應用日誌

## 故障排除

### 容器無法啟動

```bash
# 檢查日誌
docker-compose logs

# 檢查配置文件
cat configs.yml
cat .env
```

### 記憶體不足

如果您的 VM 記憶體較小，可以：

1. 升級 VM 規格
2. 添加 swap 空間：

```bash
sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### 網絡問題

檢查防火牆設置：

```bash
# Ubuntu/Debian
sudo ufw status

# 如果需要開放端口（通常不需要，除非您添加了 Web 介面）
sudo ufw allow 8000
```

## 監控和維護

### 設置定期備份

創建備份腳本：

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf "/backup/x-bot-backup-$DATE.tar.gz" /path/to/x_bot_ntf/data/
```

### 日誌輪轉

Docker 預設會處理日誌輪轉，但您可以調整設置：

```yaml
# 在 docker-compose.yml 中添加
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

## 支援

如果您遇到問題，請：

1. 檢查日誌：`docker-compose logs`
2. 確認配置文件正確
3. 查看項目的其他文檔文件
4. 提交 Issue 到 GitHub 倉庫
