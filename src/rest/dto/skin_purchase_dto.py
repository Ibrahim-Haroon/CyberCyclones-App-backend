from typing import TypedDict
from dataclasses import dataclass


@dataclass
class SkinPurchaseDto(TypedDict):
    skin_name: str
    points_spent: int
    new_balance: int
    rarity: str
