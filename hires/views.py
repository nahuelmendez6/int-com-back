from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from postulations.models import Postulation
from .serializers import HireSerializer
from authentication.models import Provider, Customer

# ====================================================
# API para listar postulations aprobadas (contrataciones)
# ====================================================
class HireAPIView(generics.ListAPIView):
    """
    API view para recuperar una lista de postulations aprobadas (hires).

    - Si el usuario es un Customer, retorna las hires de sus petitions.
    - Si el usuario es un Provider, retorna sus postulations aprobadas.
    """
    serializer_class = HireSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Devuelve el queryset de Postulations aprobadas según el tipo de usuario:
        - Customer: postulations aprobadas de sus petitions
        - Provider: postulations aprobadas realizadas por ellos mismos
        - Otros usuarios: queryset vacío
        """
        user = self.request.user
        
        # Estado de postulations "APROBADO"
        # Nota: Verificar que el ID 4 corresponde al estado aprobado en la tabla n_postulation_state
        approved_state_id = 4

        try:
            # Si el usuario es un Customer
            customer = Customer.objects.get(user=user)
            # Obtener todas las petitions de este cliente
            from petitions.models import Petition
            petition_ids = Petition.objects.filter(id_customer=customer.id_customer).values_list('id_petition', flat=True)
            
            # Obtener todas las postulations aprobadas para esas petitions
            return Postulation.objects.filter(
                id_petition__in=petition_ids,
                id_state=approved_state_id
            ).select_related('id_state')
        except Customer.DoesNotExist:
            pass

        try:
            # Si el usuario es un Provider
            provider = Provider.objects.get(user=user)
            return Postulation.objects.filter(
                id_provider=provider.id_provider, 
                id_state=approved_state_id
            ).select_related('id_state')
        except Provider.DoesNotExist:
            pass

        # Si el usuario no es Customer ni Provider, o no tiene hires
        return Postulation.objects.none()