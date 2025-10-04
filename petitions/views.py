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


class TypePetitionAPIView(APIView):

    """
    APIView para consumir Typepetition
    """
    def get(self, request):
        typePetition = TypePetition.objects.all()
        serializer = TypePetitionSerializer(typePetition, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class PetitionAPIView(APIView):

    """
    APIView para CRUD de peticiones con escritura anidada y filtro por proveedor
    """

    def get(self, request, pk=None):
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
                    Petition.objects.filter(id_customer=customer.id_customer), pk=pk
                )
                serializer = PetitionSerializer(petition)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            petitions = Petition.objects.filter(id_customer=customer.id_customer)
            serializer = PetitionSerializer(petitions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Caso: no es proveedor ni cliente
        return Response(
            {'detail':'El usuario no tiene un perfil válido.'},
            status=status.HTTP_403_FORBIDDEN
        )
        
    def post(self, request):
        serializer = PetitionSerializer(data=request.data)

        if serializer.is_valid():
            petition = serializer.save()

            # Crear categorias anidadas
            for cat in request.data.get("categories", []):
                PetitionCategory.objects.create(
                    id_petition=petition,
                    id_category_id=cat.get("id_category")
                )

            
            # Crear adjuntos anidados
            for att in request.data.get("attachments", []):
                PetitionAttachment.objects.create(
                    id_petition=petition,
                    url=att.get("url"),
                    type=att.get("type"),
                    id_user_create=att.get("id_user_create")
                )

            # Crear materiales anidados
            for mat in request.data.get("materials", []):
                PetitionMaterial.objects.create(
                    id_petition=petition,
                    id_article=mat.get("id_article"),
                    quantity=mat.get("quantity"),
                    unit_price=mat.get("unit_price"),
                    id_user_create=mat.get("id_user_create")
                )

            return Response(PetitionSerializer(petition).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        petition = get_object_or_404(Petition, pk=pk)
        serializer = PetitionSerializer(petition, data=request.data, partial=True)  # partial=True permite actualizar solo los campos enviados
        if serializer.is_valid():
            petition = serializer.save()

            #  Actualizar categorías
            if "categories" in request.data:
                PetitionCategory.objects.filter(id_petition=petition).delete()
                for cat in request.data.get("categories", []):
                    PetitionCategory.objects.create(
                        id_petition=petition,
                        id_category_id=cat.get("id_category")
                    )

            # Actualizar adjuntos
            if "attachments" in request.data:
                PetitionAttachment.objects.filter(id_petition=petition).delete()
                for att in request.data.get("attachments", []):
                    PetitionAttachment.objects.create(
                        id_petition=petition,
                        url=att.get("url"),
                        type=att.get("type"),
                        id_user_create=att.get("id_user_create")
                    )

            # Actualizar materiales
            if "materials" in request.data:
                PetitionMaterial.objects.filter(id_petition=petition).delete()
                for mat in request.data.get("materials", []):
                    PetitionMaterial.objects.create(
                        id_petition=petition,
                        id_article=mat.get("id_article"),
                        quantity=mat.get("quantity"),
                        unit_price=mat.get("unit_price"),
                        id_user_create=mat.get("id_user_create")
                    )

            return Response(PetitionSerializer(petition).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

