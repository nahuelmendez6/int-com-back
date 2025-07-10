from rest_framework import serializers

from locations.models import Address
from profiles.models import Category, TypeProvider, Profession
from .models import User, Customer, Provider


class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    name = serializers.CharField()
    lastname = serializers.CharField()
    role = serializers.ChoiceField(choices=[('customer', 'Cliente'), ('provider', 'Proveedor')])

    # Datos opcionales de cliente
    dni = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), required=False)

    # Datos opcionales de proveedor
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
    type_provider = serializers.PrimaryKeyRelatedField(queryset=TypeProvider.objects.all(), required=False)
    profession = serializers.PrimaryKeyRelatedField(queryset=Profession.objects.all(), required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'lastname', 'role', 'dni', 'phone', 'address', 'category',
                  'type_provider', 'profession', 'description']

    def validate(self, data):
        role = data.get('role')
        if role == 'customer':
            #if not data.get('address'):
            #    raise serializers.ValidationError('Direccion obligatoria para cliente')
            required_fields = ['email', 'password', 'name', 'lastname', 'dni', 'phone']
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError(f'{field} es obligatorio')

        elif role == 'provider':
            required_fields = ['category', 'type_provider', 'profession', 'address']
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError(f'{field} es obligatorio')

        else:
            raise serializers.ValidationError('Rol inválido o no especificado')

        return data

    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        name = validated_data.pop('name')
        lastname = validated_data.pop('lastname')

        user = User.objects.create_user(email=email, password=password, name=name, lastname=lastname)

        if role == 'customer':
            Customer.objects.create(
                user=user,
                dni=validated_data.get('dni'),
                phone=validated_data.get('phone'),
                address=validated_data.get('address')
            )
        elif role == 'provider':
            Provider.objects.create(
                user=user,
                category=validated_data.get("category"),
                type_provider=validated_data.get("type_provider"),
                profession=validated_data.get("profession"),
                address=validated_data.get("address"),
                description=validated_data.get("description", "")
            )
        return user