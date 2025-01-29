from rest_framework.serializers import ModelSerializer
from user.models import User
from webshocket.models import CallNotification
from rest_framework import serializers

class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name','last_name','role']



class CallNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallNotification
        fields = '__all__'