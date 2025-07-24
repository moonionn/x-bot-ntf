import aiohttp
import asyncio
import re
from bs4 import BeautifulSoup
from typing import Optional
try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None
from src.log import setup_logger

log = setup_logger(__name__)


class TweetTranslator:
    def __init__(self, gemini_api_key: str):
        """
        初始化推文翻譯器
        
        Args:
            gemini_api_key: Gemini API 金鑰
        """
        if genai is None:
            raise ImportError("google-genai 套件未安裝，請執行: pip install google-genai")
        
        # 使用新的 Google Gen AI SDK
        self.client = genai.Client(api_key=gemini_api_key)
        
        # 按順序嘗試可用的模型，從最新開始
        self.model_name = self._select_best_model()
        log.info(f"成功初始化 Google Gen AI 客戶端，使用模型: {self.model_name}")
        
    def _select_best_model(self) -> str:
        """選擇最佳可用的 Gemini 模型"""
        # 按優先順序排列的模型列表 (根據用戶要求使用 gemini-2.5-pro)
        model_candidates = [
            'gemini-2.5-pro',      # 用戶指定的最新模型
            'gemini-2.0-flash-001', # 文檔中的推薦模型，備用選項
            'gemini-1.5-pro',      # 穩定版本
            'gemini-1.5-flash',    # 較快的版本
        ]
        
        # 使用用戶指定的 gemini-2.5-pro 模型
        return model_candidates[0]
        
    def extract_username_from_url(self, tweet_url: str) -> Optional[str]:
        """
        從推文 URL 中提取發文者的用戶名
        
        Args:
            tweet_url: 推文網址
            
        Returns:
            發文者的用戶名，如果提取失敗則返回 None
        """
        try:
            import re
            # 匹配 Twitter/X URL 格式：https://twitter.com/username/status/1234567890
            # 或 https://x.com/username/status/1234567890
            pattern = r'https?://(?:twitter\.com|x\.com)/([^/]+)/status/\d+'
            match = re.match(pattern, tweet_url)
            if match:
                username = match.group(1)
                log.info(f"從 URL 提取到用戶名: {username}")
                return username
            else:
                log.warning(f"無法從 URL 提取用戶名: {tweet_url}")
                return None
        except Exception as e:
            log.error(f"提取用戶名時發生錯誤: {e}")
            return None

    async def fetch_tweet_content(self, tweet_url: str) -> Optional[str]:
        """
        爬取推文內容 - 僅提取發文者的原始推文內容
        
        Args:
            tweet_url: 推文網址
            
        Returns:
            發文者的推文文字內容（不包含引用、回覆等），如果失敗則返回 None
        """
        try:
            # 使用簡短的 headers 避免 "Header value is too long" 錯誤
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; bot/1.0)'
            }
            
            # 設置連線超時和讀取超時
            timeout = aiohttp.ClientTimeout(total=30, connect=10)
            
            async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
                # 使用 fxtwitter 來獲取更清潔的內容
                fx_url = tweet_url.replace('twitter.com', 'fxtwitter.com').replace('x.com', 'fxtwitter.com')
                
                try:
                    async with session.get(fx_url) as response:
                        if response.status == 200:
                            html = await response.text()
                            content = self._extract_clean_content(html, method='fxtwitter')
                            if content:
                                log.info(f"成功從 fxtwitter 獲取內容: {content[:50]}...")
                                return content
                        else:
                            log.warning(f"fxtwitter 返回狀態碼: {response.status}")
                except Exception as e:
                    log.warning(f"fxtwitter 請求失敗: {e}")
                
                # 如果失敗，返回 None
                return None
                        
        except Exception as e:
            log.error(f"爬取推文內容失敗: {e}")
            return None
        
        return None
    
    def _extract_clean_content(self, html: str, method: str = 'fxtwitter') -> Optional[str]:
        """
        從 HTML 中提取乾淨的推文內容
        
        Args:
            html: 網頁 HTML 內容
            method: 提取方法 ('fxtwitter', 'twitter', 或 'nitter')
            
        Returns:
            清理後的推文內容
        """
        soup = BeautifulSoup(html, 'html.parser')
        content = None
        
        if method == 'fxtwitter':
            # 從 fxtwitter 的 meta 標籤提取
            meta_description = soup.find('meta', property='og:description')
            if meta_description:
                content = meta_description.get('content', '')
            
        elif method == 'nitter':
            # 從 nitter 提取推文內容
            selectors = [
                '.tweet-content',
                '.tweet-text', 
                '[class*="tweet"] .tweet-content',
                '.timeline-item .tweet-content',
                'meta[property="og:description"]'
            ]
            
            for selector in selectors:
                element = soup.select_one(selector)
                if element:
                    if element.name == 'meta':
                        content = element.get('content', '')
                    else:
                        # 從 nitter 的推文內容中提取純文字
                        content = element.get_text(separator=' ', strip=True)
                    if content:
                        break
            
        elif method == 'twitter':
            # 嘗試從原生 Twitter 頁面提取
            selectors = [
                '[data-testid="tweetText"]',
                '.tweet-text',
                '[role="article"] [data-testid="tweetText"]',
                'meta[property="og:description"]'
            ]
            
            for selector in selectors:
                element = soup.select_one(selector)
                if element:
                    if element.name == 'meta':
                        content = element.get('content', '')
                    else:
                        content = element.get_text(strip=True)
                    break
        
        if content:
            # 清理內容，只保留發文者的原始內容
            content = self._clean_tweet_content(content)
            if content and len(content.strip()) > 5:  # 確保有實際內容
                return content.strip()
        
        return None

    def _clean_tweet_content(self, content: str, tracked_users: list = None) -> str:
        """
        清理推文內容，移除不必要的部分，但保留 emoji 和特殊字符
        
        Args:
            content: 原始推文內容
            
        Returns:
            清理後的內容
        """

        # 檢查是否為單純轉推，如果是就直接返回空字串
        rt_match = re.match(r'^RT @(\w+):\s*(.*?)$', content.strip(), re.DOTALL)
        if rt_match:
            retweeted_username = rt_match.group(1).lower() # 被轉推的用戶名
            remaining_content = rt_match.group(2).strip()

            # 如果是單純轉推（沒有額外評論）
            if not remaining_content:
                # 檢查被轉推的用戶是否在追蹤列表中
                if tracked_users and retweeted_username in [user.lower() for user in tracked_users]:
                    log.info(f"偵測到對追蹤用戶 @{retweeted_username} 的單純轉推，跳過翻譯")
                    return ""
                else:
                    log.info(f"偵測到對非追蹤用戶 @{retweeted_username} 的單純轉推，繼續處理")
            return ""

        # 保持原始內容的完整性，只做必要的清理
        original_content = content
        
        # 移除多餘的空白字符，但保留換行
        content = re.sub(r'[ \t]+', ' ', content)  # 只合併空格和tab，保留換行
        content = re.sub(r'\n\s*\n', '\n', content)  # 移除多餘的空行
        content = content.strip()
        
        # 移除明顯的 Twitter 界面元素，但保留用戶內容
        patterns_to_remove = [
            r'^Quote Tweet\s*',                    # 引用推文前綴
            r'^Replying to @[\w\s,]+\s*',         # 回覆前綴（支援多個用戶）
            r'\s*·\s*\d+[hms]\s*$',               # 時間戳後綴
            r'\s*·\s*\w+\s+\d+,?\s*\d*\s*$',     # 日期後綴
            r'^RT @\w+:\s*',                      # 轉推前綴
            r'\s*Show this thread\s*$',          # 顯示串文後綴
            r'\s*Translate Tweet\s*$',           # 翻譯推文後綴
            r'\s*View Tweet activity\s*$',        # 查看推文活動
            r'\s*\d+\.\d+[KMB]?\s+(Retweets?|Likes?|Replies?)\s*$',  # 互動數據
        ]
        
        # 移除所有前綴的 @ 提及（位於句子開頭或空白字符後）
        content = re.sub(r'(^|\s)@\w+\s*', r'\1', content)  # 移除所有前綴 @username
        
        for pattern in patterns_to_remove:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)
        
        # 不移除 @ 提及和 # 標籤，因為這些可能是內容的重要部分
        # 不移除 URL，因為在社群媒體中連結經常是內容的一部分
        
        # 只移除明顯的引用內容（完整的引號包圍的長段落）
        # 但保留短的引用或對話
        content = re.sub(r'^".*"$', '', content).strip()  # 只移除整個推文都是引號的情況
        
        # 保留所有 Unicode 字符（包括 emoji、各種語言文字）
        # 不進行任何 Unicode 正規化，保持原始字符
        
        # 最終清理：移除前後空白，但保留內容的完整性
        content = content.strip()
        
        # 如果清理後內容為空或只有標點符號，記錄原始內容
        if not content or re.match(r'^[\s\W]*$', content):
            log.warning(f"內容清理後為空，原始內容: {original_content[:100]}...")
            # 如果清理得太乾淨，返回稍微清理的原始內容
            minimal_clean = re.sub(r'^\s*(RT @\w+:\s*|Quote Tweet\s*)', '', original_content).strip()
            if minimal_clean and len(minimal_clean) > 2:
                log.info(f"使用最小清理版本: {minimal_clean[:50]}...")
                return minimal_clean
            return ""
        
        return content
    
    async def translate_text(self, text: str, target_language: str = "繁體中文", platform: str = None, username: str = None) -> Optional[str]:
        """
        使用新的 Google Gen AI SDK 翻譯文字 - 專門針對社群媒體內容優化
        
        Args:
        text: 要翻譯的文字（已清理的推文內容）
        target_language: 目標語言
        platform: 平台名稱（可選，僅用於手動指令）
        username: 發文者用戶名（可選，僅用於手動指令）
            
        Returns:
            翻譯結果，如果失敗則返回 None
        """
        try:
            prompt = f"""將以下社群媒體內容翻譯成{target_language}：

原文：
{text}
請按照以下格式輸出：

**語氣分析：**
[簡短描述原文的語氣、情感特色]

**整句話的意思：**
「[核心含義的直接翻譯]」

**翻成自然且符合台灣情境的{target_language}：**
「[最自然、口語化的翻譯]」

**逐字拆解泰文：**
[對重要詞彙進行羅馬拼音標註和解釋，包含語氣詞、俚語等]

**文化背景說明：**
[如有特殊用法、文化背景或語言特色需要說明(人名、CP 名稱等不解釋)]

翻譯要求：
- 不要出現，這就為您翻譯並分析這則社群媒體內容等開頭，直接進入翻譯。
- 保留原文的語氣情感和 emoji
- 人名識別：Tip, Racha, Namtan, Film, Ying, Muv, Any, Polcasan, Sang, Naree, TipNaree, MuvMuv
- CP 名稱識別：TipRacha, NamtanFilm, MilkLove
- 注意拖長音處理：ร้าช้าาาา → Racha
- 提供自然流暢的台灣口語化翻譯
- 解釋泰文語氣詞和俚語的含義
- 注意X推文有Keyword和Hashtag的使用，保留原有格式，但不用解釋"""

            # 使用新的 SDK 生成內容 - 調整為適合 gemini-2.5-pro 的配置
            if types:
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: self.client.models.generate_content(
                        model=self.model_name,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            temperature=0.5,
                            max_output_tokens=16384,  # 增加輸出 token 限制以支援格式化輸出
                            top_p=0.95,
                            top_k=40,
                            safety_settings=[
                                types.SafetySetting(
                                    category='HARM_CATEGORY_HARASSMENT',
                                    threshold='BLOCK_NONE',
                                ),
                                types.SafetySetting(
                                    category='HARM_CATEGORY_HATE_SPEECH',
                                    threshold='BLOCK_NONE',
                                ),
                                types.SafetySetting(
                                    category='HARM_CATEGORY_SEXUALLY_EXPLICIT',
                                    threshold='BLOCK_NONE',
                                ),
                                types.SafetySetting(
                                    category='HARM_CATEGORY_DANGEROUS_CONTENT',
                                    threshold='BLOCK_NONE',
                                ),
                            ]
                        )
                    )
                )
            else:
                # 備用方案：如果 types 未導入，使用字典配置
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: self.client.models.generate_content(
                        model=self.model_name,
                        contents=prompt,
                        config={
                            'temperature': 0.3,
                            'max_output_tokens': 8192,  # 增加輸出 token 限制
                            'top_p': 0.95,
                            'top_k': 40,
                        }
                    )
                )
            
            # 處理回應
            # 檢查各種可能的回應格式
            if hasattr(response, 'text') and response.text:
                translated_text = response.text.strip()

                # 只有在手動指令且提供來源資訊時才添加前綴
                if platform or username:
                    source_info = ""
                    if username and platform:
                        source_info = f"來自 {username}'s {platform}\n\n"
                    elif username:
                        source_info = f"來自 {username}\n\n"
                    elif platform:
                        source_info = f"來自 {platform}\n\n"
                    
                    if source_info:
                        translated_text = f"{source_info}{translated_text}"
                
                if translated_text and len(translated_text.strip()) > 0:
                    log.info(f"翻譯成功: {translated_text[:100]}...")
                    return translated_text
            
            # 檢查 candidates 結構
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                
                # 檢查 finish_reason
                if hasattr(candidate, 'finish_reason'):
                    if str(candidate.finish_reason) == 'MAX_TOKENS':
                        log.error("回應被截斷 (MAX_TOKENS)，翻譯失敗")
                        return None
                
                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts') and candidate.content.parts:
                        part = candidate.content.parts[0]
                        if hasattr(part, 'text') and part.text:
                            translated_text = part.text.strip()

                            # 只有在手動指令且提供來源資訊時才添加前綴
                            if platform or username:
                                source_info = ""
                                if username and platform:
                                    source_info = f"來自 {username}'s {platform}\n\n"
                                elif username:
                                    source_info = f"來自 {username}\n\n"
                                elif platform:
                                    source_info = f"來自 {platform}\n\n"
                                
                                if source_info:
                                    translated_text = f"{source_info}{translated_text}"

                            if translated_text:
                                log.info(f"翻譯成功: {translated_text[:100]}...")
                                return translated_text
            
            log.warning("無法從 API 回應中提取翻譯內容")
            return None
            
        except Exception as e:
            log.error(f"新 SDK 翻譯失敗: {e}")
            return None
    
    async def translate_tweet(self, tweet_url: str, target_language: str = "繁體中文", tracked_users: list = None) -> dict:
        """
        完整的推文翻譯流程 - 只翻譯發文者的原始內容
        
        Args:
            tweet_url: 推文網址
            target_language: 目標語言
            
        Returns:
            包含原文、翻譯和發文者資訊的字典
        """
        result = {
            "success": False,
            "original_text": None,
            "cleaned_text": None,  # 新增：顯示清理後的文字
            "translated_text": None,
            "username": None,  # 新增：發文者用戶名
            "error": None
        }
        
        try:
            # 步驟1: 提取發文者用戶名
            username = self.extract_username_from_url(tweet_url)
            if username:
                result["username"] = username
                log.info(f"推文發文者: @{username}")
            
            # 步驟2: 爬取推文內容
            log.info(f"正在爬取推文內容: {tweet_url}")
            raw_content = await self.fetch_tweet_content(tweet_url)
            
            if not raw_content:
                result["error"] = "❌ 無法獲取推文內容\n\n可能原因：\n• 推文已被刪除或設為私人\n• 網路連線問題\n• Twitter 反爬蟲限制\n• 推文連結格式錯誤\n\n💡 建議：\n• 確認推文是公開可見的\n• 檢查網址是否正確\n• 稍後再試"
                return result
            
            result["original_text"] = raw_content
            log.info(f"成功獲取推文內容 (長度: {len(raw_content)}): {raw_content[:100]}...")
            
            # 步驟3: 進一步清理內容（移除非發文者內容）
            cleaned_content = self._further_clean_for_translation(raw_content, tracked_users)
            
            if not cleaned_content or len(cleaned_content.strip()) < 2:
                # 如果清理後內容太少，使用原始內容
                cleaned_content = raw_content
                log.warning("清理後內容過短，使用原始內容進行翻譯")
            
            result["cleaned_text"] = cleaned_content
            log.info(f"用於翻譯的內容 (長度: {len(cleaned_content)}): {cleaned_content}")
            
            # 步驟4: 翻譯內容
            log.info(f"開始翻譯成{target_language}")
            translated_text = await self.translate_text(cleaned_content, target_language)
            
            if not translated_text:
                result["error"] = "❌ 翻譯失敗\n\n可能原因：\n• Gemini API 配額用盡\n• API 金鑰無效\n• 網路連線問題\n• 內容包含不支援的格式\n\n💡 建議：\n• 檢查 API 金鑰是否有效\n• 稍後再試\n• 聯繫管理員檢查配置"
                return result
            
            result["translated_text"] = translated_text
            result["success"] = True
            log.info(f"翻譯完成: {translated_text[:50]}...")
            
        except Exception as e:
            result["error"] = f"處理過程中發生錯誤: {str(e)}"
            log.error(f"翻譯推文時發生錯誤: {e}")
        
        return result
    
    def _further_clean_for_translation(self, content: str, tracked_users: list = None) -> str:
        """
        為翻譯進一步清理內容，確保只包含發文者的核心內容
        
        Args:
            content: 初步清理的內容
            
        Returns:
            進一步清理後的內容
        """

         # 首先使用原有的清理邏輯
        content = self._clean_tweet_content(content, tracked_users)
        
        # 如果已經被標記為跳過（返回空字串），直接返回
        if not content:
            return content

        # 移除用戶提及（但保留在句子中間的提及）
        content = re.sub(r'^@\w+\s+', '', content)  # 移除開頭的 @username
        
        # 移除話題標籤前的多餘空格
        content = re.sub(r'\s+#', ' #', content)
        
        # 移除 "RT @username:" 格式的轉推標記
        content = re.sub(r'^RT @\w+:\s*', '', content)
        
        # 移除引用推文的標記
        content = re.sub(r'QT\s+@\w+:\s*', '', content)
        
        # 移除時間相關的後綴
        content = re.sub(r'\s*\b(ago|前|earlier|earlier today)\b.*$', '', content, flags=re.IGNORECASE)
        
        # 移除互動數據（讚、轉推、回覆數）
        content = re.sub(r'\s*\d+\s*(likes?|retweets?|replies?|個讚|次轉推|則回覆)\s*$', '', content, flags=re.IGNORECASE)
        
        # 移除推文來源資訊
        content = re.sub(r'\s*via\s+\w+.*$', '', content, flags=re.IGNORECASE)
        
        # 確保內容不只是標點符號或空白
        if re.match(r'^[\s\W]*$', content):
            return ""
        
        return content.strip()
