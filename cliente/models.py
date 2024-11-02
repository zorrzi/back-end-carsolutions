# clientes/models.py
from django.contrib.auth.models import User
from django.db import models
from carros.models import Car

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11, unique=True)
    cnh = models.CharField(max_length=11, unique=True)
    favoritos = models.ManyToManyField(Car, related_name="favoritado_por", blank=True)
    pontos = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    
    def adicionar_pontos(self, quantidade):
        """Método para adicionar pontos ao cliente."""
        self.pontos += quantidade
        self.save()
