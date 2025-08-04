from rest_framework import serializers

from authentication.models import User, Provider
from .models import Category, TypeProvider, Profession

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'lastname', 'email']


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

class ProviderProfileSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    type_provider = TypeProviderSerializer(read_only=True)
    profession = ProfessionSerializer(read_only=True)

    class Meta:
        model = Provider
        fields = ['categories', 'type_provider', 'profession', 'description']
