import os
import yaml
import discord
from discord import app_commands
from discord.ext import commands

from core.classes import Cog_Extension
from configs.load_configs import configs
from src.log import setup_logger

log = setup_logger(__name__)


def save_configs():
    """保存配置到文件"""
    try:
        with open('./configs.yml', 'w', encoding='utf8') as yfile:
            yaml.dump(configs, yfile, default_flow_style=False, allow_unicode=True)
        log.info("配置已保存到文件")
    except Exception as e:
        log.error(f"保存配置失敗: {e}")


class AutoTranslation(Cog_Extension):
    """自動翻譯管理功能"""
    
    def __init__(self, bot):
        super().__init__(bot)

    auto_translate_group = app_commands.Group(
        name='autotranslate', 
        description='自動翻譯管理功能'
    )

    @auto_translate_group.command(name='add_channel')
    @app_commands.describe(
        channel="要添加自動翻譯功能的頻道"
    )
    async def add_auto_translate_channel(
        self, 
        interaction: discord.Interaction, 
        channel: discord.TextChannel
    ):
        """
        將頻道添加到自動翻譯列表
        
        Parameters
        ----------
        channel: discord.TextChannel
            要添加自動翻譯功能的頻道
        """
        # 檢查權限
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message(
                "❌ 您需要「管理頻道」權限才能使用此功能",
                ephemeral=True
            )
            return
        
        # 獲取配置
        translation_config = configs.get('translation', {})
        auto_translate_channels = translation_config.get('auto_translate_channels', [])
        
        if channel.id in auto_translate_channels:
            await interaction.response.send_message(
                f"❌ 頻道 {channel.mention} 已經在自動翻譯列表中",
                ephemeral=True
            )
            return
        
        # 添加頻道ID
        auto_translate_channels.append(channel.id)
        configs['translation']['auto_translate_channels'] = auto_translate_channels
        
        # 保存配置到文件
        save_configs()
        save_configs()
        
        embed = discord.Embed(
            title="✅ 自動翻譯已啟用",
            description=f"已為頻道 {channel.mention} 啟用自動翻譯功能",
            color=0x00ff00
        )
        embed.add_field(
            name="📋 說明",
            value="當此頻道收到包含 Twitter/X 連結的消息時，機器人會自動進行翻譯",
            inline=False
        )
        embed.set_footer(text="✅ 設置已永久保存")
        
        await interaction.response.send_message(embed=embed)
        log.info(f"已為頻道 {channel.name} (ID: {channel.id}) 啟用自動翻譯功能")

    @auto_translate_group.command(name='remove_channel')
    @app_commands.describe(
        channel="要移除自動翻譯功能的頻道"
    )
    async def remove_auto_translate_channel(
        self, 
        interaction: discord.Interaction, 
        channel: discord.TextChannel
    ):
        """
        從自動翻譯列表中移除頻道
        
        Parameters
        ----------
        channel: discord.TextChannel
            要移除自動翻譯功能的頻道
        """
        # 檢查權限
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message(
                "❌ 您需要「管理頻道」權限才能使用此功能",
                ephemeral=True
            )
            return
        
        # 獲取配置
        translation_config = configs.get('translation', {})
        auto_translate_channels = translation_config.get('auto_translate_channels', [])
        
        if channel.id not in auto_translate_channels:
            await interaction.response.send_message(
                f"❌ 頻道 {channel.mention} 不在自動翻譯列表中",
                ephemeral=True
            )
            return
        
        # 移除頻道ID
        auto_translate_channels.remove(channel.id)
        configs['translation']['auto_translate_channels'] = auto_translate_channels
        
        # 保存配置到文件
        save_configs()
        
        # 保存配置
        save_configs()
        
        embed = discord.Embed(
            title="✅ 自動翻譯已停用",
            description=f"已為頻道 {channel.mention} 停用自動翻譯功能",
            color=0xff9900
        )
        
        await interaction.response.send_message(embed=embed)
        log.info(f"已為頻道 {channel.name} (ID: {channel.id}) 停用自動翻譯功能")

    @auto_translate_group.command(name='list_channels')
    async def list_auto_translate_channels(self, interaction: discord.Interaction):
        """
        列出所有啟用自動翻譯的頻道
        """
        # 獲取配置
        translation_config = configs.get('translation', {})
        auto_translate_channels = translation_config.get('auto_translate_channels', [])
        
        if not auto_translate_channels:
            await interaction.response.send_message(
                "📋 目前沒有啟用自動翻譯的頻道",
                ephemeral=True
            )
            return
        
        embed = discord.Embed(
            title="📋 自動翻譯頻道列表",
            color=0x1da0f2
        )
        
        channel_list = []
        for channel_id in auto_translate_channels:
            channel = self.bot.get_channel(channel_id)
            if channel:
                channel_list.append(f"• {channel.mention} (`{channel_id}`)")
            else:
                channel_list.append(f"• 未知頻道 (`{channel_id}`)")
        
        embed.add_field(
            name="啟用自動翻譯的頻道",
            value="\n".join(channel_list) if channel_list else "無",
            inline=False
        )
        
        embed.set_footer(text="在這些頻道中，包含推文連結的消息會自動觸發翻譯")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @auto_translate_group.command(name='status')
    async def auto_translate_status(self, interaction: discord.Interaction):
        """
        檢查自動翻譯功能狀態
        """
        # 檢查翻譯器配置
        translation_config = configs.get('translation', {})
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        
        embed = discord.Embed(
            title="🤖 自動翻譯功能狀態",
            color=0x1da0f2
        )
        
        # API 狀態
        if gemini_api_key:
            embed.add_field(
                name="🔑 API 狀態",
                value="✅ Gemini API 金鑰已配置",
                inline=True
            )
        else:
            embed.add_field(
                name="🔑 API 狀態",
                value="❌ Gemini API 金鑰未配置",
                inline=True
            )
        
        # 頻道數量
        auto_translate_channels = translation_config.get('auto_translate_channels', [])
        embed.add_field(
            name="📊 啟用頻道數",
            value=f"{len(auto_translate_channels)} 個頻道",
            inline=True
        )
        
        # 功能狀態
        if gemini_api_key and auto_translate_channels:
            status = "🟢 正常運行"
        elif gemini_api_key:
            status = "🟡 API 已配置，但未設置頻道"
        else:
            status = "🔴 未配置"
        
        embed.add_field(
            name="⚡ 功能狀態",
            value=status,
            inline=True
        )
        
        embed.add_field(
            name="📝 使用說明",
            value="• 使用 `/autotranslate add_channel` 添加頻道\n"
                  "• 使用 `/autotranslate list_channels` 查看頻道列表\n"
                  "• 在啟用的頻道中發送推文連結即可自動翻譯",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @auto_translate_group.command(name='test')
    async def test_auto_translate(self, interaction: discord.Interaction):
        """
        測試自動翻譯功能的配置和狀態
        """
        # 獲取配置
        translation_config = configs.get('translation', {})
        auto_translate_channels = translation_config.get('auto_translate_channels', [])
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        
        embed = discord.Embed(
            title="🧪 自動翻譯功能測試",
            color=0x1da0f2
        )
        
        # 當前頻道狀態
        current_channel_enabled = interaction.channel.id in auto_translate_channels
        embed.add_field(
            name="📍 當前頻道狀態",
            value=f"{'✅ 已啟用' if current_channel_enabled else '❌ 未啟用'} 自動翻譯",
            inline=True
        )
        
        # API 狀態
        embed.add_field(
            name="🔑 API 狀態",
            value=f"{'✅ 已配置' if gemini_api_key else '❌ 未配置'} Gemini API",
            inline=True
        )
        
        # 總頻道數
        embed.add_field(
            name="📊 啟用頻道總數",
            value=f"{len(auto_translate_channels)} 個頻道",
            inline=True
        )
        
        # 測試說明
        test_url = "https://twitter.com/example/status/1234567890"
        embed.add_field(
            name="🔬 測試方法",
            value=f"請在此頻道發送推文連結進行測試：\n`{test_url}`",
            inline=False
        )
        
        # 配置詳情
        embed.add_field(
            name="⚙️ 配置詳情",
            value=f"• 當前頻道ID: `{interaction.channel.id}`\n"
                  f"• 啟用頻道列表: {auto_translate_channels}",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @auto_translate_group.command(name='set_mapping')
    @app_commands.describe(
        source_channel="推文通知頻道",
        target_channel="翻譯結果頻道"
    )
    async def set_channel_mapping(
        self, 
        interaction: discord.Interaction, 
        source_channel: discord.TextChannel,
        target_channel: discord.TextChannel
    ):
        """
        設置頻道映射：通知頻道 -> 翻譯頻道
        
        Parameters
        ----------
        source_channel: discord.TextChannel
            接收推文通知的頻道
        target_channel: discord.TextChannel
            發送翻譯結果的頻道
        """
        # 檢查權限
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message(
                "❌ 您需要「管理頻道」權限才能使用此功能",
                ephemeral=True
            )
            return
        
        # 獲取配置
        translation_config = configs.get('translation', {})
        channel_mapping = translation_config.get('channel_mapping', {})
        
        # 設置映射
        channel_mapping[source_channel.id] = target_channel.id
        translation_config['channel_mapping'] = channel_mapping
        translation_config['translation_mode'] = 'separate'
        configs['translation'] = translation_config
        
        # 保存配置到文件
        save_configs()
        
        embed = discord.Embed(
            title="✅ 頻道映射已設置",
            description=f"通知頻道: {source_channel.mention}\n翻譯頻道: {target_channel.mention}",
            color=0x00ff00
        )
        embed.add_field(
            name="📋 說明",
            value="當通知頻道收到推文通知時，翻譯結果將自動發送到指定的翻譯頻道",
            inline=False
        )
        embed.set_footer(text="✅ 設置已永久保存")
        
        await interaction.response.send_message(embed=embed)
        log.info(f"設置頻道映射: {source_channel.name} -> {target_channel.name}")

    @auto_translate_group.command(name='list_mappings')
    async def list_channel_mappings(self, interaction: discord.Interaction):
        """
        列出所有頻道映射關係
        """
        # 獲取配置
        translation_config = configs.get('translation', {})
        channel_mapping = translation_config.get('channel_mapping', {})
        translation_mode = translation_config.get('translation_mode', 'reply')
        
        embed = discord.Embed(
            title="📋 頻道映射列表",
            color=0x1da0f2
        )
        
        embed.add_field(
            name="⚙️ 翻譯模式",
            value=f"{'🔀 分離模式' if translation_mode == 'separate' else '💬 回覆模式'}",
            inline=True
        )
        
        if channel_mapping:
            mapping_list = []
            for source_id, target_id in channel_mapping.items():
                source_channel = self.bot.get_channel(int(source_id))
                target_channel = self.bot.get_channel(target_id)
                
                source_name = source_channel.mention if source_channel else f"未知頻道 (`{source_id}`)"
                target_name = target_channel.mention if target_channel else f"未知頻道 (`{target_id}`)"
                
                mapping_list.append(f"📡 {source_name} → 📝 {target_name}")
            
            embed.add_field(
                name="🔗 頻道映射關係",
                value="\n".join(mapping_list),
                inline=False
            )
        else:
            embed.add_field(
                name="🔗 頻道映射關係",
                value="無設置的映射關係",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(AutoTranslation(bot))
