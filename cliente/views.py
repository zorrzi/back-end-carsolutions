# clientes/views.py
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cliente

@api_view(['POST'])
def cadastro_cliente(request):
    data = request.data
    username = data.get('username')
    password = data.get('senha')
    confirm_password = data.get('confirmar_senha')  # Campo para confirmar senha
    email = data.get('email')
    cpf = data.get('cpf')
    print(data)
    print(password, confirm_password)
    

    
    # Validações básicas
    if password != confirm_password:
        print('a')
        return Response({'message': 'As senhas não coincidem.'}, status=400)
    
    if User.objects.filter(username=username).exists():
        print('b')
        return Response({'message': 'Usuário já existe.'}, status=400)
    
    if Cliente.objects.filter(cpf=cpf).exists():
        print('c')
        return Response({'message': 'CPF já está cadastrado.'}, status=400)

    # Criação do usuário e cliente
    
    user = User.objects.create_user(username=username, password=password, email=email)
    print(user)
    Cliente.objects.create(user=user, cpf=cpf)
    return Response({'message': 'Cadastro realizado com sucesso!'}, status=201)

@api_view(['POST'])
def login_cliente(request):
    data = request.data
    username = data.get('username')
    password = data.get('senha')

    user = authenticate(request, username=username, password=password)
    if user is not None and hasattr(user, 'cliente'):
        login(request, user)
        return Response({'message': 'Login realizado com sucesso!'}, status=200)
    else:
        return Response({'message': 'Erro ao fazer login. Verifique os dados e tente novamente.'}, status=401)
