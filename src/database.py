import sqlite3

def conectar_banco(caminho_banco):
    return sqlite3.connect(caminho_banco)

def criar_tabela_pedidos(conexao):
    cursor = conexao.cursor()

    sql_criar_tabela = """
    CREATE TABLE IF NOT EXISTS pedidos(
        pedido_id TEXT PRIMARY KEY,
        data_pedido TEXT NOT NULL,
        hora_pedido TEXT NOT NULL,
        canal TEXT NOT NULL,
        status TEXT NOT NULL,
        categoria TEXT NOT NULL,
        itens_qtd INTEGER NOT NULL,
        valor_bruto REAL NOT NULL,
        desconto REAL NOT NULL,
        valor_total REAL NOT NULL,
        custo_estimado REAL NOT NULL,
        forma_pagamento TEXT NOT NULL,
        tempo_estimado_preparo_min INTEGER NOT NULL,
        tempo_real_preparo_min INTEGER,
        avaliacao_cliente INTEGER
    )
    """

    cursor.execute(sql_criar_tabela)
    conexao.commit()

def inserir_pedido(conexao, pedido):
    cursor = conexao.cursor()

    sql_inserir = """
    INSERT OR IGNORE INTO pedidos (
        pedido_id,
        data_pedido,
        hora_pedido,
        canal,
        status,
        categoria,
        itens_qtd,
        valor_bruto,
        desconto,
        valor_total,
        custo_estimado,
        forma_pagamento,
        tempo_estimado_preparo_min,
        tempo_real_preparo_min,
        avaliacao_cliente
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    valores = (
        pedido["pedido_id"],
        pedido["data_pedido"].isoformat(),
        pedido["hora_pedido"],
        pedido["canal"],
        pedido["status"],
        pedido["categoria"],
        pedido["itens_qtd"],
        pedido["valor_bruto"],
        pedido["desconto"],
        pedido["valor_total"],
        pedido["custo_estimado"],
        pedido["forma_pagamento"],
        pedido["tempo_estimado_preparo_min"],
        pedido["tempo_real_preparo_min"],
        pedido["avaliacao_cliente"]
    )

    cursor.execute(sql_inserir, valores)
    conexao.commit()

def contar_pedidos(conexao):
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    resultado = cursor.fetchone()

    return resultado[0]

def contar_pedidos_por_status(conexao, status):
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM pedidos WHERE status = ?",
        (status,)
        )
    resultado = cursor.fetchone()

    return resultado[0]

def resumir_pedidos_por_status(conexao):
    cursor = conexao.cursor()
    cursor.execute(""" 
        SELECT status, COUNT(*)
        FROM pedidos
        GROUP BY status
        """)
    resultado = cursor.fetchall()

    return resultado
    

def resumir_status_por_canal(conexao):
    cursor = conexao.cursor()
    cursor.row_factory = sqlite3.Row
    cursor.execute("""
    SELECT
        canal,
        SUM(CASE WHEN status = 'finalizado' THEN 1 ELSE 0 END)
            AS quantidade_finalizados,
        SUM(CASE WHEN status = 'em_preparo' THEN 1 ELSE 0 END)
            AS quantidade_em_preparo,
        SUM(CASE WHEN status = 'cancelado' THEN 1 ELSE 0 END)
            AS quantidade_cancelados,
        100.0 * SUM(CASE WHEN status = 'cancelado' THEN 1 ELSE 0 END)
            / COUNT (*) AS percentual_cancelados
        

    FROM pedidos
    GROUP BY canal
    ORDER BY canal
    """)

    resultado = cursor.fetchall()

    resumo = []

    for linha in resultado:
        dados_canal = dict(linha)
        resumo.append(dados_canal)

    return resumo


