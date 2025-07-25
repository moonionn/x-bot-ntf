import asyncio
import os
import sys
import re

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from configs.load_configs import configs
from src.checker import check_configs, check_env, check_db, check_upgrade
from src.db_function.init_db import init_db
from src.db_function.repair_db import auto_repair_mismatched_clients
from src.presence_updater import update_presence
from src.log import setup_logger

log = setup_logger(__name__)

load_dotenv()

intents = discord.Intents(guilds=True, messages=True, message_content=True, emojis=True)
bot = commands.Bot(command_prefix=configs['prefix'], intents=intents)


@bot.event
async def on_ready():
    if not (os.path.isfile(os.path.join(os.getenv('DATA_PATH'), 'tracked_accounts.db'))):
        await init_db()
        
    check_upgrade()
    
    # 檢查是否只在翻譯模式下運行
    translation_only_mode = (
        'translation' in configs and 
        configs.get('translation', {}).get('auto_translate_channels') and
        not os.getenv('TWITTER_TOKEN')
    )
    
    if translation_only_mode:
        log.info('detected translation-only configuration, running in translation mode')
        
    if not check_env(translation_only_mode):
        log.warning('incomplete environment variables detected, will retry in 30 seconds')
        await asyncio.sleep(30)
        load_dotenv()
        
    if not check_configs(configs):
        log.warning('incomplete configs file detected, will retry in 30 seconds')
        await asyncio.sleep(30)
        os.execv(sys.executable, ['python'] + sys.argv)
        
    invalid_clients = await check_db(translation_only_mode)
    if invalid_clients:
        log.warning('detected environment variable undefined client name in database')
        if configs['auto_repair_mismatched_clients']:
            await auto_repair_mismatched_clients(invalid_clients)
            log.info('automatically replace mismatched client names with the first client name in the environment variable, use the sync slash command in discord to ensure notifications are turned on')
        else:
            log.warning('set auto_repair_mismatched_clients to true in configs to automatically fix this error or manually update the database or environment variables')
    else:
        log.info('database check passed')

    await update_presence(bot)

    bot.tree.on_error = on_tree_error
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
    log.info(f'{bot.user} is online')
    slash = await bot.tree.sync()
    log.info(f'synced {len(slash)} slash commands')


@bot.command()
@commands.is_owner()
async def load(ctx: commands.context.Context, extension):
    await bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'Loaded {extension} done.')


@bot.command()
@commands.is_owner()
async def unload(ctx: commands.context.Context, extension):
    await bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Un - Loaded {extension} done.')


@bot.command()
@commands.is_owner()
async def reload(ctx: commands.context.Context, extension):
    await bot.reload_extension(f'cogs.{extension}')
    await ctx.send(f'Re - Loaded {extension} done.')


@bot.command()
@commands.is_owner()
async def download_log(ctx: commands.context.Context):
    message = await ctx.send(file=discord.File('console.log'))
    await message.delete(delay=15)


@bot.command()
@commands.is_owner()
async def download_data(ctx: commands.context.Context):
    message = await ctx.send(file=discord.File(os.path.join(os.getenv('DATA_PATH'), 'tracked_accounts.db')))
    await message.delete(delay=15)


@bot.command()
@commands.is_owner()
async def upload_data(ctx: commands.context.Context):
    raw = await [attachment for attachment in ctx.message.attachments if attachment.filename[-3:] == '.db'][0].read()
    with open(os.path.join(os.getenv('DATA_PATH'), 'tracked_accounts.db'), 'wb') as wbf:
        wbf.write(raw)
    message = await ctx.send('successfully uploaded data')
    await message.delete(delay=5)


@bot.event
async def on_tree_error(itn: discord.Interaction, error: app_commands.AppCommandError):
    await itn.response.send_message(error, ephemeral=True)
    log.warning(f'an error occurred but was handled by the tree error handler, error message : {error}')


@bot.event
async def on_command_error(ctx: commands.context.Context, error: commands.errors.CommandError):
    if isinstance(error, commands.errors.CommandNotFound):
        return
    else:
        await ctx.send(error)
    log.warning(f'an error occurred but was handled by the command error handler, error message : {error}')


@bot.event
async def on_message(message):
    """監聽消息事件，自動翻譯推文連結"""
    # 檢查是否包含Twitter/X連結
    twitter_pattern = r'https?://(?:twitter\.com|x\.com)/\w+/status/\d+'
    tweet_urls = re.findall(twitter_pattern, message.content)
    
    if tweet_urls:
        log.info(f"檢測到推文連結: {tweet_urls}")
        
        # 檢查是否在配置的翻譯頻道中
        translation_config = configs.get('translation', {})
        auto_translate_channels = translation_config.get('auto_translate_channels', [])
        channel_mapping = translation_config.get('channel_mapping', {})
        translation_mode = translation_config.get('translation_mode', 'reply')
        
        log.info(f"當前頻道ID: {message.channel.id}, 自動翻譯頻道列表: {auto_translate_channels}")
        log.info(f"頻道映射: {channel_mapping}, 翻譯模式: {translation_mode}")
        
        # 檢查頻道是否啟用自動翻譯
        if message.channel.id in auto_translate_channels:
            # 檢查是否有環境變數設置
            gemini_api_key = os.getenv('GEMINI_API_KEY')
            if not gemini_api_key:
                log.warning("未設定 GEMINI_API_KEY 環境變數，無法進行自動翻譯")
                return
            
            # 檢查是否為機器人自己發送的通知或用戶發送的連結
            if message.author.bot:
                log.info(f"檢測到機器人 {message.author.name} 發送的推文通知")
            else:
                log.info(f"檢測到用戶 {message.author.name} 發送的推文連結")
            
            log.info(f"頻道 {message.channel.id} 在自動翻譯列表中，開始處理...")
            
            # 動態導入翻譯器以避免循環導入
            try:
                from src.translation.tweet_translator import TweetTranslator
                
                log.info("開始初始化翻譯器...")
                translator = TweetTranslator(gemini_api_key=gemini_api_key)
                
                # 確定翻譯結果的目標頻道
                target_channel_id = None
                if translation_mode == 'separate':
                    target_channel_id = channel_mapping.get(message.channel.id)
                    if target_channel_id:
                        target_channel = bot.get_channel(target_channel_id)
                        if target_channel:
                            log.info(f"翻譯結果將發送到指定翻譯頻道: {target_channel.name} ({target_channel_id})")
                        else:
                            log.warning(f"找不到目標翻譯頻道 {target_channel_id}，將在原頻道回覆")
                            target_channel_id = None
                    else:
                        log.info("未設置頻道映射，將在原頻道回覆")
                else:
                    log.info("翻譯模式設置為回覆模式，將在原頻道回覆")
                
                # 處理找到的每個推文URL
                for tweet_url in tweet_urls:
                    log.info(f"正在處理推文連結: {tweet_url}")
                    await auto_translate_tweet(message, tweet_url, translator, target_channel_id)
                        
            except Exception as e:
                log.error(f"自動翻譯功能初始化失敗: {e}")
        else:
            log.info(f"頻道 {message.channel.id} 不在自動翻譯列表中，跳過翻譯")
    else:
        # 如果沒有檢測到推文連結，記錄一下（用於調試）
        if any(keyword in message.content.lower() for keyword in ['twitter.com', 'x.com', 'tweet']):
            log.debug(f"消息包含推文關鍵字但未匹配模式: {message.content}")
    
    # 處理其他命令（只對非機器人消息處理）
    if not message.author.bot:
        await bot.process_commands(message)


async def auto_translate_tweet(message, tweet_url, translator, target_channel_id=None):
    """自動翻譯推文的輔助函數"""
    try:
        log.info(f"開始翻譯推文: {tweet_url}")
        
        # 確定發送翻譯結果的目標頻道
        if target_channel_id:
            target_channel = bot.get_channel(target_channel_id)
            if not target_channel:
                log.warning(f"無法找到目標頻道 {target_channel_id}，將在原頻道回覆")
                target_channel = message.channel
                is_separate_channel = False
            else:
                is_separate_channel = True
        else:
            target_channel = message.channel
            is_separate_channel = False
        
        # 在目標頻道顯示正在翻譯的狀態
        async with target_channel.typing():
            result = await translator.translate_tweet(tweet_url, "繁體中文")
            
            log.info(f"翻譯結果: success={result['success']}")
            log.info(f"發文者: {result.get('username', 'None')}")
            log.info(f"翻譯內容長度: {len(result.get('translated_text', ''))}")
            
            if result["success"]:
                # 創建翻譯結果embed
                embed = discord.Embed(
                    title="翻譯結果",
                    color=0x1da0f2
                )
                
                # 添加發文者資訊（如果成功提取到）
                username = result.get("username")
                if username and username.strip():
                    embed.add_field(
                        name="👤 發文者",
                        value=f"@{username}",
                        inline=True
                    )
                    log.info(f"顯示發文者信息: @{username}")
                else:
                    log.warning("未獲取到發文者用戶名信息")
                
                # 如果是發送到分離的翻譯頻道，添加來源信息
                if is_separate_channel:
                    embed.add_field(
                        name="📍 來源",
                        value=f"來自 {message.channel.mention} 的推文通知\n[原始連結]({tweet_url})",
                        inline=False
                    )
                
                # 顯示原始推文內容（類似圖片中的格式）
                original_text = result["original_text"]
                # 如果原文過長，裁剪並添加省略號
                if len(original_text) > 800:
                    display_text = original_text[:800] + "..."
                else:
                    display_text = original_text
                
                # 格式化原文顯示（使用引用格式）
                formatted_original = f"> {display_text.replace(chr(10), chr(10) + '> ')}"
                
                embed.add_field(
                    name="📝 原文",
                    value=formatted_original,
                    inline=False
                )
                
                # 處理翻譯結果
                translated_text = result["translated_text"]
                
                # 使用更寬鬆的關鍵字匹配來檢測結構化翻譯
                has_structured_translation = any(keyword in translated_text for keyword in [
                    "翻譯一", "翻譯二", "詞句詳細解說", "## ", "翻譯 (", "翻譯（"
                ])
                
                if has_structured_translation:
                    # 分離翻譯內容和詞句解說
                    explanation_part = ""
                    translation_part = translated_text
                    
                    # 查找詞句詳細解說部分
                    explanation_markers = ["## 詞句詳細解說", "詞句詳細解說", "## "]
                    for marker in explanation_markers:
                        if marker in translated_text:
                            parts = translated_text.split(marker, 1)
                            if len(parts) == 2:
                                translation_part = parts[0].strip()
                                explanation_part = parts[1].strip()
                                break
                    
                    # 清理翻譯部分，移除原文，只保留翻譯內容
                    lines = translation_part.split('\n')
                    cleaned_lines = []
                    found_translation = False
                    
                    for line in lines:
                        line_clean = line.strip()
                        # 跳過原文行
                        if line_clean.endswith('原文：') or '原文：' in line_clean:
                            continue
                        # 找到翻譯行後開始收集
                        if '翻譯' in line_clean and ('(' in line_clean or '（' in line_clean):
                            found_translation = True
                            cleaned_lines.append(line)
                        elif found_translation and line_clean:
                            cleaned_lines.append(line)
                    
                    # 如果沒有找到結構化翻譯，使用原始內容
                    if not cleaned_lines:
                        final_translation = translated_text
                    else:
                        final_translation = '\n'.join(cleaned_lines).strip()
                    
                    # 確保翻譯內容不為空
                    if not final_translation.strip():
                        final_translation = translated_text
                    
                    embed.add_field(
                        name="🌏 翻譯結果",
                        value=final_translation[:1024],
                        inline=False
                    )
                    
                    # 添加詞句詳細解說（如果存在且有實際內容）
                    if explanation_part and len(explanation_part.strip()) > 20:
                        # 清理解說內容
                        explanation_clean = explanation_part.strip()
                        
                        # 限制長度
                        if len(explanation_clean) > 1000:
                            explanation_clean = explanation_clean[:1000] + "..."
                        
                        embed.add_field(
                            name="📚 詞句詳細解說",
                            value=explanation_clean,
                            inline=False
                        )
                else:
                    # 沒有結構化內容，直接顯示翻譯
                    embed.add_field(
                        name="🌏 翻譯結果", 
                        value=translated_text[:1024],
                        inline=False
                    )
                
                # 根據消息來源和發送方式設置不同的footer
                if is_separate_channel:
                    if message.author.bot:
                        embed.set_footer(text="🤖 自動翻譯推文通知 | 由 Gemini AI 提供翻譯服務，僅供參考。")
                    else:
                        embed.set_footer(text="🤖 自動翻譯用戶連結 | 由 Gemini AI 提供翻譯服務，僅供參考。")
                else:
                    if message.author.bot:
                        embed.set_footer(text="🤖 自動翻譯推文通知 | 由 Gemini AI 提供翻譯服務，僅供參考。")
                    else:
                        embed.set_footer(text="🤖 自動翻譯 | 由 Gemini AI 提供翻譯服務，僅供參考。")
                
                # 發送翻譯結果
                if is_separate_channel:
                    await target_channel.send(embed=embed)
                    log.info(f"自動翻譯完成，已發送到翻譯頻道: {target_channel.name}")
                else:
                    await message.reply(embed=embed, mention_author=False)
                    log.info("自動翻譯完成，已回覆原消息")
                
            else:
                # 翻譯失敗時的簡單提示
                if is_separate_channel:
                    await target_channel.send(f"❌ 翻譯推文時發生錯誤：{result.get('error', '未知錯誤')}")
                else:
                    await message.add_reaction("❌")
                log.warning(f"翻譯失敗: {result.get('error', '未知錯誤')}")
                
    except Exception as e:
        log.error(f"自動翻譯推文時發生錯誤: {e}")
        if target_channel_id:
            target_channel = bot.get_channel(target_channel_id)
            if target_channel:
                await target_channel.send(f"❌ 翻譯推文時發生錯誤：{str(e)}")
            else:
                await message.add_reaction("❌")
        else:
            await message.add_reaction("❌")


if __name__ == '__main__':
    bot.run(os.getenv('BOT_TOKEN'))