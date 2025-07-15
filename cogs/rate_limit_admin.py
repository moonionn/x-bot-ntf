import discord
from discord.ext import commands

from src.notification.rate_limiter import rate_limiter
from src.log import setup_logger

log = setup_logger(__name__)

class RateLimitCommands(commands.Cog):
    """速率限制監控和管理指令"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(name="ratelimit", description="速率限制管理指令")
    @commands.has_permissions(administrator=True)
    async def ratelimit(self, ctx):
        """速率限制管理指令群組"""
        if ctx.invoked_subcommand is None:
            await ctx.send("請使用 `/ratelimit status` 查看速率限制狀態")

    @ratelimit.command(name="status", description="查看所有帳戶的速率限制狀態")
    async def status(self, ctx):
        """查看速率限制狀態"""
        try:
            status_summary = rate_limiter.get_status_summary()
            
            embed = discord.Embed(
                title="🚦 Twitter API 速率限制狀態",
                description=f"```\n{status_summary}\n```",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="📊 說明",
                value=(
                    "• **OK**: 正常運作\n"
                    "• **consecutive errors**: 連續錯誤次數\n" 
                    "• **total rate limits**: 總速率限制次數"
                ),
                inline=False
            )
            embed.set_footer(text="速率限制會自動使用指數退避策略處理")
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            log.error(f"Error checking rate limit status: {e}")
            await ctx.send("❌ 檢查速率限制狀態時發生錯誤")

    @ratelimit.command(name="reset", description="重置指定帳戶的速率限制記錄")
    async def reset(self, ctx, account_name: str):
        """重置指定帳戶的速率限制記錄"""
        try:
            if account_name in rate_limiter.rate_limit_info:
                old_info = rate_limiter.rate_limit_info[account_name].copy()
                rate_limiter.rate_limit_info[account_name] = {
                    'consecutive_errors': 0,
                    'last_error_time': None,
                    'total_rate_limits': 0
                }
                
                embed = discord.Embed(
                    title="✅ 速率限制記錄已重置",
                    description=f"帳戶 `{account_name}` 的速率限制記錄已重置",
                    color=discord.Color.green()
                )
                embed.add_field(
                    name="重置前狀態",
                    value=(
                        f"連續錯誤: {old_info['consecutive_errors']}\n"
                        f"總速率限制: {old_info['total_rate_limits']}"
                    ),
                    inline=False
                )
                
                await ctx.send(embed=embed)
                log.info(f"Rate limit record reset for account: {account_name}")
                
            else:
                await ctx.send(f"❌ 找不到帳戶 `{account_name}` 的速率限制記錄")
                
        except Exception as e:
            log.error(f"Error resetting rate limit for {account_name}: {e}")
            await ctx.send("❌ 重置速率限制記錄時發生錯誤")

    @ratelimit.error
    async def ratelimit_error(self, ctx, error):
        """處理指令錯誤"""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ 您需要管理員權限才能使用此指令")
        else:
            log.error(f"Rate limit command error: {error}")
            await ctx.send("❌ 指令執行時發生錯誤")

async def setup(bot):
    await bot.add_cog(RateLimitCommands(bot))
