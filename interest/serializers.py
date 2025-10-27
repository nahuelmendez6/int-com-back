from rest_framework import serializers
from .models import Interest

# ====================================================
# Serializer Interest
# ====================================================
class InterestSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Interest.

    Función:
    - Convierte los datos del modelo Interest a formato JSON para las APIs REST.
    - Permite la creación y actualización de intereses a través de la API.

    Campos incluidos: todos los campos del modelo Interest
    (id_interest, id_customer, id_category, id_user_create, 
     id_user_update, date_create, date_update, is_deleted)
    """
    class Meta:
        model = Interest
        fields = '__all__'