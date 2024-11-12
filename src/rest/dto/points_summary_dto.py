from typing import TypedDict
from dataclasses import dataclass


@dataclass
class PointsSummaryDto(TypedDict):
    current_balance: int
    total_earned: int
    current_rank: int
    rank_title: str
    leaderboard_position: int
    next_rank: int | None
    points_to_next_rank: int | None
    discoveries_count: int
