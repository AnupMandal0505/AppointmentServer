from django.shortcuts import render
from appointment.models import Appointment
# from appointment.Serializers import AppointmentSerializer
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from user.models import User
from .models import CallNotification,Snacks, Order
from webshocket.serializer import ContactListSerializer,CallNotificationSerializer,SnacksSerializer,OrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class BaseAuthentication(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]



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



# API View for creating a notification
class CallNotifications(BaseAuthentication):
    def create(self,request):
        receiver_id = request.data.get('receiver')
        
        if not receiver_id:
            return Response({'ERR': 'Receiver and message fields are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            receiver = User.objects.get(unique_id=receiver_id)
        except User.DoesNotExist:
            return Response({'ERR': 'Receiver not found'}, status=status.HTTP_404_NOT_FOUND)
        
        notification = CallNotification.objects.create(sender=request.user, receiver=receiver)
        serializer = CallNotificationSerializer(notification)
        
        return Response({"RES":True})
    




class ContactList(BaseAuthentication):
    def list(self, request):
        try:
            data=User.objects.filter(gm=request.user)
            serial=ContactListSerializer(data,many=True)
            return Response({'RES':serial.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Failed to log out'}, status=status.HTTP_400_BAD_REQUEST)
        

class AcceptCall(BaseAuthentication):
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


# Snacks ViewSet
class SnacksViewSet(viewsets.ReadOnlyModelViewSet):  # Only GET methods allowed
    queryset = Snacks.objects.all()
    serializer_class = SnacksSerializer

# SnacksItem ViewSet
# class SnacksItemViewSet(viewsets.ReadOnlyModelViewSet):  # Only GET methods allowed
#     queryset = SnacksItem.objects.all()
#     serializer_class = SnacksItemSerializer


class Order(BaseAuthentication):
    def create(self,request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            # Assign the logged-in user as created_by and updated_by
            serializer.save(created_by=request.user, updated_by=request.user)
            return Response({"RES": True, "message": "Order created successfully"}, status=status.HTTP_201_CREATED)
        return Response({"RES": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
