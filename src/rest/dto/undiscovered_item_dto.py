from typing import TypedDict
from dataclasses import dataclass


@dataclass
class UndiscoveredItemDto(TypedDict):
    name: str
    category: str
    rarity: str
    point_value: int
