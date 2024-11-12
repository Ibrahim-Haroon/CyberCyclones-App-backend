from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password, is_password_usable


class UserManager(BaseUserManager):
    def create_user(self, username: str, email: str, password: str, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        if not email:
            raise ValueError('Email is required')
        if not password:
            raise ValueError('Password is required')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    points_balance = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_points_earned = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(default=timezone.now)
    last_login_at = models.DateTimeField(null=True)
    display_name = models.CharField(max_length=50, null=True)
    active_skin = models.ForeignKey('Skin', null=True, on_delete=models.SET_NULL)
    rank = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'  # field to use for auth
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        # Hash password if it's not already hashed (is_password_usable returns False for hashed passwords)
        if self.password is not None and not is_password_usable(self.password):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['-total_points_earned']),  # For leaderboard queries (negative sign for desc)
        ]

    @property
    def rank_title(self):
        ranks = {
            0: "Beginner",
            1: "Explorer", 
            2: "Guardian",
            3: "Ocean Protector"
        }
        return ranks.get(self.rank, "Unknown")

    def update_rank(self):
        if self.total_points_earned >= 1000:
            self.rank = 3
        elif self.total_points_earned >= 500:
            self.rank = 2
        elif self.total_points_earned >= 100:
            self.rank = 1
        else:
            self.rank = 0

    def add_points(self, points: int):
        self.points_balance += points
        self.total_points_earned += points
        self.update_rank()
        self.save()

    def deduct_points(self, points: int) -> None:
        self.points_balance = max(0, self.points_balance - points)
        self.save()
