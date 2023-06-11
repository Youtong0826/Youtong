import discord

from discord.ext import commands
from datetime import datetime, timedelta
from core.bot import CogExtension
from core.checks import (
    is_emoji,
    is_available_language
)

from core.functions import (
    get_time,
    get_time_map,
    creat_unix,
    rep_str
)


class General(CogExtension):
    def __init__(self, bot: discord.Bot | commands.Bot) -> None:
        super().__init__(bot)

        self.bot.build_custom_command("nick", "暱稱", "管理你的暱稱")
        self.bot.build_custom_command("setting", "暱稱設定", "管理暱稱設定")

    async def upload(self, ctx: commands.Context | discord.ApplicationContext, file: discord.Attachment):
        #await file.save(self.bot.setting.path)

        await ctx.response.send_message("Hello!", ephemeral=True)


    #@discord.application_command(name="上傳設定擋", description="上傳暱稱設定檔案(json)")
    async def slash_upload(self, ctx: commands.Context, file: discord.Option(discord.Attachment, "設定檔(json)")):
        await self.upload(ctx, file)

    @discord.application_command(name="禁用文字", description="查詢被禁用的文字")
    async def show_block_words(self, ctx: discord.ApplicationContext):
        await ctx.respond(f'以下為被禁用的文字```{", ".join(self.bot.database.block_words)}```')

    @commands.Cog.listener()
    async def on_interaction(self, interaction:discord.Interaction):

        if interaction.custom_id:
            custom_id = interaction.custom_id.replace("_setting", "") if interaction.custom_id.endswith("_setting") else interaction.custom_id
            data = self.bot.get_interaction_data(custom_id) 
            values = self.bot.get_interaction_value(interaction)

            async def append_data(mode: int = 0):
                values = self.bot.get_select_value(interaction)
                for v in values:
                    if mode == 0 and v in self.bot.database.block_roles:
                        return await interaction.response.send_message(data["already_in"], role=interaction.guild.get_role(int(v)).mention)

                    self.bot.database.append_block_user(int(v))

            if custom_id == "nick_modal":
                nick = values[0]
                user_cooldown = self.bot.get_user_cooldown(interaction.user.id)

                if not nick:
                    embed = discord.Embed(
                        title="錯誤!",
                        description="```無法讀取資料 請再試一次或是將此情形回報給開發者```"
                    )
                    return await interaction.response.send_message(embed=embed, ephemeral=True)
                
                if len(list(filter(lambda x:x in self.bot.database.block_words, nick))) or is_emoji(nick) or (not is_available_language(nick)):
                    return await interaction.response.send_message("錯誤! 偵測到不該使用的字元", ephemeral=True)
                
                if  user_cooldown and user_cooldown > get_time():
                    unix = f"<t:{creat_unix(user_cooldown)}:R>"
                    return await interaction.response.send_message(rep_str(data["cooling"], time=unix), ephemeral=True)

                try:
                    managements = self.bot.setting.managements
                    nick = managements.get("start_word", "") + nick + managements.get("end_word", "")
                    await interaction.user.edit(nick=nick)
                    config: list[int] = self.bot.setting.managements["cooldown"]
                    cooldown = get_time()+timedelta(
                        hours=config[0],
                        minutes=config[1],
                        seconds=config[2]
                    )
                    
                    self.bot.database.set_user_cooldown(interaction.user.id, **get_time_map(cooldown))
                    return await interaction.response.send_message(rep_str(data["end_cooling"], nick), ephemeral=True)

                except discord.errors.Forbidden as error:
                    if error.text == "Missing Permissions":
                        return await interaction.response.send_message("權限不足!", ephemeral=True)

                    else:
                        embed = discord.Embed(
                            title="錯誤! 表單好像出了點問題>< 請將此情形回報給開發者們",
                            description=f"```Msg: {error.text}\nStatus: {error.status}\nCode: {error.code}```"
                        )

                        return await interaction.response.send_message(embed=embed, ephemeral=True)
                        
            elif custom_id == "check":
                cooldown = self.bot.get_user_cooldown(interaction.user.id)
                description = data["end_cooling"]

                if cooldown and cooldown >= get_time():
                    unix_time  = creat_unix(cooldown)
                    description = rep_str(data["cooling"], time=f"<t:{unix_time}:R>")

                return await interaction.response.send_message(description, ephemeral=True)

            elif custom_id == "nick_format":
                
                self.bot.setting.set("managements",
                    "start_word", values[0] 
                ) if values[0] != "" else None

                self.bot.setting.set("managements",
                    "end_word", values[1]
                ) if values[1] != "" else None
                
                return await interaction.response.send_message(data["content"], ephemeral=True)
            
            elif custom_id == "words_modal":
  
                if values[0] in self.bot.database.block_words:
                    return await interaction.response.send_message(rep_str(data["already_in"], word=values[0]), ephemeral=True)
                
                if values[1] != "" and values[1] not in self.bot.database.block_words:
                    return await interaction.response.send_message(rep_str(data["not_in"], word=values[1]), ephemeral=True)

                self.bot.database.append_block_words(
                    values[0] ) if values[0] != "" else None
                
                self.bot.database.remove_block_words(
                    values[1] ) if values[1] != "" else None

                return await interaction.response.send_message(data["content"], ephemeral=True)

            elif custom_id == "add_block_roles_select":
                values = self.bot.get_select_value(interaction)
                for v in values:
                    if v in self.bot.database.block_roles:
                        return await interaction.response.send_message(data["already_in"], role=interaction.guild.get_role(int(v)).mention)

                    self.bot.database.append_block_user(int(v))

            elif custom_id == "remove_roles_select": 
                ...

            if data.get("type") == "select":
                try:
                    data = self.bot.get_select_interaction_data(custom_id, self.bot.get_select_value(interaction, 0))

                except IndexError:
                    return await interaction.response.send_message("請重試一次!", ephemeral=True)

            await self.bot.interaction_respond(interaction, data)

             


def setup(bot: discord.Bot):
    bot.add_cog(General(bot))
    