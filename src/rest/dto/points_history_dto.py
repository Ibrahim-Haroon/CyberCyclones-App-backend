from typing import TypedDict
from dataclasses import dataclass


@dataclass
class PointsHistoryDto(TypedDict):
    period: str  # ISO format datetime
    points_earned: int
    discoveries_count: int
    average_points_per_discovery: float
