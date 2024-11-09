from typing import Optional
from src.models.user import User
from django.core.exceptions import ValidationError
from src.repository.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.__user_repository.find_by_id(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.__user_repository.find_by_username(username)

    def create_user(self, username: str, email: str, password: str, display_name: str = None) -> User:
        """
        Create a new user with validation
        """
        # Validate username and email are unique
        if self.__user_repository.find_by_username(username):
            raise ValidationError("Username already exists")

        if self.__user_repository.find_by_email(email):
            raise ValidationError("Email already exists")

        # Validate password strength
        self.__validate_password(password)

        # Create user with optional display name
        extra_fields = {}
        if display_name:
            extra_fields['display_name'] = display_name

        return self.__user_repository.create(
            username=username,
            email=email,
            password=password,
            **extra_fields
        )

    def update_display_name(self, user_id: int, new_display_name: str) -> User:
        """Update user's display name"""
        if not new_display_name or len(new_display_name.strip()) == 0:
            raise ValidationError("Display name cannot be empty")

        return self.__user_repository.update_display_name(user_id, new_display_name.strip())

    def get_profile(self, user_id: int) -> dict:
        """Get user's complete profile information"""
        user = self.__user_repository.find_by_id(user_id)
        if not user:
            raise ValidationError("User not found")

        rank_position = self.__user_repository.get_user_rank_position(user_id)

        return {
            "username": user.username,
            "display_name": user.display_name,
            "rank": user.rank,
            "rank_title": user.rank_title,
            "points_balance": user.points_balance,
            "total_points_earned": user.total_points_earned,
            "leaderboard_position": rank_position,
            "active_skin": user.active_skin.id if user.active_skin else None,
            "member_since": user.created_at,
            "last_login": user.last_login_at
        }

    def deactivate_user(self, user_id: int) -> None:
        """Deactivate a user account"""
        user = self.__user_repository.find_by_id(user_id)
        if not user:
            raise ValidationError("User not found")

        user.is_active = False
        self.__user_repository.update(user)

    def reactivate_user(self, user_id: int) -> None:
        """Reactivate a user account"""
        user = self.__user_repository.find_by_id(user_id)
        if not user:
            raise ValidationError("User not found")

        user.is_active = True
        self.__user_repository.update(user)

    @staticmethod
    def __validate_password(password: str) -> None:
        """Validate password strength"""
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")

        if not any(c.isupper() for c in password):
            raise ValidationError("Password must contain at least one uppercase letter")

        if not any(c.islower() for c in password):
            raise ValidationError("Password must contain at least one lowercase letter")

        if not any(c.isdigit() for c in password):
            raise ValidationError("Password must contain at least one number")
