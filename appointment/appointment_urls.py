
from django.urls import path
from appointment.views import AppointmentCreateView,AppointmentListView,AppointmentUpdateView,DeleteAppointmentView

urlpatterns = [
    path('create-appointments/',AppointmentCreateView.as_view(), name='create-appointment'),
    path('get-appointments/',AppointmentListView.as_view(), name='get-appointments'),
    path('update-appointments/',AppointmentUpdateView.as_view(), name='update-appointments'),
    path('delete-appointments/', DeleteAppointmentView.as_view(), name='delete_appointment'),

]
