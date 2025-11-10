from rest_framework import serializers
from .models import Grade, GradeCustomer, GradeProvider
from authentication.models import User


# ====================================================
# Serializer simple para el modelo Grade
# ====================================================
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id_grade', 'name', 'description', 'value']


# ====================================================
# Serializer para usuario (tanto customer como provider)
# ====================================================
class UserBasicSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id_user', 'name', 'lastname', 'profile_image']

    def get_profile_image(self, obj):
        if obj.profile_image:
            if hasattr(obj.profile_image, 'url'):
                return obj.profile_image.url
            return str(obj.profile_image)
        return None


# ====================================================
# Serializer principal para GradeCustomer (lectura)
# ====================================================
class GradeCustomerSerializer(serializers.ModelSerializer):
    provider = UserBasicSerializer()
    customer = UserBasicSerializer()
    #grade = GradeSerializer()

    class Meta:
        model = GradeCustomer
        fields = [
            'id_grade_customer',
            'provider',
            'customer',
            #'grade',
            'rating',
            'comment',
            'response',
            'is_visible',
            'user_create',
            'user_update',
            'date_create',
            'date_update',
        ]


# ====================================================
# Serializer principal para GradeProvider (lectura)
# ====================================================
class GradeProviderSerializer(serializers.ModelSerializer):
    provider = UserBasicSerializer()
    customer = UserBasicSerializer()
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
            'user_create',
            'user_update',
            'date_create',
            'date_update',
        ]


# ====================================================
# Serializer para crear/actualizar GradeCustomer
# ====================================================
class GradeCustomerWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeCustomer
        fields = [
            'provider',
            'customer',
            'rating',
            'comment',
            'response',
            'is_visible',
            'user_create',
            'user_update',
        ]


# ====================================================
# Serializer para crear/actualizar GradeProvider
# ====================================================
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
