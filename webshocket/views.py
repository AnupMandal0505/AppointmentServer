from django.shortcuts import render
from appointment.models import Appointment
# from appointment.Serializers import AppointmentSerializer
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from user.models import User
from .models import CallNotification


def index(request):
    appointments = Appointment.objects.all()
    return render(request, 'i.html', {'appointments': appointments})


# Create your views here.
# def ws_appointments(request):
#     # data=Appointment.objects.all()
#     # serial=AppointmentSerializer.AppointmentSerializer(data, many=True)
#     # return Response({'RES': serial.data})
#     appointments = Appointment.objects.all()
#     return render(request, 'i.html', {'appointments': appointments})



# Serializer
class CallNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallNotification
        fields = '__all__'

# API View for creating a notification
class CallNotifications(viewsets.ViewSet):
    def create(self,request):
        receiver_id = request.data.get('receiver')
        
        if not receiver_id:
            return Response({'ERR': 'Receiver and message fields are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response({'ERR': 'Receiver not found'}, status=status.HTTP_404_NOT_FOUND)
        
        notification = CallNotification.objects.create(sender=request.user, receiver=receiver)
        serializer = CallNotificationSerializer(notification)
        
        return Response({"RES":serializer.data})
    


class AcceptCall(viewsets.ViewSet):
    def create(self, request):
        if not request.data.get('call_id'):
            return Response({'ERR': 'Call id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            call_notification = CallNotification.objects.get(call_id=request.data.get('call_id'))
            call_notification.read = True
            call_notification.save()
            return Response({'success': 'Call marked as read'}, status=status.HTTP_200_OK)
        except CallNotification.DoesNotExist:
            return Response({'ERR': 'Call not found'}, status=status.HTTP_404_NOT_FOUND)
