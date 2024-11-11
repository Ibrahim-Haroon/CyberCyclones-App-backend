from typing import TypedDict
from dataclasses import dataclass


@dataclass
class SkinEquipDto(TypedDict):
    skin_name: str
    rarity: str
    equipped_at: str  # ISO format datetime
