from typing import TypedDict
from dataclasses import dataclass


@dataclass
class PointsDeductionDto(TypedDict):
    new_balance: int
    status_message: str
