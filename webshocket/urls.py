
from django.urls import path,include
from webshocket.views import CallNotifications,AcceptCall
from rest_framework.routers import SimpleRouter

webshocket = SimpleRouter()
webshocket.register(r'call', CallNotifications, basename='call')
webshocket.register(r'accept_call',AcceptCall , basename='accept_call')

urlpatterns = webshocket.urls
