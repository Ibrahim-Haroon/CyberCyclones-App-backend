from typing import TypedDict
from dataclasses import dataclass


@dataclass
class PasswordResetRequestDto(TypedDict):
    email: str
