from rest_framework import serializers

from authentication.models import User, Provider, Customer
from locations.serializers import AddressSerializer
from .models import Category, TypeProvider, Profession

# ====================================
# SERIALIZER DE PERFIL DE USUARIO
# ====================================
class ProfileSerializer(serializers.ModelSerializer):
    
    """
    Serializer para representar información básica de un usuario
    junto con su imagen de perfil y dirección asociada.
    """
    profile_image = serializers.SerializerMethodField()  # <-- aquí
    address = AddressSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['name', 'lastname', 'email', 'profile_image', 'address']

    def get_profile_image(self, obj):
        """
        Construye la URL completa de la imagen de perfil si existe.
        """
        
        if obj.profile_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.profile_image.url)
        return None


# ====================================
# SERIALIZERS DE CATEGORIAS
# ====================================
class CategorySerializer(serializers.ModelSerializer):
    
    """
    Serializer para representar categorías.
    """
    class Meta:
        model = Category
        fields = '__all__'

class TypeProviderSerializer(serializers.ModelSerializer):
    """
    Serializer para representar tipos de proveedores.
    """
    class Meta:
        model = TypeProvider
        fields = '__all__'

class ProfessionSerializer(serializers.ModelSerializer):
    """
    Serializer para representar profesiones.
    """
    class Meta:
        model = Profession
        fields = '__all__'

# ====================================
# SERIALIZER DE PERFIL DE CLIENTE
# ====================================
class CustomerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer que devuelve información del cliente,
    incluyendo dirección y datos personales.
    """
    
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ['id_customer', 'dni', 'phone', 'address']

# ====================================
# SERIALIZER DE PERFIL DE PROVEEDOR (LECTURA)
# ====================================
class ProviderProfileSerializer(serializers.ModelSerializer):
    """
    Serializer para mostrar información detallada del proveedor,
    incluyendo categorías, tipo, profesión y dirección.
    """
    categories = CategorySerializer(many=True, read_only=True)
    type_provider = TypeProviderSerializer(read_only=True)
    profession = ProfessionSerializer(read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Provider
        fields = ['id_provider','categories', 'type_provider', 'profession', 'description', 'address']

# ====================================
# SERIALIZER DE ACTUALIZACIÓN DE PROVEEDOR
# ====================================
class ProviderProfileUpdateSerializer(serializers.ModelSerializer):

    """
    Serializer para actualizar datos de un proveedor,
    incluyendo dirección, categoría, profesión y tipo de proveedor.
    """
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
        """
        Sobrescribe el método update para manejar actualización anidada de dirección
        y dejar que DRF maneje profession, type_provider y categories automáticamente.
        """
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
