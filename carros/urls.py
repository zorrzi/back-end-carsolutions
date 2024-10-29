from django.urls import path
from . import views

urlpatterns = [
    path('', views.car_create, name='car-create'),
    path('<int:id>/', views.car_update_delete, name='car-update-delete'),
    path('years/', views.get_all_years, name='get-all-years'),
    path('brands/<int:ano>/', views.get_all_brands_by_year, name='get-brands-by-year'),  # Passa o ano diretamente na URL
    path('models/<int:ano>/<str:marca>/', views.get_all_models_by_year_and_brand, name='get-models-by-year-and-brand'),  # Passa ano e marca diretamente na URL
    path('buscar/<int:ano>', views.get_all_cars_by_year, name='get-cars-by-year'),  # Passa o ano diretamente na URL
    path('buscar/<int:ano>/<str:marca>', views.get_all_cars_by_year_and_brand, name='get-cars-by-year-and-brand'),  # Passa ano e marca diretamente na URL
    path('buscar/<int:ano>/<str:marca>/<str:modelo>', views.get_all_cars_by_year_brand_and_model, name='get-cars-by-year-brand-and-model'),  # Passa ano, marca e modelo diretamente na URL
    path('catalogo/', views.car_list, name='get-catalog'),
    path('delete-em-massa/', views.delete_em_massa, name='bulk_delete_cars'),
    path('reserve/<int:id>/', views.reserve_car, name='reserve-car'),

]

