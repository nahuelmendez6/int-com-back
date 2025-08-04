from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Category, TypeProvider, Profession
from .serializers import (
    CategorySerializer, TypeProviderSerializer, ProfessionSerializer, ProfileSerializer, ProviderProfileSerializer
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