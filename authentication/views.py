from django.core.serializers import serialize
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from .models import User, Provider
from .serializers import (RegisterSerializer,
                          LoginSerializer, VerifyCodeSerializer, UserSerializer, ProviderSerializer)


from .services import send_verification_email

class RegisterUserAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            send_verification_email(user)
            return Response({
                'message':'Usuario creado exitosamente',
                'email': user.email,
                'role':'provider' if hasattr(user, 'provider') else 'customer'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail = False, methods=['get'], url_path='user')
    def get_authenticated_user(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)



class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        #print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserAPIView(APIView):

    """
    Usamos esta view para gestionar el perfil del usuario
    """

    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = RegisterSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Perfil actualizado correctamente'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateProviderAPIView(APIView):

        """
        Vista para actualizar perfil de proveedor
        """
        def patch(self, request):
            user = request.user
            try:
                provider = Provider.objects.get(user=user)
            except Provider.DoesNotExist:
                raise NotFound('Proveedor no encontrado')

            serializer = ProviderSerializer(provider, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Perfil actualizado correctamente'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeAPIView(APIView):
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Código verificado correctamente"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)