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
            style=discord.ButtonStyle.success,
            label="文字設定",
            custom_id="words_setting",
            emoji="📰"
        )

        role = discord.ui.Button(
            style=discord.ButtonStyle.primary,
            label="身分組設定",
            custom_id="role_setting",
            emoji="📜",
            row=1
        )

        other = discord.ui.Button(
            style=discord.ButtonStyle.gray,
            label="其他設定",
            custom_id="other_setting",
            emoji="🔧",
            row=1
        )

        item = nick,words,role,other

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

    @commands.Cog.listener()
    async def on_interaction(self, interaction:discord.Interaction):
        if not interaction.custom_id: return
        
        if interaction.custom_id.endswith("_setting"):
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
                            title="暱稱預設格式設定", 
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
                            custom_id="nick_modal_setting"
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
                                label="管理權的身分組",
                                custom_id="admin_roles_setting",
                                emoji="⚙️"
                            ),
                            timeout=None
                        ),
                        ephemeral=True
                    )

                case "other":
                    await interaction.response.send_message(
                        "此功能暫時停用",
                        ephemeral=True
                    )


def setup(bot):
    bot.add_cog(Manage(bot))