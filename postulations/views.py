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




