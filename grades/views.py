from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import GradeProvider, GradeCustomer
from .serializers import GradeProviderSerializer, GradeProviderWriteSerializer, GradeCustomerSerializer, GradeCustomerWriteSerializer
from django.db import connection

# Listado de calificaciones (GET) y creación (POST)
class GradeProviderAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Listar todas las calificaciones visibles.
        Opcionalmente filtrar por proveedor: ?provider=<id>
        """
        provider_id = request.query_params.get('provider')
        queryset = GradeProvider.objects.filter(is_visible=True)
        if provider_id:
            queryset = queryset.filter(provider_id=provider_id)
        queryset = queryset.order_by('-date_create')
        serializer = GradeProviderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Crear nueva calificación.
        Se asigna automáticamente el customer y los campos user_create/user_update.
        """
        data = request.data.copy()
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




class GradeCustomerAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Listar todas las calificaciones visibles.
        Opcionalmente filtrar por provider: ?provider=<id>
        """
        provider_id = request.query_params.get('provider')
        queryset = GradeCustomer.objects.filter(is_visible=True)
        if provider_id:
            queryset = queryset.filter(provider_id=provider_id)
        queryset = queryset.order_by('-date_create')

        serializer = GradeCustomerSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Crear nueva calificación de cliente hacia un proveedor.
        Se asignan automáticamente los campos de usuario y cliente.
        """
        data = request.data.copy()
        # El customer es el usuario autenticado (suponiendo que es un cliente)
        data['customer'] = request.user.id_user  
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
