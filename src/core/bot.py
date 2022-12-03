import discord
import os

from discord.ext import commands
from dotenv import load_dotenv
from core.functions import (
    load_extension,
)

from core.database import (
    Database
)

from core.configs import (
    Setting,
)

load_dotenv()

class Bot(commands.Bot):
    def __init__(self,command_prefix="!", description=None, setting_path="setting", *args, **options):
        super().__init__(command_prefix, description, *args, **options)

        self.setting = Setting(setting_path)

        self.database_path = self.setting.database.get("path","bot.db")
        self.database = Database(self.database_path)

        self.token:str = os.getenv("TOKEN")

        self.version = self.setting.general.get("version", [0, 0, 0])
        self.avatar = self.setting.general.get("avatar_url", "")
        self.id = self.setting.general.get("id",0)

        self.cooldown = self.setting.managements.get("cooldown", [0, 0, 0])
        self.vips = self.setting.managements.get("vips", [0, 0, 0])

    def is_administrator(self, ctx:commands.Context):
        return ctx.author.guild_permissions.administrator or ctx.author.id in self.vips

    def is_available_channel(self, ctx:commands.Context):
        return ctx.channel.id in self.setting.checks["channel"]

    def is_test_channel(self, ctx:commands.Context):
        return ctx.channel.id in self.setting.checks["test_channel"]

    def reload_setting(self, path:str = None):
        self.setting = Setting(self.setting.path) if not path else Setting(path)
        return self.setting

    def setup(self):
        "setup the bot"
        default = [] if not (data := self.setting.database.get("default_block_words")) else data
        if default not in list(self.database.block_words) and len(default) > 0:
            self.database.append_block_words(default)

        [load_extension(self,folder) for folder in self.setting.cog.get("folder", [])]

        if self.setting.general["version"][0] < 1:
            self.add_check(self.is_test_channel)

        async def delete_after_sent(ctx:commands.Context, msg:discord.Message, sec:float = 5.0):
            await ctx.message.delete()
            await msg.delete(delay=sec)

        @self.command()
        @commands.check(self.is_administrator)
        async def load(ctx:commands.Context, extension:str = None, folder:str = "commands"):
            load_extension(self, folder) if not extension else self.load_extension(f"{folder}.{extension}")
            msg = await ctx.reply("loading end!")
            await delete_after_sent(ctx, msg)
            
        @self.command()
        @commands.check(self.is_administrator)
        async def unload(ctx:commands.Context, extension:str = None, folder:str = "commands"):
            load_extension(self, folder, "unload") if not extension else self.unload_extension(f"{folder}.{extension}")
            msg = await ctx.reply("unloading end!")
            await delete_after_sent(ctx, msg)

        @self.command()
        @commands.check(self.is_administrator)
        async def reload(ctx:commands.Context, extension:str = None, folder:str = "commands"):
            load_extension(self, folder, "reload") if not extension else self.reload_extension(f"{folder}.{extension}")
            msg = await ctx.reply("reloading end!")
            await delete_after_sent(ctx, msg)

        @commands.command(name="reload-setting")
        async def reload_setting(ctx:commands.Context,):
            self.reload_setting()
            msg = await ctx.reply("reloading setting end!")
            await delete_after_sent(ctx, msg)
    
        return None

class CogExtension(discord.Cog):
    def __init__(self, bot:Bot) -> None:
        self.bot = bot