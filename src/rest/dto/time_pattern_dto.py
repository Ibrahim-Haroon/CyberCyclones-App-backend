from typing import TypedDict
from dataclasses import dataclass


@dataclass
class TimePatternDto(TypedDict):
    points: int
    discoveries: int
