from typing import TypedDict
from dataclasses import dataclass


@dataclass
class PointsDeductionRequestDto(TypedDict):
    points: int
