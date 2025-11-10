from rest_framework import serializers
from .models import Portfolio, PortfolioAttachment, Material, MaterialAttachment
from postulations.models import PostulationMaterial

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



class PostulationMaterialSerializer(serializers.ModelSerializer):
    """
    Serializer para los materiales asociados a una postulación.
    Incluye la información básica del material y los datos presupuestados.
    """
    material = serializers.SerializerMethodField()

    class Meta:
        model = PostulationMaterial
        fields = [
            'id_postulation_material',
            'material',
            'quantity',
            'unit_price',
            'total',
            'notes',
        ]

    def get_material(self, obj):
        """
        Retorna la información del Material asociado.
        """
        material = obj.id_material
        if material:
            return {
                'id': material.id_material,
                'name': material.name,
                'description': getattr(material, 'description', None),
                'unit': getattr(material, 'unit', None),
                'category': getattr(material, 'category', None),
            }
        return None
