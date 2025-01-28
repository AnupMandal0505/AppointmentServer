import json
import logging
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from appointment.models import Appointment
from appointment.Serializers.AppointmentSerializer import AppointmentSerializer

logger = logging.getLogger(__name__)

class AppointmentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info("WebSocket connect attempt from %s", self.scope["client"])
        
        # Get filter parameters from query string (if any)
        filters = self.scope.get("query_string", b"").decode("utf-8")  # Adjust how you pass filters in your WebSocket connection
        filter_dict = self.parse_filters(filters)

        try:
            # Join the appointments group
            await self.channel_layer.group_add("appointments", self.channel_name)
            await self.accept()
            
            # Send initial data
            try:
                initial_data = await self.get_initial_data(filter_dict)
                await self.send(text_data=json.dumps({
                    'type': 'initial_data',
                    'data': initial_data
                }))
                logger.info("Initial data sent successfully")
            except Exception as e:
                logger.error(f"Error getting initial data: {str(e)}")
                raise
                
            logger.info("WebSocket connection established successfully")
            
        except Exception as e:
            logger.error(f"Error in connect: {str(e)}", exc_info=True)
            raise

    async def appointment_update(self, event):
        """
        Handle appointment updates and send to WebSocket
        """
        try:
            # Get the update data with optional filters
            filters = event.get('filters', {})  # Get filters from the event (if any)
            update_data = await self.get_update_data(filters)
            await self.send(text_data=json.dumps({
                'type': 'appointment_update',
                'data': update_data
            }))
            logger.info("Update sent to client")
        except Exception as e:
            logger.error(f"Error sending update: {str(e)}")

    @database_sync_to_async
    def get_initial_data(self, filters):
        """
        Get all appointments for initial data load with optional filters
        """
        try:
            data = Appointment.objects.filter(**filters)  # Apply filters dynamically
            serializer = AppointmentSerializer(data, many=True)
            return serializer.data
        except Exception as e:
            logger.error(f"Error in get_initial_data: {str(e)}")
            raise

    @database_sync_to_async
    def get_update_data(self, filters):
        """
        Get all appointments for update load with optional filters
        """
        try:
            data = Appointment.objects.filter(**filters)  # Apply filters dynamically
            serializer = AppointmentSerializer(data, many=True)
            return serializer.data
        except Exception as e:
            logger.error(f"Error in get_update_data: {str(e)}")
            raise

    def parse_filters(self, filter_string):
        """
        Parse the query string into a filter dictionary
        """
        filters = {}
        if filter_string:
            # Example: 'date=2025-01-29&status=confirmed'
            for param in filter_string.split("&"):
                key, value = param.split("=")
                filters[key] = value
        return filters
