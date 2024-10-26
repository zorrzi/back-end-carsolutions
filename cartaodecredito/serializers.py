from rest_framework import serializers
from .models import CartaoCredito

class CartaoCreditoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartaoCredito
        fields = ['id', 'numero_cartao', 'nome_titular', 'data_validade', 'codigo_seguranca', 'salvar_para_futuro', 'nome_cartao']
        extra_kwargs = {
            'codigo_seguranca': {'write_only': True},
            'numero_cartao': {'write_only': True}
        }
