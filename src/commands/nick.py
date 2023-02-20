import discord
import time

from discord.ext import commands
from datetime import datetime, timedelta
from core.bot import CogExtension
from core.checks import (
    is_emoji,
    is_available_language
)

from core.functions import (
    get_time,
    creat_unix    
)

class General(CogExtension):
    def __init__(self, bot: discord.Bot | commands.Bot) -> None:
        super().__init__(bot)

        self.bot.build_custom_command("nick", "暱稱", "管理你的你稱")
        self.bot.build_custom_command("setting", "暱稱設定", "管理暱稱設定")

    async def upload(self, ctx: commands.Context | discord.ApplicationContext, file: discord.Attachment):
        await file.save(self.bot.setting.path)

        await ctx.response.send_message("Hello!", ephemeral=True)

    @discord.application_command(name="上傳設定擋", description="上傳暱稱設定檔案(json)")
    async def slash_upload(self, ctx, file: discord.Option(discord.Attachment, "設定檔(json)")):
        await self.upload(ctx, file)

    @commands.Cog.listener()
    async def on_interaction(self, interaction:discord.Interaction):

        if interaction.custom_id and interaction.custom_id.endswith("_setting"):
            match interaction.custom_id.replace("_setting", ""):
                case "main_select":
                    match interaction.data.get("values",[""])[0].replace("_setting", ""):
                        case "nick":
                            await interaction.response.send_modal(
                                discord.ui.Modal(
                                    discord.ui.InputText(
                                        label="暱稱前方的預設值",
                                        placeholder="請輸入指定的預設格式(在暱稱前方)",
                                        required=False
                                    ), 
                                    discord.ui.InputText(
                                        label="暱稱後方的預設值",
                                        placeholder="輸入指定的預設格式(在暱稱後方)",
                                        required=False
                                    ),
                                    title="暱稱格式設定", 
                                    custom_id="nick_modal_setting"
                                )
                            )

                        case "words":
                            await interaction.response.send_modal(
                                discord.ui.Modal(
                                    discord.ui.InputText(
                                        label="禁用的文字",
                                        placeholder="輸入指定的文字",
                                    ),
                                    discord.ui.InputText(
                                        label="特殊身分組禁用的文字",
                                        placeholder="輸入指定的文字"
                                    ),
                                    title="文字設定", 
                                    custom_id="words_modal_setting"
                                )
                            )

                        case "roles":
                            await interaction.response.send_message(
                                embed=discord.Embed(
                                    title="身分組設定",
                                    description="請透過下方按鈕來進行操作"
                                ),
                                view=discord.ui.View(
                                    discord.ui.Button(
                                        style=discord.ButtonStyle.danger,
                                        label="禁用的身分組",
                                        custom_id="block_roles_setting",
                                        emoji="📌"
                                    ),
                                    discord.ui.Button(
                                        style=discord.ButtonStyle.primary,
                                        label="具有管理權的身分組",
                                        custom_id="admin_roles_setting",
                                        emoji="⚙️"
                                    ),
                                    timeout=None
                                ),
                                ephemeral=True
                            )

                        case "other":
                            await interaction.response.send_message(
                                "此功能暫時停用~",
                                ephemeral=True
                            )

                case "block_roles":
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title="禁用身分組設定",
                            description="請從以下選單選擇身分組"
                        ),
                        view=discord.ui.View(
                            discord.ui.Select(
                                select_type=discord.ComponentType.role_select,
                                placeholder="選擇身分組",
                                max_values=25,
                                custom_id="block_roles_select_setting"
                            ),
                            timeout=None
                        ),
                        ephemeral=True
                    )

                case "admin_roles":
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title="管理權身分組設定",
                            description="請從以下選單選擇身分組"
                        ),
                        view=discord.ui.View(
                            discord.ui.Select(
                                select_type=discord.ComponentType.role_select,
                                placeholder="選擇身分組",
                                max_values=25,
                                custom_id="admin_roles_select_setting"
                            ),
                            timeout=None
                        ),
                        ephemeral=True
                    )

        match interaction.custom_id:
            case "modify":
                new_nick = discord.ui.InputText(
                    label="新暱稱",
                    placeholder="輸入你的新暱稱",
                    min_length=1,
                    max_length=16
                )        

                modal = discord.ui.Modal(new_nick, title="修改你的暱稱", custom_id="nick_modal")

                return await interaction.response.send_modal(modal)

            case "check":
                cooldown = self.bot.get_user_cooldown(interaction.user.id)
                unix_time  = creat_unix(cooldown)
                description = f"<t:{unix_time}:R> 才能修改一次"

                if not cooldown or cooldown <= get_time():
                    description = "冷卻已結束!"
                
                embed = discord.Embed(
                    title="冷卻時間",
                    description=description
                )
                return await interaction.response.send_message(embed=embed, ephemeral=True)

            case "nick_modal":         
                nick = interaction.data.get("components",{})[0].get("components",{})[0].get("value")
                user_cooldown = self.bot.get_user_cooldown(interaction.user.id)

                if not nick:
                    embed = discord.Embed(
                        title="錯誤!",
                        description="```無法讀取資料 請再試一次或是將此情形回報給開發者```"
                    )
                    return await interaction.response.send_message(embed=embed, ephemeral=True)
                
                if len(list(filter(lambda x:x in self.bot.database.block_words, nick))) > 0 or is_emoji(nick) or (not is_available_language(nick)):
                    return await interaction.response.send_message("錯誤! 偵測到不該使用的字元", ephemeral=True)
                
                if  user_cooldown is not None and user_cooldown > get_time():
                    return await interaction.response.send_message(f"你已經修改過了! <t:{creat_unix(user_cooldown)}:R> 才能在修改一次", ephemeral=True)

                try:
                    #await interaction.user.edit(nick="〡"+nick)
                    cooldown = datetime(**get_time(type="dict"))+timedelta(minutes=30.0)
                    
                    self.bot.database.set_user_cooldown(interaction.user.id, **get_time(cooldown, type="dict"))
                    return await interaction.response.send_message("已成功修改你的暱稱~", ephemeral=True)

                except discord.errors.Forbidden as error:
                    match error.text:
                        case "Missing Permissions":
                            return await interaction.response.send_message("權限不足!", ephemeral=True)

                        case _:
                            embed = discord.Embed(
                                title="錯誤! 表單好像出了點問題>< 請將此情形回報給開發者們",
                                description=f"```Msg: {error.text}\nStatus: {error.status}\nCode: {error.code}```"
                            )

                            return await interaction.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(General(bot))
    