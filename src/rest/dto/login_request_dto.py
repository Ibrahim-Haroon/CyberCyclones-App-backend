from typing import TypedDict
from dataclasses import dataclass


@dataclass
class LoginRequestDto(TypedDict):
    username: str
    password: str
