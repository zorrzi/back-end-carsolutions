from django.urls import path
from . import views

urlpatterns = [
    path('', views.car_create, name='car-create'),
    path('<int:id>/', views.car_update_delete, name='car-update-delete'),
]
