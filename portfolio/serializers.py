from rest_framework import serializers
from .models import Portfolio, PortfolioAttachment, Material


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
