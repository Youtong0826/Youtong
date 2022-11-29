import discord

from discord.ext import commands
from core.bot import CogExtension

class Manage(CogExtension):
    
    async def setting(self, ctx:commands.Context):
        options = {
            "nick_setting":{
                "label":"暱稱設定",
                "emoji":"📰"
            },
            "words_setting":{
                "label":"文字設定",
                "emoji":"📃"
            },
            "roles_setting":{
                "label":"身分組設定",
                "emoji":"📜"
            },
            "other_setting":{
                "label":"其他設定",
                "emoji":"🔧"
            }
        }

        kwargs = {
            "embed":discord.Embed(
                title="設定",
                description="請透過選單進行下一步操作"
            ),
            "view":discord.ui.View(
                discord.ui.Select(
                    custom_id="main_select_setting",
                    placeholder="請選擇下一步操作",
                    options=[
                        discord.SelectOption(
                            value=value,
                            label=option["label"],
                            emoji=option["emoji"]
                        )
                        for value,option in options.items()
                    ]
                ),
                timeout=None
            )
        }

        if isinstance(ctx, commands.Context):
            await ctx.reply(
                mention_author=False,
                **kwargs
            )

        else:
            await ctx.respond(
                **kwargs
            )

    @discord.application_command(name="設定", description="管理機器人設定")
    async def slash_setting(self, ctx):
        await self.setting(ctx)

    @commands.command(name="setting")
    async def text_setting(self, ctx):
        await self.setting(ctx)

    @commands.Cog.listener()
    async def on_interaction(self, interaction:discord.Interaction):
        print(interaction.data)

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

                

def setup(bot):
    bot.add_cog(Manage(bot))