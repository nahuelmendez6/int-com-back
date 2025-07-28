from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Category, TypeProvider, Profession
from .serializers import CategorySerializer, TypeProviderSerializer, ProfessionSerializer

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