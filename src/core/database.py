import discord

from quick_sqlite import Database
from dotenv import load_dotenv

from typing import (
    Any,
    List
)

load_dotenv()

class Database(Database):
    def __init__(self, path: str, db_name: str = "__default__", auto_init: Any = None) -> None:
        super().__init__(path, db_name, auto_init)

        self.data = {
            "block_roles":self.block_roles,
            "block_words":self.block_words,
        }

    def __str__(self) -> str:
        all = super().get_all()
        return str([(item.key, item.value) for item in all])

    def append(self, key, more, mode="int") -> Any:
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

    def set_primary_users(self, new:List[int]):
        "set the new value to the `primary_users`"

        return None if not self.get("primary_users") else (self.set("primary_users", new) if isinstance(new, list) else None)
    
    def set_user_cooldown(self, new:List[List[int]]):
        "set the new value to the `user_cooldown`"

        return None if not self.get("user_cooldown") else (self.set("user_cooldown", new) if isinstance(new, list) else None)

    def append_block_roles(self, role:discord.Role) -> None:
        "append the value to the `block_roles`"

        return None if not self.get("block_roles") else self.append("block_words", role, "list")

    def append_block_words(self, words:str)  -> None:
        "append the value to the `block_words`"
        return None if not self.get("block_words") else self.append("block_words", words, "list")

    def append_primary_users(self, id:int)  -> None:
        "append the value to the `primary_users`"
        return None if not self.get("block_words") else self.append("block_words", id)

    def append_user_cooldown(self, id:int)  -> None:
        "append the value to the `user_cooldown`"
        return None if not self.get("user_cooldown") else self.append("user_cooldown", id)

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

    @property
    def primary_users(self) -> list:
        if not self.get("primary_users"):
            self.set("primary_users",[])

        return self.get("primary_users")

    @property
    def user_cooldown(self) -> list:
        if not self.get("user_cooldown"):
            self.set("user_cooldown",[])

        return self.get("user_cooldown")

if __name__ == "__main__":
    pass