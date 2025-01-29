from rest_framework.serializers import ModelSerializer
from user.models import User
from webshocket.models import CallNotification, Snacks, SnacksItem
from rest_framework import serializers

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
