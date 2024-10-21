from rest_framework import serializers
from .models import Cliente

class ClienteCreateSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True)
    confirmar_senha = serializers.CharField(write_only=True)
    cpf = serializers.CharField(write_only=True)

    class Meta:
        model = Cliente
        fields = ['username', 'email', 'cpf', 'senha', 'confirmar_senha']

    def validate(self, data):
        if data['senha'] != data['confirmar_senha']:
            raise serializers.ValidationError("As senhas não coincidem.")
        if len(data['cpf']) != 11:
            raise serializers.ValidationError("O CPF deve ter 11 dígitos.")
        return data

    def create(self, validated_data):
        cliente = Cliente(
            username=validated_data['username'],
            email=validated_data['email'],
            cpf=validated_data['cpf'],
        )
        cliente.set_password(validated_data['senha'])
        cliente.save()
        return cliente
