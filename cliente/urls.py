from django.urls import path
from .views import cadastro_cliente, login_cliente

urlpatterns = [
    path('cadastro/', cadastro_cliente, name='cadastro_cliente'),
    path('login/', login_cliente, name='login_cliente'),
]
