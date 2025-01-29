from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

ROLE_CHOICES = (
        ('gm', 'GM'),
        ('pa', 'PA'),
    )
class User(AbstractUser):
    # Add other custom fields if needed
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='pa'
    )
    gm = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='team_members',limit_choices_to={'role': 'gm'})
    unique_id=models.UUIDField(unique=True, default=uuid.uuid4, editable=False)


    

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
