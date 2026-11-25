def calcular_resumo_financeiro(pedidos):
    quantidade_finalizados = 0
    faturamento_bruto = 0
    desconto_total = 0
    custo_total_estimado = 0
    margem_estimada = 0
    margem_percentual = 0
    ticket_medio = 0
    faturamento_liquido = 0

    for pedido in pedidos:
        status = pedido["status"]
        if status == "finalizado":
            
            valor_bruto = pedido["valor_bruto"]
            desconto = pedido["desconto"]
            custo_estimado = pedido["custo_estimado"]
            valor_total = pedido["valor_total"]


            
            quantidade_finalizados += 1
            faturamento_bruto += valor_bruto
            desconto_total += desconto
            custo_total_estimado += custo_estimado
            faturamento_liquido += valor_total

    if quantidade_finalizados > 0:
        margem_estimada = faturamento_liquido - custo_total_estimado
        margem_percentual = (margem_estimada / faturamento_liquido) * 100
        ticket_medio = faturamento_liquido / quantidade_finalizados

    return {
        "quantidade_finalizados": quantidade_finalizados,
        "faturamento_bruto": faturamento_bruto,
        "desconto_total": desconto_total,
        "faturamento_liquido": faturamento_liquido,
        "margem_estimada": margem_estimada,
        "margem_percentual": margem_percentual,
        "ticket_medio": ticket_medio
    }


def resumir_por_categoria(pedidos):
    quantidade = {}


    for pedido in pedidos:
        status = pedido["status"]
        categoria = pedido['categoria']
        if status == "finalizado":

            if categoria not in quantidade:
                quantidade[categoria] = {
                    "quantidade_finalizados": 0,
                    "faturamento_liquido": 0,
                    "custo_total_estimado": 0
                }
            quantidade[categoria]["quantidade_finalizados"] += 1
            quantidade[categoria]["faturamento_liquido"] += pedido["valor_total"]
            quantidade[categoria]["custo_total_estimado"] += pedido["custo_estimado"]

    for categoria, dados in quantidade.items():
        margem = dados["faturamento_liquido"] - dados["custo_total_estimado"]
        dados["margem_estimada"] = margem


    return quantidade


def analisar_horarios(pedidos):
    horarios = {}

    for pedido in pedidos:
        status = pedido["status"]
        hora_pedido = pedido["hora_pedido"]

        if status == "finalizado":
            hora = int(hora_pedido.split(':')[0])
            

            if hora not in horarios:
                horarios[hora] = {
                    "quantidade_finalizados": 0,
                    "quantidade_atrasados": 0,
                    "atraso_total_min": 0
                    }
            horarios[hora]["quantidade_finalizados"] += 1

            tempo_real = pedido["tempo_real_preparo_min"]
            tempo_estimado = pedido["tempo_estimado_preparo_min"]
           

            if tempo_real is not None:
                atraso = tempo_real - tempo_estimado
                if atraso > 0:
                    horarios[hora]["quantidade_atrasados"] += 1
                    horarios[hora]["atraso_total_min"] += atraso

    return horarios

def classificar_prioridade(atraso_medio_min):
    if atraso_medio_min <= 3:
        return "normal"
    elif atraso_medio_min <= 6:
        return "atencao"
    else:
        return "critica"



def gerar_painel_canais(pedidos):
    atrasos_salao_min = 0
    qtd_analisada_salao = qtd_analisada_delivery = 0
    qtd_pedidos_finalizados_salao = qtd_pedidos_finalizados_delivery = 0
    faturamento_finalizado_salao = faturamento_finalizado_delivery = 0
    atrasos_delivery_min = 0
    qtd_atrasados_salao = qtd_atrasados_delivery = 0
    atraso_medio_min_salao = atraso_medio_min_delivery = 0


    for pedido in pedidos:
        if pedido["status"] == "finalizado":
            canal = pedido["canal"]

            if canal == "salao":
                faturamento_finalizado_salao += pedido['valor_total']
                qtd_pedidos_finalizados_salao += 1
                

            elif canal == "delivery":
                faturamento_finalizado_delivery += pedido['valor_total']
                qtd_pedidos_finalizados_delivery += 1
                
                
            if pedido["tempo_real_preparo_min"] is not None:
                tempo_real = pedido['tempo_real_preparo_min']
                tempo_estimado = pedido['tempo_estimado_preparo_min']
                atraso = tempo_real - tempo_estimado

                if canal == "salao":
                    qtd_analisada_salao += 1

                    
                elif canal == "delivery":
                    qtd_analisada_delivery += 1


                if atraso > 0:
                    if canal == "salao":
                        qtd_atrasados_salao += 1
                        atrasos_salao_min += atraso

                    elif canal == "delivery":
                        qtd_atrasados_delivery += 1
                        atrasos_delivery_min += atraso

                       

                        
    if qtd_atrasados_salao > 0:
        atraso_medio_min_salao = atrasos_salao_min / qtd_atrasados_salao

    if qtd_atrasados_delivery > 0:
        atraso_medio_min_delivery = atrasos_delivery_min / qtd_atrasados_delivery
 

    prioridade_salao = classificar_prioridade(atraso_medio_min_salao)
    prioridade_delivery = classificar_prioridade(atraso_medio_min_delivery)

    return {
        "salao": {
            "quantidade_finalizados": qtd_pedidos_finalizados_salao,
            "faturamento_finalizados": faturamento_finalizado_salao,
            "quantidade_analisada": qtd_analisada_salao,
            "quantidade_atrasados": qtd_atrasados_salao,
            "atraso_total_min": atrasos_salao_min,
            "atraso_medio_min": atraso_medio_min_salao,
            "prioridade": prioridade_salao
        },
        "delivery": {
            "quantidade_finalizados": qtd_pedidos_finalizados_delivery,
            "faturamento_finalizados": faturamento_finalizado_delivery,
            "quantidade_analisada": qtd_analisada_delivery,
            "quantidade_atrasados": qtd_atrasados_delivery,
            "atraso_total_min": atrasos_delivery_min,
            "atraso_medio_min": atraso_medio_min_delivery,
            "prioridade": prioridade_delivery
        }
    }


def calcular_avaliacao_media(pedidos):
    
    quantidade_avaliacoes = 0
    soma_avaliacao = 0
    avaliacao_media = 0
    
    for pedido in pedidos:
        status = pedido["status"]
        avaliacao_cliente = pedido["avaliacao_cliente"]
        
    
        if (status == "finalizado" and 
            avaliacao_cliente is not None
            ):
            quantidade_avaliacoes += 1
            soma_avaliacao += avaliacao_cliente


    if quantidade_avaliacoes > 0:
        avaliacao_media = soma_avaliacao / quantidade_avaliacoes

    return {
        "quantidade_avaliacoes": quantidade_avaliacoes,
        "avaliacao_media": avaliacao_media
    }

def gerar_painel_executivo(pedidos):
    financeiro = calcular_resumo_financeiro(pedidos)
    canais = gerar_painel_canais(pedidos)
    categoria = resumir_por_categoria(pedidos)
    horarios = analisar_horarios(pedidos)
    avaliacoes = calcular_avaliacao_media(pedidos)

    return {
    "financeiro": financeiro,
    "canais": canais,
    "categorias": categoria,
    "horarios": horarios,
    "avaliacoes": avaliacoes
}