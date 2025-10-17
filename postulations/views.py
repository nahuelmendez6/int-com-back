from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import (
    Postulation,
    PostulationState,
    PostulationStateHistory
)
from .serializers import PostulationSerializer, PostulationReadSerializer
from petitions.models import Petition


class PostulationAPIView(APIView):
    """
    Gestiona la creación, listado, actualización y eliminación de postulaciones
    con presupuestos y materiales.
    """

    # --------------------------
    # LIST / DETAIL
    # --------------------------
    def get(self, request, pk=None, id_petition=None):
        provider = getattr(request.user, 'provider', None)
        customer = getattr(request.user, 'customer', None)

        # --- Proveedor ---
        if provider:
            if pk:
                postulation = get_object_or_404(Postulation, pk=pk, id_provider=provider.id_provider)
                serializer = PostulationSerializer(postulation)
                return Response(serializer.data, status=status.HTTP_200_OK)

            postulations = Postulation.objects.filter(id_provider=provider.id_provider).order_by('-date_create')
            serializer = PostulationSerializer(postulations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # --- Cliente ---
        elif customer:
            if not id_petition:
                return Response({"detail": "Debe especificar una petición (id_petition)."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Validamos que la petición pertenezca al cliente
            petition = get_object_or_404(Petition, pk=id_petition, id_customer=customer.id_customer)

            if pk:
                postulation = get_object_or_404(Postulation, pk=pk, id_petition=id_petition)
                serializer = PostulationSerializer(postulation)
                return Response(serializer.data, status=status.HTTP_200_OK)

            postulations = Postulation.objects.filter(id_petition=id_petition).order_by('-date_create')
            serializer = PostulationSerializer(postulations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Usuario sin rol válido
        return Response({"detail": "Usuario no válido."}, status=status.HTTP_403_FORBIDDEN)

    # --------------------------
    # CREATE
    # --------------------------
    def post(self, request):
        provider = getattr(request.user, 'provider', None)
        if not provider:
            return Response({"detail": "Solo los proveedores pueden crear postulaciones."},
                            status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data['id_provider'] = provider.id_provider
        data['id_user_create'] = request.user.id_user

        serializer = PostulationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # --------------------------
    # PATCH / UPDATE
    # --------------------------
    def patch(self, request, pk=None, id_petition=None):
        provider = getattr(request.user, 'provider', None)
        customer = getattr(request.user, 'customer', None)
        print(request.data)
        if not pk:
            return Response({"detail": "Debe especificar el ID de la postulación."},
                            status=status.HTTP_400_BAD_REQUEST)

        # --- Proveedor: actualizar toda la postulación ---
        if provider:
            postulation = get_object_or_404(Postulation, pk=pk, id_provider=provider.id_provider)
            serializer = PostulationSerializer(postulation, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(id_user_update=request.user.id_user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # --- Cliente: solo puede actualizar el estado ---
        elif customer:
            # lee id_petition del body de la solicitud
            id_petition = request.data.get('id_petition')

            if not id_petition:
                return Response({"detail": "Debe especificar id_petition en el cuerpo de la solicitud."}, status=status.HTTP_400_BAD_REQUEST)
            
            # validamos que la peticion sea del cliente
            petition = get_object_or_404(Petition, pk=id_petition, id_customer=customer.id_customer)

            postulation = get_object_or_404(Postulation, pk=pk, id_petition=id_petition)

            new_state_id = request.data.get('id_state')
            if not new_state_id:
                return Response({"detail": "Debe especificar id_state en el cuerpo de la solicitud."}, status=status.HTTP_400_BAD_REQUEST)

            new_state = get_object_or_404(PostulationState, pk=new_state_id)
            postulation.id_state = new_state
            postulation.id_user_update = request.user.id_user
            postulation.save(update_fields=["id_state", "id_user_update","date_update"])

            # Registrar historial
            PostulationStateHistory.objects.create(
                id_postulation=postulation,
                id_state=new_state
            )

            return Response({"detail": f"Estado actualizado a '{new_state.name}'."},
      status=status.HTTP_200_OK)

        # Usuario sin rol válido
        return Response({"detail": "Usuario no válido."}, status=status.HTTP_403_FORBIDDEN)
