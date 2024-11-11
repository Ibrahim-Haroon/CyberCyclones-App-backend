from typing import TypedDict
from dataclasses import dataclass


@dataclass
class UpdateDisplayNameRequestDto(TypedDict):
    display_name: str
