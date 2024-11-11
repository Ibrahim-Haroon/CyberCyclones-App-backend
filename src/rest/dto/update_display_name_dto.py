from typing import TypedDict
from dataclasses import dataclass


@dataclass
class UpdateDisplayNameDto(TypedDict):
    username: str
    display_name: str
    updated_at: str  # ISO format datetime
