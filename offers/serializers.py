from rest_framework import serializers
from .models import TypeOffer, Offer

# ====================================================
# Serializer: TypeOfferSerializer
# ====================================================
class TypeOfferSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo TypeOffer.
    Convierte instancias de TypeOffer a JSON y valida datos entrantes.
    Incluye todos los campos del modelo.
    """
    class Meta:
        model = TypeOffer
        fields = "__all__"

# ====================================================
# Serializer: OfferSerializer
# ====================================================
class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Offer.
    Convierte instancias de Offer a JSON y valida datos entrantes.
    Campos:
    - Todos los campos del modelo.
    - Campos de solo lectura: offer_id, date_create, date_update.
    """
    class Meta:
        model = Offer
        fields = "__all__"
        read_only_fields = ["offer_id", "date_create", "date_update"]