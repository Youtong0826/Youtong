from dotenv import load_dotenv

from typing import (
    Any
)

from core.functions import (
    write_json,
    read_json
)

load_dotenv()

class BaseSetting:
    def __init__(self, path:str) -> None:
        self._setting:dict = read_json(path)
        self.path = path
    
    def get(self, key:str, default:Any = {}):
        return self._setting.get(key, default)

    def add(self, category:str, key:str, value):
        "add data"
        return write_json(self.path, category, {key : value})

    def add_category(self, name:str, default:dict={}):
        "add new category or value"
        return write_json(self.path, name ,default)

    def __str__(self) -> str:
        return str(self._setting)

class Setting(BaseSetting):
    def __init__(self, path: str) -> None:
        super().__init__(path)

        self.managements = self.get("managements", {})
        self.database = self.get("database", {})
        self.general = self.get("general", {})
        self.checks = self.get("checks", {})
        self.cog = self.get("cog",{})
    