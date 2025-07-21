from django.core.serializers import serialize
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (RegisterSerializer,
                          LoginSerializer, VerifyCodeSerializer)


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


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        #print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserAPIView(APIView):

    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = RegisterSerializer(user, data=request.data, partial=True)
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