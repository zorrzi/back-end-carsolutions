# clientes/views.py
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Cliente
from carros.models import Car
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

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

@api_view(['POST'])
def logout_cliente(request):
    logout(request)
    return Response({'message': 'Logout realizado com sucesso!'}, status=200)
    

@api_view(['POST'])
def adicionar_favorito(request, car_id):
    print(request.user)
    if not request.user.is_authenticated:
        return Response({'message': 'Usuário não autenticado.'}, status=401)

    cliente = getattr(request.user, 'cliente', None)
    if not cliente:
        return Response({'message': 'Usuário não é um cliente.'}, status=403)

    try:
        car = Car.objects.get(id=car_id)
        
        # Verifica se o carro já está nos favoritos
        if car in cliente.favoritos.all():
            cliente.favoritos.remove(car)
            return Response({'message': 'Carro removido dos favoritos com sucesso!'}, status=200)
        else:
            cliente.favoritos.add(car)
            return Response({'message': 'Carro adicionado aos favoritos com sucesso!'}, status=200)
        
    except Car.DoesNotExist:
        return Response({'message': 'Carro não encontrado.'}, status=404)


@api_view(['GET'])
def verificar_favorito(request, car_id):
    try:
        cliente = request.user.cliente
        carro = Car.objects.get(id=car_id)
        is_favorito = carro in cliente.favoritos.all()
        return Response({'isFavorito': is_favorito}, status=200)
    except Car.DoesNotExist:
        return Response({'message': 'Carro não encontrado.'}, status=404)
    except Cliente.DoesNotExist:
        return Response({'message': 'Cliente não encontrado.'}, status=404)