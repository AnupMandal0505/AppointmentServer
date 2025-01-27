from django.shortcuts import render
from appointment.models import Appointment
from appointment.Serializers import AppointmentSerializer
from rest_framework.response import Response

# Create your views here.
def ws_appointments(request):
    data=Appointment.objects.all()
    serial=AppointmentSerializer.AppointmentSerializer(data, many=True)
    return Response({'RES': serial.data})