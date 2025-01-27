from django.contrib import admin
from django.urls import path, include, re_path
from user import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index),
    path('api/', include('appointment.urls')),
    path('api/', include('user.urls')),
    re_path(r'^ws/', include('webshocket.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)