from typing import TypedDict
from dataclasses import dataclass


@dataclass
class PasswordChangeRequestDto(TypedDict):
    old_password: str
    new_password: str
