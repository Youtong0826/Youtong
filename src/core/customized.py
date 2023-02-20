from core.functions import read_json

from typing import (
    List,
    Tuple
)

class Customization:
    def __init__(self, path: str) -> None:
        self._data = read_json(path)
        self.path = path

class CustomCommandConfig(Customization):
    def __init__(self, path: str) -> None:
        super().__init__(path)

    @property
    def commands(self) -> List[Tuple[str,dict]]:
        return [(key,value) for key,value in self._data.items()]
