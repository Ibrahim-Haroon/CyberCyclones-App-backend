from typing import TypedDict
from dataclasses import dataclass


@dataclass
class GlobalLeaderboardDto(TypedDict):
    rank: int
    username: str
    display_name: str | None
    total_points: int
    rank_title: str
