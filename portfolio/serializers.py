from rest_framework import serializers
from .models import Portfolio, PortfolioAttachment, Material, MaterialAttachment

# ====================================================
# Serializer: PortfolioAttachmentSerializer
# ====================================================
class PortfolioAttachmentSerializer(serializers.ModelSerializer):
    """
    Serializador para los archivos adjuntos de un portafolio.
    Permite convertir los objetos PortfolioAttachment a JSON y viceversa.
    """
    class Meta:
        model = PortfolioAttachment
        fields = '__all__'

# ====================================================
# Serializer: PortfolioSerializer
# ====================================================
class PortfolioSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Portfolio.
    Incluye los attachments relacionados de forma anidada (read-only).
    """
    attachments = PortfolioAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Portfolio
        fields = '__all__'

# ====================================================
# Serializer: MaterialSerializer
# ====================================================
class MaterialSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Material.
    Permite CRUD sobre materiales de proveedores.
    """
    class Meta:
        model = Material
        fields = '__all__'

# ====================================================
# Serializer: MaterialAttachmentSerializer
# ====================================================
class MaterialAttachmentSerializer(serializers.ModelSerializer):
    """
    Serializador para los archivos asociados a materiales.
    Permite CRUD sobre MaterialAttachment.
    """
    class Meta:
        model = MaterialAttachment
        fields = '__all__'