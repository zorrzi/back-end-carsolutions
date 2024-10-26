# chat/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # Obtém o modelo de usuário configurado no projeto

class Chat(models.Model):
    cliente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="client_chats",
        limit_choices_to={'is_staff': False}
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat com {self.cliente.username}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_employee = models.BooleanField(default=False)

    def __str__(self):
        return f"Mensagem de {self.sender.username} em {self.timestamp}"
