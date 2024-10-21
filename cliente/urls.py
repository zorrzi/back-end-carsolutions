from django.urls import path
from .views import cadastrar_cliente, login_cliente

urlpatterns = [
    path('cadastro/', cadastrar_cliente, name='cadastrar_cliente'),
    path('login/', login_cliente, name='login_cliente'),
]
