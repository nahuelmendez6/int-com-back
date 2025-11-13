from django.db.models import Q, Subquery, Prefetch
from .models import Petition, PetitionCategory, PetitionAttachment, PetitionMaterial, PetitionStateHistory
from authentication.models import Customer, Provider

# ====================================================
# FUNCIÓN: get_petition_list_queryset
# ====================================================
def get_petition_list_queryset():
    """
    Retorna el queryset para listas de Petitions, optimizado para rendimiento.
    Precarga solo las relaciones necesarias para la vista de lista.
    """
    return (
        Petition.objects.select_related(
            "id_type_petition",
            "id_state",
            "id_profession",
            "id_type_provider",
        )
        .prefetch_related(
            Prefetch(
                "petitioncategory_set",
                queryset=PetitionCategory.objects.select_related("id_category"),
            ),
        )
    )

# ====================================================
# FUNCIÓN: get_petition_detail_queryset
# ====================================================
def get_petition_detail_queryset():
    """
    Retorna el queryset para la vista de detalle de una Petition.
    Precarga todas las relaciones anidadas para una serialización completa.
    """
    return (
        Petition.objects.select_related(
            "id_type_petition",
            "id_state",
            "id_profession",
            "id_type_provider",
        )
        .prefetch_related(
            Prefetch(
                "petitioncategory_set",
                queryset=PetitionCategory.objects.select_related("id_category"),
            ),
            Prefetch(
                "petitionattachment_set",
                queryset=PetitionAttachment.objects.all(),
            ),
            Prefetch(
                "petitionmaterial_set",
                queryset=PetitionMaterial.objects.all(),
            ),
            Prefetch(
                "petitionstatehistory_set",
                queryset=PetitionStateHistory.objects.select_related("id_state"),
            ),
        )
    )


# ====================================================
# FUNCIÓN: filter_petitions_for_provider
# ====================================================
def filter_petitions_for_provider(provider):
    """
    Filtra las peticiones disponibles para un proveedor según su perfil.
    
    Criterios de filtrado:
    1. Solo peticiones no eliminadas (soft delete)
    2. Coincidencia de profesión (si se especifica) o sin profesión requerida
    3. Coincidencia de tipo de proveedor (si se especifica) o sin tipo requerido
    4. Coincidencia de categorías entre proveedor y petición
    5. Coincidencia geográfica: ciudades del proveedor y clientes
    """

    qs = get_petition_list_queryset()
    # ------------------------------------------------
    # Filtrar por profesión del proveedor
    # Si la petición especifica una profesión, debe coincidir con la del proveedor.
    # Si la petición no especifica profesión (isnull=True), también se incluye.
    # ------------------------------------------------
    qs = qs.filter(
        Q(id_profession=provider.profession) | Q(id_profession__isnull=True)
    )
    # ------------------------------------------------
    # Filtrar por tipo de proveedor
    # Similar al filtro de profesión: se incluye si coincide o si no se especifica
    # ------------------------------------------------
    qs = qs.filter(
        Q(id_type_provider=provider.type_provider) | Q(id_type_provider__isnull=True)
    )
    # ------------------------------------------------
    # Filtrar por categorías del proveedor
    # Si el proveedor tiene categorías asignadas, la petición debe tener al menos una coincidencia
    # ------------------------------------------------
    if provider.categories.exists():
        qs = qs.filter(categories__in=provider.categories.all())

    # ------------------------------------------------
    # Filtrar por zonas geográficas (ciudades del proveedor)
    # Solo se incluyen las peticiones cuyo cliente está en alguna de las ciudades del proveedor
    # ------------------------------------------------
    if provider.cities.exists():
        customer_ids = Customer.objects.filter(
            address__city__in=provider.cities.all()
        ).values('id_customer')
        qs = qs.filter(id_customer__in=Subquery(customer_ids))
    return qs.distinct()
