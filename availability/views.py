from .models import Availability
from .serializers import AvailabilitySerializer

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

class AvaialabilityAPIView(APIView):

    """
    APIView para crud de disponibilidades
    """
    
    def post(self, request):
        
        """
        Crea una disponibilidad
        """
        
        serializer = AvailabilitySerializer(data=request.data)

        if serializer.is_valid():
            availability = serializer.save(many=True)
            return Response(
                serializer.validated_data, 
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def get(self, request, id_provider):
        """
        Devuelve la disponibilidad del provider(id_provider)
        """
        availabilitites = Availability.objects.filter(id_provider=id_provider)
        serializer = AvailabilitySerializer(availabilitites, many=True)
        
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


    def get(self, request, pk=None):
        """
        si se pasa pk devuelve una disponibilidad especifica
        sino devuelve todas
        """
        pass