from django.urls import path
from .views import listar_cartoes, adicionar_cartao, excluir_cartao

urlpatterns = [
    path('listar/', listar_cartoes, name='listar_cartoes'),
    path('adicionar/', adicionar_cartao, name='adicionar_cartao'),
    path('excluir/<int:cartao_id>/', excluir_cartao, name='excluir_cartao'),
]
