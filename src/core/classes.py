import discord
import json
import os

from quick_sqlite import Database
from discord.ext import commands
from dotenv import load_dotenv

from typing import (
    Any,
    List
)

from core.functions import (
    load_extension,
    write_json,
    read_json
)

load_dotenv()

class Database(Database):
    def __init__(self, path: str, db_name: str = "__default__", auto_init: Any = None) -> None:
        super().__init__(path, db_name, auto_init)

        self.data = {
            "block_roles":self.block_roles,
            "block_words":self.block_words
        }

    def append(self, key, more, mode="int") -> any:
        """
        if mode `int` that will add more to the value of key. 
        if mode `list` that will append new obj to the value(list) of key
        """
        if mode == "int":
            return super().append(key, more) 

        elif mode == "list":
            data = list(self.get(key))
            data += more if isinstance(more,list) else data.append(more)
                
        return self.set(key,data)
            
    def reset(self) -> None:
        "reset all the value "
        return [self.set(key, None) for key in self.get_all_key()]

    def set_block_roles(self, new:List[discord.Role]) :
        "set the new value to the `block_roles`"

        return None if not self.get("block_roles") else (self.set("block_roles", new) if isinstance(new, list) else None)

    def set_block_words(self, new:List[discord.Role]):
        "set the new value to the `block_words`"

        return None if not self.get("block_words") else (self.set("block_words", new) if isinstance(new, list) else None)

    def append_block_roles(self, role:discord.Role) -> None:
        "append the value to the `block_roles`"

        return None if not self.get("block_roles") else self.append("block_words", role, "list")

    def append_block_words(self, words:str)  -> None:
        "append the value to the `block_words`"
        return None if not self.get("block_words") else self.append("block_words", words, "list")

    @property
    def block_roles(self) -> list:
        if not self.get("block_roles"):
            self.set("block_roles",[])

        return self.get("block_roles")
        
    @property
    def block_words(self) -> list:
        if not self.get("block_words"):
            self.set("block_words",[])

        return self.get("block_words")

class Setting:
    def __init__(self, path:str) -> None:
        self._setting:dict = read_json(path)
        self.database = self._setting.get("database",{})
        self.general = self._setting.get("general",{})
        self.admins:list = self._setting.get("managements",{}).get("admin",[])
        self.cog:dict = self._setting.get("cog",{})
        self.path = path

    def add_category(self, name:str, default:dict={}):
        "add new category"
        return write_json(self.path, name ,default)

    def add_admin(self, id:int):
        "add new admin(id)"
        self.admins.append(id)
        return self.add_category("managements", {"admin":self.admins})

    def add_cog(self, key:str, value:Any):
        "add new data in the cog"
        return self.add_category("cog", {key:value})

    def add_database(self, key:str, value:Any):
        "add new data in the database"
        return self.add_category("database", {key:value})

class Bot(commands.Bot):
    def __init__(self,command_prefix="!", description=None, setting_path="setting", *args, **options):
        super().__init__(command_prefix, description, *args, **options)

        self.setting = Setting(setting_path)
        self.database_path = self.setting.database.get("path","bot.db")
        self.database = Database(self.database_path)
        self.token:str = os.getenv("TOKEN")

    def is_administrator(self,ctx:commands.Context):
        return ctx.author.id in self.setting.admins

    def setup(self):
        "setup the bot"
        default = self.setting.database["default_block_words"]
        if default not in self.database.block_words:
            self.database.append_block_words(default)

        [load_extension(self,folder) for folder in self.setting.cog["folder"]]

        @self.command()
        @commands.check(self.is_administrator)
        async def load(ctx:commands.Context, extension:str = None, folder:str = "commands"):
            load_extension(self, folder) if not extension else self.load_extension(f"{folder}.{extension}")
            await ctx.reply("loading end!")

        @self.command()
        @commands.check(self.is_administrator)
        async def unload(ctx:commands.Context, extension:str = None, folder:str = "commands"):
            load_extension(self, folder, "unload") if not extension else self.unload_extension(f"{folder}.{extension}")
            await ctx.reply("unloading end!")

        @self.command()
        @commands.check(self.is_administrator)
        async def reload(ctx:commands.Context, extension:str = None, folder:str = "commands"):
            load_extension(self, folder, "reload") if not extension else self.reload_extension(f"{folder}.{extension}")
            await ctx.reply("reloading end!")

        return None


class CogExtension(discord.Cog):
    def __init__(self,bot:Bot) -> None:
        self.bot = bot

if __name__ == "__main__":
    print(list([]))