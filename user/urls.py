
from django.urls import path,include
from user.views import *
# from .views import AppointmentCreateAPIView,AppointmentDetailAPIView

urlpatterns = [
    path('login/',LoginAPI.as_view(), name='user-login'),
    # path('appointments-create/', AppointmentCreateAPIView.as_view(), name='create_appointment'),  # Create appointment

]