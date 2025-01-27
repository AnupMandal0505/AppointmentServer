from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from appointment.models import Appointment
from appointment.Serializers import AppointmentSerializer

import logging

logger = logging.getLogger(__name__)

@receiver([post_save, post_delete], sender=Appointment)
def appointment_update_handler(sender, instance=None, created=False, **kwargs):
    """
    Signal handler to send WebSocket updates when appointments change
    """
    try:
        data=Appointment.objects.all()
        serial=AppointmentSerializer.AppointmentSerializer(data, many=True)
        
        # Get channel layer
        channel_layer = get_channel_layer()
        
        # Send update to all clients
        async_to_sync(channel_layer.group_send)(
            "appointments",
            {
                "type": "appointment_update",
                "data": serial.data
            }
        )
        
        action = "created" if created else "updated"
        logger.info(f"Appointment {action}: {instance.name}")
    except Exception as e:
        logger.error(f"Error in appointment_update_handler: {str(e)}") 