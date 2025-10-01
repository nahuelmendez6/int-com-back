from .models import Availability
from .serializers import AvailabilitySerializer

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

class AvaialabilityAPIView(APIView):
    
    def post(self, request):
        serializer = AvailabilitySerializer(data=request.data)

        if serializer.is_valid():
            availability = serializer.save(many=True)
            return Response(
                serializer.validated_data, 
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)