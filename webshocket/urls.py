
from django.urls import path,include
from webshocket.views import CallNotifications,AcceptCall,ContactList,SnacksViewSet
from rest_framework.routers import SimpleRouter

webshocket = SimpleRouter()
webshocket.register(r'call', CallNotifications, basename='call')
webshocket.register(r'contact_list',ContactList , basename='contact_list')
webshocket.register(r'accept_call',AcceptCall , basename='accept_call')
webshocket.register(r"snacks", SnacksViewSet, basename="snacks")
# webshocket.register(r"snacks-items", SnacksItemViewSet, basename="snacks-items")

urlpatterns = webshocket.urls
