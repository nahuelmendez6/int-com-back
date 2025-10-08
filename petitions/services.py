from django.db.models import Q, Subquery
from .models import Petition
from authentication.models import Customer, Provider

def filter_petitions_for_provider(provider):
    qs = Petition.objects.filter(is_deleted=False)

    # Profesión (opcional)
    qs = qs.filter(
        Q(id_profession=provider.profession) | Q(id_profession__isnull=True)
    )

    # Tipo de proveedor (opcional)
    qs = qs.filter(
        Q(id_type_provider=provider.type_provider) | Q(id_type_provider__isnull=True)
    )

    # Categorías
    if provider.categories.exists():
        qs = qs.filter(categories__in=provider.categories.all())

    # Zonas (ciudades del proveedor)
    if provider.cities.exists():
        customer_ids = Customer.objects.filter(
            address__city__in=provider.cities.all()
        ).values('id_customer')
        qs = qs.filter(id_customer__in=Subquery(customer_ids))

    return qs.distinct()
