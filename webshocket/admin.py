from django.contrib import admin
from .models import Message, ChatRoom, CallNotification

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'message', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'message')
    list_filter = ('sender', 'receiver')

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_participants', 'last_message')

    def get_participants(self, obj):
        return ', '.join([user.username for user in obj.participants.all()])
    get_participants.short_description = 'Participants'

@admin.register(CallNotification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'read')
    search_fields = ('sender__username', 'receiver__username')
    list_filter = ('sender', 'receiver', 'read')