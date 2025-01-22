from django.db import models
from user.models import User
import uuid


STATUS_CHOICES = (
        ('PENDING','Pending'),
        ('GOINGON', 'Going On'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED','Completed'),
)
class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateField()
    description = models.TextField(blank=True)
    status = models.CharField(
            max_length=20,
            choices=STATUS_CHOICES,
            default="PENDING",
        )  # Status field (Pending, In Progress, Completed)
    
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_appointments"
    ) 

    # Add creation and update tracking fields
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updated on save
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_appointments")  # User who created the appointment
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_appointments")  # User who last updated the appointment

    def __str__(self):
        return f"{self.client} - {self.date}"
    

class Participant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    participants = models.ForeignKey(Appointment,on_delete=models.CASCADE, related_name="participant",default=None)  # Multiple participants

    def __str__(self):
        return self.email