from rest_framework import serializers
from .models import Category, TypeProvider, Profession

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TypeProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeProvider
        fields = '__all__'

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = '__all__'
