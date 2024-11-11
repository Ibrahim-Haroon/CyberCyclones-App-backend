from typing import TypedDict
from dataclasses import dataclass


@dataclass
class OwnedSkinDto(TypedDict):
    skin_id: int
    name: str
    rarity: str
    acquired_at: str  # ISO format datetime
    acquisition_type: str
    is_equipped: bool
