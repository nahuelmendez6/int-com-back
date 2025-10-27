from rest_framework import serializers

from .models import (
    TypePetition,
    PetitionState,
    Petition,
    PetitionCategory,
    PetitionAttachment,
    PetitionMaterial,
    PetitionStateHistory
)

# ====================================================
# SERIALIZER: TypePetitionSerializer
# ====================================================
class TypePetitionSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo TypePetition.
    Permite serializar y deserializar los tipos de peticiones.
    """

    class Meta:
        model = TypePetition
        fields = '__all__'

# ====================================================
# SERIALIZER: PetitionStateSerializer
# ====================================================
class PetitionStateSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo PetitionState.
    Permite manejar la serialización de los estados de una petición.
    """

    class Meta:
        model = PetitionState
        fields = '__all__'


# ====================================================
# SERIALIZER: PetitionCategorySerializer
# ====================================================
class PetitionCategorySerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo intermedio PetitionCategory.
    Permite representar las categorías asociadas a cada petición.
    """
    class Meta:
        model = PetitionCategory
        fields = '__all__'

# ====================================================
# SERIALIZER: PetitionAttachmentSerializer
# ====================================================
class PetitionAttachmentSerializer(serializers.ModelSerializer):
    """
    Serializer para los archivos adjuntos a una petición.
    Gestiona la serialización de los attachments.
    """
    class Meta:
        model = PetitionAttachment
        fields = '__all__'

# ====================================================
# SERIALIZER: PetitionMaterialSerializer
# ====================================================
class PetitionMaterialSerializer(serializers.ModelSerializer):
    """
    Serializer para los materiales asociados a una petición.
    Incluye cantidad, precio unitario y referencias de creación/actualización.
    """
    class Meta:
        model = PetitionMaterial
        fields = '__all__'


# ====================================================
# SERIALIZER: PetitionStateHistorySerializer
# ====================================================
class PetitionStateHistorySerializer(serializers.ModelSerializer):
    """
    Serializer para el historial de cambios de estado de una petición.
    Permite auditar los cambios y mostrarlos en APIs.
    """
    class Meta:
        model = PetitionStateHistory
        fields = '__all__'

# ====================================================
# SERIALIZER PRINCIPAL: PetitionSerializer
# ====================================================
class PetitionSerializer(serializers.ModelSerializer):
    """
    Serializer principal para el modelo Petition.
    Incluye relaciones anidadas a:
    - categories: Categorías asociadas a la petición
    - attachments: Archivos adjuntos
    - materials: Materiales solicitados
    - state_history: Historial de cambios de estado

    También incluye relaciones directas con TypePetition y PetitionState.
    """

    # Relaciones anidadas
    categories = PetitionCategorySerializer(many=True, source='petitioncategory_set', read_only=True)
    attachments = PetitionAttachmentSerializer(many=True, source="petitionattachment_set", read_only=True)
    materials = PetitionMaterialSerializer(many=True, source="petitionmaterial_set", read_only=True)
    state_history = PetitionStateHistorySerializer(many=True, source="petitionstatehistory_set", read_only=True)


    # Relaciones directas
    id_type_petition = serializers.PrimaryKeyRelatedField(
        queryset=TypePetition.objects.all()
    )
    id_state = serializers.PrimaryKeyRelatedField(
        queryset=PetitionState.objects.all()
    )

    class Meta:
        model = Petition
        fields = '__all__'

    def validate(self, data):
        
        date_since = data.get('date_since')
        date_until = data.get('date_until')

        if date_since and date_until and date_since > date_until:
            raise serializers.ValidationError(
                {'date_until':'La fecha de cierre no puede ser anterior a la fecha de incio'}
            )
        
        return data
    

