from rest_framework import viewsets, status, serializers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from locations.models import Address
from locations.serializers import AddressSerializer
from .models import Category, TypeProvider, Profession
from .serializers import (
    CategorySerializer, TypeProviderSerializer, ProfessionSerializer, ProfileSerializer, ProviderProfileSerializer,
    ProviderProfileUpdateSerializer, CustomerProfileSerializer
)
import json

from authentication.models import User, Customer, Provider
from authentication.serializers import UserSerializer, ProviderReadSerializer


# profiles/views.py

# ====================================
# API VIEW: PERFIL DEL USUARIO AUTENTICADO
# ====================================
class UserProfileAPIView(APIView):
    """
    Permite obtener o actualizar el perfil del usuario actualmente autenticado.
    Soporta usuarios de tipo provider o customer.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retorna los datos del usuario logueado y su perfil asociado.
        """
        user = request.user
        role = None
        profile_data = None

        if hasattr(user, "provider"):
            role = "provider"
            serializer = ProviderProfileSerializer(user.provider, context={'request': request})
            profile_data = serializer.data
        elif hasattr(user, "customer"):
            role = "customer"
            serializer = CustomerProfileSerializer(user.customer, context={'request': request})
            profile_data = serializer.data
        else:
            return Response({"error": "El usuario no tiene perfil asociado"}, status=400)

        user_serializer = UserSerializer(user, context={'request': request})

        return Response({
            "role": role,
            "user": user_serializer.data,
            "profile": profile_data
        })

    def patch(self, request):
        """
        Permite actualizar el perfil del usuario autenticado.
        - Actualiza imagen de perfil en User.
        - Maneja datos de Provider o Customer, incluyendo dirección anidada.
        """
        user = request.user
        profile_data = request.data.copy()

        # Guardar imagen directamente en user
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
            user.save()

        # Manejo de Provider
        if hasattr(user, "provider"):
            profile = user.provider
            serializer_class = ProviderProfileUpdateSerializer
            # Manejo de address
            address_data_str = request.data.get("address")
            if address_data_str:
                try:
                    address_data = json.loads(address_data_str)
                except json.JSONDecodeError:
                    return Response({'address': 'Formato de dirección inválido'}, status=400)
                if address_data:
                    if profile.address:
                        addr_serializer = AddressSerializer(profile.address, data=address_data, partial=True)
                    else:
                        addr_serializer = AddressSerializer(data=address_data)
                    addr_serializer.is_valid(raise_exception=True)
                    addr_instance = addr_serializer.save()
                    profile.address = addr_instance
                    profile.save()

            # Guardar resto de campos en Provider
            profile_data.pop('address', None)
            profile_data.pop('profile_image', None)  # ya lo guardamos en User
            serializer = serializer_class(profile, data=profile_data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            profile_serializer = ProviderProfileSerializer(profile, context={'request': request})
            user_serializer = UserSerializer(user, context={'request': request})
            return Response({
                "message": "Perfil actualizado correctamente",
                "role": "provider",
                "user": user_serializer.data,
                "profile": profile_serializer.data
            }, status=200)

        # Caso customer
        elif hasattr(user, "customer"):
            # Solo address si aplica
            customer = user.customer
            address_data_str = request.data.get("address")
            if address_data_str:
                try:
                    address_data = json.loads(address_data_str)
                    if address_data:
                        if customer.address:
                            addr_serializer = AddressSerializer(customer.address, data=address_data, partial=True)
                        else:
                            addr_serializer = AddressSerializer(data=address_data)
                        addr_serializer.is_valid(raise_exception=True)
                        addr_instance = addr_serializer.save()
                        customer.address = addr_instance
                        customer.save()
                except json.JSONDecodeError:
                    return Response({'address': 'Formato de dirección inválido'}, status=400)

            customer_serializer = CustomerProfileSerializer(customer, context={'request': request})
            user_serializer = UserSerializer(user, context={'request': request})
            return Response({
                "message": "Perfil actualizado correctamente",
                "role": "customer",
                "user": user_serializer.data,
                "profile": customer_serializer.data
            }, status=200)

        return Response({"error": "No se pudo actualizar el perfil"}, status=400)


# ====================================
# API VIEW: DETALLES DE PERFIL DE UN USUARIO POR ID
# ====================================
class ProfileUserDetailAPIView(APIView):

    """
    Esta vista permite obtener el perfil de un usuario
    a partir de un id_customer o un id_provider.
    Ejemplo:
    GET /api/profile/?id_customer=3
    GET /api/profile/?id_provider=7
    """
    def get(self, request):
        """
        Retorna los datos del usuario logueado y su perfil asociado.
        """
        id_customer = request.query_params.get('id_customer')
        id_provider = request.query_params.get('id_provider')

        if not id_customer and not id_provider:
            return Response(
                {"detail": "Debe enviar id_customer o id_provider."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if id_customer:
            customer = get_object_or_404(Customer, pk=id_customer)
            serializer = UserSerializer(customer.user)
        else:
            provider = get_object_or_404(Provider, pk=id_provider)
            serializer = ProviderReadSerializer(provider) 

        return Response(serializer.data, status=status.HTTP_200_OK)



            


# ====================================
# API VIEW: DETALLES DEL PERFIL DEL USUARIO LOGUEADO
# ====================================
class ProfileDetailAPIView(APIView):
    """
    Retorna información básica del perfil del usuario autenticado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user, context={'request': request})
        return Response(serializer.data)

# ====================================
# VIEWSETS DE CATÁLOGOS
# ====================================
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TypeProviderViewSet(viewsets.ModelViewSet):
    queryset = TypeProvider.objects.all()
    serializer_class = TypeProviderSerializer

class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


# ====================================
# API VIEW: ESTADO DEL PERFIL
# ====================================
class ProfileStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        is_complete = False
        if hasattr(user, 'provider'):
            is_complete = user.provider.is_profile_complete()

        return Response({
            'profile_complete': is_complete
        })



