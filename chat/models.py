from django.db import models
from django.conf import settings

# Modelo que representa una conversación entre usuarios
class Conversation(models.Model):
    """
    Modelo que representa una conversación entre usuarios.

    Atributos:
        id_conversation (AutoField): Identificador único de la conversación.
        participants (ManyToManyField): Usuarios participantes de la conversación.
        created_at (DateTimeField): Fecha y hora en que se creó la conversación.

    Métodos:
        __str__(): Devuelve una representación legible de la conversación.
        get_other_participant(user): Devuelve el otro participante distinto al usuario dado.
    """

    id_conversation = models.AutoField(primary_key=True)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Metadatos del modelo Conversation.
        """
        db_table = 'n_conversation'
        ordering = ['-created_at']
        managed = False

    def __str__(self):
        """
        Devuelve una representación en texto de la conversación,
        mostrando los correos electrónicos de los participantes.

        Returns:
            str: Cadena con el ID de la conversación y los correos de los participantes.
        """
        participants = ", ".join([u.email for u in self.partipants.all()])
        return f"Conversación {self.id_conversation} ({participants})"
    
    def get_other_participant(self, user):

        """
        Devuelve el otro participante distinto del usuario dado.

        Args:
            user (User): Usuario actual.

        Returns:
            User | None: El otro participante de la conversación, o None si no existe.
        """
        return self.partipants.exclude(id_user=user.id_user).first()
    

class Message(models.Model):

    """
    Modelo que representa un mensaje dentro de una conversación.

    Atributos:
        id_message (AutoField): Identificador único del mensaje.
        conversation (ForeignKey): Referencia a la conversación correspondiente.
        sender (ForeignKey): Usuario que envió el mensaje.
        content (TextField): Contenido del mensaje.
        created_at (DateTimeField): Fecha y hora en que se creó el mensaje.
        read (BooleanField): Indica si el mensaje fue leído por el destinatario.

    Métodos:
        __str__(): Devuelve una representación breve del mensaje.
    """

    id_message = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        db_table = 'n_message'
        ordering = ['created_at']
        managed = False

    def __str__(self):
        """
        Devuelve una representación legible del mensaje.

        Returns:
            str: Correo del remitente y los primeros 20 caracteres del contenido.
        """
        return f"{self.sender.email}: {self.content[:20]}"