from django.db import models
from django.contrib.auth.models import User
from carros.models import Car

class Agendamento(models.Model):
    TIPO_AGENDAMENTO = [
        ('venda', 'Venda'),
        ('aluguel', 'Aluguel'),
    ]

    STATUS_AGENDAMENTO = [
        ('pendente', 'Pendente'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]

    carro = models.ForeignKey(Car, on_delete=models.CASCADE)  # Relacionamento com o modelo Car
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuário que realizou o agendamento
    data = models.DateField(null=True, blank=True)  # Data da visita (para venda)
    horario = models.TimeField(null=True, blank=True)  # Horário da visita (para venda)
    data_retirada = models.DateField(null=True, blank=True)  # Data de retirada (para aluguel)
    horario_retirada = models.TimeField(null=True, blank=True)  # Horário de retirada (para aluguel)
    data_devolucao = models.DateField(null=True, blank=True)  # Data de devolução (para aluguel)
    horario_devolucao = models.TimeField(null=True, blank=True)  # Horário de devolução (para aluguel)
    tipo = models.CharField(max_length=7, choices=TIPO_AGENDAMENTO)  # Se é venda ou aluguel
    status = models.CharField(max_length=10, choices=STATUS_AGENDAMENTO, default='pendente')  # Status do agendamento

    def __str__(self):
        return f"{self.usuario.username} - {self.carro.model} - {self.tipo}"
