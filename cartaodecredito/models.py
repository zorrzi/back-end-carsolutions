from django.db import models
from cliente.models import Cliente

class CartaoCredito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='cartoes')
    numero_cartao = models.CharField(max_length=16)
    nome_titular = models.CharField(max_length=100)
    data_validade = models.DateField()
    codigo_seguranca = models.CharField(max_length=3)
    salvar_para_futuro = models.BooleanField(default=False)
    nome_cartao = models.CharField(max_length=50, blank=True) 

    def __str__(self):
        return f"{self.nome_cartao if self.nome_cartao else f'Cartão {self.numero_cartao[-4:]}' } - {self.nome_titular}"
