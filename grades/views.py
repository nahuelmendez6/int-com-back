from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from authentication.models import User, Customer, Provider
from .models import GradeProvider, GradeCustomer
from .serializers import GradeProviderSerializer, GradeProviderWriteSerializer, GradeCustomerSerializer, GradeCustomerWriteSerializer
from django.db import connection



# ====================================================
# API para listar y crear calificaciones de Provider
# ====================================================


class GradeProviderAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Listar todas las calificaciones visibles.
        Opcionalmente filtrar por proveedor: ?provider=<id>
        """
        provider_id = request.query_params.get('provider')
        customer_id = request.query_params.get('customer')

        queryset = GradeProvider.objects.filter(is_visible=True)
        if provider_id:
            queryset = queryset.filter(provider_id=provider_id)

        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        
        queryset = queryset.order_by('-date_create')
        serializer = GradeProviderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Crear nueva calificación.
        Se asigna automáticamente el customer y los campos user_create/user_update.
        """
        data = request.data.copy()

        if 'provider' in data:
            try:
                provider_obj = Provider.objects.get(id_provider=data['provider'])
                data['provider'] = provider_obj.user.id_user
            except Provider.DoesNotExist:
                return Response(
                    {'provider':['El proveedor especificado no existe']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except AttributeError:
                return Response(
                    {'provider': ['El proveedor no tiene usuario asociado.']},
                    status=status.HTTP_400_BAD_REQUEST
                )

        data['customer'] = request.user.id_user
        data['user_create'] = request.user.id_user
        data['user_update'] = request.user.id_user

        serializer = GradeProviderWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Detalle y actualización de una calificación
class GradeProviderDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            return GradeProvider.objects.get(id=id)
        except GradeProvider.DoesNotExist:
            return None

    def get(self, request, id):
        obj = self.get_object(id)
        if not obj:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = GradeProviderSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        obj = self.get_object(id)
        if not obj:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['user_update'] = request.user.id_user  # actualizar quién modificó

        serializer = GradeProviderSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ====================================================
# API para obtener el promedio de calificaciones de un Provider
# ====================================================
class ProviderAverageRatingView(APIView):
    def get(self, request, provider_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT AVG(rating) as avg_rating
                FROM n_grade_provider
                WHERE id_provider = %s
            """, [provider_id])
            row = cursor.fetchone()  # Solo un resultado

        if row[0] is None:
            return Response({"id_provider": provider_id, "avg_rating": None})
        
        return Response({"id_provider": provider_id, "avg_rating": float(row[0])})





# ====================================================
# API para listar y crear calificaciones de Customer
# ====================================================

class GradeCustomerAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Listar todas las calificaciones visibles.
        Opcionalmente filtrar por cliente: ?customer=<id>
        """
        customer_id = request.query_params.get('customer')
        queryset = GradeCustomer.objects.filter(is_visible=True)
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        queryset = queryset.order_by('-date_create')
        serializer = GradeCustomerSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """
        Crear nueva calificación.
        Se asigna automáticamente el provider y los campos user_create/user_update.
        """
        data = request.data.copy()

        if 'customer' in data:
            try:
                customer_obj = Customer.objects.get(id_customer=data['customer'])
                if not hasattr(customer_obj, 'user') or not customer_obj.user:
                    return Response(
                        {'customer': ['El cliente no tiene usuario asociado.']},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                data['customer'] = customer_obj.user.id_user  # Usamos el id_user del cliente
            except Customer.DoesNotExist:
                return Response(
                    {'customer': ['El cliente especificado no existe.']},
                    status=status.HTTP_400_BAD_REQUEST
                )

        data['provider'] = request.user.id_user
        data['user_create'] = request.user.id_user
        data['user_update'] = request.user.id_user

        serializer = GradeCustomerWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GradeCustomerDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            return GradeCustomer.objects.get(pk=id)
        except GradeCustomer.DoesNotExist:
            return None

    def get(self, request, id):
        """
        Obtener detalle de una calificación por ID.
        """
        obj = self.get_object(id)
        if not obj:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = GradeCustomerSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        """
        Actualizar calificación (ej. respuesta del proveedor o cambio de rating).
        """
        obj = self.get_object(id)
        if not obj:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['user_update'] = request.user.id_user  # quién actualiza

        serializer = GradeCustomerWriteSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
