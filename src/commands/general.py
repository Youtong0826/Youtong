import discord

from discord.ext import commands
from datetime import datetime

from core.bot import CogExtension
from core.checks import (
    is_emoji,
    is_available_language
)

from core.item import (
    Button,
    Select
)
class General(CogExtension):
        
    async def nick(self, ctx: commands.Context | discord.ApplicationContext):
        config = self.bot.get_custom_commands("nick")[0][1]
        embed = discord.Embed.from_dict(config["embed"])
        embed.timestamp = datetime.utcnow()

        view = discord.ui.View(
            *self.bot.get_items_from_dict(config),
            timeout=config["view"]["timeout"]
        )

        if isinstance(ctx, commands.Context):
            await ctx.reply(
                embed=embed,
                view=view,
                mention_author=False
            )

        elif isinstance(ctx, discord.ApplicationContext):
            await ctx.response.send_message(
                embed=embed,
                view=view
            )

    @commands.command(name="nick", description="管理你的暱稱")
    async def text_nick(self, ctx:commands.Context):
        await self.nick(ctx)

    @discord.application_command(name="暱稱", description="管理你的暱稱")
    async def slash_nick(self, ctx:discord.ApplicationContext):
        await self.nick(ctx)
            
    @commands.Cog.listener()
    async def on_interaction(self, interaction:discord.Interaction):
        custom_id = self.bot.get_custom_commands()
        match interaction.custom_id:
            case "modify":
                new_nick = discord.ui.InputText(
                    label="新暱稱",
                    placeholder="輸入你的新暱稱",
                    min_length=1,
                    max_length=16
                )        

                async def on_modal_error(error:Exception, interaction:discord.Interaction):
                    embed = discord.Embed(
                        title="好像出了點問題>< 請你將錯誤回報給開發者們",
                        description=f"```{error}```"
                    )
                    return await interaction.response.send_message(embed=embed, ephemeral=True)

                modal = discord.ui.Modal(new_nick, title="修改你的暱稱", custom_id="nick_modal")
                modal.on_error = on_modal_error

                return await interaction.response.send_modal(modal)

            case "check":
                cooldown:list = self.bot.setting.managements.get("cooldown", [0, 0, 0])
                
                embed = discord.Embed(
                    title="冷卻時間",
                    description=f"距離下一次修改機會還有 `{':'.join(list(map(str, cooldown)))}`",
                    timestamp=datetime.utcnow()
                )
                return await interaction.response.send_message(embed=embed, ephemeral=True)

            case "nick_modal":
                nick = interaction.data.get("components",{})[0].get("components",{})[0].get("value")
                if not nick:
                    embed = discord.Embed(
                        title="錯誤!",
                        description="```無法讀取資料 請再試一次或是將此情形回報給開發者```"
                    )
                    return await interaction.response.send_message(embed=embed, ephemeral=True)
                
                if len(list(filter(lambda x:x in self.bot.database.block_words, nick))) > 0 or is_emoji(nick) or (not is_available_language(nick)):
                    return await interaction.response.send_message("錯誤! 偵測到不該使用的字元 請你閱讀完修改規則後再重新提交一次申請~", ephemeral=True)

                await interaction.user.edit(nick="〡"+nick)
                return await interaction.response.send_message("已成功修改你的暱稱~", ephemeral=True)

def setup(bot):
    bot.add_cog(General(bot))