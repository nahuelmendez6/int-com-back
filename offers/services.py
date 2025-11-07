from django.db.models import Q
from django.utils import timezone

from interest.models import Interest
from .models import Offer
from authentication.models import Provider  # usar Provider para sacar providers por categoría


def filter_offers_for_customer_by_city_interest(customer):
    """
    Filtra ofertas para un cliente por ciudad y categorías de interés.
    Retorna un QuerySet de Offer (sin duplicados).
    """

    # 1) categorías de interés (ids)
    category_ids_qs = Interest.objects.filter(
        id_customer=customer,
        is_deleted=False
    ).values_list('id_category', flat=True)  # QuerySet de enteros

    # 2) ciudad del cliente (instancia de City) o None
    customer_city = getattr(customer.address, 'city', None)

    if not customer_city or not category_ids_qs.exists():
        # si no hay ciudad o categorías de interés, no hay ofertas relevantes
        return Offer.objects.none()
    
    
    # 3) ofertas base: no eliminadas, activas y dentro del rango de fechas
    now = timezone.now()
    qs = Offer.objects.filter(
        is_deleted=False,
        status='active',
        date_open__lte=now,
        date_close__gte=now
    )

    # 4) si hay categorias de interés, sacar proveedores que tengan esas categorías
    if category_ids_qs.exists():
        # obtenemos ids de proveedores que tienen alguna de esas categorías
        provider_ids_by_category = Provider.objects.filter(
            categories__in=category_ids_qs
        ).values_list('id_provider', flat=True)

        # filtrar ofertas cuyo id_provider esté en la lista
        # mantengo la opción de incluir ofertas sin proveedor si eso fuera necesario:
        qs = qs.filter(Q(id_provider__in=provider_ids_by_category) | Q(id_provider__isnull=True))

    # 5) si hay ciudad, filtrar por proveedores que trabajen en esa ciudad
    if customer_city:
        provider_ids_by_city = customer_city.city_providers.values_list('provider_id', flat=True)
        qs = qs.filter(id_provider__in=provider_ids_by_city)

    # 6) evitar duplicados
    return qs.distinct()
