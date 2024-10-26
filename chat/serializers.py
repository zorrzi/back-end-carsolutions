# chat/serializers.py

from rest_framework import serializers
from .models import Chat, Message

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()  # Para exibir o nome do remetente
    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'content', 'timestamp', 'is_employee']

class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)  # Inclui todas as mensagens do chat
    cliente = serializers.StringRelatedField()  # Exibe o nome do cliente

    class Meta:
        model = Chat
        fields = ['id', 'cliente', 'criado_em', 'messages']
