from typing import List
from src.models.user import User
from datetime import datetime, timedelta
from django.db.models.functions import Rank
from django.core.exceptions import ValidationError
from django.db.models import Count, Sum, Window, F
from src.models.user_discoveries import UserDiscovery
from src.repository.user_repository import UserRepository


class LeaderboardService:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    @staticmethod
    def get_global_leaderboard(limit: int = 10) -> List[dict]:
        """Get global leaderboard based on total points earned"""
        leaderboard = User.objects.filter(
            is_active=True
        ).annotate(
            rank=Window(
                expression=Rank(),
                order_by=F('total_points_earned').desc()
            )
        ).order_by('rank')[:limit]

        return [{
            "rank": entry.rank,
            "username": entry.username,
            "display_name": entry.display_name,
            "total_points": entry.total_points_earned,
            "rank_title": entry.rank_title
        } for entry in leaderboard]

    @staticmethod
    def get_weekly_leaderboard(limit: int = 10) -> List[dict]:
        """Get weekly leaderboard based on points earned in the last 7 days"""
        week_ago = datetime.now() - timedelta(days=7)

        # Get points earned from discoveries in last week
        weekly_points = (
            UserDiscovery.objects.filter(
                discovered_at__gte=week_ago
            ).values(
                'user'
            ).annotate(
                weekly_total=Sum('points_awarded')
            ).order_by('-weekly_total')[:limit]
        )

        # Fetch user details for these users
        users = User.objects.filter(
            id__in=[entry['user'] for entry in weekly_points]
        )
        user_map = {user.id: user for user in users}

        return [{
            "rank": idx + 1,  # 1 based indexing
            "username": user_map[entry['user']].username,
            "display_name": user_map[entry['user']].display_name,
            "weekly_points": entry['weekly_total'],
            "rank_title": user_map[entry['user']].rank_title
        } for idx, entry in enumerate(weekly_points)]

    @staticmethod
    def get_category_leaderboard(category: str, limit: int = 10) -> List[dict]:
        """Get leaderboard for specific item category discoveries"""
        category_discoveries = (
            UserDiscovery.objects.filter(
                item__category=category
            ).values(
                'user'
            ).annotate(
                discoveries=Count('id'),
                points=Sum('points_awarded')
            ).order_by('-points')[:limit]
        )

        users = User.objects.filter(
            id__in=[entry['user'] for entry in category_discoveries]
        )
        user_map = {user.id: user for user in users}

        return [{
            "rank": idx + 1,
            "username": user_map[entry['user']].username,
            "display_name": user_map[entry['user']].display_name,
            "discoveries": entry['discoveries'],
            "points": entry['points'],
            "category": category
        } for idx, entry in enumerate(category_discoveries)]

    def get_user_ranking_details(self, user_id: int) -> dict:
        """Get detailed ranking information for a user"""
        user = self.__user_repository.find_by_id(user_id)
        if not user:
            raise ValidationError("User not found")

        # Get global rank
        global_rank = self.__user_repository.get_user_rank_position(user_id)

        # Get weekly points
        week_ago = datetime.now() - timedelta(days=7)
        weekly_points = UserDiscovery.objects.filter(
            user_id=user_id,
            discovered_at__gte=week_ago
        ).aggregate(total=Sum('points_awarded'))['total'] or 0

        # Get category breakdown
        category_rankings = {}
        for category in ['PLASTIC', 'METAL', 'GLASS', 'OTHER']:
            category_rank = UserDiscovery.objects.filter(
                item__category=category,
                points_awarded__gt=(
                        UserDiscovery.objects.filter(
                            user_id=user_id,
                            item__category=category
                        ).aggregate(total=Sum('points_awarded'))['total'] or 0
                )
            ).values('user').distinct().count() + 1

            category_rankings[category] = category_rank

        return {
            "username": user.username,
            "display_name": user.display_name,
            "global_rank": global_rank,
            "total_points": user.total_points_earned,
            "weekly_points": weekly_points,
            "rank_title": user.rank_title,
            "category_rankings": category_rankings,
            "total_discoveries": UserDiscovery.objects.filter(user_id=user_id).count()
        }

    def get_nearby_rankings(self, user_id: int, range: int = 2) -> List[dict]:
        """Get rankings for users nearby in rank (above and below)"""
        user_rank = self.__user_repository.get_user_rank_position(user_id)

        nearby_users = User.objects.filter(
            is_active=True
        ).annotate(
            rank=Window(
                expression=Rank(),
                order_by=F('total_points_earned').desc()
            )
        ).filter(
            rank__range=(max(1, user_rank - range), user_rank + range)
        ).order_by('rank')

        return [{
            "rank": user.rank,
            "username": user.username,
            "display_name": user.display_name,
            "total_points": user.total_points_earned,
            "is_current_user": user.id == user_id
        } for user in nearby_users]
    