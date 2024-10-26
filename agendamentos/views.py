import datetime
from django.shortcuts import get_object_or_404
from cartaodecredito.serializers import CartaoCreditoSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Agendamento, Car
from cartaodecredito.models import CartaoCredito
from cliente.models import Cliente

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def agendar_visita(request):
    usuario = request.user
    carro_id = request.data.get('carro_id')
    data = request.data.get('data')
    horario = request.data.get('horario')

    if not data or not horario:
        return Response({"error": "Data e horário são obrigatórios para a visita."}, status=status.HTTP_400_BAD_REQUEST)

    carro = get_object_or_404(Car, id=carro_id)
    agendamento = Agendamento.objects.create(
        carro=carro,
        usuario=usuario,
        data=data,
        horario=horario,
        tipo='visita',
        status='pendente'
    )
    return Response({"message": "Visita agendada com sucesso!"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reservar_veiculo(request):
    print(request.data)
    usuario = request.user
    cliente = Cliente.objects.get(user=usuario)
    carro_id = request.data.get('carro_id')
    cartao_id = request.data.get('cartao_id')
    novo_cartao_dados = request.data.get('novo_cartao')

    if not carro_id:
        return Response({"error": "ID do carro é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

    # Verifica se está usando um cartão salvo ou adicionando um novo
    if cartao_id:
        cartao = get_object_or_404(CartaoCredito, id=cartao_id, cliente=cliente)
    elif novo_cartao_dados:
        serializer = CartaoCreditoSerializer(data=novo_cartao_dados)
        if serializer.is_valid():
            cartao = serializer.save(cliente=cliente)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Cartão de crédito é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

    # Calcula o prazo de 14 dias para a reserva
    data_reserva = datetime.date.today()
    data_expiracao = data_reserva + datetime.timedelta(days=14)

    carro = get_object_or_404(Car, id=carro_id)
    Agendamento.objects.create(
        carro=carro,
        usuario=usuario,
        tipo='reserva',
        data=data_reserva,
        data_expiracao=data_expiracao,
        status='pendente'
    )
    
    return Response({"message": "Reserva de veículo realizada com sucesso!"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reservar_aluguel(request):
    usuario = request.user
    cliente = Cliente.objects.get(user=usuario)
    carro_id = request.data.get('carro_id')
    data_retirada = request.data.get('data_retirada')
    horario_retirada = request.data.get('horario_retirada')
    data_devolucao = request.data.get('data_devolucao')
    horario_devolucao = request.data.get('horario_devolucao')
    cartao_id = request.data.get('cartao_id')
    novo_cartao_dados = request.data.get('novo_cartao')

    # Validação dos campos obrigatórios
    if not carro_id:
        return Response({"error": "ID do carro é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
    if not data_retirada or not data_devolucao:
        return Response({"error": "Datas de retirada e devolução são obrigatórias."}, status=status.HTTP_400_BAD_REQUEST)
    if not horario_retirada or not horario_devolucao:
        return Response({"error": "Horários de retirada e devolução são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

    # Verifica se está usando um cartão salvo ou adicionando um novo
    if cartao_id:
        cartao = get_object_or_404(CartaoCredito, id=cartao_id, cliente=cliente)
    elif novo_cartao_dados:
        serializer = CartaoCreditoSerializer(data=novo_cartao_dados)
        if serializer.is_valid():
            cartao = serializer.save(cliente=cliente)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Cartão de crédito é obrigatório para reserva de aluguel."}, status=status.HTTP_400_BAD_REQUEST)

    # Validação do carro
    carro = get_object_or_404(Car, id=carro_id)

    # Criando o agendamento de aluguel com datas e horários
    Agendamento.objects.create(
        carro=carro,
        usuario=usuario,
        tipo='aluguel',
        data_retirada=data_retirada,
        horario_retirada=horario_retirada,
        data_devolucao=data_devolucao,
        horario_devolucao=horario_devolucao,
        status='pendente'
    )

    return Response({"message": "Reserva de aluguel realizada com sucesso!"}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_agendamentos_cliente(request):
    usuario = request.user
    cliente = Cliente.objects.get(user=usuario)
    agendamentos = Agendamento.objects.filter(usuario=usuario)

    agendamentos_data = []
    for agendamento in agendamentos:
        if agendamento.tipo == 'reserva':
            agendamento_info = {
                "carro": f"{agendamento.carro.brand} {agendamento.carro.model}",
                "tipo": agendamento.tipo,
                "data": agendamento.data.strftime('%Y-%m-%d') if agendamento.data else '',
                "horario": agendamento.horario.strftime('%H:%M') if agendamento.horario else '',
                "data_expiracao": agendamento.data_expiracao.strftime('%Y-%m-%d') if agendamento.data_expiracao else '',
                "status": agendamento.status
            }
            
        elif agendamento.tipo == 'aluguel':
            agendamento_info = {
                "carro": f"{agendamento.carro.brand} {agendamento.carro.model}",
                "tipo": agendamento.tipo,
                "data_retirada": agendamento.data_retirada.strftime('%Y-%m-%d') if agendamento.data_retirada else '',
                "horario_retirada": agendamento.horario_retirada.strftime('%H:%M') if agendamento.horario_retirada else '',
                "data_devolucao": agendamento.data_devolucao.strftime('%Y-%m-%d') if agendamento.data_devolucao else '',
                "horario_devolucao": agendamento.horario_devolucao.strftime('%H:%M') if agendamento.horario_devolucao else '',
                "status": agendamento.status
            }

        elif agendamento.tipo == 'visita':
            agendamento_info = {
                "carro": f"{agendamento.carro.brand} {agendamento.carro.model}",
                "tipo": agendamento.tipo,
                "data": agendamento.data.strftime('%Y-%m-%d') if agendamento.data else '',
                "horario": agendamento.horario.strftime('%H:%M') if agendamento.horario else '',
                "status": agendamento.status
            }

        else:
            agendamento_info = {}

        agendamentos_data.append(agendamento_info)

    return Response(agendamentos_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_agendamentos_pendentes(request):
    # Filtra apenas agendamentos de tipo 'visita' e com status 'pendente'
    agendamentos_pendentes = Agendamento.objects.filter(tipo='visita', status='pendente')

    agendamentos_data = []
    for agendamento in agendamentos_pendentes:
        agendamento_info = {
            "id": agendamento.id,
            "nome_cliente": agendamento.usuario.username,
            "carro": f"{agendamento.carro.brand} {agendamento.carro.model}",
            "tipo": agendamento.tipo,
            "data": agendamento.data.strftime('%Y-%m-%d') if agendamento.data else '',
            "horario": agendamento.horario.strftime('%H:%M') if agendamento.horario else '',
            "status": agendamento.status,
        }
        agendamentos_data.append(agendamento_info)

    return Response(agendamentos_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assumir_agendamento(request, agendamento_id):
    usuario = request.user
    agendamento = get_object_or_404(Agendamento, id=agendamento_id, status='pendente')

    if agendamento.tipo == 'visita':
        agendamento.funcionario = usuario
        agendamento.status = 'em atendimento'
        agendamento.save()
        return Response({"message": "Agendamento assumido com sucesso!"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Apenas agendamentos de visita podem ser assumidos."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_atendimentos_funcionario(request):
    usuario = request.user
    
    atendimentos = Agendamento.objects.filter(funcionario=usuario, status='em atendimento')
    
    atendimentos_data = [
        {
            "id": atendimento.id,
            "nome": atendimento.usuario.username,
            "tipo": atendimento.tipo,
            "data": atendimento.data.strftime('%Y-%m-%d') if atendimento.data else '',
            "horario": atendimento.horario.strftime('%H:%M') if atendimento.horario else '',
            "data_retirada": atendimento.data_retirada.strftime('%Y-%m-%d') if atendimento.data_retirada else '',
            "horario_retirada": atendimento.horario_retirada.strftime('%H:%M') if atendimento.horario_retirada else '',
            "data_devolucao": atendimento.data_devolucao.strftime('%Y-%m-%d') if atendimento.data_devolucao else '',
            "horario_devolucao": atendimento.horario_devolucao.strftime('%H:%M') if atendimento.horario_devolucao else '',
            "status": atendimento.status
        }
        for atendimento in atendimentos
    ]

    return Response(atendimentos_data, status=status.HTTP_200_OK)
