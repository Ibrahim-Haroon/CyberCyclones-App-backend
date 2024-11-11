from typing import TypedDict
from dataclasses import dataclass


@dataclass
class PopularDiscoveryDto(TypedDict):
    item_name: str
    category: str
    times_discovered: int
