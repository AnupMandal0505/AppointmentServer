from rest_framework.serializers import ModelSerializer
from user.models import User
from webshocket.models import CallNotification, Snacks, SnacksItem,Order
from rest_framework import serializers
from appointment.models import Appointment
class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['unique_id', 'first_name','last_name','role']



class CallNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallNotification
        fields = '__all__'



class SnacksItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnacksItem
        fields = ["id", "name", "image"]

class SnacksSerializer(serializers.ModelSerializer):
    items = SnacksItemSerializer(many=True, source="SnacksItem")  # Using related_name

    class Meta:
        model = Snacks
        fields = ["id", "name", "items"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "items", "status", "created_by", "updated_by", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]  # Auto-generated fields

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
