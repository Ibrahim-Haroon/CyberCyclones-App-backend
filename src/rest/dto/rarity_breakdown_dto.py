from typing import TypedDict
from dataclasses import dataclass


@dataclass
class RarityBreakdownDto(TypedDict):
    points: int
    count: int
    average_points: float
