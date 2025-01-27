from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^appointments/$', consumers.AppointmentConsumer.as_asgi()),
]