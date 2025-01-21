from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE_CHOICES = (
        ('GM', 'gm'),
        ('PA', 'pa'),
    )
class User(AbstractUser):
    # Add other custom fields if needed
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='PA'
    )

    

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
