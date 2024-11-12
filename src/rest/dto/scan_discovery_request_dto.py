from typing import TypedDict
from dataclasses import dataclass
from django.core.files import File


@dataclass
class ScanDiscoveryRequestDto(TypedDict):
    image: File
