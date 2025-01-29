from django.db import models
from user.models import User
import uuid
# class Message(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
#     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
#     message = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.sender.username} to {self.receiver.username}'

# class ChatRoom(models.Model):
#     participants = models.ManyToManyField(User)
#     last_message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)

#     def __str__(self):
#         return f'Chat Room {self.id}'

class CallNotification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_notifications')
    # message = models.ForeignKey(Message, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    call_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return f'{self.sender.username} to {self.receiver.username}'
    


class Snacks(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class SnacksItem(models.Model):
    category = models.ForeignKey(Snacks, on_delete=models.CASCADE, related_name="SnacksItem")
    name = models.CharField(max_length=200)
    image = models.FileField(upload_to='Snacks/' ,blank=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Order(models.Model):
    items = models.JSONField()  # Store ordered items in JSON format
    status = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="order_created_by",limit_choices_to={'role': 'pa'})  # User who created the appointment
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="order_updated_by")  # User who last updated the appointment
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updated on save
    def __str__(self):
        return f"Order {self.id} - {self.created_at}"
