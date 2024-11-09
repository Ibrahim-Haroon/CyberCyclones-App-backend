from django.db import models
from django.utils import timezone


class UserSkin(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    skin = models.ForeignKey('Skin', on_delete=models.CASCADE)
    acquired_at = models.DateTimeField(default=timezone.now)
    acquisition_type = models.CharField(
        max_length=20,
        choices=[
            ('PURCHASE', 'Purchase'),
            ('ACHIEVEMENT', 'Achievement'),
            ('SPECIAL_EVENT', 'Special Event')
        ]
    )

    class Meta:
        db_table = 'user_skins'
        indexes = [
            models.Index(fields=['user', 'skin']),
            models.Index(fields=['acquired_at']),
        ]
        # Prevent duplicate skin ownership
        unique_together = ['user', 'skin']

    def __str__(self):
        return f"{self.user.username} owns {self.skin.name}"

    def save(self, *args, **kwargs):
        if not self.pk and self.acquisition_type == 'PURCHASE':
            # Deduct points only for new purchases
            if not self.user.deduct_points(self.skin.price_points):
                raise ValueError("Insufficient points to purchase skin")
        super().save(*args, **kwargs)
