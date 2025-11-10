from rest_framework import serializers
from .models import Grade, GradeCustomer, GradeProvider
from authentication.models import User
from django.conf import settings

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
            image_str = str(obj.profile_image).strip()

            # 🔧 Normalizar posibles URLs mal formadas (https:/ -> https://)
            if image_str.startswith("https:/") and not image_str.startswith("https://"):
                image_str = image_str.replace("https:/", "https://", 1)
            elif image_str.startswith("http:/") and not image_str.startswith("http://"):
                image_str = image_str.replace("http:/", "http://", 1)

            # 🔹 Si ya es URL externa
            if image_str.startswith("http"):
                return image_str

            # 🔹 Si es un archivo local
            return f"{settings.MEDIA_URL}{image_str}"

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
