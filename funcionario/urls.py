# funcionarios/urls.py
from django.urls import path
from .views import login_funcionario

urlpatterns = [
    path('loginFuncionario/', login_funcionario, name='login_funcionario'),
]
