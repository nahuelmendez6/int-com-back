from rest_framework import serializers

from authentication.models import Provider
from .models import Country, Province, Department, City, Address, ProviderCity

# ====================================
# SERIALIZER: COUNTRY
# ====================================
class CountrySerializer(serializers.ModelSerializer):

    """
    Serializer para el modelo Country.
    Incluye todos los campos de la tabla.
    """
    class Meta:
        model = Country
        fields = '__all__'

# ====================================
# SERIALIZER: PROVINCE
# ====================================
class ProvinceSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Province.
    Incluye todos los campos de la tabla.
    """
    class Meta:
        model = Province
        fields = '__all__'

# ====================================
# SERIALIZER: DEPARTMENT
# ====================================
class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Department.
    Incluye todos los campos de la tabla.
    """
    class Meta:
        model = Department
        fields = '__all__'

# ====================================
# SERIALIZER: CITY
# ====================================
class CitySerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo City.
    Incluye todos los campos de la tabla.
    """
    class Meta:
        model = City
        fields = '__all__'

# ====================================
# SERIALIZER: ADDRESS
# ====================================
class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Address.
    - Permite lectura de la ciudad asociada con detalles.
    - Permite escritura mediante id_city.
    """

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

# ====================================
# SERIALIZER: PROVIDERCITY
# ====================================
class ProviderCitySerializer(serializers.ModelSerializer):
    """
    Serializer para la relación ProviderCity (Many-to-Many entre proveedores y ciudades).
    - provider: id del proveedor
    - city: id de la ciudad
    """

    provider = serializers.PrimaryKeyRelatedField(queryset=Provider.objects.all())
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = ProviderCity
        fields = '__all__'
