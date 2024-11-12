from typing import TypedDict
from dataclasses import dataclass


@dataclass
class CategoryBreakdownDto(TypedDict):
    points: int
    count: int
    average_points: float
