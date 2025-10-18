from rest_framework import serializers
from .models import Grade, GradeProvider
from authentication.models import Provider, User


# Serializer simple para Grade
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id_grade', 'name', 'description', 'value']


# Serializer para Customer / User (quien calificó)
class CustomerSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id_user', 'first_name', 'last_name', 'profile_image']

    def get_profile_image(self, obj):
        # Maneja ImageField o varchar (ruta)
        if not obj.profile_image:
            return None
        if hasattr(obj.profile_image, 'url'):
            return obj.profile_image.url
        return str(obj.profile_image)


# Serializer para Provider
class ProviderSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Provider
        fields = ['id_provider', 'name', 'lastname', 'profession', 'profile_image']

    def get_profile_image(self, obj):
        if obj.user and obj.user.profile_image:
            if hasattr(obj.user.profile_image, 'url'):
                return obj.user.profile_image.url
            return str(obj.user.profile_image)
        return None


# Serializer principal para GradeProvider
class GradeProviderSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer()
    customer = CustomerSerializer()
    grade = GradeSerializer()

    class Meta:
        model = GradeProvider
        fields = [
            'id_grade_provider',
            'provider',
            'customer',
            'grade',
            'rating',
            'coment',
            'response',
            'is_visible',
            'date_create',
            'date_update',
        ]

class GradeProviderWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeProvider
        fields = [
            'provider',
            'customer',
            'grade',
            'rating',
            'coment',
            'response',
            'is_visible',
            'user_create',
            'user_update',
        ]
