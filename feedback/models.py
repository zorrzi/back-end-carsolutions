from django.db import models
from django.contrib.auth.models import User
from .models import Agendamento

class Feedback(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE)
    comentario = models.TextField(blank=True, null=True)
    nota = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    def __str__(self):
        return f"{self.usuario.username} - Nota: {self.nota} - Agendamento ID: {self.agendamento.id}"
