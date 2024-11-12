import logging
from rest_framework_simplejwt.tokens import RefreshToken
from src.models.user import User
from typing import Tuple
from django.core.exceptions import ValidationError
from src.repository.user_repository import UserRepository


class AuthService:
    logger = logging.getLogger(__name__)

    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def login(self, username: str, password: str) -> Tuple[User, str]:
        """
        Authenticate user and return user object with JWT token
        Returns tuple of (user, token)
        """
        # Verify credentials
        if not self.__user_repository.verify_password(username, password):
            self.logger.info(f"Login failed for user: {username}")
            raise ValidationError("Invalid credentials")

        # Get user
        user = self.__user_repository.find_by_username(username)
        if not user.is_active:
            self.logger.info(f"Login attempt for inactive user: {username}")
            raise ValidationError("Account is deactivated")

        # Update last login
        self.__user_repository.update_last_login(user.id)

        # Generate token using Simple JWT
        refresh = RefreshToken.for_user(user)
        return user, str(refresh.access_token)

    def register(self, username: str, email: str, password: str, display_name: str = None) -> Tuple[User, str]:
        """
        Register new user and return user object with JWT token
        Returns tuple of (user, token)
        """
        # Password strength validation
        self.__validate_password_strength(password)

        # Create user
        user = self.__user_repository.create(
            username=username,
            email=email,
            password=password,
            display_name=display_name
        )

        # Generate token using Simple JWT
        refresh = RefreshToken.for_user(user)
        return user, str(refresh.access_token)  # Using access_token instead of refresh token

    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """Change user's password"""
        user = self.__user_repository.find_by_id(user_id)
        if not user:
            raise ValidationError("User not found")

        # Verify old password
        if not self.__user_repository.verify_password(user.username, old_password):
            raise ValidationError("Current password is incorrect")

        # Validate new password strength
        self.__validate_password_strength(new_password)

        # Update password
        self.__user_repository.update_password(user_id, new_password)
        return True

    def reset_password_request(self, email: str) -> RefreshToken:
        """
        Request a password reset token using Simple JWT
        Returns a refresh token that can be used for password reset
        """
        user = self.__user_repository.find_by_email(email)
        if not user:
            self.logger.info(f"Password reset attempted for non-existent email: {email}")
            raise ValidationError("If this email exists, a reset link will be sent")

        # Generate token with shorter expiry
        token = RefreshToken.for_user(user)
        # You could customize the token payload here if needed
        token['purpose'] = 'password_reset'

        return token

    def reset_password(self, token: str, new_password: str) -> bool:
        """Reset password using reset token"""
        try:
            # Validate token
            refresh = RefreshToken(token)
            user_id = refresh['user_id']

            # Check if it's a password reset token
            if refresh.get('purpose') != 'password_reset':
                raise ValidationError("Invalid reset token")

            # Validate new password
            self.__validate_password_strength(new_password)

            # Update password
            self.__user_repository.update_password(user_id, new_password)
            return True

        except Exception as e:
            self.logger.error(f"Password reset failed: {str(e)}")
            raise ValidationError("Invalid or expired reset token")

    @staticmethod
    def __validate_password_strength(password: str) -> None:
        """Validate password meets strength requirements"""
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")

        if not any(c.isupper() for c in password):
            raise ValidationError("Password must contain at least one uppercase letter")

        if not any(c.islower() for c in password):
            raise ValidationError("Password must contain at least one lowercase letter")

        if not any(c.isdigit() for c in password):
            raise ValidationError("Password must contain at least one number")