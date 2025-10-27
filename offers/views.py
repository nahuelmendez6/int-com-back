from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import TypeOffer, Offer
from .serializers import TypeOfferSerializer, OfferSerializer
from authentication.models import Provider, Customer

from .services import filter_offers_for_customer_by_city_interest

# ====================================================
# APIView: TypeOfferListCreateAPIView
# ====================================================
class TypeOfferListCreateAPIView(APIView):
    """
    API para listar todos los TypeOffer existentes y crear nuevos TypeOffer.
    GET: devuelve todos los TypeOffer.
    POST: crea un nuevo TypeOffer.
    """
    def get(self, request):
        type_offers = TypeOffer.objects.all()
        serializer = TypeOfferSerializer(type_offers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TypeOfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ====================================================
# APIView: TypeOfferDetailAPIView
# ====================================================
class TypeOfferDetailAPIView(APIView):
    """
    API para obtener, actualizar o eliminar un TypeOffer específico.
    GET: obtener TypeOffer por ID.
    PUT: actualizar TypeOffer (parcial permitido).
    DELETE: eliminar TypeOffer.
    """
    def get_object(self, pk):
        return get_object_or_404(TypeOffer, pk=pk)

    def get(self, request, pk):
        type_offer = self.get_object(pk)
        serializer = TypeOfferSerializer(type_offer)
        return Response(serializer.data)

    def put(self, request, pk):
        type_offer = self.get_object(pk)
        serializer = TypeOfferSerializer(type_offer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        type_offer = self.get_object(pk)
        type_offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ====================================================
# APIView: OfferListCreateAPIView
# ====================================================
class OfferListCreateAPIView(APIView):
    """
    API para listar y crear ofertas (Offer) de un proveedor.
    Solo muestra las ofertas activas (soft delete excluido por el Manager).
    """
    def get(self, request):
        
        user = request.user
        provider = Provider.objects.filter(user=user).first()

        id_provider = provider.id_provider
        if id_provider is None:
             return Response({"detail": "No se pudo obtener el proveedor logueado."}, status=400)
        
        offers = Offer.objects.filter(id_provider=id_provider)  # ya excluye is_deleted=True gracias al Manager
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)
        

    def post(self, request):
        
        provider = Provider.objects.filter(user=request.user).first()
        if not provider:
            return Response({"detail": "El usuario no está asociado a ningún proveedor."}, status=400)
        
        data = request.data.copy()
        data['id_provider'] = provider.id_provider
        data['user_create_id'] = request.user.id_user
        
        serializer = OfferSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ====================================================
# APIView: OfferDetailAPIView
# ====================================================
class OfferDetailAPIView(APIView):
    """
    API para obtener, actualizar o eliminar (soft delete) una oferta específica.
    GET: obtener oferta por ID.
    PATCH: actualizar parcialmente una oferta.
    DELETE: soft delete (marcar is_deleted=True).
    """
    def get_object(self, pk):
        return get_object_or_404(Offer, pk=pk)

    def get(self, request, pk):
        offer = self.get_object(pk)
        serializer = OfferSerializer(offer)
        return Response(serializer.data)

    def patch(self, request, pk):
        offer = self.get_object(pk)
        serializer = OfferSerializer(offer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        offer = self.get_object(pk)
        offer.delete()  # soft delete (cambia is_deleted=True)
        return Response({"detail": "Offer deleted (soft delete)."}, status=status.HTTP_204_NO_CONTENT)



# ====================================================
# APIView: CustomerOfferFeedAPIView
# ====================================================
class CustomerOfferFeedAPIView(APIView):

    """
    API para que un cliente obtenga un feed de ofertas filtradas.
    Filtra ofertas según intereses del cliente y ciudades de interés.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        
        try:
            customer = Customer.objects.filter(user=user).first()
        except Customer.DoesNotExist:
            return Response({'detail':'El usuario no es un cliente'}, status=status.HTTP_403_FORBIDDEN)
        
        # aplicamos filtro
        offers  = filter_offers_for_customer_by_city_interest(customer)
        serializer = OfferSerializer(offers, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)