from discord import (
    Colour,
)

from discord.embeds import (
    Embed,
    EmbedField,
    _EmptyEmbed,
)

from discord.types.embed import EmbedType

from typing import Any
from datetime import datetime

class Embed(Embed):
    def __init__(self, *, colour: int | Colour | _EmptyEmbed = ..., color: int | Colour | _EmptyEmbed = ..., title: Any = ..., type: EmbedType = "rich", url: Any = ..., description: Any = ..., timestamp: datetime = None, fields: list[EmbedField] | None = None):
        super().__init__(colour=colour, color=color, title=title, type=type, url=url, description=description, timestamp=timestamp, fields=fields)

    @classmethod
    def from_dict(self, data: dict):
        if data.get("timestamp") == "<now>":
            data["timestamp"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    
        embed = super().from_dict(data)

        return embed