from typing import TypedDict
from dataclasses import dataclass


@dataclass
class RegisterUserDto(TypedDict):
    user_id: int
    username: str
    display_name: str | None
    email: str
    token: str
    created_at: str  # ISO format datetime
