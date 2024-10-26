from django.urls import path
from .views import agendar_visita, reservar_veiculo, reservar_aluguel, listar_agendamentos_cliente, listar_agendamentos_pendentes, assumir_agendamento, listar_atendimentos_funcionario
 

urlpatterns = [
    path('agendar/visita/', agendar_visita, name='agendar_visita'),
    path('reservar/veiculo/', reservar_veiculo, name='reservar_veiculo'),
    path('reservar/aluguel/', reservar_aluguel, name='reservar_aluguel'),
    path('agendamento/', listar_agendamentos_cliente, name='listar_agendamentos'),
    path('agendamento/pendentes/', listar_agendamentos_pendentes, name='listar_agendamentos_pendentes'),
    path('agendamento/assumir/<int:agendamento_id>/', assumir_agendamento, name='assumir_agendamento'),
    path('agendamento/meus/', listar_atendimentos_funcionario, name='listar_atendimentos_funcionario'),
]
