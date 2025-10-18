from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import GradeProvider
from .serializers import GradeProviderSerializer, GradeProviderWriteSerializer


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
