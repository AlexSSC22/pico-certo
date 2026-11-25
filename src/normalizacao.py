import csv
from datetime import datetime

def leitura_caminho_csv(caminho_csv):
    lista_pedido = []

    with open(caminho_csv, encoding='utf-8', newline='') as arquivo:
        leitor = csv.DictReader(arquivo)

        for pedido in leitor:
            lista_pedido.append(pedido)

    return lista_pedido


def converter_data(valor):
    return datetime.strptime(valor, "%Y-%m-%d").date()

def converter_tempo(valor):
    if valor == "":
        return None

    return int(valor)

def normalizar_pedido(linha):
    pedido = linha.copy()

    pedido["data_pedido"] = converter_data(pedido["data_pedido"])

    for campo in [
        "valor_bruto",
        "desconto",
        "valor_total",
        "custo_estimado"
    ]:
        pedido[campo] = float(pedido[campo])

    for campo in [
        "itens_qtd",
        "tempo_estimado_preparo_min"
        
    ]:
        pedido[campo] = int(pedido[campo])

    pedido["tempo_real_preparo_min"] = converter_tempo(
        pedido["tempo_real_preparo_min"]
    )

    pedido["avaliacao_cliente"] = converter_tempo(
    pedido["avaliacao_cliente"]
    )

    return pedido


def carregar_pedidos_seguro(caminho_csv):
    try:
        lista_pedido = leitura_caminho_csv(caminho_csv)
        return lista_pedido
    except FileNotFoundError:
        print("Arquivo não encontrado")
        return []