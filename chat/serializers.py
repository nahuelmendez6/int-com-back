from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()

class UserSimpleSerializer(serializers.ModelSerializer):
    """
    Serializador simple para el modelo de usuario.

    Incluye solo los campos básicos para identificar al usuario,
    utilizado principalmente en los listados de conversaciones y mensajes.
    """
    class Meta:
        model = User
        fields = ['id_user', 'email', 'name', 'lastname']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Message.

    Incluye la información del remitente (serializada mediante UserSimpleSerializer)
    y los datos principales del mensaje.
    """
    sender = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id_message', 'sender', 'content', 'created_at', 'read']


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Conversation.

    Incluye los participantes de la conversación, el último mensaje y
    el conteo de mensajes no leídos por el usuario autenticado.

    Campos adicionales:
        last_message (SerializerMethodField): Último mensaje de la conversación.
        unread_count (SerializerMethodField): Cantidad de mensajes no leídos.
    """

    participants = UserSimpleSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()


    class Meta:
        model = Conversation
        fields = ['id_conversation', 'participants', 'created_at', 'last_message', 'unread_count']

    def get_last_message(self, obj):
        """
        Obtiene el último mensaje enviado en la conversación.

        Args:
            obj (Conversation): Instancia de la conversación.

        Returns:
            dict | None: Datos serializados del último mensaje, o None si no existen mensajes.
        """
        last_msg = obj.messages.last()
        return MessageSerializer(last_msg).data if last_msg else None

    def get_unread_count(self, obj):
        """
        Calcula la cantidad de mensajes no leídos en la conversación
        por el usuario autenticado.

        Args:
            obj (Conversation): Instancia de la conversación.

        Returns:
            int: Número de mensajes no leídos.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.messages.filter(read=False).exclude(sender=request.user).count()
        return 0
    

class CreateMessageSerializer(serializers.ModelSerializer):
    """
    Serializador utilizado para crear nuevos mensajes.

    Solo incluye el campo 'content', ya que el remitente y la conversación
    se asignan en la vista o el método de creación correspondiente.
    """
    class Meta:
        model = Message
        fields = ['content']