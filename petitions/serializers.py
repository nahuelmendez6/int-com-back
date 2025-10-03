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

class TypePetitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypePetition
        fields = '__all__'


class PetitionStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PetitionState
        fields = '__all__'



class PetitionCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PetitionCategory
        fields = '__all__'


class PetitionAttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PetitionAttachment
        fields = '__all__'


class PetitionMaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = PetitionMaterial
        fields = '__all__'


class PetitionStateHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PetitionStateHistory
        fields = '__all__'


class PetitionSerializer(serializers.ModelSerializer):


    # Relaciones anidadas
    categories = PetitionCategorySerializer(many=True, source='petitioncategory_set', read_only=True)
    attachments = PetitionAttachmentSerializer(many=True, source="petitionattachment_set", read_only=True)
    materials = PetitionMaterialSerializer(many=True, source="petitionmaterial_set", read_only=True)
    state_history = PetitionStateHistorySerializer(many=True, source="petitionstatehistory_set", read_only=True)


    # Relaciones directas
    id_type_petition = TypePetitionSerializer(read_only=True)
    id_state = PetitionStateSerializer(read_only=True)

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
    

