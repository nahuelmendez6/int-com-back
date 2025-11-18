from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .services import filter_petitions_for_provider, get_petition_detail_queryset, get_petition_list_queryset
from .models import (
    Petition,
    PetitionAttachment,
    PetitionCategory,
    PetitionMaterial,
    TypePetition
)
from .serializers import (
    PetitionSerializer,
    PetitionListSerializer,
    TypePetitionSerializer
)
from authentication.models import Provider


# ====================================================
# APIView: TypePetitionAPIView
# ====================================================
class TypePetitionAPIView(APIView):
    """
    APIView para listar todos los tipos de peticiones.
    GET: devuelve todos los registros de TypePetition.
    """
    def get(self, request):
        typePetition = TypePetition.objects.all()
        serializer = TypePetitionSerializer(typePetition, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


# ====================================================
# APIView: PetitionAPIView
# ====================================================
class PetitionAPIView(APIView):
    """
    APIView para CRUD de Peticiones con soporte de relaciones anidadas:
    - Crear/actualizar categorías, adjuntos y materiales
    - Filtrado según perfil del usuario (Proveedor o Cliente)
    - Serializadores dinámicos para vistas de lista y detalle
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Devuelve el serializer apropiado para la acción (lista o detalle)."""
        if self.kwargs.get('pk'):
            return PetitionSerializer
        return PetitionListSerializer

    def get(self, request, pk=None):
        """
        GET:
        - Si es proveedor, devuelve peticiones filtradas según su perfil.
        - Si es cliente, devuelve solo sus peticiones.
        - pk opcional: si se pasa, devuelve un solo objeto (vista de detalle).
        """
        serializer_class = self.get_serializer_class()
        provider = getattr(request.user, 'provider', None)
        customer = getattr(request.user, 'customer', None)

        # Caso: vista de detalle (pk proporcionado)
        if pk:
            qs = get_petition_detail_queryset()
            if provider:
                # Un proveedor solo puede ver detalles de peticiones que le corresponden
                petition = get_object_or_404(filter_petitions_for_provider(provider).distinct(), pk=pk)
            elif customer:
                # Un cliente solo puede ver detalles de sus propias peticiones
                petition = get_object_or_404(qs.filter(id_customer=customer.id_customer), pk=pk)
            else:
                return Response({'detail': 'El usuario no tiene un perfil válido.'}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = serializer_class(petition)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Caso: vista de lista (sin pk)
        else:
            if provider:
                petitions = filter_petitions_for_provider(provider)
            elif customer:
                petitions = get_petition_list_queryset().filter(id_customer=customer.id_customer)
            else:
                return Response({'detail': 'El usuario no tiene un perfil válido.'}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = serializer_class(petitions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        """
        POST: Crear una nueva petición con relaciones anidadas
        - categories: lista de categorías
        - attachments: archivos adjuntos
        - materials: lista de materiales
        """
        serializer = PetitionSerializer(data=request.data)

        if serializer.is_valid():
            petition = serializer.save(
                id_customer=request.user.customer.id_customer,
                id_user_create=request.user.id_user
            )

            # Crear categorías - CORRECCIÓN: usar getlist() para obtener todos los valores
            categories_list = request.data.getlist("categories")  # Cambio aquí
            for cat in categories_list:
                # cat viene como string desde FormData, convertir a int
                id_category = int(cat) if isinstance(cat, str) else cat
                if isinstance(cat, dict):
                    id_category = int(cat.get("id_category")) if cat.get("id_category") else None
                
                if id_category:
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
        """
        PATCH: Actualizar una petición existente y sus relaciones anidadas
        """
        petition = get_object_or_404(Petition, pk=pk)
        serializer = PetitionSerializer(petition, data=request.data, partial=True)
        if serializer.is_valid():
            petition = serializer.save()

            # Actualizar categorías - CORRECCIÓN: usar getlist()
            if "categories" in request.data:
                PetitionCategory.objects.filter(id_petition=petition).delete()
                categories_list = request.data.getlist("categories")  # Cambio aquí
                for cat in categories_list:
                    # Convertir string a int si es necesario
                    if isinstance(cat, str):
                        id_category = int(cat)
                    elif isinstance(cat, dict):
                        id_category = int(cat.get("id_category")) if cat.get("id_category") else None
                    else:
                        id_category = int(cat) if cat else None
                    
                    if id_category:
                        PetitionCategory.objects.create(
                            id_petition=petition,
                            id_category_id=id_category
                        )

        # ... resto del código igual

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

# ====================================================
# APIView: ProviderPetitionsFeedAPIView
# ====================================================
class ProviderPetitionsFeedAPIView(APIView):
    """
    APIView para que un proveedor obtenga el feed de peticiones filtradas
    según su perfil.
    - Solo usuarios autenticados
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        GET: Devuelve todas las peticiones que coinciden con el perfil del proveedor
        """
        try:
            provider = Provider.objects.get(user=request.user)
        except Provider.DoesNotExist:
            return Response({'detail': 'El usuario no es un proveedor'}, status=status.HTTP_403_FORBIDDEN)

        petitions = filter_petitions_for_provider(provider)
        serializer = PetitionListSerializer(petitions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
