from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cliente.urls')), 
    path('cars/', include('carros.urls')),
    path('', include('funcionario.urls')),
    path('agendamentos/', include('agendamentos.urls')),
    path('cartaodecredito/', include('cartaodecredito.urls')),
    
]
