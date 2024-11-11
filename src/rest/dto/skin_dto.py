from typing import TypedDict
from dataclasses import dataclass


@dataclass
class SkinDto(TypedDict):
    skin_id: int
    name: str
    rarity: str
    price_points: int
    description: str
