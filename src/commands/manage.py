import discord

from discord.ext import commands
from core.bot import CogExtension

class Manage(CogExtension):
    
    async def setting(self, ctx:commands.Context):
        embed = discord.Embed(
            title="伺服器設定",
            description="請透過下方按鈕來進行操作",
        )

        nick = discord.ui.Button(
            style=discord.ButtonStyle.primary,
            label="預設暱稱格式設定",
            custom_id="nick_setting",
            emoji="📃"
        )

        words = discord.ui.Button(
            style=discord.ButtonStyle.danger,
            label="文字設定",
            custom_id="words_setting",
            emoji="📰"
        )

        role = discord.ui.Button(
            style=discord.ButtonStyle.danger,
            label="身分組設定",
            custom_id="role_setting",
            emoji="📜"
        )

        item = nick,words,role

        if isinstance(ctx, commands.Context):
            await ctx.reply(
                embed=embed,
                view=discord.ui.View(*item, timeout=None),
                mention_author=False
            )

        else:
            await ctx.respond(
                embed=embed,
                view=discord.ui.View(*item, timeout=None),
            )

    @discord.application_command(name="設定", description="管理機器人設定")
    async def slash_setting(self, ctx):
        await self.setting(ctx)

    @commands.command(name="setting")
    async def text_setting(self, ctx):
        await self.setting(ctx)

def setup(bot):
    bot.add_cog(Manage(bot))