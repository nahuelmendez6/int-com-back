from rest_framework import serializers

from .models import (Address,
                     ProviderCity,
                     City,
                     Department,
                     Province)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        field = '__all__'


class ProviderCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderCity
        fields = '__all__'