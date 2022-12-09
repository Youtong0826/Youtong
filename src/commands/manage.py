import discord

from discord.ext import commands
from core.bot import CogExtension

class Manage(CogExtension):
    
    async def setting(self, ctx:commands.Context):
        config = self.bot.get_custom_commands("setting")[0][1]

        kwargs = {
            "embed":discord.Embed.from_dict(config["embed"]),
            "view":discord.ui.View(*self.bot.get_items_from_dict(config))
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