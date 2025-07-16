import os
import discord
from discord import app_commands
from discord.ext import commands
import re

from core.classes import Cog_Extension
from src.log import setup_logger

# 暫時註解掉，等安裝套件後再啟用
from src.translation.tweet_translator import TweetTranslator

log = setup_logger(__name__)


class Translation(Cog_Extension):
    """推文翻譯功能"""
    
    def __init__(self, bot):
        super().__init__(bot)
        self.translator = None
        
        # 從環境變數讀取 Gemini API 金鑰
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        
        if gemini_api_key:
            try:
                self.translator = TweetTranslator(gemini_api_key=gemini_api_key)
                log.info("Gemini API 翻譯器初始化成功")
            except Exception as e:
                log.error(f"Gemini API 翻譯器初始化失敗: {e}")
        else:
            log.warning("未設定 GEMINI_API_KEY 環境變數，翻譯功能將無法使用")
        
        if not self.translator:
            log.warning("翻譯器未初始化，翻譯功能將無法使用")

    translate_group = app_commands.Group(
        name='translate', 
        description='翻譯相關功能'
    )

    @translate_group.command(name='tweet')
    async def translate_tweet(
        self, 
        interaction: discord.Interaction, 
        url: str, 
        language: str = "繁體中文"
    ):
        """
        翻譯推文內容
        
        Parameters
        ----------
        url: str
            推文網址 (例如: https://twitter.com/username/status/1234567890)
        language: str
            目標語言 (預設: 繁體中文)
        """
        await interaction.response.defer(ephemeral=True)
        
        # 驗證網址格式
        if not self._is_valid_twitter_url(url):
            await interaction.followup.send(
                "❌ 請提供有效的 Twitter 網址\n"
                "格式範例: https://twitter.com/username/status/1234567890",
                ephemeral=True
            )
            return
        
        # 檢查翻譯器是否已初始化
        if not self.translator:
            await interaction.followup.send(
                "❌ 翻譯功能尚未設定完成\n"
                "請聯繫管理員設定 Gemini API 金鑰",
                ephemeral=True
            )
            return
        
        try:
            # 執行翻譯
            embed = discord.Embed(
                title="🔄 正在翻譯推文...",
                description="🕸️ 正在爬取推文內容...\n🧹 清理非必要內容...\n🧠 AI 翻譯中...",
                color=0x1da0f2
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            
            # 執行翻譯流程
            result = await self.translator.translate_tweet(url, language)
            
            if result["success"]:
                # 翻譯成功 - 使用新的格式
                embed = discord.Embed(
                    title="✅ 翻譯完成",
                    color=0x00ff00
                )
                
                # 添加發文者資訊（如果成功提取到）
                if result.get("username"):
                    embed.add_field(
                        name="👤 發文者",
                        value=f"@{result['username']}",
                        inline=True
                    )
                
                # 格式化原文 - 不需要語言檢測
                original_text = result["original_text"]
                
                embed.add_field(
                    name="📝 原文",
                    value=self._truncate_text(original_text, 1024),
                    inline=False
                )
                
                # 格式化翻譯結果 - 如果是新格式就直接顯示，否則包裝一下
                if result["translated_text"]:
                    translated_text = result["translated_text"]
                    
                    # 檢查是否已經是格式化的輸出（包含新的格式標識）
                    if any(keyword in translated_text for keyword in ["翻譯一 (直接翻譯", "翻譯二 (最自然", "## 詞句詳細解說"]):
                        # 已經是新格式，分割並顯示
                        self._add_formatted_translation_fields(embed, translated_text)
                    else:
                        # 舊格式或簡單翻譯，包裝一下
                        formatted_translation = f"**翻譯結果：**\n\n{translated_text}"
                        embed.add_field(
                            name="🌏 翻譯結果",
                            value=self._truncate_text(formatted_translation, 1024),
                            inline=False
                        )
                
                # # 添加來源連結
                # embed.add_field(
                #     name="🔗 來源",
                #     value=f"[查看原推文]({url})",
                #     inline=False
                # )
                
                embed.set_footer(text="✨ 已過濾引用、回覆等內容，僅翻譯發文者原創內容 | 由 Gemini AI 提供翻譯服務")
                
                # 創建一個按鈕，讓用戶可以將翻譯結果發送到頻道
                view = TranslationResultView(embed, url)
                await interaction.edit_original_response(embed=embed, view=view)
                
            else:
                # 翻譯失敗
                embed = discord.Embed(
                    title="❌ 翻譯失敗",
                    description=f"錯誤原因: {result.get('error', '未知錯誤')}",
                    color=0xff0000
                )
                await interaction.edit_original_response(embed=embed)
                
        except Exception as e:
            log.error(f"翻譯推文時發生錯誤: {e}")
            embed = discord.Embed(
                title="❌ 系統錯誤",
                description="處理請求時發生未預期的錯誤，請稍後再試",
                color=0xff0000
            )
            await interaction.edit_original_response(embed=embed)

    @translate_group.command(name='text')
    async def translate_text(
        self, 
        interaction: discord.Interaction, 
        text: str, 
        language: str = "繁體中文"
    ):
        """
        翻譯一般文字
        
        Parameters
        ----------
        text: str
            要翻譯的文字
        language: str
            目標語言 (預設: 繁體中文)
        """
        await interaction.response.defer(ephemeral=True)
        
        if not self.translator:
            await interaction.followup.send(
                "❌ 翻譯功能尚未設定完成\n"
                "請聯繫管理員設定 Gemini API 金鑰",
                ephemeral=True
            )
            return
        
        if len(text) > 2000:
            await interaction.followup.send(
                "❌ 文字長度不能超過 2000 字元",
                ephemeral=True
            )
            return
        
        try:
            # 執行翻譯
            embed = discord.Embed(
                title="🔄 正在翻譯文字...",
                description="請稍候，正在處理您的請求",
                color=0x1da0f2
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            
            translated_text = await self.translator.translate_text(text, language)
            
            if translated_text:
                embed = discord.Embed(
                    title="✅ 翻譯完成",
                    color=0x00ff00
                )
                
                embed.add_field(
                    name="📝 原文",
                    value=self._truncate_text(text, 1024),
                    inline=False
                )
                
                embed.add_field(
                    name=f"🌏 翻譯 ({language})",
                    value=self._truncate_text(translated_text, 1024),
                    inline=False
                )
                
                embed.set_footer(text="由 Gemini AI 提供翻譯服務，僅供參考。")
                
                # 創建一個按鈕，讓用戶可以將翻譯結果發送到頻道
                view = TextTranslationResultView(embed)
                await interaction.edit_original_response(embed=embed, view=view)
                
            else:
                embed = discord.Embed(
                    title="❌ 翻譯失敗",
                    description="無法翻譯此文字，請檢查內容是否正確",
                    color=0xff0000
                )
                await interaction.edit_original_response(embed=embed)
                
        except Exception as e:
            log.error(f"翻譯文字時發生錯誤: {e}")
            embed = discord.Embed(
                title="❌ 系統錯誤",
                description="處理請求時發生未預期的錯誤，請稍後再試",
                color=0xff0000
            )
            await interaction.edit_original_response(embed=embed)

    def _is_valid_twitter_url(self, url: str) -> bool:
        """驗證 Twitter 網址格式"""
        pattern = r'https?://(twitter\.com|x\.com)/\w+/status/\d+'
        return bool(re.match(pattern, url))
    
    def _truncate_text(self, text: str, max_length: int) -> str:
        """截斷過長的文字"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."

    def _add_formatted_translation_fields(self, embed: discord.Embed, translated_text: str):
        """
        將格式化的翻譯結果分割成多個字段以避免 Discord 字符限制
        
        Args:
            embed: Discord embed 對象
            translated_text: 格式化的翻譯文本
        """
        # 分割翻譯結果 - 尋找 "## 詞句詳細解說" 分隔符
        if "## 詞句詳細解說" in translated_text:
            parts = translated_text.split("## 詞句詳細解說")
            translation_part = parts[0].strip()
            explanation_part = parts[1].strip() if len(parts) > 1 else ""  # 移除重複的標題
        else:
            translation_part = translated_text
            explanation_part = ""
        
        # 處理翻譯部分 - 提取翻譯一和翻譯二
        if translation_part:
            # 移除原文部分，只保留翻譯部分
            lines = translation_part.split('\n')
            translation_content = []
            skip_until_translation = True
            
            for line in lines:
                # 跳過原文部分，從翻譯一開始收集
                if "翻譯一 (直接翻譯" in line or "翻譯二 (最自然" in line:
                    skip_until_translation = False
                    translation_content.append(line)
                elif not skip_until_translation and not line.strip().endswith("原文："):
                    translation_content.append(line)
            
            final_translation = '\n'.join(translation_content).strip()
            
            # 為翻譯內容加粗格式化（只對引號內的翻譯內容加粗）
            formatted_translation = self._format_translation_bold(final_translation)
            
            if formatted_translation:
                embed.add_field(
                    name="🌏 翻譯結果",
                    value=self._truncate_text(formatted_translation, 1024),
                    inline=False
                )
        
        # 處理詞彙解釋部分
        if explanation_part:
            embed.add_field(
                name="📚 詞句詳細解說",
                value=self._truncate_text(explanation_part, 1024),
                inline=False
            )

    def _format_translation_bold(self, translation_text: str) -> str:
        """
        為翻譯內容添加格式化
        
        Args:
            translation_text: 原始翻譯文本
            
        Returns:
            格式化後的文本
        """
        # 使用 Discord 的引用格式來突出翻譯內容
        # 為引號內的內容添加引用格式（藍色線條）
        formatted_text = re.sub(r'「([^」]+)」', lambda m: f'> 「{m.group(1)}」', translation_text)
        
        return formatted_text


class TranslationResultView(discord.ui.View):
    """翻譯結果的操作界面"""
    
    def __init__(self, embed: discord.Embed, tweet_url: str):
        super().__init__(timeout=300)  # 5分鐘後超時
        self.embed = embed
        self.tweet_url = tweet_url
        
        # 添加查看原推文的連結按鈕
        self.add_item(discord.ui.Button(
            label='🔗 查看原推文',
            style=discord.ButtonStyle.link,
            url=tweet_url
        ))

    @discord.ui.button(label='📤 發送到頻道', style=discord.ButtonStyle.primary)
    async def send_to_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        """將翻譯結果發送到目前頻道"""
        try:
            # 創建新的 embed 供公開顯示
            public_embed = discord.Embed(
                title="🌏 推文翻譯",
                color=0x1da0f2
            )
            
            # 複製字段
            for field in self.embed.fields:
                public_embed.add_field(
                    name=field.name,
                    value=field.value,
                    inline=field.inline
                )
            
            public_embed.set_footer(text=f"翻譯請求者: {interaction.user.display_name} | 由 Gemini AI 提供翻譯服務，僅供參考。")
            
            await interaction.response.send_message(embed=public_embed)
            
            # 更新原始訊息，顯示已發送
            button.disabled = True
            button.label = "✅ 已發送"
            await interaction.edit_original_response(view=self)
            
        except Exception:
            await interaction.response.send_message(
                "❌ 發送失敗，請稍後再試",
                ephemeral=True
            )


class TextTranslationResultView(discord.ui.View):
    """文字翻譯結果的操作界面"""
    
    def __init__(self, embed: discord.Embed):
        super().__init__(timeout=300)  # 5分鐘後超時
        self.embed = embed

    @discord.ui.button(label='📤 發送到頻道', style=discord.ButtonStyle.primary)
    async def send_to_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        """將翻譯結果發送到目前頻道"""
        try:
            # 創建新的 embed 供公開顯示
            public_embed = discord.Embed(
                title="🌏 文字翻譯",
                color=0x1da0f2
            )
            
            # 複製字段
            for field in self.embed.fields:
                public_embed.add_field(
                    name=field.name,
                    value=field.value,
                    inline=field.inline
                )
            
            public_embed.set_footer(text=f"翻譯請求者: {interaction.user.display_name} | 由 Gemini AI 提供翻譯服務，僅供參考。")
            
            await interaction.response.send_message(embed=public_embed)
            
            # 更新原始訊息，顯示已發送
            button.disabled = True
            button.label = "✅ 已發送"
            await interaction.edit_original_response(view=self)
            
        except Exception:
            await interaction.response.send_message(
                "❌ 發送失敗，請稍後再試",
                ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Translation(bot))
