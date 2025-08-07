from rest_framework import serializers
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
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(),
        required=False,
        allow_null=True)

    class Meta:
        model = Address
        fields = '__all__'

    extra_kwargs = {
        'city': {'required': False, 'allow_null': True},
        'department': {'required': False, 'allow_blank': True},
        'province': {'required': False, 'allow_blank': True},
    }

    def create(self, validated_data):
        return Address.objects.create(**validated_data)

class ProviderCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderCity
        fields = '__all__'
