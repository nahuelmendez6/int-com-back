from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import (
    Postulation,
    PostulationState,
    PostulationStateHistory,
    PostulationMaterial
)
from .serializers import (PostulationSerializer, 
                            PostulationReadSerializer, 
                            PostulationMaterialSerializer)
from petitions.models import Petition

# ====================================================
# API VIEW: PostulationAPIView
# ====================================================
class PostulationAPIView(APIView):
    """
    API para gestionar postulaciones:
        - Listar postulaciones de un proveedor o cliente
        - Recuperar detalle de una postulación
        - Crear nuevas postulaciones
        - Actualizar postulación o estado según rol del usuario
    """

    # --------------------------
    # MÉTODO GET (LIST / DETAIL)
    # --------------------------
    def get(self, request, pk=None, id_petition=None):
        """
        Listar todas las postulaciones de un proveedor o de un cliente
        dependiendo del rol del usuario.
        - Proveedor: puede listar todas sus postulaciones.
        - Cliente: puede listar todas las postulaciones de una petición propia.
        """
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
    # MÉTODO POST (CREATE)
    # -------------------------
    def post(self, request):
        """
        Crear una nueva postulación.
        Solo los proveedores pueden crear postulaciones.
        """
        print("Datos recibidos:", request.data)
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
        """
        Actualizar una postulación existente.
        - Proveedor: puede actualizar toda la postulación (presupuestos, materiales, propuesta, etc.)
        - Cliente: solo puede actualizar el estado de la postulación
        """
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



# ====================================================
# API VIEW: PostulationMaterialAPIView
# ====================================================
class PostulationMaterialAPIView(APIView):
    """
    API para gestionar materiales de una postulación:
        - Listar materiales de una postulación
        - Crear un nuevo material
        - Actualizar un material existente
        - Eliminar un material
    """

    def get(self, request, id_postulation=None):
        """
        Listar materiales asociados a una postulacion especifica
        """

        if not id_postulation:
            return Response(
                {"detail":"Debe especificar el ID de la postulacion"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        postulation = get_object_or_404(Postulation, pk=id_postulation)
        materials = PostulationMaterial.objects.filter(id_postulation=postulation)
        sealizer = PostulationMaterialSerializer(materials, many=True)
        return Response(sealizer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """
        Crear un nuevo material asociado a una postulacion
        """
        provider = getattr(request.user, 'provider', None)
        if not provider:
            return Response({"detail": "Solo los proveedores pueden agregar materiales."},
                            status=status.HTTP_403_FORBIDDEN)
        
        serializer = PostulationMaterialSerializer(data=request.data)
        if serializer.is_valid():
            postulation = serializer.validated_data.get("id_postulation")

            # Verificamos que la postulacion pertenezca al proveedor actual
            if postulation.id_provider != provider.id_provider:
                return Response({"detail": "No tiene permiso para agregar materiales a esta postulación."},
                                status=status.HTTP_403_FORBIDDEN)
            

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def patch(self, request, pk=None):
        """
        Actualiza un material específico.
        """
        provider = getattr(request.user, 'provider', None)
        if not provider:
            return Response({"detail": "Solo los proveedores pueden modificar materiales."},
                            status=status.HTTP_403_FORBIDDEN)

        if not pk:
            return Response({"detail": "Debe especificar el ID del material."},
                            status=status.HTTP_400_BAD_REQUEST)

        material = get_object_or_404(PostulationMaterial, pk=pk)
        postulation = material.id_postulation

        # Verificamos que la postulación sea del proveedor actual
        if postulation.id_provider != provider.id_provider:
            return Response({"detail": "No tiene permiso para modificar materiales de esta postulación."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = PostulationMaterialSerializer(material, data=request.data, partial=True)
        if serializer.is_valid():
            quantity = serializer.validated_data.get("quantity", material.quantity)
            unit_price = serializer.validated_data.get("unit_price", material.unit_price)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """
        Elimina un material específico de una postulación.
        """
        provider = getattr(request.user, 'provider', None)
        if not provider:
            return Response({"detail": "Solo los proveedores pueden eliminar materiales."},
                            status=status.HTTP_403_FORBIDDEN)

        if not pk:
            return Response({"detail": "Debe especificar el ID del material."},
                            status=status.HTTP_400_BAD_REQUEST)

        material = get_object_or_404(PostulationMaterial, pk=pk)
        postulation = material.id_postulation

        if postulation.id_provider != provider.id_provider:
            return Response({"detail": "No tiene permiso para eliminar materiales de esta postulación."},
                            status=status.HTTP_403_FORBIDDEN)

        material.delete()
        return Response({"detail": "Material eliminado correctamente."}, status=status.HTTP_204_NO_CONTENT)

