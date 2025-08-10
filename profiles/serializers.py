from rest_framework import serializers

from authentication.models import User, Provider
from locations.serializers import AddressSerializer
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
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Provider
        fields = ['id_provider','categories', 'type_provider', 'profession', 'description', 'address']

class ProviderProfileUpdateSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)

    class Meta:
        model = Provider
        fields = ['description', 'address']

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)

        print("Datos validados recibidos:", validated_data)
        print("Datos de dirección recibidos:", address_data)

        if address_data:
            if instance.address:
                address_serializer = AddressSerializer(instance.address, data=address_data, partial=True)
                address_serializer.is_valid(raise_exception=True)
                address_instance = address_serializer.save()
                # Si la dirección cambió, actualizamos FK y guardamos Provider
                if instance.address_id != address_instance.id_address:
                    instance.address_id = address_instance.id_address
                    instance.save()
            else:
                address_serializer = AddressSerializer(data=address_data)
                address_serializer.is_valid(raise_exception=True)
                address_instance = address_serializer.save()
                instance.address_id = address_instance.id_address
                instance.save()

        return super().update(instance, validated_data)