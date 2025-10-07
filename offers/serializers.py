from rest_framework import serializers
from .models import TypeOffer, Offer

class TypeOfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeOffer
        fields = "__all__"


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = "__all__"
        read_only_fields = ["offer_id", "date_create", "date_update", "is_deleted"]