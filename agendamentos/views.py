import datetime
import pytz

from django.shortcuts import get_object_or_404
from cartaodecredito.serializers import CartaoCreditoSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Agendamento, Car, Feedback
from cartaodecredito.models import CartaoCredito
from cliente.models import Cliente
from .serializers import FeedbackSerializer
from decimal import Decimal

# Função auxiliar para atualizar status
def atualizar_status_agendamento(agendamento):
    hoje = datetime.date.today()
    hora = datetime.datetime.now().time()
    hora_br = hora.astimezone(pytz.timezone('America/Sao_Paulo'))
    if agendamento.tipo == 'reserva' and agendamento.data_expiracao and agendamento.data_expiracao <= hoje and hora_br >= agendamento.horario_devolucao and agendamento.status == 'confirmado':
        agendamento.status = 'concluido'
        agendamento.save()
    elif agendamento.tipo == 'aluguel' and agendamento.data_devolucao and agendamento.data_devolucao <= hoje and hora_br >= agendamento.horario_devolucao and agendamento.status == 'confirmado':
        agendamento.status = 'concluido'
        agendamento.save()
    elif agendamento.tipo == 'visita' and agendamento.data <= hoje and hora_br >= agendamento.horario and agendamento.status == 'confirmado':
        agendamento.status = 'concluido'
        agendamento.save()
    elif agendamento.tipo == 'visita' and  agendamento.data <= hoje and hora_br >= agendamento.horario and agendamento.status == 'pendente':
        agendamento.status = 'cancelado'
        agendamento.save()
    elif agendamento.tipo == 'reserva' and agendamento.data_expiracao and agendamento.data_expiracao <= hoje and hora_br >= agendamento.horario_devolucao and agendamento.status == 'pendente':
        agendamento.status = 'cancelado'
        agendamento.save()
    elif agendamento.tipo == 'aluguel' and agendamento.data_devolucao and agendamento.data_devolucao <= hoje and hora_br >= agendamento.horario_devolucao and agendamento.status == 'pendente':
        agendamento.status = 'cancelado'
        agendamento.save()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def agendar_visita(request):
    usuario = request.user
    cliente = Cliente.objects.get(user=usuario)
    carro_id = request.data.get('carro_id')
    data = request.data.get('data')
    horario = request.data.get('horario')

    if not data or not horario:
        return Response({"error": "Data e horário são obrigatórios para a visita."}, status=status.HTTP_400_BAD_REQUEST)

    carro = get_object_or_404(Car, id=carro_id)
    valor_visita = 0
    agendamento = Agendamento.objects.create(
        carro=carro,
        carro_marca=carro.brand,
        carro_modelo=carro.model,
        carro_preco=0,
        carro_ano=carro.year,
        usuario=usuario,
        data=data,
        horario=horario,
        tipo='visita',
        valor_agendamento=0,
        valor_pago=0,
        status='pendente'
    )

    cliente.adicionar_pontos(1)
    return Response({"message": "Visita agendada com sucesso!"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reservar_veiculo(request):
    usuario = request.user
    cliente = Cliente.objects.get(user=usuario)
    carro_id = request.data.get('carro_id')
    cartao_id = request.data.get('cartao_id')
    novo_cartao_dados = request.data.get('novo_cartao')
    pontos_utilizados = int(request.data.get('pontos_utilizados', 0))

    if not carro_id:
        return Response({"error": "ID do carro é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

    # Verificação de cartão de crédito
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

    carro = get_object_or_404(Car, id=carro_id)

    # Definir o preço da reserva com desconto se aplicável
    preco_reserva = carro.purchase_price
    if carro.is_discounted_sale:
        preco_reserva *= (1 - carro.discount_percentage_sale)

    # Aplicar desconto adicional com base nos pontos
    if pontos_utilizados > 0:
        if pontos_utilizados > cliente.pontos:
            return Response({"error": "Pontos insuficientes."}, status=status.HTTP_400_BAD_REQUEST)
        
        desconto_percentual = Decimal(1) / Decimal(pontos_utilizados)
        desconto = preco_reserva * desconto_percentual
        preco_reserva = max(preco_reserva - desconto, 0)

        # Subtrair os pontos utilizados
        cliente.pontos -= pontos_utilizados
        cliente.save()


    print(carro.brand)
    print(carro.model)
    # Criar o agendamento com as informações do carro incluídas
    Agendamento.objects.create(
        carro=carro,
        carro_marca=carro.brand,
        carro_modelo=carro.model,
        carro_preco=carro.purchase_price,
        carro_ano=carro.year,
        usuario=usuario,
        tipo='reserva',
        data=datetime.datetime.today().date(),
        data_expiracao=datetime.datetime.today().date() + datetime.timedelta(days=14),
        valor_agendamento=preco_reserva,  # Salva o valor com desconto
        valor_pago=1000,
        status='pendente'
    )

    pontos_ganhos = 100
    cliente.pontos += pontos_ganhos
    cliente.save()

    return Response({
        "message": "Reserva de veículo realizada com sucesso!",
        "preco_reserva": preco_reserva,
        "pontos_utilizados": pontos_utilizados
    }, status=status.HTTP_201_CREATED)


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
    pontos_utilizados = int(request.data.get('pontos_utilizados', 0))

    if not carro_id or not data_retirada or not data_devolucao:
        return Response({"error": "Dados obrigatórios ausentes."}, status=status.HTTP_400_BAD_REQUEST)

    carro = get_object_or_404(Car, id=carro_id)

    # Verificar se o carro está disponível para aluguel
    if not carro.is_for_rent:
        return Response({"error": "Carro não disponível para aluguel."}, status=status.HTTP_400_BAD_REQUEST)

    # Calcular o total de dias de aluguel e preço com desconto se aplicável
    data_retirada_dt = datetime.datetime.strptime(data_retirada, "%Y-%m-%d")
    data_devolucao_dt = datetime.datetime.strptime(data_devolucao, "%Y-%m-%d")
    dias_aluguel = (data_devolucao_dt - data_retirada_dt).days
    preco_total_aluguel = dias_aluguel * carro.rental_price

    if carro.is_discounted_rent:
        preco_total_aluguel *= (1 - carro.discount_percentage_rent)

    # Aplicar desconto adicional com base nos pontos
    if pontos_utilizados > 0:
        if pontos_utilizados > cliente.pontos:
            return Response({"error": "Pontos insuficientes."}, status=status.HTTP_400_BAD_REQUEST)
        
        desconto = Decimal(pontos_utilizados) / Decimal(100)
        preco_total_aluguel = max(preco_total_aluguel - desconto, 0)

        # Subtrair os pontos utilizados
        cliente.pontos -= pontos_utilizados
        cliente.save()

    # Criar o agendamento de aluguel com as informações do carro incluídas
    print(carro.brand)
    print(carro.model)
    Agendamento.objects.create(
        carro=carro,
        carro_marca=carro.brand,
        carro_modelo=carro.model,
        carro_preco=carro.rental_price,
        carro_ano=carro.year,
        usuario=usuario,
        tipo='aluguel',
        data_retirada=data_retirada,
        horario_retirada=horario_retirada,
        data_devolucao=data_devolucao,
        horario_devolucao=horario_devolucao,
        valor_agendamento=preco_total_aluguel,
        valor_pago=(preco_total_aluguel / 2),
        status='pendente'
    )

    pontos_por_dia = 10
    pontos_ganhos = dias_aluguel * pontos_por_dia
    cliente.pontos += pontos_ganhos
    cliente.save()

    return Response({
        "message": "Reserva de aluguel realizada com sucesso!",
        "preco_total_aluguel": preco_total_aluguel,
        "pontos_utilizados": pontos_utilizados
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_agendamentos_cliente(request):
    usuario = request.user
    agendamentos = Agendamento.objects.filter(usuario=usuario)

    agendamentos_data = []
    for agendamento in agendamentos:
        atualizar_status_agendamento(agendamento)
        agendamento_info = {
            "id": agendamento.id,
            "carro_marca": agendamento.carro_marca,
            "carro_modelo": agendamento.carro_modelo,
            "carro_preco": agendamento.carro_preco,
            "carro_ano": agendamento.carro_ano,
            "tipo": agendamento.tipo,
            "data": agendamento.data.strftime('%Y-%m-%d') if agendamento.data else '',
            "horario": agendamento.horario.strftime('%H:%M') if agendamento.horario else '',
            "data_retirada": agendamento.data_retirada.strftime('%Y-%m-%d') if agendamento.data_retirada else '',
            "horario_retirada": agendamento.horario_retirada.strftime('%H:%M') if agendamento.horario_retirada else '',
            "data_devolucao": agendamento.data_devolucao.strftime('%Y-%m-%d') if agendamento.data_devolucao else '',
            "data_expiracao": agendamento.data_expiracao.strftime('%Y-%m-%d') if agendamento.data_expiracao else '',
            "horario_devolucao": agendamento.horario_devolucao.strftime('%H:%M') if agendamento.horario_devolucao else '',
            "status": agendamento.status,
            "valor_agendamento": agendamento.valor_agendamento,
            "valor_pago": agendamento.valor_pago,
            "feedbackEnviado": agendamento.feedbackEnviado
        }
        agendamentos_data.append(agendamento_info)

    return Response(agendamentos_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_agendamentos_pendentes(request):
    agendamentos_pendentes = Agendamento.objects.filter(status='pendente')
    agendamentos_data = []
    for agendamento in agendamentos_pendentes:
        atualizar_status_agendamento(agendamento)
        if agendamento.tipo == 'visita':
            agendamentos_data.append({
                "id": agendamento.id,
                "nome_cliente": agendamento.usuario.username,
                "carro_marca": agendamento.carro_marca,
                "carro_modelo": agendamento.carro_modelo,
                "tipo": agendamento.tipo,
                "data": agendamento.data.strftime('%Y-%m-%d') if agendamento.data else '',
                "horario": agendamento.horario.strftime('%H:%M') if agendamento.horario else '',
                "status": agendamento.status,
            })
        elif agendamento.tipo == 'reserva':

            agendamentos_data.append({
                "id": agendamento.id,
                "nome_cliente": agendamento.usuario.username,
                "carro_marca": agendamento.carro_marca,
                "carro_modelo": agendamento.carro_modelo,
                "tipo": agendamento.tipo,
                "data": agendamento.data.strftime('%Y-%m-%d') if agendamento.data else '',
                "status": agendamento.status,
            })

        elif agendamento.tipo == 'aluguel':
            agendamentos_data.append({
                "id": agendamento.id,
                "nome_cliente": agendamento.usuario.username,
                "carro_marca": agendamento.carro_marca,
                "carro_modelo": agendamento.carro_modelo,
                "tipo": agendamento.tipo,
                "data_retirada": agendamento.data_retirada.strftime('%Y-%m-%d') if agendamento.data_retirada else '',
                "horario_retirada": agendamento.horario_retirada.strftime('%H:%M') if agendamento.horario_retirada else '',
                "status": agendamento.status,
            })
        
    return Response(agendamentos_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assumir_agendamento(request, agendamento_id):
    usuario = request.user
    agendamento = get_object_or_404(Agendamento, id=agendamento_id, status='pendente')

    if agendamento.tipo == 'visita' or agendamento.tipo == 'reserva' or agendamento.tipo == 'aluguel':
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
            "carro_marca": atendimento.carro_marca,
            "carro_modelo": atendimento.carro_modelo,
            "data": atendimento.data.strftime('%Y-%m-%d') if atendimento.data else '',
            "horario": atendimento.horario.strftime('%H:%M') if atendimento.horario else '',
            "data_retirada": atendimento.data_retirada.strftime('%Y-%m-%d') if atendimento.data_retirada else '',
            "horario_retirada": atendimento.horario_retirada.strftime('%H:%M') if atendimento.horario_retirada else '',
            "data_devolucao": atendimento.data_devolucao.strftime('%Y-%m-%d') if atendimento.data_devolucao else '',
            "horario_devolucao": atendimento.horario_devolucao.strftime('%H:%M') if atendimento.horario_devolucao else '',
            "status": atendimento.status,
            "valor_agendamento": atendimento.valor_agendamento,
            "valor_pago": atendimento.valor_pago
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


@api_view(['GET'])
def listar_feedbacks(request):
    feedbacks = Feedback.objects.all()
    feedbacks_data = [
        {
            "id": feedback.id,
            "usuario": feedback.usuario.username,  # Adiciona o nome de usuário em vez do ID
            "comentario": feedback.comentario,
            "nota": feedback.nota,
            "agendamento_id": feedback.agendamento.id,
        }
        for feedback in feedbacks
    ]
    return Response(feedbacks_data)