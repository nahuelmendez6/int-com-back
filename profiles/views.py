from rest_framework import viewsets, status, serializers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from locations.models import Address
from locations.serializers import AddressSerializer
from .models import Category, TypeProvider, Profession
from .serializers import (
    CategorySerializer, TypeProviderSerializer, ProfessionSerializer, ProfileSerializer, ProviderProfileSerializer,
    ProviderProfileUpdateSerializer
)


class ProviderProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        provider = request.user.provider
        serializer = ProviderProfileSerializer(provider)
        return Response(serializer.data)


class ProfileDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TypeProviderViewSet(viewsets.ModelViewSet):
    queryset = TypeProvider.objects.all()
    serializer_class = TypeProviderSerializer

class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer



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

class ProviderProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        provider = request.user.provider

        address_data = request.data.get('address')
        print("Received address data:", address_data)
        print("Received address data:", address_data)

        # si se reciben datos de direccion, se crea o actualiza la direccion
        if address_data:
            address_id = address_data.get('id_address', None)
            if address_id:
                # actualizar direccion existente
                try:
                    address = Address.objects.get(id_address=address_id)
                    address_serializer = AddressSerializer(address, data=address_data, partial=True)
                except Address.DoesNotExist:
                    return Response({'address': 'Dirección no encontrada'}, status=status.HTTP_404_NOT_FOUND)

            else:
                # Crear nueva direccion
                address_serializer = AddressSerializer(data=address_data)

            try:
                address_serializer.is_valid(raise_exception=True)
                address_instance = address_serializer.save()
                # Asociar dirección al proveedor si no está asociado o cambió
                if provider.address_id != address_instance.id_address:
                    provider.address_id = address_instance.id_address
                    provider.save()
            except serializers.ValidationError as e:
                print("Address validation errors:", e.detail)
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        # Actualizar el resto del proveedor (excepto dirección)
        provider_serializer = ProviderProfileUpdateSerializer(provider, data=request.data, partial=True)
        if provider_serializer.is_valid():
            provider_serializer.save()
            return Response(provider_serializer.data)
        return Response(provider_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


