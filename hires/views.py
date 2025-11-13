from django.db.models import Prefetch
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from postulations.models import Postulation, PostulationBudget, PostulationMaterial
from petitions.models import Petition
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
        if hasattr(self, "_cached_queryset"):
            return self._cached_queryset

        user = self.request.user
        approved_state_id = 4  # Estado "Aprobada"

        queryset = Postulation.objects.none()

        customer = getattr(user, "customer", None)
        provider = getattr(user, "provider", None)

        if customer:
            petition_ids = Petition.objects.filter(
                id_customer=customer.id_customer
            ).values_list("id_petition", flat=True)

            queryset = Postulation.objects.filter(
                id_petition__in=petition_ids,
                id_state=approved_state_id,
            )

        elif provider:
            queryset = Postulation.objects.filter(
                id_provider=provider.id_provider,
                id_state=approved_state_id,
            )

        queryset = queryset.select_related("id_state").prefetch_related(
            Prefetch("budgets", queryset=PostulationBudget.objects.all()),
            Prefetch(
                "materials",
                queryset=PostulationMaterial.objects.select_related("id_material"),
            ),
        )

        self._cached_queryset = queryset
        return self._cached_queryset

    def list(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())

        petition_ids = {obj.id_petition for obj in queryset}
        provider_ids = {obj.id_provider for obj in queryset if obj.id_provider is not None}

        petitions = (
            Petition.objects.filter(id_petition__in=petition_ids)
            .select_related("id_state", "id_type_petition")
            .prefetch_related("categories")
        )
        petition_map = {petition.id_petition: petition for petition in petitions}

        customer_ids = {
            petition.id_customer for petition in petitions if petition.id_customer
        }

        customers = Customer.objects.filter(
            id_customer__in=customer_ids
        ).select_related("user")
        customer_map = {customer.id_customer: customer for customer in customers}

        providers = Provider.objects.filter(
            id_provider__in=provider_ids
        ).select_related("user", "profession")
        provider_map = {provider.id_provider: provider for provider in providers}

        context = self.get_serializer_context()
        context.update(
            {
                "petition_map": petition_map,
                "customer_map": customer_map,
                "provider_map": provider_map,
            }
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context=context)
        return Response(serializer.data)
