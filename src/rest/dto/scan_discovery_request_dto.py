from typing import TypedDict
from dataclasses import dataclass


@dataclass
class ScanDiscoveryRequestDto(TypedDict):
    image: str  # base64 encoded image
