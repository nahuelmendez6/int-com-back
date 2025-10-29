from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    CreateMessageSerializer
)

class ConversationViewSewt(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """ Lista todas las conversaciones donde participa el usuario autenticado"""
        converstions = Conversation.objects.filter(participants=request.user).distinct()
        serializer = ConversationSerializer(converstions, many=True, context={'request': request})
        return Response(serializer.data)
    
    
    def retrieve(self, request, pk=None):
        """Devuelve todos los mensajes de una conversacion"""
        conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)
        messages = conversation.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def start(self, request):
        """
        Crea o devuelve una conversacion existente entre dos usuarios
        """
        other_user_id = request.data.get('user_id')
        if not other_user_id:
            return Response({'error': 'user_id es requerido'}, status=400)
        
        # Buscar si ya existe una conversación entre ambos
        conversation = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants=other_user_id
        ).distinct().first()

        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.set([request.user.id, other_user_id])

        serializer = ConversationSerializer(conversation, context={'request': request})
        return Response(serializer.data, status=201)
    

    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        """Envía un mensaje en una conversación existente."""
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
        """Marca todos los mensajes de la conversación como leídos (excepto los enviados por el usuario)."""
        conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)
        unread_messages = conversation.messages.filter(read=False).exclude(sender=request.user)
        updated = unread_messages.update(read=True)
        return Response({'mensajes_actualizados': updated}, status=200)