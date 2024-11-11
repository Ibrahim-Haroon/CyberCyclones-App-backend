from typing import TypedDict
from dataclasses import dataclass


@dataclass
class WeeklyLeaderboardDto(TypedDict):
    rank: int
    username: str
    display_name: str | None
    weekly_points: int
    rank_title: str
