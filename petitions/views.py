from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .services import filter_petitions_for_provider
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from .models import Petition, PetitionCategory, PetitionAttachment, PetitionMaterial
from .serializers import PetitionSerializer

from authentication.models import Provider


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
            petition = serializer.save(id_customer=request.user.customer.id_customer)

            # Crear categorías
            for cat in request.data.get("categories", []):
                # cat puede ser un dict o un string con id_category
                id_category = cat
                if isinstance(cat, dict):
                    id_category = cat.get("id_category")
                PetitionCategory.objects.create(
                    id_petition=petition,
                    id_category_id=id_category
                )

            # Crear adjuntos
            for att in request.FILES.getlist("attachments"):
                PetitionAttachment.objects.create(
                    id_petition=petition,
                    file=att,
                    #type=None,  # si tenés un campo type, enviarlo como input adicional
                    id_user_create=request.user.pk
                )

            # Crear materiales si vienen en JSON
            for mat in request.data.get("materials", []):
                PetitionMaterial.objects.create(
                    id_petition=petition,
                    id_article=mat.get("id_article"),
                    quantity=mat.get("quantity"),
                    unit_price=mat.get("unit_price"),
                    id_user_create=request.user.id
                )

            return Response(PetitionSerializer(petition).data, status=status.HTTP_201_CREATED)
        print('errores del serializador ', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, pk):
        petition = get_object_or_404(Petition, pk=pk)
        serializer = PetitionSerializer(petition, data=request.data, partial=True)
        if serializer.is_valid():
            petition = serializer.save()

            # Actualizar categorías
            if "categories" in request.data:
                PetitionCategory.objects.filter(id_petition=petition).delete()
                categories_list = request.data.get("categories", [])
                for cat in categories_list:
                    id_category = cat.get("id_category") if isinstance(cat, dict) else cat
                    PetitionCategory.objects.create(
                        id_petition=petition,
                        id_category_id=id_category
                    )

            # Actualizar adjuntos
            if "attachments" in request.FILES:
                PetitionAttachment.objects.filter(id_petition=petition).delete()
                for att in request.FILES.getlist("attachments"):
                    PetitionAttachment.objects.create(
                        id_petition=petition,
                        file=att,
                        id_user_create=request.user.pk
                    )

            # Actualizar materiales
            if "materials" in request.data:
                PetitionMaterial.objects.filter(id_petition=petition).delete()
                materials_list = request.data.get("materials", [])
                for mat in materials_list:
                    PetitionMaterial.objects.create(
                        id_petition=petition,
                        id_article=mat.get("id_article"),
                        quantity=mat.get("quantity"),
                        unit_price=mat.get("unit_price"),
                        id_user_create=request.user.pk
                    )

            return Response(PetitionSerializer(petition).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProviderPetitionsFeedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        
        try:
            provider = Provider.objects.filter(user=request.user).first()

        except Provider.DoesNotExist:
            return Response({'detail':'El usuario no es un proveedor'}, status=status.HTTP_403_FORBIDDEN)

        petitions = filter_petitions_for_provider(provider)
        serializer = PetitionSerializer(petitions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)