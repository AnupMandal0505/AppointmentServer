from django.contrib import admin
from .models import CallNotification, Snacks, SnacksItem, Order

# @admin.register(Message)
# class MessageAdmin(admin.ModelAdmin):
#     list_display = ('sender', 'receiver', 'message', 'timestamp')
#     search_fields = ('sender__username', 'receiver__username', 'message')
#     list_filter = ('sender', 'receiver')

# @admin.register(ChatRoom)
# class ChatRoomAdmin(admin.ModelAdmin):
#     list_display = ('id', 'get_participants', 'last_message')

#     def get_participants(self, obj):
#         return ', '.join([user.username for user in obj.participants.all()])
#     get_participants.short_description = 'Participants'




# Format CallNotification display
@admin.register(CallNotification)
class CallNotificationAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "timestamp", "read")
    list_filter = ("read", "timestamp")
    search_fields = ("sender__username", "receiver__username")
    ordering = ("-timestamp",)

# Format Snacks category
@admin.register(Snacks)
class SnacksAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

# Format SnacksItem display
@admin.register(SnacksItem)
class SnacksItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "image_preview")
    list_filter = ("category",)
    search_fields = ("name", "category__name")

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50"/>'
        return "No Image"
    image_preview.allow_tags = True
    image_preview.short_description = "Image"

# Format Order display
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_by", "status", "created_at", "updated_at")
    list_filter = ("status", "created_at")
    search_fields = ("created_by__username",)
    ordering = ("-created_at",)
