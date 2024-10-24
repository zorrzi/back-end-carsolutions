from django.urls import path
from .views import agendar_visita,listar_agendamentos_cliente, listar_agendamentos_pendentes, assumir_agendamento, listar_agendamentos_funcionario

urlpatterns = [
    path('agendar/', agendar_visita, name='agendar_visita'),
    path('agendamento/', listar_agendamentos_cliente, name='listar_agendamentos_cliente'),
    path('pendentes/', listar_agendamentos_pendentes, name='listar_agendamentos_pendentes'),
    path('assumir/<int:agendamento_id>/', assumir_agendamento, name='assumir_agendamento'),
    path('meus/', listar_agendamentos_funcionario, name='listar_agendamentos_funcionario'),
]
