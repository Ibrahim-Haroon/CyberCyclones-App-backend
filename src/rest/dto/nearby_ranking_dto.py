from typing import TypedDict
from dataclasses import dataclass


@dataclass
class NearbyRankingDto(TypedDict):
    rank: int
    username: str
    display_name: str | None
    total_points: int
    is_current_user: bool
