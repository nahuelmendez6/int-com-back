from .models import Availability
from .serializers import AvailabilitySerializer

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

class AvaialabilityAPIView(APIView):

    """
    APIView para crud de disponibilidades
    """
    
    def post(self, request):
        """
        Crea una disponibilidad
        """
        serializer = AvailabilitySerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            availability = serializer.save(id_user_create=request.user.id_user)
            #  devolvemos los datos serializados en JSON
            output_serializer = AvailabilitySerializer(availability)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

    def get(self, request, id_provider):
        """
        Devuelve la disponibilidad del provider(id_provider)
        """
        availabilitites = Availability.objects.filter(id_provider=id_provider)
        serializer = AvailabilitySerializer(availabilitites, many=True, context={'request': request})

        
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


    def patch(self, request, pk=None):
        """
        actualiza disponibilidades
        """
        availability = get_object_or_404(Availability, pk=pk)
        
        serializer = AvailabilitySerializer(availability, data=request.data, partial=True, context={'request': request})


        if serializer.is_valid():
            availability = serializer.save(id_user_update=request.user.id_user)
            return Response(AvailabilitySerializer(availability).data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk=None):
        """
        Eliminar una disponibilidad
        """
        availability = get_object_or_404(Availability, pk=pk)
        availability.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)