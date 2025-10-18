from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from postulations.models import Postulation
from .serializers import HireSerializer
from authentication.models import Provider, Customer

class HireAPIView(generics.ListAPIView):
    """
    API view to retrieve a list of approved postulations (hires).

    - If the user is a Customer, it returns hires for their petitions.
    - If the user is a Provider, it returns their approved postulations.
    """
    serializer_class = HireSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # State for "Approved" postulations
        # Assuming '3' is the ID for the 'APROBADO' state.
        # This should be verified against the n_postulation_state table in the database.
        approved_state_id = 4

        try:
            # Check if the user is a Customer
            customer = Customer.objects.get(user=user)
            # Find all petitions for this customer
            from petitions.models import Petition
            petition_ids = Petition.objects.filter(id_customer=customer.id_customer).values_list('id_petition', flat=True)
            
            # Find all approved postulations for those petitions
            return Postulation.objects.filter(
                id_petition__in=petition_ids,
                id_state=approved_state_id
            ).select_related('id_state')
        except Customer.DoesNotExist:
            pass

        try:
            # Check if the user is a Provider
            provider = Provider.objects.get(user=user)
            return Postulation.objects.filter(
                id_provider=provider.id_provider, 
                id_state=approved_state_id
            ).select_related('id_state')
        except Provider.DoesNotExist:
            pass

        # If user is neither a Customer nor a Provider, or has no hires
        return Postulation.objects.none()