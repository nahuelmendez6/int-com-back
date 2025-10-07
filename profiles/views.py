from rest_framework import viewsets, status, serializers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from locations.models import Address
from locations.serializers import AddressSerializer
from .models import Category, TypeProvider, Profession
from .serializers import (
    CategorySerializer, TypeProviderSerializer, ProfessionSerializer, ProfileSerializer, ProviderProfileSerializer,
    ProviderProfileUpdateSerializer, CustomerProfileSerializer
)
import json

from authentication.serializers import UserSerializer

"""
class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        role = None
        profile_data = None

        try:
            provider = user.provider
            serializer = ProviderProfileSerializer(provider, context={'request': request})
            role = "provider"
            profile_data = serializer.data
        except ObjectDoesNotExist:
            try:
                customer = user.customer
                serializer = CustomerProfileSerializer(customer, context={'request': request})
                role = "customer"
                profile_data = serializer.data
            except ObjectDoesNotExist:
                return Response({"error": "El usuario no tiene perfil asociado"}, status=400)

        user_serializer = UserSerializer(user, context={'request': request})

        return Response({
            "role": role,
            "user": user_serializer.data,
            "profile": profile_data
        })


    def patch(self, request):

        user = request.user
        profile_data = request.data.copy()
        
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
            user.save()

        # Determinar perfil
        try:
            if hasattr(user, "provider"):
                profile = user.provider
                serializer_class = ProviderProfileUpdateSerializer
                role = "provider"
            elif hasattr(user, "customer"):
                profile = user.customer
                serializer_class = None  # para customer no hay serializer de update
                role = "customer"
            else:
                return Response({"error": "El usuario no tiene perfil asociado"}, status=400)
        except ObjectDoesNotExist:
            return Response({"error": "El perfil no existe en BD"}, status=404)

        # Manejo de dirección
        #address_data = request.data.get("address")
        address_data_str = request.data.get("address")
        address_data = None
        if address_data_str:
            try:
                address_data = json.loads(address_data_str)
            except json.JSONDecodeError:
                return Response({'address': 'Formato de dirección inválido'}, status=status.HTTP_400_BAD_REQUEST)
        if address_data:
            address_id = address_data.get("id_address")
            if address_id:
                try:
                    address = Address.objects.get(id_address=address_id)
                    address_serializer = AddressSerializer(address, data=address_data, partial=True)
                except Address.DoesNotExist:
                    return Response({'address': 'Dirección no encontrada'}, status=status.HTTP_404_NOT_FOUND)
            else:
                address_serializer = AddressSerializer(data=address_data)

            try:
                address_serializer.is_valid(raise_exception=True)
                address_instance = address_serializer.save()
                if profile.address_id != address_instance.id_address:
                    profile.address = address_instance
                    profile.save()
            except serializers.ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        # Manejo de otros datos
        profile_data = request.data.copy()
        profile_data.update(request.FILES)  # incluir archivos (foto, etc)
        profile_data.pop("address", None)

        if serializer_class:
            serializer = serializer_class(profile, data=profile_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": f"Perfil de {role} actualizado correctamente",
                    "role": role,
                    "profile": serializer.data
                }, status=200)
            return Response(serializer.errors, status=400)
        else:
            # Caso customer (no tiene serializer de update)
            return Response({
                "message": "Perfil de cliente actualizado correctamente",
                "role": "customer",
                "customer": {
                    "id": profile.id_customer,
                    "email": profile.user.email,
                    "address": AddressSerializer(profile.address).data if profile.address else None
                }
            }, status=200)
"""

# profiles/views.py
class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
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

            

class ProfileDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user, context={'request': request})
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





"""
class CustomerProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        customer = request.user.customer
        address_data = request.data.get('address')
        print("Received address data:", address_data)

        if address_data:
            address_id = address_data.get('id_address', None)
            if address_id:
                try:
                    address = Address.objects.get(id_address=address_id)
                    address_serializer = AddressSerializer(address, data=address_data, partial=True)
                except Address.DoesNotExist:
                    return Response({'address': 'Dirección no encontrada'}, status=status.HTTP_404_NOT_FOUND)
            else:
                address_serializer = AddressSerializer(data=address_data)

            try:
                address_serializer.is_valid(raise_exception=True)
                address_instance = address_serializer.save()

                if customer.address_id != address_instance.id_address:
                    customer.address_id = address_instance.id_address
                    customer.save()

            except serializers.ValidationError as e:
                print("Address validation errors:", e.detail)
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

            print("Pasó validación de address")

        # 👇 Este return faltaba
        return Response(
            {
                "message": "Perfil de cliente actualizado correctamente",
                "customer": {
                    "id": customer.id_customer,
                    "email": customer.user.email,
                    "address": AddressSerializer(customer.address).data if customer.address else None
                }
            },
            status=status.HTTP_200_OK
        )



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

            print("Pasó validación de address")

        provider_data = request.data.copy()
        provider_data.pop('address', None)

        # Actualizar el resto del proveedor (excepto dirección)
        provider_serializer = ProviderProfileUpdateSerializer(provider, data=provider_data, partial=True)
        if provider_serializer.is_valid():
            provider_serializer.save()
            return Response(provider_serializer.data)
        return Response(provider_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""