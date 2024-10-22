# clientes/models.py
from django.contrib.auth.models import User
from django.db import models

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11, unique=True)  # Campo CPF único para cada cliente

    def __str__(self):
        return self.user.username
