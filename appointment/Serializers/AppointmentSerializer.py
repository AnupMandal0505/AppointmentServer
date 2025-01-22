from rest_framework import serializers
from appointment.models import Appointment, AdditionalVisitor

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalVisitor
        fields = ['name', 'img']

class AppointmentSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer(many=True)  # To handle multiple participants

    class Meta:
        model = Appointment
        fields = ['id','visitor_name','visitor_img', 'email', 'phone', 'date', 'description', 'status', 'assigned_to','company_name','company_adress','purpose_of_visit' ,'participant']

    def create(self, validated_data):
        # Extract participants from validated data
        participants_data = validated_data.pop('participant')
        
        # Create the appointment
        appointment = Appointment.objects.create(**validated_data)
        
        # Create participants
        for participant_data in participants_data:
            AdditionalVisitor.objects.create(participants=appointment, **participant_data)
        
        return appointment
