import discord
from discord.ext import commands
from datetime import datetime

from core.classes import CogExtension

class General(CogExtension):

    @commands.command(description="管理你的暱稱")
    async def nick(self, ctx:commands.Context):
        embed = discord.Embed(
            title="暱稱修改系統 (beta)",
            description="歡迎使用 `暱稱修改系統` ! | 請選擇您要進行的操作",
            timestamp=datetime.utcnow()
        )

        embed.set_footer(
            text="Nick Modifier | 管理暱稱的最佳選擇",
            icon_url=self.bot.setting.general["avatar_url"]
        )

        modify = discord.ui.Button(
            style=discord.ButtonStyle.success,
            label="修改你的暱稱",
            emoji="🔧",
            custom_id="modify"
        )

        check_cooldown = discord.ui.Button(
            style=discord.ButtonStyle.primary,
            label="查看冷卻時間",
            emoji="🕐",
            custom_id="check"
        )

        async def callback(interaction:discord.Interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message("非指令使用者無法進行操作!",ephemeral=True)

            elif interaction.custom_id == "modify":
                new_nick = discord.ui.InputText(
                    label="新暱稱",
                    placeholder="輸入你的新暱稱",
                    min_length=1,
                    max_length=16
                )

                async def modal_callback(interaction:discord.Interaction):
                    nick = modal.children[0].value
                    await interaction.user.edit(nick="〡"+nick)
                    await interaction.response.send_message("已成功修改您的暱稱~",ephemeral=True)
                
                async def on_modal_error(error:Exception, interaction:discord.Interaction):
                    embed = discord.Embed(
                        title="指令出了點問題>< 請您將錯誤回報給開發者們",
                        description=f"```{error}```"
                    )

                    await interaction.response.send_message(embed=embed,ephemeral=True)

                modal = discord.ui.Modal(new_nick,title="修改你的暱稱")
                modal.callback = modal_callback
                modal.on_error = on_modal_error

                await interaction.response.send_modal(modal)

            elif interaction.custom_id == "check":
                await interaction.response.send_message("此功能尚在製作中~",ephemeral=True)

        for button in [modify,check_cooldown]:button.callback = callback

        await ctx.reply(
            embed=embed,
            view=discord.ui.View(
                modify,
                check_cooldown,
                timeout=None
            ),
            mention_author = False
        )

def setup(bot):
    bot.add_cog(General(bot))