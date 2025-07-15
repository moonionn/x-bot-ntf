from datetime import datetime, timezone, timedelta
from typing import Dict

from src.log import setup_logger

log = setup_logger(__name__)

class RateLimiter:
    """
    Twitter API 速率限制管理器
    """
    
    def __init__(self):
        self.rate_limit_info: Dict[str, Dict] = {}
        self.backoff_delays = [15, 30, 60, 120, 300]  # 指數退避延遲（分鐘）
    
    def is_rate_limited_error(self, error: Exception) -> bool:
        """檢查錯誤是否為速率限制錯誤"""
        error_str = str(error).lower()
        rate_limit_keywords = [
            'rate limit', 'too many requests', '429', 
            'rate_limit_exceeded', 'quota exceeded',
            'requests per', 'limit reached'
        ]
        return any(keyword in error_str for keyword in rate_limit_keywords)
    
    def get_backoff_delay(self, account_name: str) -> int:
        """獲取指定帳戶的退避延遲時間（秒）"""
        if account_name not in self.rate_limit_info:
            self.rate_limit_info[account_name] = {
                'consecutive_errors': 0,
                'last_error_time': None,
                'total_rate_limits': 0
            }
        
        info = self.rate_limit_info[account_name]
        error_count = min(info['consecutive_errors'], len(self.backoff_delays) - 1)
        delay_minutes = self.backoff_delays[error_count]
        
        return delay_minutes * 60
    
    def record_rate_limit(self, account_name: str, error: Exception):
        """記錄速率限制錯誤"""
        if account_name not in self.rate_limit_info:
            self.rate_limit_info[account_name] = {
                'consecutive_errors': 0,
                'last_error_time': None,
                'total_rate_limits': 0
            }
        
        info = self.rate_limit_info[account_name]
        info['consecutive_errors'] += 1
        info['last_error_time'] = datetime.now(timezone.utc)
        info['total_rate_limits'] += 1
        
        delay_minutes = self.backoff_delays[
            min(info['consecutive_errors'] - 1, len(self.backoff_delays) - 1)
        ]
        
        log.warning(
            f"Rate limit hit for account '{account_name}' "
            f"(consecutive: {info['consecutive_errors']}, total: {info['total_rate_limits']}). "
            f"Will wait {delay_minutes} minutes before retry."
        )
    
    def record_success(self, account_name: str):
        """記錄成功請求，重置連續錯誤計數"""
        if account_name in self.rate_limit_info:
            if self.rate_limit_info[account_name]['consecutive_errors'] > 0:
                log.info(f"Account '{account_name}' recovered from rate limiting")
            self.rate_limit_info[account_name]['consecutive_errors'] = 0
    
    def should_skip_request(self, account_name: str, max_wait_hours: int = 6) -> bool:
        """
        檢查是否應該跳過請求（當連續錯誤過多時）
        
        Args:
            account_name: 帳戶名稱
            max_wait_hours: 最大等待時間（小時）
        
        Returns:
            True 如果應該跳過請求
        """
        if account_name not in self.rate_limit_info:
            return False
        
        info = self.rate_limit_info[account_name]
        
        # 如果連續錯誤次數超過閾值
        if info['consecutive_errors'] >= len(self.backoff_delays):
            if info['last_error_time']:
                time_since_error = datetime.now(timezone.utc) - info['last_error_time']
                if time_since_error < timedelta(hours=max_wait_hours):
                    return True
        
        return False
    
    def get_status_summary(self) -> str:
        """獲取所有帳戶的速率限制狀態摘要"""
        if not self.rate_limit_info:
            return "No rate limit data available"
        
        summary = []
        for account, info in self.rate_limit_info.items():
            if info['consecutive_errors'] > 0:
                last_error = info['last_error_time'].strftime('%H:%M:%S') if info['last_error_time'] else 'Unknown'
                summary.append(
                    f"  {account}: {info['consecutive_errors']} consecutive errors, "
                    f"last at {last_error}, total: {info['total_rate_limits']}"
                )
            else:
                summary.append(f"  {account}: OK (total rate limits: {info['total_rate_limits']})")
        
        return "Rate limit status:\n" + "\n".join(summary)

# 全域速率限制管理器實例
rate_limiter = RateLimiter()
