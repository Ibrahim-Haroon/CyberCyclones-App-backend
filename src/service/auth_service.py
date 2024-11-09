import jwt
from src.models.user import User
from django.conf import settings
from typing import Optional, Tuple
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from src.repository.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository
        self.__jwt_secret = settings.SECRET_KEY
        self.__token_expiry = timedelta(days=1)  # 24 hour tokens

    def login(self, username: str, password: str) -> Tuple[User, str]:
        """
        Authenticate user and return user object with JWT token
        Returns tuple of (user, token)
        """
        # Verify credentials
        if not self.__user_repository.verify_password(username, password):
            raise ValidationError("Invalid credentials")

        # Get user
        user = self.__user_repository.find_by_username(username)
        if not user.is_active:
            raise ValidationError("Account is deactivated")

        # Update last login
        self.__user_repository.update_last_login(user.id)
        # Generate token
        token = self.__generate_token(user)

        return user, token

    def verify_token(self, token: str) -> Optional[User]:
        """Verify JWT token and return associated user"""
        try:
            payload = jwt.decode(token, self.__jwt_secret, algorithms=["HS256"])

            # Check token expiry
            exp = datetime.fromtimestamp(payload['exp'])
            if datetime.now() > exp:
                return None

            # Get and verify user
            user = self.__user_repository.find_by_id(payload['user_id'])
            if not user or not user.is_active:
                return None

            return user

        except jwt.InvalidTokenError:
            return None

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
        # Generate token
        token = self.__generate_token(user)

        return user, token

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

    def generate_password_reset_token(self, email: str) -> Optional[str]:
        """Generate password reset token"""
        user = self.__user_repository.find_by_email(email)
        if not user:
            return None  # Don't reveal if email exists

        # Generate short-lived token (2 hours)
        payload = {
            'user_id': user.id,
            'purpose': 'password_reset',
            'exp': datetime.now() + timedelta(hours=2)
        }
        return jwt.encode(payload, self.__jwt_secret, algorithm="HS256")

    def reset_password(self, token: str, new_password: str) -> bool:
        """Reset password using reset token"""
        try:
            payload = jwt.decode(token, self.__jwt_secret, algorithms=["HS256"])

            # Verify it's a password reset token
            if payload.get('purpose') != 'password_reset':
                raise ValidationError("Invalid reset token")

            # Check expiry
            exp = datetime.fromtimestamp(payload['exp'])
            if datetime.now() > exp:
                raise ValidationError("Reset token has expired")

            # Validate new password
            self.__validate_password_strength(new_password)

            # Update password
            self.__user_repository.update_password(payload['user_id'], new_password)
            return True

        except jwt.InvalidTokenError:
            raise ValidationError("Invalid reset token")

    def __generate_token(self, user: User) -> str:
        """Generate JWT token for user"""
        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.now() + self.__token_expiry
        }
        return jwt.encode(payload, self.__jwt_secret, algorithm="HS256")

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