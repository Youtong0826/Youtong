import discord
import time

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

timestamp_format_definition = {  
    "t": ["短時間", "16:20"],
    "T": ["長時間", "16:20:30"],
    "d": ["短日期", "20/04/2021"],
    "D": ["長日期", "20 April 2021"],
    "f": ["短日期/時間", "20 April 2021 16:20"],	
    "F": ["長日期/時間", "Tuesday, 20 April 2021 16:20"],
    "R": ["相對時間", "2 months ago"]
}

timestamp_format = "f"
original_time = "2001:01:01:00:00:00"

class General(CogExtension):
        
    async def nick(self, ctx: commands.Context | discord.ApplicationContext):
        config = self.bot.get_custom_commands("nick")[0][1]
        embed = discord.Embed.from_dict(config["embed"])
        embed.timestamp = datetime.utcnow()

        view = discord.ui.View(
            *self.bot.get_items(config),
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

    @discord.application_command(name="生成timestamp",description="將日期轉為timestamp")
    async def timestamp(self, ctx:discord.ApplicationContext):
        embed = discord.Embed(
            title="生成timestamp (beta)",
            description="將日期轉為timestamp"
        )

        input_datetime = Button(
            style=discord.ButtonStyle.primary,
            label="輸入時間",
            custom_id="timestamp_input_datetime"
        )

        creat_timestamp = Button(
            style=discord.ButtonStyle.success,
            label="生成",
            custom_id="timestamp_creat"
        )

        select_format = Select(
            placeholder="選擇格式",
            custom_id="timestamp_select_format",
            options=[
                discord.SelectOption(
                    label=v[0],
                    value=k,
                    description=f"example: {v[1]}"
                )
                for k,v in timestamp_format_definition.items()
            ]
        )

        
        await ctx.response.send_message(embed=embed, view=discord.ui.View(input_datetime, creat_timestamp, select_format))

    @commands.Cog.listener()
    async def on_interaction(self, interaction:discord.Interaction):

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

            case "timestamp_input_datetime":
                return await interaction.response.send_modal(discord.ui.Modal(
                    discord.ui.InputText(
                        label="輸入年份,日期與時間",
                        placeholder="格式為YYYY:MM:DD:hh:mm:ss",
                        max_length=20,
                        required=False,
                    ),
                    title="輸入資料",
                    custom_id="timestamp_input_datetime_modal"
                ))

            case "timestamp_input_datetime_modal":
                global original_time
                original_time = interaction.data.get("components",{})[0].get("components",{})[0].get("value")

                if original_time == "2001:01:01:00:00:00":
                    return await interaction.response.send_message("因為你沒有輸入時間 所以預設為 `2001:01:01:00:00:00` ", ephemeral=True)

                return await interaction.response.send_message("成功將時間設定為 " + original_time, ephemeral=True)

            case "timestamp_select_format":
                global timestamp_format
                timestamp_format = interaction.data.get("values")[0]

                return await interaction.response.send_message("成功將timestamp格式設定為 " + timestamp_format, ephemeral=True)
            
            case "timestamp_creat":
                dtime = datetime(*list(map(int,original_time.split(":"))))
                unix_time = int(time.mktime(dtime.timetuple()))
                return  await interaction.response.send_message(
                    embed=discord.Embed(
                        title="生成結果!",
                        fields=[
                            discord.EmbedField(
                                name="展示",
                                value=f"<t:{unix_time}:{timestamp_format}>"
                            ),
                            discord.EmbedField(
                                name="原始訊息",
                                value=f"```<t:{unix_time}:{timestamp_format}>```"
                            )
                        ]
                    ),
                    ephemeral=True
                )

            




def setup(bot):
    bot.add_cog(General(bot))