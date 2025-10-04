from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .services import filter_petitions_for_provider

from .models import (Petition,
                      PetitionAttachment,
                      PetitionCategory,
                      PetitionMaterial,
                      PetitionState,
                      PetitionStateHistory,
                      TypePetition)

from .serializers import (PetitionSerializer,
                          PetitionStateHistorySerializer,
                          TypePetitionSerializer,
                          PetitionStateSerializer,
                          PetitionCategorySerializer,
                          PetitionMaterialSerializer,
                          PetitionAttachmentSerializer)


class PetitionAPIView(APIView):

    """
    APIView para CRUD de peticiones con escritura anidada y filtro por proveedor
    """

    def get(slef, request, pk=None):
        provider = getattr(request.user, 'provider', None)
        customer = getattr(request.user, 'customer', None)

        # Caso: proveedor autenticado
        if provider:
            if pk:
                petition = get_object_or_404(
                    filter_petitions_for_provider(provider), pk=pk
                )
                serializer = PetitionSerializer(petition)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            petitions = filter_petitions_for_provider(provider)
            serializer = PetitionSerializer(petitions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

        # Caso: cliente autenticado
        elif customer:
            if pk:
                petition = get_object_or_404(
                    Petition.objects.filter(id_customer=customer), pk=pk
                )
                serializer = PetitionSerializer(petition)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            petitions = Petition.objects.filter(id_customer=customer)
            serializer = PetitionSerializer(petitions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Caso: no es proveedor ni cliente
        return Response(
            {'detail':'El usuario no tiene un perfil válido.'},
            status=status.HTTP_403_FORBIDDEN
        )
        
