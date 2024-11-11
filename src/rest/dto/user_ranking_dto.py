from typing import TypedDict
from dataclasses import dataclass


@dataclass
class UserRankingDto(TypedDict):
    username: str
    display_name: str | None
    global_rank: int
    total_points: int
    weekly_points: int
    rank_title: str
    category_rankings: dict[str, int]  # e.g., {"PLASTIC": 1, "METAL": 3}
    total_discoveries: int
