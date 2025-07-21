from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken



from locations.models import Address
from profiles.models import Category, TypeProvider, Profession
from .models import User,  Customer, Provider




class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    name = serializers.CharField()
    lastname = serializers.CharField()
    role = serializers.ChoiceField(choices=[('customer', 'Cliente'), ('provider', 'Proveedor')])

    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'lastname', 'role']

    def validate_role(self, value):
        if value not in ['customer', 'provider']:
            raise serializers.ValidationError('Rol inválido')
        return value

    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')

        user = User.objects.create_user(
            email=validated_data['email'],
            password=password,
            name=validated_data['name'],
            lastname=validated_data['lastname'],
            is_active=False  # para verificación por código
        )

        # Asociar al tipo de perfil correspondiente
        if role == 'customer':
            Customer.objects.create(user=user)
        elif role == 'provider':
            Provider.objects.create(user=user)

        # Generar y enviar código de verificación
        # generate_verification_code(user)

        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email is None or password is None:
            raise serializers.ValidationError('Email y contraseña son requeridos.')

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError('Credenciales inválidas.')

        if not user.enabled:
            raise serializers.ValidationError('Usuario deshabilitado.')

        refresh = RefreshToken.for_user(user)

        # Obtener rol
        role = None
        if hasattr(user, 'customer'):
            role = 'customer'
        elif hasattr(user, 'provider'):
            role = 'provider'
        else:
            role = 'admin' if user.is_staff else 'user'


        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "role": role,
            "user_id": user.id_user,
            "email": user.email,
        }