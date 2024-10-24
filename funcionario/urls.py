# funcionarios/urls.py
from django.urls import path
from .views import login_funcionario, logout_funcionario, funcionario_pagina

urlpatterns = [
    path('loginFuncionario/', login_funcionario, name='login_funcionario'),
    path('logoutFuncionario/', logout_funcionario, name='logout_funcionario'),
    path('funcionario/', funcionario_pagina, name='funcionario_pagina'),
]
