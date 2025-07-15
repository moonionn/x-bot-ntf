# 使用 Alpine Linux 作為基礎映像，更小且更安全
FROM python:3.11-alpine

# 設定工作目錄
WORKDIR /app

# 安裝系統依賴
RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers

# 複製 requirements.txt 並安裝 Python 依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式代碼
COPY . .

# 創建必要的目錄
RUN mkdir -p /app/data

# 設定環境變數
ENV PYTHONPATH=/app
ENV DATA_PATH=/app/data

# 創建非 root 用戶以提高安全性
RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /app
USER botuser

# 暴露端口（如果需要健康檢查或監控）
EXPOSE 8000

# 啟動命令
CMD ["python", "bot.py"]
