from django.urls import path
from .views import cadastro_cliente, login_cliente, adicionar_favorito, logout_cliente, verificar_favorito, listar_favoritos, solicitar_redefinicao_senha, redefinir_senha 

urlpatterns = [
    path('cadastro/', cadastro_cliente, name='cadastro_cliente'),
    path('login/', login_cliente, name='login_cliente'),
    path('logout/', logout_cliente, name='logout_cliente'),
    path('favoritar/<int:car_id>/', adicionar_favorito, name='adicionar_favorito'),
    path('favoritar/<int:car_id>/status/', verificar_favorito, name='verificar_favorito'),
    path('favoritos/', listar_favoritos, name='lista_favoritos'),
    path('solicitar-redefinicao-senha/', solicitar_redefinicao_senha, name='solicitar_redefinicao_senha'),
    path('redefinir-senha/<uidb64>/<token>/', redefinir_senha, name='redefinir_senha'),
    

]
