import json
import logging
from urllib.parse import parse_qs, unquote
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Appointment

logger = logging.getLogger(__name__)

class AppointmentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Handle WebSocket connection and dynamically apply filters."""
        logger.info("WebSocket connect attempt")

        try:
            # Extract query parameters
            self.query_params = self.parse_query_params()

            # Decode the 'filter' parameter (if provided)
            encoded_filter = self.query_params.get("filter", [None])[0]
            self.filters = self.decode_filter(encoded_filter)

            # Join WebSocket group
            await self.channel_layer.group_add("appointments", self.channel_name)
            await self.accept()

            # Send initial filtered data
            initial_data = await self.get_initial_data()
            await self.send(text_data=json.dumps({
                'type': 'initial_data',
                'data': initial_data
            }))

            logger.info(f"WebSocket connected with filters: {self.filters}")
        except Exception as e:
            logger.error(f"Error in connect: {str(e)}")
            await self.close()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        await self.channel_layer.group_discard("appointments", self.channel_name)
        logger.info(f"WebSocket disconnected with code: {close_code}")

    async def appointment_update(self, event):
        """Send only filtered updates to the client."""
        try:
            filtered_appointments = [
                appointment for appointment in event['data']
                if all(
                    str(appointment.get(key)).lower() == str(value).lower()
                    for key, value in self.filters.items()
                )
            ]

            if filtered_appointments:
                await self.send(text_data=json.dumps({
                    'type': 'appointment_update',
                    'data': filtered_appointments
                }))
                logger.info("Filtered update sent to client")
        except Exception as e:
            logger.error(f"Error sending update: {str(e)}")

    @database_sync_to_async
    def get_initial_data(self):
        """Fetch only the appointments matching provided filters."""
        return list(Appointment.objects.filter(**self.filters).values('id', 'name', 'status'))

    def parse_query_params(self):
        """Parse all query parameters from the WebSocket URL."""
        query_string = self.scope.get('query_string', b'').decode()
        return parse_qs(query_string)

    def decode_filter(self, encoded_filter):
        """Decode and parse the filter JSON string."""
        if not encoded_filter:
            return {}

        try:
            decoded_str = unquote(encoded_filter)  # URL Decode
            return json.loads(decoded_str)  # Parse JSON
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Error decoding filter: {str(e)}")
            return {}
