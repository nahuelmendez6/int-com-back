from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import TypeOffer, Offer
from .serializers import TypeOfferSerializer, OfferSerializer


class TypeOfferListCreateAPIView(APIView):
    """
    Listar y crear TypeOffers
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


class TypeOfferDetailAPIView(APIView):
    """
    Obtener, actualizar o eliminar un TypeOffer
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


class OfferListCreateAPIView(APIView):
    """
    Listar y crear Offers (solo las que no están soft-deleted)
    """
    def get(self, request):
        offers = Offer.objects.all()  # gracias al Manager, excluye is_deleted=True
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfferDetailAPIView(APIView):
    """
    Obtener, actualizar o soft delete de una Offer
    """
    def get_object(self, pk):
        return get_object_or_404(Offer, pk=pk)

    def get(self, request, pk):
        offer = self.get_object(pk)
        serializer = OfferSerializer(offer)
        return Response(serializer.data)

    def put(self, request, pk):
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


