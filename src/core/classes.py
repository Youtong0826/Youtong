import discord

from quick_sqlite import Database
from dotenv import load_dotenv

from typing import (
    Any,
    List
)

from core.functions import (
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

    def __str__(self) -> str:
        all = super().get_all()
        return str([(item.key, item.value) for item in all])

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

    def set_block_words(self, new:List[str]):
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
    def __init__(self, path:str, categories:list = []) -> None:
        self._setting:dict = read_json(path)
        self.general = self._setting.get("general", {})
        self.managements = self._setting.get("managements", {})
        self.database = self._setting.get("database", {})
        self.checks = self._setting.get("checks", {})
        self.cog = self._setting.get("cog",{})
        self.path = path

    def __str__(self) -> str:
        return str(self._setting)

    def add(self, category:str, key:str, value):
        "add data"
        return write_json(self.path, category, {key : value})

    def add_category(self, name:str, default:dict={}):
        "add new category or value"
        return write_json(self.path, name ,default)

if __name__ == "__main__":
    pass