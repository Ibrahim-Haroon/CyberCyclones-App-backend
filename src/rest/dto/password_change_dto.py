from typing import TypedDict
from dataclasses import dataclass


@dataclass
class PasswordChangeDto(TypedDict):
    success: bool
    last_changed: str  # ISO format datetime
