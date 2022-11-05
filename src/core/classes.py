import discord
import json
import os

from quick_sqlite import Database
from discord.ext import commands
from dotenv import load_dotenv

from typing import (
    Any
)

from core.functions import (
    load_extension,
    write_json,
    read_json
)

load_dotenv()

class Setting:
    def __init__(self,path:str) -> None:
        self._setting:dict = read_json(path)
        self.database = self._setting.get("database",{})
        self.general = self._setting.get("general",{})
        self.admins:list = self._setting.get("managements",{}).get("admin",[])
        self.cog:dict = self._setting.get("cog",{})
        self.path = path

    def add_category(self, name:str, default:dict={}):
        return write_json(self.path, name ,default)

    def add_admin(self, id:int):
        self.admins.append(id)
        return self.add_category("managements", {"admin":self.admins})

    def add_cog(self, key:str, value:Any):
        return self.add_category("cog",{ key:value})

    def add_database(self, key:str, value:Any):
        return self.add_category("database", {key:value})

class Bot(commands.Bot):
    def __init__(self,command_prefix="!", description=None, setting_path="setting", *args, **options):
        super().__init__(command_prefix, description, *args, **options)

        self.setting = Setting(setting_path)
        self.database_path = self.setting.database.get("path","bot.db")
        self.database = Database(self.database_path)
        self.token:str = os.getenv("TOKEN")

        @commands.check
        def is_administrator(ctx:commands.Context):
            return ctx.author.id in self.setting.admins
        
        @self.command()
        async def load(ctx:commands.Context, extension:str = None, folder:str = "commands"):
            load_extension(self, folder) if not extension else self.load_extension(f"{folder}.{extension}")
            await ctx.reply("loading end!")

        @self.command()
        async def unload(ctx, extension:str = None, folder:str = "commands"):
            load_extension(self, folder, "unload") if not extension else self.unload_extension(f"{folder}.{extension}")
            await ctx.reply("unloading end")

        @self.command()
        async def reload(ctx, extension:str = None, folder:str = "commands"):
            load_extension(self, folder, "reload") if not extension else self.reload_extension(f"{folder}.{extension}")
            await ctx.reply("reloading end")

    def setup(self):
        return [load_extension(self,folder) for folder in self.setting.cog["folder"]]

class CogExtension(discord.Cog):
    def __init__(self,bot : Bot) -> None:
        self.bot = bot

if __name__ == "__main__":
    pass