from functions import (
    write_json,
    read_json
)

class BaseCustomCommandObject:
    def __init__(self, data:dict) -> None:
        self._data = data

class CustomCommandEmbedField(BaseCustomCommandObject):
    def __init__(self, id:str, data:dict) -> None:
        super().__init__(data)
        self.id = id
        self.name = data.get("name")
        self.value = data.get("value")
        self.inline = data.get("inline")
        
    def __str__(self) -> str:
        return self.name

    def __bool__(self) -> bool:
        return self.inline

class CustomCommandEmbed(BaseCustomCommandObject):
    def __init__(self, data:dict) -> None:
        super().__init__(data)
        self.title = data.get("title")
        self.description = data.get("description")
        self.footer_text = data.get("footer_text")

        self.fields = [
            CustomCommandEmbedField(id, data) 
            for id, data in data.get("fields",{}).items()
        ]

    def __str__(self) -> str:
        return self.title

class CustomCommandButton(BaseCustomCommandObject):
    def __init__(self, id:str, data:dict) -> None:
        if data.get("type") != "button":
            raise TypeError("this is not a button")

        self.id = id
        self.row = data.get("row")
        self.style = data.get("style")
        self.lable = data.get("label")
        self.emoji = data.get("emoji")
        self.custom_id = data.get("custom_id")

class CustomCommandSelectOption(BaseCustomCommandObject):
    def __init__(self, id:str, data:dict) -> None:
        self.id = id
        self.label = data.get("label")
        self.emoji = data.get("emoji")

class CustomCommandSelect(BaseCustomCommandObject):
    def __init__(self, id:str, data:dict) -> None:
        if data.get("type") != "select":
            raise TypeError("this is not a button")

        self.id = id
        self.placeholder = data.get("placeholder")
        self.custom_id = data.get("custom_id")

        self.options = [
            CustomCommandSelectOption(id, data) 
            for id, data in data.get("options",{}).items()
        ]

class CustomCommandView(BaseCustomCommandObject):
    def __init__(self, data:dict) -> None:
        self.timeout = data.get("timeout")
        self._items = data.get("items",{})

        self.buttons = [
            CustomCommandButton(id, data) 
            for id, data in self._items.items() if data.get("type") == "button"
        ]

        self.select = [
            CustomCommandSelect(id, data)
            for id, data in self._items.items() if data.get("type") == "select"
        ]

        self.items = [self.buttons, self.select]

class CustomCommandConfig:
    def __init__(self, path:str) -> None:
        self._data = read_json(path)
        self.path = path

    def set(self, key:str, value:str):
        return write_json(self.path, key, value)

    def get(self, command:str, key:str):
        return self._data.get(command, {}).get(key, {})

    def get_embed(self, command:str):
        return CustomCommandEmbed(self.get(command, "embed"))

    def get_view(self, command:str):
        return CustomCommandView(self.get(command, "view"))

    @property
    def commands(self):
        return [(key,value) for key,value in self._data.items()]

class CustomCommand:
    def __init__(self, name:str, path:str=None) -> None:
        self.name = name
        self.config = CustomCommandConfig(path)
        self.embed = self.config.get_embed(name)
        self.view = self.config.get_view(name)

    def __str__(self) -> str:
        return self.name

if __name__ == "__main__":
    test = CustomCommand("nick","commands.json")
    print(test.embed)
    print(test.view)