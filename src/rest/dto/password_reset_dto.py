from typing import TypedDict
from dataclasses import dataclass


@dataclass
class PasswordResetDto(TypedDict):
    reset_token: str
    expiry: str  # ISO format datetime
