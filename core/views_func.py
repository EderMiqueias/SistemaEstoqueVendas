from django.conf import settings

from .models import Venda

import matplotlib.pyplot as plt

from datetime import datetime
import os


def add_estado(item):
    item.load_image()
    if item.quant > item.quant_minima:
        item.estado = 'primary'
    elif item.quant == item.quant_minima:
        item.estado = 'success'
    else:
        item.estado = 'danger'
    return item


def get_vendas(user):
    return Venda.objects.filter(user=user)


def get_mes_atual():
    return datetime.now().strftime("%m")


def get_ano_atual():
    return datetime.now().strftime("%Y")


def gerar_dict_mes():
    meses30 = ('04', '06', '09', '11')
    mes_atual = get_mes_atual()
    mapa = dict()
    for x in range(1, 10):
        mapa['0'+str(x)] = 0
    for x in range(10, 32):
        mapa[str(x)] = 0
    if mes_atual in meses30:
        mapa.pop('31')
    elif mes_atual == '02':
        var = 31
        while var != 28:
            mapa.pop(str(var))
            var += -1
    return mapa


def gerar_lista_mes_valores(user):
    mes_atual = get_mes_atual()
    dias_mes = gerar_dict_mes()
    vendas = get_vendas(user)
    vendas_json = list(map(lambda x: x.to_json(), vendas))
    vendas_mes_atual = list(
        filter(lambda i: i['criado'].strftime("%m") == mes_atual, vendas_json))
    for item in vendas_mes_atual:
        dia = item['criado'].strftime("%d")
        dias_mes[dia] += item['valor']
    lista_valores = list()
    for item in dias_mes:
        lista_valores.append(dias_mes[item])
    return lista_valores


def gerar_grafico_mensal(user_creator):
    path = "core" + settings.STATIC_URL if settings.DEBUG else str(settings.STATIC_ROOT) + "/"

    valores = gerar_lista_mes_valores(user_creator)
    dias = list()
    for x in gerar_dict_mes():
        dias.append(x)
    plt.figure(figsize=(10, 5))
    plt.plot(dias, valores, color='#007bff')
    plt.scatter(dias, valores)
    plt.title(f"Vendas do Mês\n{user_creator}")
    plt.ylabel("Apurado em R$")
    plt.xlabel("Dia")
    try:
        plt.savefig(f'{path}images/{user_creator}/grafico_mensal.png',
                    transparent=True, orientation='landscape')
    except FileNotFoundError:
        os.makedirs(f'{path}images/{user_creator}/')
        plt.savefig(f'{path}images/{user_creator}/grafico_mensal.png',
                    transparent=True, orientation='landscape')


def gerar_dict_ano():
    meses = dict()
    for x in range(1, 10):
        meses['0' + str(x)] = 0
    for x in range(10, 13):
        meses[str(x)] = 0
    return meses


def gerar_lista_ano_valores(user_creator):
    ano_atual = get_ano_atual()
    ano_dict = gerar_dict_ano()
    vendas = get_vendas(user_creator)
    vendas_json = list(map(lambda x: x.to_json(), vendas))
    vendas_ano_atual = list(
        filter(lambda i: i['criado'].strftime("%Y") == ano_atual, vendas_json))
    for item in vendas_ano_atual:
        mes = item['criado'].strftime("%m")
        ano_dict[mes] += item['valor']
    lista_valores = list()
    for item in ano_dict:
        lista_valores.append(ano_dict[item])
    return lista_valores


def gerar_grafico_anual(user_creator):
    path = "core" + settings.STATIC_URL if settings.DEBUG else str(settings.STATIC_ROOT) + "/"

    meses = ('Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
             'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro')
    valores = gerar_lista_ano_valores(user_creator)
    plt.figure(figsize=(10, 5))
    plt.bar(meses, valores, color='#007bff')
    plt.title(f"Vendas Este Ano\n{user_creator}")
    plt.ylabel("Apurado em R$")
    plt.xticks(rotation=30)
    try:
        plt.savefig(f'{path}images/{user_creator}/grafico_anual.png',
                    transparent=True, orientation='landscape')
    except FileNotFoundError:
        os.makedirs(f'{path}images/{user_creator}/')
        plt.savefig(f'{path}images/{user_creator}/grafico_anual.png',
                    transparent=True, orientation='landscape')
