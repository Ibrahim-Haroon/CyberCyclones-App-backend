from typing import TypedDict
from dataclasses import dataclass


@dataclass
class LoginDto(TypedDict):
    user_id: int
    username: str
    display_name: str | None
    token: str
    points_balance: int
    rank_title: str
