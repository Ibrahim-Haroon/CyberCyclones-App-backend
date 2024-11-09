from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator


class Skin(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.BinaryField()  # for storing image data
    thumbnail = models.BinaryField()  # for storing thumbnail data
    price_points = models.IntegerField(validators=[MinValueValidator(0)])
    rarity = models.CharField(
        max_length=20,
        choices=[
            ('COMMON', 'Common'),
            ('RARE', 'Rare'),
            ('EPIC', 'Epic'),
            ('LEGENDARY', 'Legendary')
        ]
    )
    release_date = models.DateTimeField(default=timezone.now)
    available = models.BooleanField(default=True)
    description = models.TextField()

    objects = models.Manager()

    class Meta:
        db_table = 'skins'
        indexes = [
            models.Index(fields=['rarity']),
            models.Index(fields=['price_points']),
        ]

    def __str__(self):
        return f"{self.name} ({self.rarity})"
