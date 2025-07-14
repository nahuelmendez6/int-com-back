from rest_framework import viewsets
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