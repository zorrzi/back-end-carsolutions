from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Car
from .serializers import CarSerializer
from .utils import get_car_info
from django.http import JsonResponse
from decimal import Decimal, InvalidOperation
import datetime
import agendamentos.models as agendamentos  # Importa o módulo de agendamentos


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


# Retorna todos os anos disponíveis por ordem crescente de carros que estão disponíveis is reserved = False
@api_view(['GET'])
def get_all_years(request):
    anos = Car.objects.filter(is_reserved=False).values_list('year', flat=True).distinct().order_by('year')
    return Response(anos)



# Retorna todas as marcas disponíveis (parâmetro na URL) de carros que estão disponíveis is reserved = False
@api_view(['GET'])
def get_all_brands_by_year(request, ano):
    marcas = Car.objects.filter(is_reserved=False).values_list('brand', flat=True).distinct()
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
        marcas = Car.objects.filter(is_reserved=False).values_list('brand', flat=True).distinct()
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
        queryset = queryset.filter(year=ano, is_reserved=False)
    if marca:
        queryset = queryset.filter(brand=marca, is_reserved=False)
    
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

@api_view(['GET'])
def car_list(request):
    is_for_sale = request.GET.get('isForSale', 'true') == 'true'
    is_for_rent = request.GET.get('isForRent', 'true') == 'true'
    min_rental_price = request.GET.get('minRentPrice', None)
    max_rental_price = request.GET.get('maxRentPrice', None)
    data_inicial = request.GET.get('startDate', None)
    data_final = request.GET.get('endDate', None)
    min_purchase_price = request.GET.get('minSalePrice', None)
    max_purchase_price = request.GET.get('maxSalePrice', None)
    min_mileage = request.GET.get('minMileage', None)
    max_mileage = request.GET.get('maxMileage', None)
    brand = request.GET.get('brand', None)
    model = request.GET.get('model', None)
    year = request.GET.get('year', None)

    # Filtro inicial
    queryset = Car.objects.filter(is_reserved=False)  # Exclui carros reservados

    # Aplica os filtros com base nos parâmetros recebidos
    if is_for_sale:
        queryset = queryset.filter(is_for_sale=True)
    if is_for_rent:
        queryset = queryset.filter(is_for_rent=True)
    if min_rental_price and max_rental_price:
        queryset = queryset.filter(rental_price__gte=min_rental_price, rental_price__lte=max_rental_price)

    # Filtra carros disponíveis no intervalo de datas especificado
    if data_inicial and data_final:
        # Converte as datas e horas para objetos datetime
        data_inicio_completa = datetime.datetime.strptime(f"{data_inicial}", "%Y-%m-%d")
        data_final_completa = datetime.datetime.strptime(f"{data_final}", "%Y-%m-%d")

        # Obtém IDs de carros que estão com agendamentos conflitantes no período especificado
        carros_indisponiveis_ids = agendamentos.Agendamento.objects.filter(
            data_retirada__lt=data_final_completa,
            data_devolucao__gt=data_inicio_completa
        ).values_list('carro_id', flat=True)

        # Exclui carros indisponíveis no período
        queryset = queryset.exclude(id__in=carros_indisponiveis_ids)

    if min_purchase_price and max_purchase_price:
        queryset = queryset.filter(purchase_price__gte=min_purchase_price, purchase_price__lte=max_purchase_price)
    if min_mileage is not None and max_mileage is not None:
        queryset = queryset.filter(mileage__gte=min_mileage, mileage__lte=max_mileage)
    if brand:
        queryset = queryset.filter(brand__icontains=brand)
    if model:
        queryset = queryset.filter(model__icontains=model)
    if year:
        queryset = queryset.filter(year=year)

    # Serializa os dados filtrados
    serializer = CarSerializer(queryset, many=True)
    return Response(serializer.data)




@api_view(['DELETE'])
def delete_em_massa(request):
    car_ids = request.data.get('ids', [])
    if not car_ids:
        return Response({"error": "No car IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

    Car.objects.filter(id__in=car_ids).delete()
    return Response({"message": "Selected cars deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def reserve_car(request, id):
    try:
        car = Car.objects.get(id=id)
    except Car.DoesNotExist:
        return Response({"error": "Carro não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    if car.is_reserved:
        return Response({"error": "Carro já está reservado."}, status=status.HTTP_400_BAD_REQUEST)

    # Marca o carro como reservado
    car.is_reserved = True
    car.save()

    return Response({"message": "Carro reservado com sucesso!"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def apply_discount(request):
    ids = request.data.get("ids", [])
    discount_type = request.data.get("discount_type")
    discount_percentage = request.data.get("discount_percentage")

    if not ids or discount_type not in ["purchase", "rental"] or discount_percentage is None:
        return Response({"error": "Dados inválidos."}, status=400)

    cars = Car.objects.filter(id__in=ids)
    for car in cars:
        # Aplicar o desconto de acordo com o tipo e disponibilidade do carro
        if discount_type == "purchase" and car.is_for_sale:
            car.is_discounted_sale = True
            car.discount_percentage_sale = discount_percentage
        elif discount_type == "rental" and car.is_for_rent:
            car.is_discounted_rent = True
            car.discount_percentage_rent = discount_percentage
        else:
            # Ignorar carros não disponíveis para o tipo de desconto solicitado
            continue
        car.save()

    return Response({"success": "Desconto aplicado com sucesso."})


@api_view(['PATCH'])
def remove_discount(request, car_id):
    try:
        # Obtém o carro pelo ID
        car = Car.objects.get(id=car_id)
        
        # Remove todos os descontos
        car.is_discounted_sale = False
        car.discount_percentage_sale = None
        car.is_discounted_rent = False
        car.discount_percentage_rent = None
        car.save()
        
        return Response({"success": "Desconto removido com sucesso."}, status=status.HTTP_200_OK)
    except Car.DoesNotExist:
        return Response({"error": "Carro não encontrado."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def carros_similares(request, car_id):
    try:
        carro_atual = Car.objects.get(id=car_id)
    except Car.DoesNotExist:
        return Response({"error": "Carro não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    carros_similares = Car.objects.filter(brand=carro_atual.brand).exclude(id=car_id)[:5]  # Limita a 5 carros similares
    serializer = CarSerializer(carros_similares, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)