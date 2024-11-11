from typing import TypedDict
from dataclasses import dataclass


@dataclass
class DiscoveryHistoryDto(TypedDict):
    item_name: str
    category: str
    points_awarded: int
    discovered_at: str  # ISO format datetime
    rarity: str
