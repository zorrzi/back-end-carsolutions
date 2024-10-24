from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Funcionario
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

@api_view(['POST'])
def login_funcionario(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')

    # Autentica o usuário
    user = authenticate(request, username=username, password=password)
    if user is not None and hasattr(user, 'funcionario'):
        # Se o usuário é um funcionário, faz o login e gera um token
        Token.objects.filter(user=user).delete()  # Remove token antigo, se existir
        token = Token.objects.create(user=user)  # Cria um novo token

        login(request, user)  # Faz login
        return Response({'message': 'Login realizado com sucesso!', 'token': token.key}, status=200)
    else:
        return Response({'message': 'Nome de usuário ou senha inválidos.'}, status=401)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Requer autenticação via token
def logout_funcionario(request):
    # Verifica se o token foi enviado
    if request.auth and hasattr(request.user, 'funcionario'):
        # Apaga o token associado ao funcionário
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': 'Logout realizado com sucesso!'}, status=200)
    return Response({'message': 'Usuário não está autenticado ou não é um funcionário.'}, status=403)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Requer autenticação via token
def funcionario_pagina(request):
    if not hasattr(request.user, 'funcionario'):
        return Response({'message': 'Acesso negado. Você não é um funcionário.'}, status=403)

    # Retorna dados da página do funcionário
    return Response({'message': 'Bem-vindo à página de funcionários!'}, status=200)
