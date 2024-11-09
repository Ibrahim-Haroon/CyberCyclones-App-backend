from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    environmental_impact_description = models.TextField()
    point_value = models.IntegerField(validators=[MinValueValidator(0)])
    category = models.CharField(
        max_length=20,
        choices=[
            ('PLASTIC', 'Plastic'),
            ('METAL', 'Metal'),
            ('GLASS', 'Glass'),
            ('OTHER', 'Other')
        ]
    )
    average_decomposition_time = models.IntegerField(  # in days
        validators=[MinValueValidator(0)]
    )
    rarity = models.CharField(
        max_length=20,
        choices=[
            ('COMMON', 'Common'),
            ('UNCOMMON', 'Uncommon'),
            ('RARE', 'Rare'),
            ('EPIC', 'Epic')
        ],
        default='COMMON'
    )
    threat_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        db_table = 'items'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['rarity']),
        ]

    def __str__(self):
        return f"{self.name} ({self.category})"
    