from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import (
    Postulation,
    PostulationBudget,
    PostulationMaterial,
    PostulationState,
    PostulationStateHistory
)

from .serializers import (
    PostulationSerializer,
    PostulationBudgetSerializer,
    PostulationMaterialSerializer,
    PostulationStateSerializer,
    PostulationStateHistorySerializer
)

from petitions.models import Petition

class PostulationAPIView(APIView):

    """"
    Gestion la creacion, listado, actualizacion y eliminacion de postulaciones
    """
    def get(self, request, pk=None, id_petition=None):
        provider = getattr(request.user, 'provider', None)
        customer = getattr(request.user, 'customer', None)

        # --- Caso: proveedor (solo sus postulaciones) ---
        if provider:
            if pk:
                # Obtener una postulación específica del proveedor
                postulation = get_object_or_404(Postulation, pk=pk, id_provider=provider.id_provider)
                serializer = PostulationSerializer(postulation)
            
            # Obtener todas las postulaciones del proveedor
            postulations = Postulation.objects.filter(
                id_provider=provider.id_provider
                ).order_by('-date_create')
            serializer = PostulationSerializer(postulations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        
        # ------------------------------
        # CASO: CLIENTE
        # ------------------------------
        elif customer:
            # el cliente debe pasar una peticion para ver sus postulaciones
            if not id_petition:
                return Response(
                    {"detail": "Debe especificar una petición (id_petition)."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # verificamos que la petiticon petenezca al cliente autenticado
            petition = get_object_or_404(
                Petition,
                pk=id_petition,
                id_customer=customer.id_customer
            )

            if pk:
                # ver un postulacion especfica de la peticion del cliente
                postulation = get_object_or_404(
                    Postulation,
                    pk=pk,
                    id_petition=id_petition
                )
                serializer = PostulationSerializer(postulation)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            # Ver todas las postulaciones recibidas sobre esa petición
            postulations = Postulation.objects.filter(
                id_petition=id_petition
            ).order_by('-date_create')
            serializer = PostulationSerializer(postulations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

         # ------------------------------
        # CASO: USUARIO SIN ROL VÁLIDO
        # ------------------------------
        return Response(
            {"detail": "El usuario no tiene un rol válido (ni provider ni customer)."},
            status=status.HTTP_403_FORBIDDEN
        )


    def patch(self, request, pk=None, id_petition=None):
        provider = getattr(request.user, 'provider', None)
        customer = getattr(request.user, 'customer', None)

        # --- Validación base ---
        if not pk:
            return Response(
                {"detail": "Debe especificar el ID de la postulación a actualizar."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ------------------------------
        # CASO: PROVEEDOR (puede editar su postulación completa)
        # ------------------------------
        if provider:
            postulation = get_object_or_404(Postulation, pk=pk, id_provider=provider.id_provider)

            serializer = PostulationSerializer(
                postulation,
                data=request.data,
                partial=True
            )

            if serializer.is_valid():
                serializer.save(id_user_update=request.user.id)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # ------------------------------
        # CASO: CLIENTE (solo puede cambiar el estado de la postulación)
        # ------------------------------
        elif customer:
            if not id_petition:
                return Response(
                    {"detail": "Debe especificar una petición (id_petition)."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Verificamos que la petición pertenezca al cliente
            petition = get_object_or_404(
                Petition,
                pk=id_petition,
                id_customer=customer.id_customer
            )

            # Traemos la postulación que pertenece a esa petición
            postulation = get_object_or_404(
                Postulation,
                pk=pk,
                id_petition=id_petition
            )

            # El cliente solo puede actualizar el campo de estado (id_state)
            new_state_id = request.data.get("id_state")

            if not new_state_id:
                return Response(
                    {"detail": "Debe proporcionar un nuevo estado (id_state)."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            new_state = get_object_or_404(PostulationState, pk=new_state_id)

            # Guardamos el nuevo estado
            postulation.id_state = new_state
            postulation.id_user_update = request.user.id
            postulation.save(update_fields=["id_state", "id_user_update", "date_update"])

            # Registramos en el historial
            PostulationStateHistory.objects.create(
                id_postulation=postulation,
                id_state=new_state,
                changed_by=request.user.id,
                notes=request.data.get("notes", "")
            )

            return Response(
                {"detail": f"Estado actualizado a '{new_state.name}'."},
                status=status.HTTP_200_OK
            )

        # ------------------------------
        # CASO: USUARIO SIN ROL VÁLIDO
        # ------------------------------
        return Response(
            {"detail": "El usuario no tiene un rol válido (ni provider ni customer)."},
            status=status.HTTP_403_FORBIDDEN
        )


