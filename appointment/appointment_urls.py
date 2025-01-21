
from django.urls import path
from appointment.views import AppointmentCreateView,AppointmentListView,AppointmentUpdateView

urlpatterns = [
    path('create-appointment/',AppointmentCreateView.as_view(), name='create-appointment'),
    path('get-appointments/',AppointmentListView.as_view(), name='get-appointments'),
    path('update-appointments/',AppointmentUpdateView.as_view(), name='update-appointments'),
   
]
