# clientes/views.py
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Cliente
from carros.models import Car
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def cadastro_cliente(request):
    data = request.data
    username = data.get('username')
    password = data.get('senha')
    confirm_password = data.get('confirmar_senha')
    email = data.get('email')
    cpf = data.get('cpf')
    cnh = data.get('cnh')  # Novo campo para CNH

    # Validações
    if password != confirm_password:
        return Response({'message': 'As senhas não coincidem.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'message': 'Usuário já existe.'}, status=status.HTTP_400_BAD_REQUEST)

    if Cliente.objects.filter(cpf=cpf).exists():
        return Response({'message': 'CPF já está cadastrado.'}, status=status.HTTP_400_BAD_REQUEST)
        
    if Cliente.objects.filter(cnh=cnh).exists():
        return Response({'message': 'CNH já está cadastrada.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    Cliente.objects.create(user=user, cpf=cpf, cnh=cnh)

    token, created = Token.objects.get_or_create(user=user)
    return Response({'message': 'Cadastro realizado com sucesso!', 'token': token.key}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_cliente(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')

    print(username)
    print(password)

    # Autentica o usuário
    user = authenticate(request, username=username, password=password)
    print('autenticado')
    print(user)

    if user is not None and hasattr(user, 'cliente'):
        print('tem cliente')
        # Gera ou recria o token (sempre cria um novo token)
        Token.objects.filter(user=user).delete()  # Remove o token antigo, se existir
        token = Token.objects.create(user=user)   # Cria um novo token para o login

        return Response({'message': 'Login realizado com sucesso!', 'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Erro ao fazer login. Verifique os dados e tente novamente.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout_cliente(request):
    print(request.auth)
    # Verifica se o token foi enviado
    if request.auth:
        try:
            # Apaga o token associado ao usuário autenticado
            request.user.auth_token.delete()
            return Response({'message': 'Logout realizado com sucesso!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Erro ao fazer logout.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Token não encontrado.'}, status=status.HTTP_400_BAD_REQUEST)
    

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
    


@api_view(['GET'])
def listar_favoritos(request):
    print(request.user)
    try:
        # Busca o cliente autenticado
        cliente = Cliente.objects.get(user=request.user)
        # Obtém todos os carros favoritados pelo cliente
        favoritos = cliente.favoritos.all()
        # Serializa os dados dos carros favoritos
        data = [{"id": car.id, "brand": car.brand, "model": car.model, "year": car.year, "image_url": car.image_url, "is_for_rent": car.is_for_rent, "is_for_sale":car.is_for_sale} for car in favoritos]
        return Response(data, status=status.HTTP_200_OK)
    except Cliente.DoesNotExist:
        return Response({"error": "Cliente não encontrado."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
