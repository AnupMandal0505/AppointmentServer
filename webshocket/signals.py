import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from appointment.models import Appointment
from appointment.Serializers import AppointmentSerializer

logger = logging.getLogger(__name__)

@receiver([post_save, post_delete], sender=Appointment)
def appointment_update_handler(sender, instance=None, created=False, **kwargs):
    """
    Signal handler to send WebSocket updates when appointments change.
    """
    try:
        # Fetch all appointments
        appointments = Appointment.objects.all()
        serialized_data = AppointmentSerializer(appointments, many=True).data

        # Get channel layer
        channel_layer = get_channel_layer()

        # Send update to all clients
        async_to_sync(channel_layer.group_send)(
            "appointments",
            {
                "type": "appointment_update",
                "data": serialized_data  # Send serialized data
            }
        )

        action = "created" if created else "updated"
        logger.info(f"Appointment {action}: {instance.visitor_name}")
    except Exception as e:
        logger.error(f"Error in appointment_update_handler: {str(e)}")
