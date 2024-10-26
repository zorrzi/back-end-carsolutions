from django.shortcuts import render

# Create your views here.
# chat/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Chat, Message
from django.contrib.auth import get_user_model
from .serializers import ChatSerializer, MessageSerializer

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_employee_chats(request):
    # Verifica se o usuário é um funcionário
    if request.auth and hasattr(request.user, 'funcionario'):
        chats = Chat.objects.all()
        serializer = ChatSerializer(chats, many=True)
        return Response({'chats': serializer.data}, status=status.HTTP_200_OK)
    return Response({"detail": "Acesso negado."}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_client_chat(request):
    # Verifica se o usuário está autenticado
    print("Usuário autenticado:", request.user)
    
    if not request.user.is_authenticated:
        return Response({'message': 'Usuário não autenticado.'}, status=401)
    
    # Verifica se o usuário é um cliente
    cliente = getattr(request.user, 'cliente', None)
    if not cliente:
        return Response({'message': 'Usuário não é um cliente.'}, status=403)
    
    # Tenta obter o chat do cliente autenticado
    try:
        print("Procurando chat para o cliente:", request.user)
        chat = Chat.objects.get(cliente=request.user)
        serializer = ChatSerializer(chat)
        return Response({'chat': serializer.data}, status=status.HTTP_200_OK)
    except Chat.DoesNotExist:
        print("Chat não encontrado para o cliente:", request.user)
        return Response({'message': 'Chat não encontrado.'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request, chat_id):
    # Verifica se o chat existe
    try:
        chat = Chat.objects.get(id=chat_id)
    except Chat.DoesNotExist:
        return Response({"detail": "Chat não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    # Determina se o remetente é funcionário ou cliente
    is_employee = True if request.auth and hasattr(request.user, 'funcionario') else False
    content = request.data.get('content', '').strip()

    if content:
        message = Message.objects.create(
            chat=chat,
            sender=request.user,
            content=content,
            is_employee=is_employee
        )
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response({"detail": "Conteúdo da mensagem está vazio."}, status=status.HTTP_400_BAD_REQUEST)

# views.py

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def iniciar_chat(request):
    # Verifica se o cliente já tem um chat ativo
    if Chat.objects.filter(cliente=request.user).exists():
        return Response({"detail": "Chat já existe."}, status=status.HTTP_400_BAD_REQUEST)

    # Cria um novo chat
    chat = Chat.objects.create(cliente=request.user)
    serializer = ChatSerializer(chat)
    return Response({"chat": serializer.data}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_messages(request, chat_id):
    try:
        # Verifica se o usuário é um funcionário
        is_employee = hasattr(request.user, 'funcionario')  # Supondo que 'funcionario' seja o atributo que indica o usuário funcionário

        if is_employee:
            # Se o usuário for um funcionário, ele pode acessar qualquer chat pelo ID
            chat = Chat.objects.get(id=chat_id)
        else:
            # Se for um cliente, ele só pode acessar o chat se for o dono
            chat = Chat.objects.get(id=chat_id, cliente=request.user)
        
        serializer = ChatSerializer(chat)
        return Response({'chat': serializer.data}, status=status.HTTP_200_OK)
    
    except Chat.DoesNotExist:
        return Response({"detail": "Chat não encontrado."}, status=status.HTTP_404_NOT_FOUND)
