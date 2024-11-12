from typing import TypedDict
from dataclasses import dataclass


@dataclass
class EngagementStatsDto(TypedDict):
    current_streak: int
    longest_streak: int
    daily_average_points: float
    most_productive_hour: int | None
