from django.db import models
from django.contrib.auth.models import User
from carros.models import Car

class Agendamento(models.Model):
    TIPO_AGENDAMENTO = [
        ('visita', 'Visita'),
        ('reserva', 'Reserva'),  # Alteração de 'venda' para 'reserva'
        ('aluguel', 'Aluguel'),
    ]

    STATUS_AGENDAMENTO = [
        ('pendente', 'Pendente'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
        ('em atendimento', 'Em Atendimento'),
    ]

    carro = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    carro_marca = models.CharField(max_length=100, null=True, blank=True)  # Marca do carro
    carro_modelo = models.CharField(max_length=100, null=True, blank=True)  # Modelo do carro
    carro_preco = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Preço do carro
    carro_ano = models.IntegerField(null=True, blank=True) # Ano do carro


    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agendamentos_cliente')
    funcionario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='agendamentos_funcionario')
    data = models.DateField(null=True, blank=True)  # Data da visita ou reserva
    horario = models.TimeField(null=True, blank=True)  # Horário da visita
    data_retirada = models.DateField(null=True, blank=True)  # Data de retirada para aluguel
    horario_retirada = models.TimeField(null=True, blank=True)  # Horário de retirada
    data_devolucao = models.DateField(null=True, blank=True)  # Data de devolução para aluguel
    horario_devolucao = models.TimeField(null=True, blank=True)  # Horário de devolução
    valor_agendamento = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Preço com desconto
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Preço final
    tipo = models.CharField(max_length=7, choices=TIPO_AGENDAMENTO)
    status = models.CharField(max_length=15, choices=STATUS_AGENDAMENTO, default='pendente')
    data_expiracao = models.DateField(null=True, blank=True)  # Data de expiração para a reserva
    feedbackEnviado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario.username} - {self.carro.model} - {self.tipo}"


class Feedback(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE)
    comentario = models.TextField(blank=True, null=True)
    nota = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    

    def __str__(self):
        return f"{self.usuario.username} - Nota: {self.nota} - Agendamento ID: {self.agendamento.id}"