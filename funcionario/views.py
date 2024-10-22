from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Funcionario

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
