import datetime
from django.shortcuts import get_object_or_404
from cartaodecredito.serializers import CartaoCreditoSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Agendamento, Car, Feedback
from cartaodecredito.models import CartaoCredito
from cliente.models import Cliente

# Função auxiliar para atualizar status
def atualizar_status_agendamento(agendamento):
    hoje = datetime.date.today()
    hora = datetime.datetime.now().time()
    if agendamento.tipo == 'reserva' and agendamento.data_expiracao and agendamento.data_expiracao <= hoje and hora >= agendamento.horario_devolucao and agendamento.status == 'confirmado':
        agendamento.status = 'concluido'
        agendamento.save()
    elif agendamento.tipo == 'aluguel' and agendamento.data_devolucao and agendamento.data_devolucao <= hoje and hora >= agendamento.horario_devolucao and agendamento.status == 'confirmado':
        agendamento.status = 'concluido'
        agendamento.save()
    elif agendamento.tipo == 'visita' and agendamento.data <= hoje and hora >= agendamento.horario and agendamento.status == 'confirmado':
        agendamento.status = 'concluido'
        agendamento.save()
    elif agendamento.tipo == 'visita' and  agendamento.data <= hoje and hora >= agendamento.horario and agendamento.status == 'pendente':
        agendamento.status = 'cancelado'
        agendamento.save()
    elif agendamento.tipo == 'reserva' and agendamento.data_expiracao and agendamento.data_expiracao <= hoje and hora >= agendamento.horario_devolucao and agendamento.status == 'pendente':
        agendamento.status = 'cancelado'
        agendamento.save()
    elif agendamento.tipo == 'aluguel' and agendamento.data_devolucao and agendamento.data_devolucao <= hoje and hora >= agendamento.horario_devolucao and agendamento.status == 'pendente':
        agendamento.status = 'cancelado'
        agendamento.save()

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
    usuario = request.user
    cliente = Cliente.objects.get(user=usuario)
    carro_id = request.data.get('carro_id')
    cartao_id = request.data.get('cartao_id')
    novo_cartao_dados = request.data.get('novo_cartao')

    if not carro_id:
        return Response({"error": "ID do carro é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

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
def verificar_disponibilidade(request):
    carro_id = request.data.get('carro_id')
    data_retirada = request.data.get('data_retirada')
    horario_retirada = request.data.get('horario_retirada')
    data_devolucao = request.data.get('data_devolucao')
    horario_devolucao = request.data.get('horario_devolucao')

    if not all([carro_id, data_retirada, horario_retirada, data_devolucao, horario_devolucao]):
        return Response({"error": "Todos os campos de data e horário são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

    # Verificar disponibilidade usando a função auxiliar `checar_disponibilidade_aluguel`
    is_available = checar_disponibilidade_aluguel(
        carro_id, data_retirada, horario_retirada, data_devolucao, horario_devolucao
    )

    if is_available:
        return Response({"disponivel": True}, status=status.HTTP_200_OK)
    else:
        return Response({"disponivel": False, "error": "O carro já está reservado para o período selecionado."}, status=status.HTTP_400_BAD_REQUEST)

# Função auxiliar para verificar a disponibilidade de aluguel de um carro
def checar_disponibilidade_aluguel(car_id, data_retirada, horario_retirada, data_devolucao, horario_devolucao):
    # Formata as datas e horários como objetos datetime completos
    data_retirada_completa = datetime.datetime.strptime(f"{data_retirada} {horario_retirada}", "%Y-%m-%d %H:%M")
    data_devolucao_completa = datetime.datetime.strptime(f"{data_devolucao} {horario_devolucao}", "%Y-%m-%d %H:%M")

    # Busca conflitos de agendamentos de aluguel para o mesmo carro e status 'pendente'
    conflitos = Agendamento.objects.filter(
        carro_id=car_id,
        tipo='aluguel',
        data_retirada__lt=data_devolucao_completa,
        data_devolucao__gt=data_retirada_completa,
        status='pendente'
    )

    return not conflitos.exists()  # Retorna True se não houver conflitos

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

    # Verificação de dados obrigatórios
    if not carro_id or not data_retirada or not data_devolucao or not horario_retirada or not horario_devolucao:
        return Response({"error": "Dados obrigatórios ausentes."}, status=status.HTTP_400_BAD_REQUEST)

    # Cartão de crédito
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

    carro = get_object_or_404(Car, id=carro_id)

    # Verificar a disponibilidade do carro no intervalo de datas fornecido
    disponibilidade = checar_disponibilidade_aluguel(carro_id, data_retirada, horario_retirada, data_devolucao, horario_devolucao)
    if not disponibilidade:
        return Response({"error": "Carro já está reservado para o período selecionado."}, status=status.HTTP_400_BAD_REQUEST)

    # Criar o agendamento de aluguel
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
    #printar os dados do request
    usuario = request.user
    agendamentos = Agendamento.objects.filter(usuario=usuario)
    

    agendamentos_data = []
    for agendamento in agendamentos:
        atualizar_status_agendamento(agendamento)
        agendamento_info = {
            "id": agendamento.id,
            "carro": f"{agendamento.carro.brand} {agendamento.carro.model}",
            "tipo": agendamento.tipo,
            "data": agendamento.data.strftime('%Y-%m-%d') if agendamento.data else '',
            "horario": agendamento.horario.strftime('%H:%M') if agendamento.horario else '',
            "data_retirada": agendamento.data_retirada.strftime('%Y-%m-%d') if agendamento.data_retirada else '',
            "horario_retirada": agendamento.horario_retirada.strftime('%H:%M') if agendamento.horario_retirada else '',
            "data_devolucao": agendamento.data_devolucao.strftime('%Y-%m-%d') if agendamento.data_devolucao else '',
            "horario_devolucao": agendamento.horario_devolucao.strftime('%H:%M') if agendamento.horario_devolucao else '',
            "status": agendamento.status,
            'feedbackEnviado': agendamento.feedbackEnviado
        }
        agendamentos_data.append(agendamento_info)

    return Response(agendamentos_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_agendamentos_pendentes(request):
    agendamentos_pendentes = Agendamento.objects.filter(tipo='visita', status='pendente')
    agendamentos_data = []
    for agendamento in agendamentos_pendentes:
        atualizar_status_agendamento(agendamento)
        agendamentos_data.append({
            "id": agendamento.id,
            "nome_cliente": agendamento.usuario.username,
            "carro": f"{agendamento.carro.brand} {agendamento.carro.model}",
            "tipo": agendamento.tipo,
            "data": agendamento.data.strftime('%Y-%m-%d') if agendamento.data else '',
            "horario": agendamento.horario.strftime('%H:%M') if agendamento.horario else '',
            "status": agendamento.status,
        })
    return Response(agendamentos_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assumir_agendamento(request, agendamento_id):
    usuario = request.user
    agendamento = get_object_or_404(Agendamento, id=agendamento_id, status='pendente')

    if agendamento.tipo == 'visita':
        agendamento.funcionario = usuario
        agendamento.status = 'confirmado'
        agendamento.save()
        return Response({"message": "Agendamento assumido com sucesso!"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Apenas agendamentos de visita podem ser assumidos."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_atendimentos_funcionario(request):
    usuario = request.user
    atendimentos = Agendamento.objects.filter(funcionario=usuario, status='confirmado')

    atendimentos_data = []
    for atendimento in atendimentos:
        atualizar_status_agendamento(atendimento)
        atendimentos_data.append({
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
        })

    return Response(atendimentos_data, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registrar_feedback(request, agendamento_id):
    usuario = request.user
    comentario = request.data.get("comentario")
    nota = request.data.get("nota")

    # Validar nota
    if not 1 <= int(nota) <= 5:
        return Response({"error": "Nota deve estar entre 1 e 5."}, status=status.HTTP_400_BAD_REQUEST)

    # Verificar se o agendamento existe, pertence ao usuário e se já foi avaliado
    try:
        agendamento = Agendamento.objects.get(id=agendamento_id, usuario=usuario)
        if agendamento.feedbackEnviado:
            return Response({"error": "Este agendamento já foi avaliado."}, status=status.HTTP_400_BAD_REQUEST)
    except Agendamento.DoesNotExist:
        return Response({"error": "Agendamento não encontrado ou não pertence ao usuário."}, status=status.HTTP_404_NOT_FOUND)

    # Criar o feedback
    feedback = Feedback.objects.create(usuario=usuario, agendamento=agendamento, comentario=comentario, nota=nota)
    
    # Atualizar o agendamento para indicar que o feedback foi enviado
    agendamento.feedbackEnviado = True
    agendamento.save()

    return Response({"message": "Feedback registrado com sucesso!"}, status=status.HTTP_201_CREATED)