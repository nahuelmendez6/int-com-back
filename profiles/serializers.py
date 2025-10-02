from rest_framework import serializers

from authentication.models import User, Provider, Customer
from locations.serializers import AddressSerializer
from .models import Category, TypeProvider, Profession

class ProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()  # <-- aquí
    address = AddressSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['name', 'lastname', 'email', 'profile_image', 'address']

    def get_profile_image(self, obj):
        if obj.profile_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.profile_image.url)
        return None


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


class CustomerProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ['id_customer', 'dni', 'phone', 'address']

class ProviderProfileSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    type_provider = TypeProviderSerializer(read_only=True)
    profession = ProfessionSerializer(read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Provider
        fields = ['id_provider','categories', 'type_provider', 'profession', 'description', 'address']

class ProviderProfileUpdateSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)
    profession = serializers.PrimaryKeyRelatedField(
        queryset=Profession.objects.all(),
        required=False,
        allow_null=True
    )
    type_provider = serializers.PrimaryKeyRelatedField(
        queryset=TypeProvider.objects.all(),
        required=False,
        allow_null=True
    )
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Provider
        fields = ['description', 'address', 'profession', 'type_provider', 'categories']

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)

        print("Datos validados recibidos:", validated_data)
        print("Datos de dirección recibidos:", address_data)

        if address_data:
            if instance.address:
                address_serializer = AddressSerializer(instance.address, data=address_data, partial=True)
                address_serializer.is_valid(raise_exception=True)
                address_instance = address_serializer.save()
                if instance.address_id != address_instance.id_address:
                    instance.address_id = address_instance.id_address
                    instance.save()
            else:
                address_serializer = AddressSerializer(data=address_data)
                address_serializer.is_valid(raise_exception=True)
                address_instance = address_serializer.save()
                instance.address_id = address_instance.id_address
                instance.save()

        # dejar que DRF maneje profession, type_provider y categories
        return super().update(instance, validated_data)
