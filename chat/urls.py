# chat/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Rota para funcionários verem todos os chats
    path('funcionario/', views.get_employee_chats, name='get_employee_chats'),

    # Rota para clientes verem o próprio chat
    path('cliente/', views.get_client_chat, name='get_client_chat'),

    # Rota para envio de mensagem em um chat específico (usado tanto por clientes quanto funcionários)
    path('send/<int:chat_id>/', views.send_message, name='send_message'),

    path('iniciar/', views.iniciar_chat, name='iniciar_chat'),

    path('cliente/<int:chat_id>/', views.get_chat_messages, name='get_chat_messages')
]
