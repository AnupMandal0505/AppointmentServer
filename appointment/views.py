from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from appointment.models import Appointment
from appointment.Serializers.AppointmentSerializer import AppointmentSerializer

# http://127.0.0.1:8000/api/appointments/create-appointment/
class AppointmentCreateView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# http://127.0.0.1:8000/api/appointments/get-appointments/?status=PENDING&client=j
class AppointmentListView(APIView):
    def get(self, request, *args, **kwargs):
        # Get all query parameters
        query_params = request.GET.dict()  # Convert QueryDict to a dictionary
        
        # Start with the base queryset
        queryset = Appointment.objects.all()
        
        # Loop through query parameters and apply filters
        for field, value in query_params.items():
            if hasattr(Appointment, field):  # Check if the field exists in the model
                queryset = queryset.filter(**{field: value})
        
        # Serialize the filtered queryset
        serializer = AppointmentSerializer(queryset, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

# http://127.0.0.1:8000/api/appointments/update-appointments/

class AppointmentUpdateView(APIView):
    """
    Update an existing appointment.
    """
    def patch(self, request: object) -> Response:
        pk = request.GET.get("pk")
        if not pk:
            return Response({"error": "Missing 'pk' parameter"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            pk = int(pk)
        except ValueError:
            return Response({"error": "Invalid 'pk' parameter"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class DeleteAppointmentView(APIView):
    """
    Delete an existing appointment.
    """
    def delete(self, request: object) -> Response:
        if not request.GET.get("id"):
            return Response({"error": "Missing 'id' parameter"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            appointment = Appointment.objects.get(id=request.GET.get("visitorId"))
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)
        appointment.delete()
        return Response({"message": "Appointment deleted successfully"}, status=status.HTTP_200_OK)
