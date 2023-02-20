from discord.ui import (
    Modal,
    InputText,
)

from discord import InputTextStyle

class InputText(InputText):
    def __init__(self, *, style: InputTextStyle = InputTextStyle.short, custom_id: str | None = None, label: str, placeholder: str | None = None, min_length: int | None = None, max_length: int | None = None, required: bool | None = True, value: str | None = None, row: int | None = None):
        super().__init__(style=style, custom_id=custom_id, label=label, placeholder=placeholder, min_length=min_length, max_length=max_length, required=required, value=value, row=row)

    @classmethod
    def from_dict(self, data: dict):
        style = {
            "long" : InputTextStyle.long,
            "short" : InputTextStyle.short,
            "multiline" : InputTextStyle.multiline,
            "paragraph" : InputTextStyle.paragraph,
            "singleline" : InputTextStyle.singleline
        }

        children = self.__new__(self)
        children.__init__(
            style=style[data.get("style")],
            label=data.get("label"),
            placeholder=data.get("placeholder"),
        )

        return children

class Modal(Modal):
    def __init__(self, *children: InputText, title: str, custom_id: str | None = None, timeout: float | None = None) -> None:
        super().__init__(*children, title=title, custom_id=custom_id, timeout=timeout)

    @classmethod
    def from_dict(self, data: dict):
        modal = self.__new__(self)
        modal.__init__(
            title=data.get("title"),
            children=(InputText.from_dict(d) for d in data.get("input_text")),
            custom_id=data.get("custom_id")
        )

        return modal