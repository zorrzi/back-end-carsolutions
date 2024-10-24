from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Funcionario
from django.contrib.auth.decorators import login_required

@api_view(['POST'])
def login_funcionario(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')

    # Autentica o usuário
    user = authenticate(request, username=username, password=password)
    if user is not None and hasattr(user, 'funcionario'):
        # Se o usuário é um funcionário, faz o login
        login(request, user)
        return Response({'message': 'Login realizado com sucesso!'}, status=200)
    else:
        return Response({'message': 'Nome de usuário ou senha inválidos.'}, status=401)


@api_view(['POST'])
def logout_funcionario(request):
    # Verifica se o usuário está autenticado
    if request.user.is_authenticated and hasattr(request.user, 'funcionario'):
        # Realiza o logout
        logout(request)
        return Response({'message': 'Logout realizado com sucesso!'}, status=200)
    return Response({'message': 'Usuário não está autenticado ou não é um funcionário.'}, status=403)


@api_view(['GET'])
@login_required  # Verifica se o usuário está autenticado
def funcionario_pagina(request):
    if not hasattr(request.user, 'funcionario'):
        return Response({'message': 'Acesso negado. Você não é um funcionário.'}, status=403)
    
    # Retorna dados da página do funcionário
    return Response({'message': 'Bem-vindo à página de funcionários!'}, status=200)