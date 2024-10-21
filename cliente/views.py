from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from .models import Cliente
from .serializers import ClienteCreateSerializer
from django.contrib.auth import get_user_model

@api_view(['POST'])
def cadastrar_cliente(request):
    serializer = ClienteCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Cliente cadastrado com sucesso!'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_cliente(request):
    username = request.data.get('username')
    senha = request.data.get('senha')

    if not username or not senha:
        return Response({'error': 'Username e senha são obrigatórios'}, status=status.HTTP_400_BAD_REQUEST)

    # Autentica o usuário com base no username e senha
    user = authenticate(username=username, password=senha)
    print(user, username, senha)


    if user is not None:
        login(request, user)
        return Response({'message': 'Login realizado com sucesso!'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Usuário ou senha incorretos'}, status=status.HTTP_400_BAD_REQUEST)