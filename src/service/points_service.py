from src.models.user import User
from src.models.items import Item
from django.core.exceptions import ValidationError
from src.models.user_discoveries import UserDiscovery
from src.repository.user_repository import UserRepository


class PointsService:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def award_points_for_discovery(self, user_id: int, item: Item) -> tuple[int, int]:
        """
        Award points to user for discovering an item
        Returns tuple of (points_awarded, new_total_points)

        Applies multipliers based on:
        - Item rarity
        - Item threat level
        """
        user = self.__user_repository.find_by_id(user_id)
        if not user:
            raise ValidationError("User not found")

        # Check if user already discovered this item
        if UserDiscovery.objects.filter(user_id=user_id, item_id=item.id).exists():
            raise ValidationError("Item already discovered by user")

        # Calculate points based on item properties
        points = self.__calculate_points_for_item(item)

        # Update user's points
        new_balance = user.points_balance + points
        new_total = user.total_points_earned + points

        updated_user = self.__user_repository.update_points(
            user_id=user_id,
            points_balance=new_balance,
            total_points=new_total
        )

        # Update user's rank if needed
        self.__check_and_update_rank(updated_user)

        # Record the discovery
        UserDiscovery.objects.create(
            user_id=user_id,
            item_id=item.id,
            points_awarded=points
        )

        return points, new_total

    def deduct_points(self, user_id: int, points: int) -> tuple[int, str]:
        """
        Deduct points from user's balance (not total earned)
        Returns tuple of (new_balance, status_message)
        """
        user = self.__user_repository.find_by_id(user_id)
        if not user:
            raise ValidationError("User not found")

        if points < 0:
            raise ValidationError("Points to deduct must be positive")

        if user.points_balance < points:
            raise ValidationError("Insufficient points balance")

        new_balance = user.points_balance - points
        self.__user_repository.update_points(
            user_id=user_id,
            points_balance=new_balance,
            total_points=user.total_points_earned  # Total earned doesn't change
        )

        return new_balance, "Points deducted successfully"

    def get_points_summary(self, user_id: int) -> dict:
        """Get summary of user's points and rank"""
        user = self.__user_repository.find_by_id(user_id)
        if not user:
            raise ValidationError("User not found")

        rank_position = self.__user_repository.get_user_rank_position(user_id)
        next_rank_info = self.__get_next_rank_info(user)

        return {
            "current_balance": user.points_balance,
            "total_earned": user.total_points_earned,
            "current_rank": user.rank,
            "rank_title": user.rank_title,
            "leaderboard_position": rank_position,
            "next_rank": next_rank_info["next_rank"],
            "points_to_next_rank": next_rank_info["points_needed"],
            "discoveries_count": UserDiscovery.objects.filter(user_id=user_id).count()
        }

    @staticmethod
    def __calculate_points_for_item(item: Item) -> int:
        """Calculate points for discovering an item based on its properties"""
        # Base points from item's point_value
        points = item.point_value

        # Multiply based on rarity
        rarity_multipliers = {
            'COMMON': 1,
            'UNCOMMON': 1.5,
            'RARE': 2,
            'EPIC': 3
        }
        points *= rarity_multipliers[item.rarity]
        # Add bonus for threat level (more threatening items = more points)
        points += (item.threat_level - 1) * 10

        return int(points)  # Round down to nearest integer

    def __check_and_update_rank(self, user: User) -> None:
        """Check and update user's rank based on total points"""
        old_rank = user.rank

        # Calculate new rank
        if user.total_points_earned >= 1000:
            new_rank = 3  # Ocean Protector
        elif user.total_points_earned >= 500:
            new_rank = 2  # Guardian
        elif user.total_points_earned >= 100:
            new_rank = 1  # Explorer
        else:
            new_rank = 0  # Beginner

        # Update if rank changed
        if new_rank != old_rank:
            self.__user_repository.update_rank(user.id, new_rank)

    @staticmethod
    def __get_next_rank_info(user: User) -> dict:
        """Get information about the next rank"""
        rank_thresholds = {
            0: {'next': 1, 'points': 100},   # Beginner -> Explorer
            1: {'next': 2, 'points': 500},   # Explorer -> Guardian
            2: {'next': 3, 'points': 1000},  # Guardian -> Ocean Protector
            3: {'next': 3, 'points': None}   # Ocean Protector (max rank)
        }

        current_rank_info = rank_thresholds[user.rank]
        points_needed = None

        if current_rank_info['points']:
            points_needed = current_rank_info['points'] - user.total_points_earned

        return {
            "next_rank": current_rank_info['next'],
            "points_needed": points_needed
        }
