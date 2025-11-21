from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from authentication.models import Customer
from .models import Interest
from .serializers import InterestSerializer

# ====================================================
# APIView para Interest
# ====================================================
class InterestAPIView(APIView):
    """
    API para gestionar intereses de clientes.

    Métodos soportados:
    - GET: Lista todos los intereses de un cliente autenticado.
    - POST: Crea un nuevo interés para el cliente autenticado.
    - DELETE: Realiza un soft delete de un interés específico.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        """
        Lista los intereses del cliente autenticado.
        
        Flujo:
        1. Obtiene el usuario logueado.
        2. Obtiene el objeto Customer asociado al usuario.
        3. Filtra los intereses del cliente que no estén eliminados (is_deleted=False).
        4. Retorna los intereses serializados.
        """
        user = request.user
        customer = Customer.objects.filter(user=user.id_user).first()
        id_customer = customer.id_customer

        interest = Interest.objects.filter(id_customer=id_customer, is_deleted=False)
        serializer = InterestSerializer(interest, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """
        Crea un nuevo interés para el cliente autenticado.
        
        Flujo:
        1. Obtiene el usuario logueado y su Customer asociado.
        2. Deserializa los datos recibidos en la request.
        3. Si son válidos, guarda el nuevo interés asociado al Customer.
        4. Retorna los datos del interés creado.
        """
        user = request.user
        customer = Customer.objects.filter(user=user.id_user).first()
        id_customer = customer.id_customer

        serializer = InterestSerializer(data=request.data)

        if serializer.is_valid():
            interest = serializer.save(id_customer=customer, id_user_create=request.user.id_user)

            return Response(InterestSerializer(interest).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        """
        Realiza un soft delete de un interés específico.
        
        Flujo:
        1. Obtiene el interés por su PK y que no esté eliminado.
        2. Llama al método delete del modelo (marca is_deleted=True).
        3. Retorna un mensaje de éxito.
        """
        interest = get_object_or_404(Interest, pk=pk, is_deleted=False)
        interest.delete()  # usa método soft delete
        return Response({"detail": "Interest eliminado (soft delete)"}, status=status.HTTP_204_NO_CONTENT)
