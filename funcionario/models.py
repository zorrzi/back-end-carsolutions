from django.contrib.auth.models import User
from django.db import models

class Funcionario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Adicione outros campos específicos do funcionário, se necessário

    def __str__(self):
        return self.user.username
