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
        try:
            # Join the appointments group
            await self.channel_layer.group_add("appointments", self.channel_name)
            await self.accept()
            
            # Send initial data
            try:
                initial_data = await self.get_initial_data()
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

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard("appointments", self.channel_name)
            logger.info(f"WebSocket disconnected with code: {close_code}")
        except Exception as e:
            logger.error(f"Error in disconnect: {str(e)}")

    async def appointment_update(self, event):
        """
        Handle appointment updates and send to WebSocket
        """
        try:
            upinitial_data = await self.get_update_data()
            await self.send(text_data=json.dumps({
                'type': 'appointment_update',
                'data': upinitial_data
            }))
            logger.info("Update sent to client")
        except Exception as e:
            logger.error(f"Error sending update: {str(e)}")

    @database_sync_to_async
    def get_initial_data(self):
        """
        Get all appointments for initial data load
        """
        try:
            data = Appointment.objects.all()
            serializer = AppointmentSerializer(data, many=True)
            return serializer.data
        except Exception as e:
            logger.error(f"Error in get_initial_data: {str(e)}")
            raise


    @database_sync_to_async
    def get_update_data(self):
        """
        Get all appointments for initial data load
        """
        try:
            data = Appointment.objects.all()
            serializer = AppointmentSerializer(data, many=True)
            return serializer.data
        except Exception as e:
            logger.error(f"Error in get_initial_data: {str(e)}")
            raise