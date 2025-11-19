from django.core.serializers import serialize
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, generics
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from .models import User, Provider
from .serializers import (RegisterSerializer,
                          LoginSerializer, UserSerializer, ProviderSerializer,
                          UserProfileSerializer)


from .services import send_verification_email

# ====================================
# API VIEW: REGISTRO DE USUARIO
# ====================================
class RegisterUserAPIView(APIView):
    """
    Endpoint para registrar nuevos usuarios en el sistema.
    Soporta tanto clientes como proveedores según el rol proporcionado.
    """

    def post(self, request, *args, **kwargs):
        """
        Recibe los datos de registro, valida y crea el usuario.
        Envía opcionalmente un email de verificación.
        
        Returns:
            Response: Mensaje de éxito o errores de validación.
        """


        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            #send_verification_email(user)
            return Response({
                'message':'Usuario creado exitosamente',
                'email': user.email,
                'role':'provider' if hasattr(user, 'provider') else 'customer'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ====================================
# VIEWSET DE USUARIOS
# ====================================
class UserViewSet(viewsets.ModelViewSet):

    """
    ViewSet para gestionar operaciones CRUD de usuarios.
    Incluye un endpoint adicional para obtener el usuario autenticado.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail = False, methods=['get'], url_path='user')
    def get_authenticated_user(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


# ====================================
# API VIEW: LOGIN DE USUARIO
# ====================================
class LoginAPIView(APIView):
    """
    Endpoint para autenticar usuarios y generar tokens de acceso.
    """
    def post(self, request):
        """
        Valida las credenciales enviadas y retorna los tokens JWT
        junto con información del usuario.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ====================================
# API VIEW: ACTUALIZACIÓN DE PERFIL DE USUARIO
# ====================================
class UpdateUserAPIView(APIView):

    """
    View para actualizar información parcial del usuario (PATCH)
    utilizando el serializer de registro.
    """

    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = RegisterSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Perfil actualizado correctamente'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ====================================
# API VIEW: ACTUALIZACIÓN DE IMAGEN DE PERFIL
# ====================================
class UserProfileUpdateView(APIView):

    """
    Endpoint para actualizar la imagen de perfil del usuario.
    Requiere autenticación y soporta envío de archivos multipart/form-data.
    """

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # DRF lo maneja correctamente

    def patch(self, request, *args, **kwargs):

        """
        Actualiza la foto de perfil del usuario autenticado.
        
        Returns:
            Response: URL absoluta de la nueva imagen de perfil o error si no se envió archivo.
        """
        user = request.user
        profile_image = request.FILES.get('profile_image')

        if not profile_image:
            return Response({"error": "No se envió ninguna imagen"}, status=status.HTTP_400_BAD_REQUEST)

        user.profile_image = profile_image
        user.save()

        profile_url = request.build_absolute_uri(user.profile_image.url)
        return Response({"profile_image": profile_url}, status=status.HTTP_200_OK)
