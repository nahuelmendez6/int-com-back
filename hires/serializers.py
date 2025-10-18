from rest_framework import serializers
from postulations.models import Postulation, PostulationBudget
from petitions.models import Petition
from authentication.models import Customer, Provider


class HireSerializer(serializers.ModelSerializer):
    petition = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    provider = serializers.SerializerMethodField()
    approved_at = serializers.DateTimeField(source='date_update', read_only=True)
    final_price = serializers.SerializerMethodField()

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
        ]

    # Petition
    def get_petition(self, obj):
        petition = Petition.objects.filter(pk=obj.id_petition).first()
        if petition:
            return {
                'id': petition.id_petition,
                'title': petition.description  # completo
            }
        return None

    # Customer (desde la Petition)
    def get_customer(self, obj):
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
        budget = PostulationBudget.objects.filter(id_postulation=obj.id_postulation).first()
        return budget.amount if budget else None



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