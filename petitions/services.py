from django.db.models import Q
from .models import Petition

def filter_petitions_for_provider(provider):

    qs = Petition.objects.all()

    # Filtrar por profesión del proveedor o peticiones sin profesion
    qs = qs.filter(
        Q(id_profession=provider.profession) | Q(id_profession__isnull=True)
    )

    # Filtrar por categorias
    provider_categories = provider.categories.values_list('id', flat=True)
    if provider_categories.exists():
        qs = qs.filter(petitioncategory__id_category__in=provider_categories)


    # Filtrar por zona (ciudad del cliente en las ciudades del proveedor)
    provider_cities = provider.cities.values_list('id_city', flat=True)
    if provider_cities.exists():
        qs = qs.filter(id_customer__address__city__id_city__in=provider_cities)


    return qs.distinct()