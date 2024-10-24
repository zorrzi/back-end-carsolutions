from django.urls import path
from .views import agendar_visita, listar_agendamentos_cliente

urlpatterns = [
    path('agendar/', agendar_visita, name='agendar_visita'),
    path('agendamento/', listar_agendamentos_cliente, name='listar_agendamentos_cliente'),
]
