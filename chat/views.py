from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Prefetch
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    CreateMessageSerializer
)

User = get_user_model()

class ConversationViewSet(viewsets.ViewSet):
    """
    ViewSet que gestiona las operaciones relacionadas con conversaciones
    y mensajes entre usuarios autenticados.

    Permite:
        - Listar las conversaciones del usuario.
        - Obtener los mensajes de una conversación.
        - Iniciar una nueva conversación entre dos usuarios.
        - Enviar mensajes dentro de una conversación.
        - Marcar mensajes como leídos.
    """

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Lista todas las conversaciones en las que participa el usuario autenticado.

        Args:
            request (Request): Objeto de solicitud HTTP con el usuario autenticado.

        Returns:
            Response: Lista serializada de conversaciones del usuario.
        """
        conversations = (
            Conversation.objects.filter(participants=request.user)
            .prefetch_related(
                Prefetch(
                    "participants",
                    queryset=User.objects.only("id_user", "email", "name", "lastname"),
                ),
                Prefetch(
                    "messages",
                    queryset=Message.objects.select_related("sender")
                    .order_by("-created_at")[:1],
                    to_attr="prefetched_last_message",
                ),
            )
            .annotate(
                unread_total=Count(
                    "messages",
                    filter=Q(messages__read=False) & ~Q(messages__sender=request.user),
                )
            )
            .distinct()
        )
        serializer = ConversationSerializer(conversations, many=True, context={'request': request})
        return Response(serializer.data)
    
    
    def retrieve(self, request, pk=None):
        """
        Devuelve todos los mensajes de una conversación específica.

        Args:
            request (Request): Objeto de solicitud HTTP.
            pk (int): ID de la conversación.

        Returns:
            Response: Lista de mensajes serializados pertenecientes a la conversación.
        """
        conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)
        messages = conversation.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def start(self, request):
        """
        Crea una nueva conversación entre dos usuarios, o devuelve una existente si ya está creada.

        Args:
            request (Request): Objeto de solicitud HTTP con el ID del otro usuario en request.data['user_id'].

        Returns:
            Response: Datos serializados de la conversación creada o existente.
        """
        other_user_id = request.data.get('user_id')
        if not other_user_id:
            return Response({'error': 'user_id es requerido'}, status=400)
        
        # Obtener el objeto User del otro usuario
        try:
            other_user = User.objects.get(id_user=other_user_id)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=404)
        
        # Verificar que no sea el mismo usuario
        if other_user.id_user == request.user.id_user:
            return Response({'error': 'No puedes iniciar una conversación contigo mismo'}, status=400)
        
        # Buscar si ya existe una conversación entre ambos
        conversation = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants=other_user
        ).distinct().first()

        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.set([request.user, other_user])

        serializer = ConversationSerializer(conversation, context={'request': request})
        return Response(serializer.data, status=201)
    

    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        """
        Envía un nuevo mensaje dentro de una conversación existente.

        Args:
            request (Request): Objeto de solicitud HTTP con los datos del mensaje.
            pk (int): ID de la conversación.

        Returns:
            Response: Mensaje recién creado, serializado.
        """
        conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)
        serializer = CreateMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=serializer.validated_data['content']
        )
        return Response(MessageSerializer(message).data, status=201)
    

    @action(detail=True, methods=['patch'])
    def mark_as_read(self, request, pk=None):
        """
        Marca todos los mensajes de la conversación como leídos,
        exceptuando aquellos enviados por el usuario autenticado.

        Args:
            request (Request): Objeto de solicitud HTTP.
            pk (int): ID de la conversación.

        Returns:
            Response: Cantidad de mensajes actualizados a estado leído.
        """
        conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)
        unread_messages = conversation.messages.filter(read=False).exclude(sender=request.user)
        updated = unread_messages.update(read=True)
        return Response({'mensajes_actualizados': updated}, status=200)