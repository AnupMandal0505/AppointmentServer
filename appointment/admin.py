# admin.py
from django.contrib import admin
from .models import Appointment, Participant
from django.utils.translation import gettext_lazy as _  # For translatable fieldset titles

# class AppointmentAdmin(admin.ModelAdmin):
#     # Customizing the layout of the appointment form in the admin panel
#     fieldsets = (
#         (None, {
#             'fields': ('name', 'email', 'phone', 'date', 'time', 'description', 'status')
#         }),
#         (_('Assigned Information'), {
#             'fields': ('assigned_to',),
#             'classes': ('collapse',),  # Collapsible section for better UI
#         }),
#         (_('Tracking Information'), {
#             'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
#             'classes': ('collapse',),  # Collapsible section for better UI
#         }),
#     )
#     list_display = ('name', 'date', 'time', 'status', 'assigned_to', 'created_by', 'updated_by')  # Columns to display in the list view
#     list_filter = ('status', 'assigned_to', 'created_by')  # Filter options
#     search_fields = ('name', 'email', 'phone', 'description')  # Searchable fields
#     readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')  # Readonly fields for tracking

#     def save_model(self, request, obj, form, change):
#         # Automatically set the user who created or updated the appointment
#         if not obj.created_by:
#             obj.created_by = request.user
#         obj.updated_by = request.user
#         super().save_model(request, obj, form, change)

# # Register the Appointment model with the custom admin
# admin.site.register(Appointment, AppointmentAdmin)



# class ParticipantAdmin(admin.ModelAdmin):
#     # Customizing the layout of the participant form in the admin panel
#     fieldsets = (
#         (None, {
#             'fields': ('name', 'email')
#         }),
#         (_('Appointment Information'), {
#             'fields': ('appointments',),
#             'classes': ('collapse',),  # Collapsible section for better UI
#         }),
#     )
#     list_display = ('name', 'email', 'appointments_count')  # Display name, email, and number of appointments linked to this participant
#     search_fields = ('name', 'email')  # Searchable fields

#     def appointments_count(self, obj):
#         return obj.appointments.count()
#     appointments_count.short_description = _('Appointments Count')

# # Register the Participant model with the custom admin
# admin.site.register(Participant, ParticipantAdmin)


class ItemInline(admin.TabularInline):  # Use StackedInline for a vertical layout
    model = Participant
    extra = 1  # Number of empty forms displayed by default
    can_delete = True  # Allow deleting items
    show_change_link = True  # Optional: Add "Edit" links for related items

@admin.register(Appointment)
class ShoppingListAdmin(admin.ModelAdmin):
    inlines = [ItemInline]
    list_display = ('client',"id")