import base64
from typing import List
from django.db.models import Sum
from src.llm.llm_provider_factory import LLMProviderFactory
from src.llm.llm_type import LlmType
from src.models.items import Item
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone
from src.service.points_service import PointsService
from src.models.user_discoveries import UserDiscovery
from src.repository.user_repository import UserRepository
from rest_framework.exceptions import ValidationError


class DiscoveryService:
    def __init__(self, user_repository: UserRepository, points_service: PointsService):
        self.__user_repository = user_repository
        self.__points_service = points_service

    def process_discovery(self, user_id: int, encoded_image: base64) -> dict:
        """
        Process a new item discovery for a user
        Returns discovery details including points awarded
        """
        user = self.__user_repository.find_by_id(user_id)
        if not user:
            raise ValidationError({"detail": "User not found"})

        try:
            openai_llm = LLMProviderFactory.get_provider(LlmType.OPENAI)
            item_name = openai_llm.get_message(encoded_image)
        except Exception as e:
            raise ValidationError({"detail": f"Error processing image: {str(e)}"})

        try:
            item = Item.objects.get(name__iexact=item_name)
        except Item.DoesNotExist:
            raise ValidationError({"detail": f"Item '{item_name}' not recognized in our database"})

        # Check for existing discovery
        if UserDiscovery.objects.filter(user_id=user_id, item_id=item.id).exists():
            raise ValidationError({"detail": f"You have already discovered {item_name}"})

        # Award points and record discovery
        points_awarded, new_total = self.__points_service.award_points_for_discovery(user_id, item)

        return {
            "item_name": item.name,
            "category": item.category,
            "points_awarded": points_awarded,
            "new_total_points": new_total,
            "environmental_impact": item.environmental_impact_description,
            "decomposition_time": item.average_decomposition_time,
            "threat_level": item.threat_level
        }

    def get_user_discoveries(self, user_id: int) -> List[dict]:
        """Get all discoveries for a user"""
        if not self.__user_repository.find_by_id(user_id):
            raise ValidationError("User not found")

        discoveries = UserDiscovery.objects.filter(user_id=user_id).order_by('-discovered_at')

        return [{
            "item_name": discovery.item.name,
            "category": discovery.item.category,
            "points_awarded": discovery.points_awarded,
            "discovered_at": discovery.discovered_at,
            "rarity": discovery.item.rarity
        } for discovery in discoveries]

    def get_discovery_statistics(self, user_id: int) -> dict:
        """Get statistics about user's discoveries"""
        if not self.__user_repository.find_by_id(user_id):
            raise ValidationError("User not found")

        discoveries = UserDiscovery.objects.filter(user_id=user_id)

        # Category breakdown
        category_counts = discoveries.values('item__category').annotate(
            count=Count('id')
        )
        # Rarity breakdown
        rarity_counts = discoveries.values('item__rarity').annotate(
            count=Count('id')
        )
        # Calculate environmental impact
        total_decomposition_time = sum(
            discovery.item.average_decomposition_time
            for discovery in discoveries
        )
        # Recent discoveries
        recent_discoveries = discoveries.filter(
            discovered_at__gte=timezone.now() - timedelta(days=7)
        ).count()

        return {
            "total_discoveries": discoveries.count(),
            "categories": {
                item['item__category']: item['count']
                for item in category_counts
            },
            "rarities": {
                item['item__rarity']: item['count']
                for item in rarity_counts
            },
            "total_decomposition_years": round(total_decomposition_time / 365, 2),
            "discoveries_last_7_days": recent_discoveries,
            "total_points_from_discoveries": discoveries.aggregate(
                total=Sum('points_awarded')
            )['total'] or 0
        }

    def get_unique_discoveries(self, user_id: int) -> List[str]:
        """Get list of unique items discovered by user"""
        if not self.__user_repository.find_by_id(user_id):
            raise ValidationError("User not found")

        return list(UserDiscovery.objects.filter(user_id=user_id)
                    .values_list('item__name', flat=True))

    def get_undiscovered_items(self, user_id: int) -> List[dict]:
        """Get list of items not yet discovered by user"""
        if not self.__user_repository.find_by_id(user_id):
            raise ValidationError("User not found")

        discovered_items = UserDiscovery.objects.filter(user_id=user_id).values_list('item_id', flat=True)
        undiscovered = Item.objects.exclude(id__in=discovered_items)

        return [{
            "name": item.name,
            "category": item.category,
            "rarity": item.rarity,
            "point_value": item.point_value
        } for item in undiscovered]

    @staticmethod
    def get_popular_discoveries() -> List[dict]:
        """Get most commonly discovered items across all users"""
        popular_items = UserDiscovery.objects.values(
            'item__name',
            'item__category'
        ).annotate(
            discovery_count=Count('id')
        ).order_by('-discovery_count')[:10]

        return [{
            "item_name": item['item__name'],
            "category": item['item__category'],
            "times_discovered": item['discovery_count']
        } for item in popular_items]
