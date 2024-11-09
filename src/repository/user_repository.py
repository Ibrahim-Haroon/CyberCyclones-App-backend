from typing import Optional
from django.db import transaction
from src.models.user import User
from src.models.skin import Skin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password, make_password


class UserRepository:
    @staticmethod
    def find_by_id(user_id: int) -> Optional[User]:
        try:
            return User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_by_username(username: str) -> Optional[User]:
        try:
            return User.objects.get(username=username)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_by_email(email: str) -> Optional[User]:
        try:
            return User.objects.get(email=email)
        except ObjectDoesNotExist:
            return None

    @transaction.atomic
    def create(self, username: str, email: str, password: str, **extra_fields) -> User:
        user = User(
            username=username,
            email=email,
            password=make_password(password),
            **extra_fields
        )
        user.save()
        return user

    @transaction.atomic
    def update(self, user: User) -> User:
        user.save()
        return user

    @transaction.atomic
    def delete(self, user_id: int) -> bool:
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def verify_password(username: str, password: str) -> bool:
        try:
            user = User.objects.get(username=username)
            return check_password(password, user.password)
        except ObjectDoesNotExist:
            return False

    @transaction.atomic
    def update_password(self, user_id: int, hashed_password: str) -> None:
        User.objects.filter(id=user_id).update(
            password=make_password(hashed_password)
        )

    @transaction.atomic
    def update_last_login(self, user_id: int) -> None:
        from django.utils import timezone
        User.objects.filter(id=user_id).update(
            last_login_at=timezone.now()
        )

    @staticmethod
    def find_active_users() -> list[User]:
        return list(User.objects.filter(is_active=True))

    @transaction.atomic
    def update_display_name(self, user_id: int, display_name: str) -> User:
        user = User.objects.get(id=user_id)
        user.display_name = display_name
        user.save()
        return user

    @transaction.atomic
    def update_active_skin(self, user_id: int, skin_id: int) -> User:
        try:
            user = User.objects.get(id=user_id)
            skin = Skin.objects.get(id=skin_id)

            # Verify user owns this skin
            if not user.userskin_set.filter(skin_id=skin_id).exists():
                raise ValueError("User does not own this skin")

            user.active_skin = skin
            user.save()
            return user
        except ObjectDoesNotExist:
            raise ValueError("User or skin not found")

    @transaction.atomic
    def update_points(self, user_id: int, points_balance: int, total_points: int) -> User:
        user = User.objects.get(id=user_id)
        user.points_balance = points_balance
        user.total_points_earned = total_points
        user.save()
        return user

    @transaction.atomic
    def update_rank(self, user_id: int, new_rank: int) -> User:
        user = User.objects.get(id=user_id)
        user.rank = new_rank
        user.save()
        return user

    @staticmethod
    def get_user_rank_position(user_id: int) -> int:
        try:
            # Get user's total points
            user = User.objects.get(id=user_id)

            # Count how many users have more points
            higher_ranked_count = User.objects.filter(
                total_points_earned__gt=user.total_points_earned
            ).count()

            # Add 1 to convert to 1-based ranking
            return higher_ranked_count + 1

        except ObjectDoesNotExist:
            raise ValueError("User not found")
