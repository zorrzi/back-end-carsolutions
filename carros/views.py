from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Car
from .serializers import CarSerializer
from .utils import get_car_info
from django.http import JsonResponse

@api_view(['GET', 'POST'])
def car_create(request):
    if request.method == 'GET':
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)  
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def car_update_delete(request, id):
    try:
        car = Car.objects.get(id=id)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CarSerializer(car)
        ficha = get_car_info(car.brand, car.model, car.year)
        if ficha == None:
            return Response(serializer.data)
        else:
            res = {**serializer.data, **ficha}
            return JsonResponse(res)

    if request.method == 'PUT':
        serializer = CarSerializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Retorna todos os anos disponíveis
@api_view(['GET'])
def get_all_years(request):
    anos = Car.objects.values_list('year', flat=True).distinct()
    return Response(anos)


# Retorna todas as marcas disponíveis para um ano específico (parâmetro na URL)
@api_view(['GET'])
def get_all_brands_by_year(request, ano):
    # Filtra as marcas de acordo com o ano fornecido pela URL
    marcas = Car.objects.filter(year=ano).values_list('brand', flat=True).distinct()
    return Response(marcas)


# Retorna todos os modelos disponíveis filtrados por ano e marca (parâmetros na URL)
@api_view(['GET'])
def get_all_models_by_year_and_brand(request, ano, marca):
    # Filtra os modelos de acordo com o ano e a marca fornecidos na URL
    modelos = Car.objects.filter(year=ano, brand=marca).values_list('model', flat=True).distinct()
    return Response(modelos)


# Função original para marcas, caso você ainda queira usá-la com query strings
@api_view(['GET'])
def get_all_brands(request):
    ano = request.GET.get('ano', None)  # Pega o parâmetro 'ano' da query string
    if ano:
        marcas = Car.objects.filter(year=ano).values_list('brand', flat=True).distinct()
    else:
        marcas = Car.objects.values_list('brand', flat=True).distinct()
    return Response(marcas)


# Função original para modelos, caso você ainda queira usá-la com query strings
@api_view(['GET'])
def get_all_models(request):
    ano = request.GET.get('ano', None)  # Pega o parâmetro 'ano'
    marca = request.GET.get('marca', None)  # Pega o parâmetro 'marca'

    queryset = Car.objects.all()
    if ano:
        queryset = queryset.filter(year=ano)
    if marca:
        queryset = queryset.filter(brand=marca)
    
    modelos = queryset.values_list('model', flat=True).distinct()
    return Response(modelos)

@api_view(['GET'])
def get_all_cars_by_year(request, ano):
    cars = Car.objects.filter(year=ano)
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_all_cars_by_year_and_brand(request, ano, marca):
    cars = Car.objects.filter(year=ano, brand=marca)
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_all_cars_by_year_brand_and_model(request, ano, marca, modelo):
    cars = Car.objects.filter(year=ano, brand=marca, model=modelo)
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)