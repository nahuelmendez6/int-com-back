from rest_framework import serializers
from .models import Portfolio, PortfolioAttachment, Material, MaterialAttachment


class PortfolioAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioAttachment
        fields = '__all__'


class PortfolioSerializer(serializers.ModelSerializer):
    attachments = PortfolioAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Portfolio
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class MaterialAttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = MaterialAttachment
        fields = '__all__'