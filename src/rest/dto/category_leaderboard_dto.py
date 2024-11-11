from typing import TypedDict
from dataclasses import dataclass


@dataclass
class CategoryLeaderboardDto(TypedDict):
    rank: int
    username: str
    display_name: str | None
    discoveries: int
    points: int
    category: str
