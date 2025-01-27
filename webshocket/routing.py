from django.urls import re_path
from webshocket.consumers import AppointmentConsumer

websocket_urlpatterns = [
    re_path(r'ws/appointments/$',AppointmentConsumer.as_asgi()),
] 