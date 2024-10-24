from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Agendamento
from carros.models import Car
from rest_framework import status

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Agendamento
from carros.models import Car
from rest_framework import status

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def agendar_visita(request):
    usuario = request.user
    carro_id = request.data.get('carro_id')
    tipo = request.data.get('tipo')

    # Verifica o tipo de agendamento (venda ou aluguel)
    if tipo == 'venda':
        data = request.data.get('data')
        horario = request.data.get('horario')

        # Validando se os campos de venda estão presentes
        if not data or not horario:
            return Response({"error": "Data e horário são obrigatórios para agendamento de visita."}, status=status.HTTP_400_BAD_REQUEST)

        # Criação do agendamento de venda
        carro = get_object_or_404(Car, id=carro_id)
        agendamento = Agendamento.objects.create(
            carro=carro,
            usuario=usuario,
            data=data,
            horario=horario,
            tipo=tipo,
            status='pendente'
        )
        return Response({"message": "Agendamento de visita realizado com sucesso!"}, status=status.HTTP_201_CREATED)

    elif tipo == 'aluguel':
        data_retirada = request.data.get('data_retirada')
        horario_retirada = request.data.get('horario_retirada')
        data_devolucao = request.data.get('data_devolucao')
        horario_devolucao = request.data.get('horario_devolucao')

        # Validando se todos os campos de aluguel estão presentes
        if not data_retirada or not horario_retirada or not data_devolucao or not horario_devolucao:
            return Response({"error": "Data e horário de retirada e devolução são obrigatórios para reservas de aluguel."}, status=status.HTTP_400_BAD_REQUEST)

        # Criação do agendamento de aluguel
        carro = get_object_or_404(Car, id=carro_id)
        agendamento = Agendamento.objects.create(
            carro=carro,
            usuario=usuario,
            data_retirada=data_retirada,
            horario_retirada=horario_retirada,
            data_devolucao=data_devolucao,
            horario_devolucao=horario_devolucao,
            tipo=tipo,
            status='pendente'
        )
        return Response({"message": "Reserva de aluguel realizada com sucesso!"}, status=status.HTTP_201_CREATED)

    return Response({"error": "Tipo de agendamento inválido."}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_agendamentos_cliente(request):
    usuario = request.user
    agendamentos = Agendamento.objects.filter(usuario=usuario)
    agendamentos_data = []

    for agendamento in agendamentos:
        if agendamento.tipo == 'venda':
            agendamentos_data.append({
                'carro': agendamento.carro.model,
                'data': agendamento.data.strftime('%Y-%m-%d'),
                'horario': agendamento.horario.strftime('%H:%M'),
                'tipo': agendamento.tipo,
                'status': agendamento.status
            })
        elif agendamento.tipo == 'aluguel':
            agendamentos_data.append({
                'carro': agendamento.carro.model,
                'data_retirada': agendamento.data_retirada.strftime('%Y-%m-%d'),
                'horario_retirada': agendamento.horario_retirada.strftime('%H:%M'),
                'data_devolucao': agendamento.data_devolucao.strftime('%Y-%m-%d'),
                'horario_devolucao': agendamento.horario_devolucao.strftime('%H:%M'),
                'tipo': agendamento.tipo,
                'status': agendamento.status
            })
    
    return Response(agendamentos_data, status=status.HTTP_200_OK)
