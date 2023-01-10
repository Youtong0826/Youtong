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

    def __str__(self) -> str:
        all = super().get_all()
        return str([(item.key, item.value) for item in all])

    def get(self, key, default=None) -> Any:
        return default if not super().get(key) else super().get(key)

    def add(self, key, more:int):
        return super().append(key, more)

    def append(self, key, more) -> Any:

        data: list = self.get(key, [])
        data.append(more)
                
        return self.set(key, data)

    def remove(self, key, id) -> Any:
        data: list = self.get(key, [])
        data.remove(id)
        self.set(key, data)
        if id in data:
            return self.remove(key, id)
            
    def reset(self, key) -> None:
        "reset all the value "
        return self.set(key, None)

    def set_block_roles(self, new:List[int]) :
        "set the new value to the `block_roles`"
        return self.set("block_roles", new if isinstance(new, list) else [])

    def set_block_words(self, new:List[str]):
        "set the new value to the `block_words`"
        return self.set("block_words", new if isinstance(new, list) else []) 

    def set_primary_users(self, new:List[int]):
        "set the new value to the `primary_users`"
        return self.set("primary_users", new if isinstance(new, list) else []) 
    
    def set_user_cooldown(self, id, year, month, day, hour, minute, second):
        "set the new value to the `user_cooldown`"

        ori = self.get("user_cooldown", {})
        data = {}
        data["year"] = year
        data["month"] = month
        data["day"] = day
        data["hour"] = hour
        data["minute"] = minute
        data["second"] = second
        ori[id] = data

        return self.set("user_cooldown", ori) 

    def append_block_roles(self, role:int) -> None:
        "append the value to the `block_roles`"
        return self.append("block_roles", role, "list")

    def append_block_words(self, words:str)  -> None:
        "append the value to the `block_words`"
        return self.append("block_words", words, "list")

    def append_primary_users(self, id:int)  -> None:
        "append the value to the `primary_users`"
        return self.append("primary_users", id)

    def append_primary_users(self, id:int)  -> None:
        "append the value to the `primary_users`"
        return self.append("primary_users", id)

    def remove_block_roles(self, id) -> None:
        "delete the value to the `block_roles`"
        return self.remove("block_roles", id)

    def remove_block_words(self, words:str)  -> None:
        "delete the value to the `block_words`"
        return self.remove("block_words", words,)

    def remove_primary_users(self, id:int)  -> None:
        "delete the value to the `primary_users`"
        return self.remove("primary_users", id)

    @property
    def block_roles(self) -> list:
        return self.get("block_roles")
        
    @property
    def block_words(self) -> list:
        return self.get("block_words")

    @property
    def primary_users(self) -> list:
        return self.get("primary_users")

    @property
    def user_cooldown(self) -> dict[str, dict[str,str]]:
        return self.get("user_cooldown")
    
if __name__ == "__main__":
    db = Database("bot.db")
    db.reset("user_cooldown")

