import discord

from discord.ext import commands
from core.bot import CogExtension

class Manage(CogExtension):
    
    async def setting(self, ctx:commands.Context):
        embed = discord.Embed(
            title="設定",
            description="請從底下選單進行下一步操作"
        )

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

        select = discord.ui.Select(
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
        )

        if isinstance(ctx, commands.Context):
            await ctx.reply(
                embed=embed,
                view=discord.ui.View(select, timeout=None),
                mention_author=False
            )

        else:
            await ctx.respond(
                embed=embed,
                view=discord.ui.View(select, timeout=None),
            )

    @discord.application_command(name="設定", description="管理機器人設定")
    async def slash_setting(self, ctx):
        await self.setting(ctx)

    @commands.command(name="setting")
    async def text_setting(self, ctx):
        await self.setting(ctx)

    @commands.Cog.listener()
    async def on_interaction(self, interaction:discord.Interaction):

        if interaction.custom_id is not None and interaction.custom_id.endswith("_setting"):
            match interaction.custom_id.replace("_setting", ""):
                case "nick":
                    await interaction.response.send_modal(
                        discord.ui.Modal(
                            discord.ui.InputText(
                                label="暱稱前方的預設值",
                                placeholder="請輸入指定的預設格式(在暱稱前方)",
                            ), 
                            discord.ui.InputText(
                                label="暱稱後方的預設值",
                                placeholder="輸入指定的預設格式(在暱稱後方)",
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

                case "role":
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
                                style=discord.ButtonStyle.danger,
                                label="具有管理權的身分組",
                                custom_id="admin_roles_setting",
                                emoji="⚙️"
                            ),
                            timeout=None
                        ),
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
                                placeholder="選擇身分組",
                                max_values=25,
                                options=[
                                    discord.SelectOption(
                                        label=role.name,
                                        value=role.id,
                                        emoji=role.unicode_emoji,
                                    )
                                    for role in interaction.guild.roles
                                ],
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
                                placeholder="選擇身分組",
                                max_values=25,
                                options=[
                                    discord.SelectOption(
                                        label=role.name,
                                        value=role.id,
                                        emoji=role.unicode_emoji,
                                    )
                                    for role in interaction.guild.roles
                                ],
                                custom_id="admin_roles_select_setting"
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


def setup(bot):
    bot.add_cog(Manage(bot))