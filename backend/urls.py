# src/urls.py
from django.contrib import admin
from django.urls import path, include
from authuser.views import index
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index, name='index'),
    path('api/', include('authuser.urls')),
    path('api/', include('appointment.urls')),
    path('realtime', include('demo.urls')),
]