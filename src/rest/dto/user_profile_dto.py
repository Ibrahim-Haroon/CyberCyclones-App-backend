from typing import TypedDict
from dataclasses import dataclass


@dataclass
class UserProfileDto(TypedDict):
    username: str
    display_name: str | None
    rank: int
    rank_title: str
    points_balance: int
    total_points_earned: int
    leaderboard_position: int
    active_skin_id: int | None
    member_since: str  # ISO format datetime
    last_login: str | None  # ISO format datetime
