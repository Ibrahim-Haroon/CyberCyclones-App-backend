from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator


class UserDiscovery(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    discovered_at = models.DateTimeField(default=timezone.now)
    points_awarded = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        db_table = 'user_discoveries'
        indexes = [
            models.Index(fields=['user', 'item']),
            models.Index(fields=['discovered_at']),
        ]
        # Prevent user from getting points multiple times from same item
        unique_together = ['user', 'item']

    def __str__(self):
        return f"{self.user.username} discovered {self.item.name}"

    def save(self, *args, **kwargs):
        # If this is a new discovery, award points to user
        if self.pk is None:  # pk is None when object is new
            self.user.add_points(self.points_awarded)
        super().save(*args, **kwargs)
