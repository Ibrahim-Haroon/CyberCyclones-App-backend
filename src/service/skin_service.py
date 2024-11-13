from typing import List
from src.models.skin import Skin
from django.db import transaction
from django.db.models import Count, Sum
from src.models.user_skins import UserSkin
from rest_framework.exceptions import ValidationError
from src.service.points_service import PointsService
from src.repository.user_repository import UserRepository


class SkinService:
    def __init__(self, user_repository: UserRepository, points_service: PointsService):
        self.__user_repository = user_repository
        self.__points_service = points_service

    def purchase_skin(self, user_id: int, skin_id: int) -> dict:
        """
        Purchase a skin for a user
        Returns purchase confirmation with updated points balance
        """
        user = self.__user_repository.find_by_id(user_id)
        if not user:
            raise ValidationError("User not found")

        try:
            skin = Skin.objects.get(id=skin_id)
        except Skin.DoesNotExist:
            raise ValidationError("Skin not found")

        # Validate skin is available for purchase
        if not skin.available:
            raise ValidationError("This skin is not available for purchase")

        # Check if user already owns this skin
        if UserSkin.objects.filter(user_id=user_id, skin_id=skin_id).exists():
            raise ValidationError("You already own this skin")

        # Check if user has enough points
        if user.points_balance < skin.price_points:
            raise ValidationError(
                f"Insufficient points. Need {skin.price_points} points, but you have {user.points_balance}"
            )

        # Process purchase
        with transaction.atomic():
            # Deduct points
            new_balance, _ = self.__points_service.deduct_points(user_id, skin.price_points)
            # Record skin ownership
            UserSkin.objects.create(
                user_id=user_id,
                skin_id=skin_id,
                acquisition_type='PURCHASE'
            )

        return {
            "skin_name": skin.name,
            "points_spent": skin.price_points,
            "new_balance": new_balance,
            "rarity": skin.rarity
        }

    def equip_skin(self, user_id: int, skin_id: int) -> dict:
        """
        Equip a skin for a user
        Returns confirmation with skin details
        """
        # Verify ownership
        if not UserSkin.objects.filter(user_id=user_id, skin_id=skin_id).exists():
            raise ValidationError("You don't own this skin")

        # Update user's active skin
        user = self.__user_repository.update_active_skin(user_id, skin_id)

        skin = Skin.objects.get(id=skin_id)
        return {
            "skin_name": skin.name,
            "rarity": skin.rarity,
            "equipped_at": user.last_login_at  # Using last_login as equip timestamp
        }

    def get_user_skins(self, user_id: int) -> List[dict]:
        """Get all skins owned by user"""
        if not self.__user_repository.find_by_id(user_id):
            raise ValidationError("User not found")

        user_skins = UserSkin.objects.filter(user_id=user_id).select_related('skin')

        return [{
            "skin_id": user_skin.skin.id,
            "name": user_skin.skin.name,
            "rarity": user_skin.skin.rarity,
            "acquired_at": user_skin.acquired_at,
            "acquisition_type": user_skin.acquisition_type,
            "is_equipped": user_skin.skin_id == user_skin.user.active_skin_id
        } for user_skin in user_skins]

    @staticmethod
    def get_available_skins(user_id: int) -> List[dict]:
        """Get all skins available for purchase (not owned by user)"""
        owned_skins = UserSkin.objects.filter(user_id=user_id).values_list('skin_id', flat=True)

        available_skins = Skin.objects.filter(
            available=True
        ).exclude(
            id__in=owned_skins
        )

        return [{
            "skin_id": skin.id,
            "name": skin.name,
            "rarity": skin.rarity,
            "price_points": skin.price_points,
            "description": skin.description
        } for skin in available_skins]

    def award_skin(self, user_id: int, skin_id: int, reason: str = "ACHIEVEMENT") -> dict:
        """
        Award a skin to a user (for achievements or special events)
        Returns confirmation with skin details
        """
        user = self.__user_repository.find_by_id(user_id)
        if not user:
            raise ValidationError("User not found")

        try:
            skin = Skin.objects.get(id=skin_id)
        except Skin.DoesNotExist:
            raise ValidationError("Skin not found")

        # Check if user already owns this skin
        if UserSkin.objects.filter(user_id=user_id, skin_id=skin_id).exists():
            raise ValidationError("User already owns this skin")

        # Record skin ownership
        user_skin = UserSkin.objects.create(
            user_id=user_id,
            skin_id=skin_id,
            acquisition_type=reason
        )

        return {
            "skin_name": skin.name,
            "rarity": skin.rarity,
            "awarded_at": user_skin.acquired_at,
            "reason": reason
        }

    def get_skin_statistics(self, user_id: int) -> dict:
        """Get statistics about user's skin collection"""
        if not self.__user_repository.find_by_id(user_id):
            raise ValidationError("User not found")

        user_skins = UserSkin.objects.filter(user_id=user_id)

        # Count skins by rarity
        rarity_counts = (
            user_skins
            .values('skin__rarity')
            .annotate(count=Count('id'))
        )
        # Count skins by acquisition type
        acquisition_counts = (
            user_skins
            .values('acquisition_type')
            .annotate(count=Count('id'))
        )
        # Calculate total points spent on skins
        total_points_spent = (
            user_skins
            .filter(acquisition_type='PURCHASE')
            .aggregate(total=Sum('skin__price_points'))
        )['total'] or 0

        return {
            "total_skins": user_skins.count(),
            "rarity_breakdown": {
                item['skin__rarity']: item['count']
                for item in rarity_counts
            },
            "acquisition_breakdown": {
                item['acquisition_type']: item['count']
                for item in acquisition_counts
            },
            "total_points_spent": total_points_spent
        }
