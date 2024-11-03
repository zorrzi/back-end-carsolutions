from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import CartaoCredito
from cliente.models import Cliente
from .serializers import CartaoCreditoSerializer
from django.shortcuts import get_object_or_404

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_cartoes(request):
    cliente = Cliente.objects.get(user=request.user)
    cartoes = CartaoCredito.objects.filter(cliente=cliente)
    serializer = CartaoCreditoSerializer(cartoes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def adicionar_cartao(request):
    cliente = Cliente.objects.get(user=request.user)
    dados_cartao = request.data['novo_cartao'] 
    serializer = CartaoCreditoSerializer(data=dados_cartao)
    print(dados_cartao)
    if serializer.is_valid():
        serializer.save(cliente=cliente)
        return Response({"message": "Cartão de crédito adicionado com sucesso!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def excluir_cartao(request, cartao_id):
    cliente = Cliente.objects.get(user=request.user)
    cartao = get_object_or_404(CartaoCredito, id=cartao_id, cliente=cliente)

    cartao.delete()
    return Response({"message": "Cartão de crédito excluído com sucesso!"}, status=status.HTTP_204_NO_CONTENT)
