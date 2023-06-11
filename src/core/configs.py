from dotenv import load_dotenv

from typing import (
    Any
)

from core.functions import (
    write_json,
    read_json
)

from core.customized import (
    CustomCommandConfig
)

load_dotenv()

class BaseSetting:
    def __init__(self, path:str) -> None:
        self.path = path

    @property
    def _data(self):
        return read_json(self.path)

    def set(self, category: str, key: str, value: Any):
        return write_json(self.path, category, {key : value})
    
    def get(self, key: str, default:Any = {}):
        return self._data.get(key, default)

    def add_category(self, name: str, default: dict = {}):
        "add new category or value"
        return write_json(self.path, name ,default)

    def __str__(self) -> str:
        return str(self._data)

class Setting(BaseSetting):
    def __init__(self, path: str) -> None:
        super().__init__(path)

        self.managements: dict = self.get("managements", {})
        self.database: dict = self.get("database", {})
        self.general: dict = self.get("general", {})
        self.checks: dict = self.get("checks", {})
        self.cog: dict = self.get("cog",{})
        self.commands_config = CustomCommandConfig("commands.json")
        self.commands = self.commands_config.commands
    