from typing import TypedDict
from dataclasses import dataclass


@dataclass
class ScanDiscoveryDto(TypedDict):
    item_name: str
    category: str
    points_awarded: int
    new_total_points: int
    environmental_impact: str
    decomposition_time: int  # in days
    threat_level: int
