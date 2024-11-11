from typing import TypedDict
from dataclasses import dataclass


@dataclass
class SkinStatsDto(TypedDict):
    total_skins: int
    rarity_breakdown: dict[str, int]  # e.g., {"COMMON": 5, "RARE": 2}
    acquisition_breakdown: dict[str, int]  # e.g., {"PURCHASE": 4, "ACHIEVEMENT": 3}
    total_points_spent: int
