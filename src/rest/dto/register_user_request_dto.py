from typing import TypedDict
from dataclasses import dataclass


@dataclass
class RegisterUserRequestDto(TypedDict):
    username: str
    email: str
    password: str
    display_name: str | None
