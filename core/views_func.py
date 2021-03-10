import matplotlib.pyplot as plt
from sistema.db import getdb
from .models import datetime


def add_estado(item):
    if item.quant > item.quant_minima:
        item.estado = 'primary'
    elif item.quant == item.quant_minima:
        item.estado = 'success'
    else:
        item.estado = 'danger'
    return item


def get_vendas():
    return getdb()["vendas"]


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


def gerar_lista_mes_valores():
    mes_atual = get_mes_atual()
    dias_mes = gerar_dict_mes()
    vendas = list(get_vendas().find())
    vendas_mes_atual = list(
        filter(lambda i: i['data'][2:4] == mes_atual, vendas))
    for item in vendas_mes_atual:
        dia = item['data'][0:2]
        dias_mes[dia] += item['valor']
    lista_valores = list()
    for item in dias_mes:
        lista_valores.append(dias_mes[item])
    return lista_valores


def gerar_grafico_mensal():
    valores = gerar_lista_mes_valores()
    dias = list()
    for x in gerar_dict_mes():
        dias.append(x)
    plt.figure(figsize=(10, 5))
    plt.plot(dias, valores, color='#007bff')
    plt.scatter(dias, valores)
    plt.title("Vendas do Mês")
    plt.ylabel("Apurado em R$")
    plt.xlabel("Dia")
    plt.savefig('staticfiles/images/grafico_mensal.png',
                transparent=True, orientation='landscape')


def gerar_dict_ano():
    meses = dict()
    for x in range(1, 10):
        meses['0' + str(x)] = 0
    for x in range(10, 13):
        meses[str(x)] = 0
    return meses


def gerar_lista_ano_valores():
    ano_atual = get_ano_atual()
    ano_dict = gerar_dict_ano()
    vendas = list(get_vendas().find())
    vendas_ano_atual = list(
        filter(lambda i: i['data'][4:8] == ano_atual, vendas))
    for item in vendas_ano_atual:
        mes = item['data'][2:4]
        ano_dict[mes] += item['valor']
    lista_valores = list()
    for item in ano_dict:
        lista_valores.append(ano_dict[item])
    return lista_valores


def gerar_grafico_anual():
    meses = ('Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
             'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro')
    valores = gerar_lista_ano_valores()
    plt.figure(figsize=(10, 5))
    plt.bar(meses, valores, color='#007bff')
    plt.title("Vendas Este Ano")
    plt.ylabel("Apurado em R$")
    plt.xticks(rotation=30)
    plt.savefig('staticfiles/images/grafico_anual.png',
                transparent=True, orientation='landscape')
