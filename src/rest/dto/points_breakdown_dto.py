from typing import TypedDict
from dataclasses import dataclass
from src.rest.dto.time_pattern_dto import TimePatternDto
from src.rest.dto.engagement_stats_dto import EngagementStatsDto
from src.rest.dto.rarity_breakdown_dto import RarityBreakdownDto
from src.rest.dto.category_breakdown_dto import CategoryBreakdownDto


@dataclass
class PointsBreakdownDto(TypedDict):
    total_discoveries: int
    total_points: int
    category_breakdown: dict[str, CategoryBreakdownDto]
    rarity_breakdown: dict[str, RarityBreakdownDto]
    time_patterns: dict[int, TimePatternDto]  # hour -> stats
    engagement_stats: EngagementStatsDto
