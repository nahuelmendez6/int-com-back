from rest_framework import serializers

from authentication.models import Provider
from .models import Country, Province, Department, City, Address, ProviderCity

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):

    # para lectura, se neceseita informacion de la ciudad
    city_detail = CitySerializer(source='city', read_only=True)

    # para escritura, solo se necesita id_city
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(),
        required=False,
        allow_null=True)

    class Meta:
        model = Address
        fields = [
            'id_address',
            'street',
            'number',
            'floor',
            'apartment',
            'postal_code',
            'city',
            'city_detail',
            'date_create',
            'date_update'
        ]

        extra_kwargs = {
            'city': {'required': False, 'allow_null': True},
            'department': {'required': False, 'allow_blank': True},
            'province': {'required': False, 'allow_blank': True},
        }

    def create(self, validated_data):
        return Address.objects.create(**validated_data)

class ProviderCitySerializer(serializers.ModelSerializer):
    provider = serializers.PrimaryKeyRelatedField(queryset=Provider.objects.all())
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = ProviderCity
        fields = '__all__'
