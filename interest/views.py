from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from authentication.models import Customer
from .models import Interest
from .serializers import InterestSerializer

class InterestAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):

        user = request.user
        customer = Customer.objects.filter(id_user=user.id_user).first()
        id_customer = customer.id_customer

        interest = Interest.objects.filter(id_customer=id_customer, is_deleted=False)
        serializer = InterestSerializer(interest, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        user = request.user
        customer = Customer.objects.filter(id_user=user.id_user).first()
        id_customer = customer.id_customer

        serializer = InterestSerializer(data=request.data)

        if serializer.is_valid():
            interest = serializer.save(id_customer=id_customer)
            return Response(InterestSerializer(interest).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)