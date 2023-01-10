import discord

import time 
import datetime

from core.bot import CogExtension
from core.item import (
    Button,
    Select
)

class Other(CogExtension):
    timestamp_format_definition = {  
        "t": ["短時間", "16:20"],
        "T": ["長時間", "16:20:30"],
        "d": ["短日期", "20/04/2021"],
        "D": ["長日期", "20 April 2021"],
        "f": ["短日期/時間", "20 April 2021 16:20"],	
        "F": ["長日期/時間", "Tuesday, 20 April 2021 16:20"],
        "R": ["相對時間", "2 months ago"]
    }

    timestamp_format:dict[str, str] = {}
    original_time:dict[str, str] = {}

    @discord.application_command(name="生成timestamp", description="將日期轉為timestamp")
    async def timestamp(self, ctx:discord.ApplicationContext):
        self.timestamp_format[str(ctx.author.id)] = None
        self.original_time[str(ctx.author.id)] = None

        embed = discord.Embed(
            title="生成timestamp (beta)",
            description="將日期轉為timestamp"
        )

        embed.add_field(
            name="> 時間",
            value=f"```{self.original_time.get(ctx.author.id,'2001:01:01:00:00:0')}```"
        )

        embed.add_field(
            name="> 格式",
            value=f"```{self.timestamp_format.get(ctx.author.id,'f')}```"
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
                for k,v in self.timestamp_format_definition.items()
            ]
        )

        await ctx.response.send_message(embed=embed, view=discord.ui.View(input_datetime, creat_timestamp, select_format))

    @discord.Cog.listener()
    async def on_interaction(self, interaction:discord.Interaction):
        if not interaction.custom_id or not interaction.custom_id.startswith("timestamp") :
            return

        match interaction.custom_id.replace("timestamp_"):
            case "input_datetime":
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

            case "input_datetime_modal":
                dt = interaction.data.get("components",{})[0].get("components",{})[0].get("value")
                if not ...:
                    self.original_time[str(interaction.user.id)] = "2001:01:01:00:00:00"
                    return await interaction.response.send_message("因為你沒有輸入時間 所以預設為 `2001:01:01:00:00:00` ", ephemeral=True)

                return await interaction.response.send_message(f"成功將時間設定為`{self.original_time.get[interaction.user.id]}` " , ephemeral=True)

            case "select_format":
                global timestamp_format
                timestamp_format = interaction.data.get("values")[0]

                return await interaction.response.send_message("成功將timestamp格式設定為 " + timestamp_format, ephemeral=True)
            
            case "creat":
                dtime = datetime(*list(map(int,self.original_time.split(":"))))
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
    bot.add_cog(Other(bot))