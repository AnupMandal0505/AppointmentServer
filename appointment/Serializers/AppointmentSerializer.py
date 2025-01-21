from rest_framework import serializers
from appointment.models import Appointment, Participant

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['name', 'email']

class AppointmentSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer(many=True)  # To handle multiple participants

    class Meta:
        model = Appointment
        fields = ['client', 'email', 'phone', 'date', 'description', 'status', 'assigned_to', 'participant']

    def create(self, validated_data):
        # Extract participants from validated data
        participants_data = validated_data.pop('participant')
        
        # Create the appointment
        appointment = Appointment.objects.create(**validated_data)
        
        # Create participants
        for participant_data in participants_data:
            Participant.objects.create(participants=appointment, **participant_data)
        
        return appointment
