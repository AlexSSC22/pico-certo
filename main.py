from src.normalizacao import carregar_pedidos_seguro, normalizar_pedido
from src.analises import gerar_painel_executivo
from src.database import conectar_banco, criar_tabela_pedidos, inserir_pedido, contar_pedidos, contar_pedidos_por_status, resumir_pedidos_por_status, resumir_status_por_canal


caminho_banco = "dados/pico_certo.db"

conexao = conectar_banco(caminho_banco)
criar_tabela_pedidos(conexao)



caminho_csv = "dados/pedidos_pico_certo_ampliado.csv"

pedidos_brutos = carregar_pedidos_seguro(caminho_csv)


pedidos_normalizados = []


for pedido in pedidos_brutos:
    pedidos_normalizados.append(normalizar_pedido(pedido))

painel_executivo = gerar_painel_executivo(pedidos_normalizados)

for pedido in pedidos_normalizados:
    inserir_pedido(conexao, pedido)

quantidade_salva = contar_pedidos(conexao)

print(f"Pedidos salvos no banco: {quantidade_salva}")


quantidade_finalizados = contar_pedidos_por_status(conexao, "cancelado")
print(quantidade_finalizados)


resumo_pedidos_status = resumir_pedidos_por_status(conexao)
print(resumo_pedidos_status)


resumo_faturamento_canal = resumir_status_por_canal(conexao)
print(resumo_faturamento_canal)

conexao.close()