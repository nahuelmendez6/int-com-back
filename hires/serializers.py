from rest_framework import serializers
from decimal import Decimal

from postulations.models import Postulation, PostulationBudget, PostulationMaterial
from postulations.serializers import PostulationBudgetSerializer
from petitions.models import Petition
from authentication.models import Customer, Provider
from portfolio.serializers import PostulationMaterialSerializer

# ====================================================
# Serializer para la contratación (Hire)
# ====================================================
class HireSerializer(serializers.ModelSerializer):
    """
    Serializer para representar una postulación aprobada (contratación),
    incluyendo información de la petición, cliente, proveedor y precio final.
    """
    petition = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    provider = serializers.SerializerMethodField()
    approved_at = serializers.DateTimeField(source='date_update', read_only=True)
    final_price = serializers.SerializerMethodField()
    budget = serializers.SerializerMethodField()
    materials = serializers.SerializerMethodField()

    class Meta:
        model = Postulation
        fields = [
            'id_postulation',
            'proposal',
            'petition',
            'customer',
            'provider',
            'approved_at',
            'final_price',
            'budget',
            'materials',
        ]

    # ====================================================
    # Métodos para campos personalizados
    # ====================================================

    def _get_petition_instance(self, obj):
        cache = getattr(self, "_petition_cache", None)
        if cache is None:
            cache = self._petition_cache = {}

        petition_id = obj.id_petition
        if petition_id in cache:
            return cache[petition_id]

        context_map = self.context.get("petition_map", {})
        petition = context_map.get(petition_id)
        if petition is None:
            petition = (
                Petition.objects.select_related("id_state", "id_type_petition")
                .prefetch_related("categories")
                .filter(pk=petition_id)
                .first()
            )
        cache[petition_id] = petition
        return petition

    def _get_customer_instance(self, petition):
        if petition is None or not petition.id_customer:
            return None

        cache = getattr(self, "_customer_cache", None)
        if cache is None:
            cache = self._customer_cache = {}

        customer_id = petition.id_customer
        if customer_id in cache:
            return cache[customer_id]

        context_map = self.context.get("customer_map", {})
        customer = context_map.get(customer_id)
        if customer is None:
            customer = Customer.objects.select_related("user").filter(
                pk=customer_id
            ).first()
        cache[customer_id] = customer
        return customer

    def _get_provider_instance(self, obj):
        cache = getattr(self, "_provider_cache", None)
        if cache is None:
            cache = self._provider_cache = {}

        provider_id = obj.id_provider
        if provider_id in cache:
            return cache[provider_id]

        context_map = self.context.get("provider_map", {})
        provider = context_map.get(provider_id)
        if provider is None:
            provider = Provider.objects.select_related("user", "profession").filter(
                pk=provider_id
            ).first()
        cache[provider_id] = provider
        return provider

    def _get_budgets(self, obj):
        if hasattr(obj, "_prefetched_objects_cache") and "budgets" in obj._prefetched_objects_cache:
            return obj._prefetched_objects_cache["budgets"]
        return PostulationBudget.objects.filter(id_postulation=obj.id_postulation)

    def _get_materials(self, obj):
        if hasattr(obj, "_prefetched_objects_cache") and "materials" in obj._prefetched_objects_cache:
            return obj._prefetched_objects_cache["materials"]
        return PostulationMaterial.objects.select_related("id_material").filter(
            id_postulation=obj.id_postulation
        )

    def get_petition(self, obj):
        """
        Obtiene la información resumida de la Petition asociada a la postulación.
        Retorna un dict con id y título de la Petition o None si no existe.
        """
        petition = self._get_petition_instance(obj)
        if petition:
            return {
                'id': petition.id_petition,
                'title': petition.description
            }
        return None

    # Customer (desde la Petition)
    def get_customer(self, obj):
        """
        Obtiene información del Customer asociado a la Petition de la Postulation.
        Retorna un dict con id, nombre, apellido y URL de la imagen de perfil.
        """
        petition = self._get_petition_instance(obj)
        if petition and petition.id_customer:
            customer = self._get_customer_instance(petition)
            if customer and customer.user:
                return {
                    'id': customer.id_customer,
                    'name': customer.user.name,
                    'lastname': customer.user.lastname,
                    'profile_image': self._get_profile_image_url(customer.user)
                }
        return None

    # Provider
    def get_provider(self, obj):
        """
        Obtiene información del Provider asociado a la Postulation.
        Retorna un dict con id, nombre, apellido, profesión y URL de imagen de perfil.
        """
        provider = self._get_provider_instance(obj)
        if provider and provider.user:
            return {
                'id': provider.id_provider,
                'name': provider.user.name,
                'lastname': provider.user.lastname,
                'profession': provider.profession.name if provider.profession else None,
                'profile_image': self._get_profile_image_url(provider.user)
            }
        return None

    # Final Price
    def get_final_price(self, obj):
        """
        Obtiene el precio final de la postulación desde PostulationBudget.
        Retorna el monto total o None si no existe presupuesto.
        Si hay múltiples presupuestos, suma todos los amounts.
        """
        budgets = self._get_budgets(obj)
        if budgets.exists():
            total = sum(
                Decimal(str(b.amount)) 
                for b in budgets 
                if b.amount is not None
            )
            return float(total) if total > 0 else None
        return None

    # Budget
    def get_budget(self, obj):
        """
        Obtiene información completa del presupuesto de la postulación.
        Retorna una lista con todos los presupuestos asociados a la postulación.
        """
        budgets = self._get_budgets(obj)
        return PostulationBudgetSerializer(budgets, many=True).data
    
    def get_materials(self, obj):
        """
        Retorna los materiales asociados a la postulacion, si existen.
        """
        materials = self._get_materials(obj)
        return PostulationMaterialSerializer(materials, many=True).data


    # ====================================================
    # Método auxiliar privado
    # ====================================================
    def _get_profile_image_url(self, user):
        """
        Devuelve una URL segura para el campo profile_image sin intentar leer el binario
        soporta ImageField
        """
        if not user.profile_image:
            return None
        
        # si es ImageField 
        if hasattr(user.profile_image, 'url'):
            return user.profile_image.url
        
        # si es un texto
        return str(user.profile_image)


