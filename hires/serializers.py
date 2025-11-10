from rest_framework import serializers
from postulations.models import Postulation, PostulationBudget
from postulations.serializers import PostulationBudgetSerializer
from petitions.models import Petition
from authentication.models import Customer, Provider
from portfolio.serializers import MaterialSerializer, PostulationMaterialSerializer
from postulations.models import PostulationMaterial

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

    def get_petition(self, obj):
        """
        Obtiene la información resumida de la Petition asociada a la postulación.
        Retorna un dict con id y título de la Petition o None si no existe.
        """
        petition = Petition.objects.filter(pk=obj.id_petition).first()
        if petition:
            return {
                'id': petition.id_petition,
                'title': petition.description  # completo
            }
        return None

    # Customer (desde la Petition)
    def get_customer(self, obj):
        """
        Obtiene información del Customer asociado a la Petition de la Postulation.
        Retorna un dict con id, nombre, apellido y URL de la imagen de perfil.
        """
        petition = Petition.objects.filter(pk=obj.id_petition).first()
        if petition and petition.id_customer:
            customer = Customer.objects.filter(pk=petition.id_customer).first()
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
        provider = Provider.objects.filter(pk=obj.id_provider).first()
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
        budgets = PostulationBudget.objects.filter(id_postulation=obj.id_postulation)
        if budgets.exists():
            # Sumar todos los amounts que no sean None
            from decimal import Decimal
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
        budgets = PostulationBudget.objects.filter(id_postulation=obj.id_postulation)
        if budgets.exists():
            return PostulationBudgetSerializer(budgets, many=True).data
        return []
    
    def get_materials(self, obj):
        """
        Retorna los materiales asociados a la postulacion, si existen.
        """
        materials = PostulationMaterial.objects.filter(id_postulation=obj.id_postulation)
        if materials.exists():
            return PostulationMaterialSerializer(materials, many=True).data
        return []


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


