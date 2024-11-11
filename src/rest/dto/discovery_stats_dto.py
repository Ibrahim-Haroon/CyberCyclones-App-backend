from typing import TypedDict
from dataclasses import dataclass


@dataclass
class DiscoveryStatsDto(TypedDict):
    total_discoveries: int
    categories: dict[str, int]  # e.g., {"PLASTIC": 10, "METAL": 5}
    rarities: dict[str, int]    # e.g., {"COMMON": 8, "RARE": 7}
    total_decomposition_years: float
    discoveries_last_7_days: int
    total_points_from_discoveries: int
