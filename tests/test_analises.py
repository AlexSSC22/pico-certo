import unittest
from src.analises import classificar_prioridade, calcular_resumo_financeiro


class TestClassificarPrioridade(unittest.TestCase):

    def test_atraso_baixo_retorna_normal(self):
        resultado = classificar_prioridade(2)

        self.assertEqual(resultado, "normal")

    def test_atraso_baixo_retorna_atencao(self):
        resultado = classificar_prioridade(4)

        self.assertEqual(resultado, "atencao")

    def test_atraso_baixo_retorna_critica(self):
        resultado = classificar_prioridade(7)

        self.assertEqual(resultado, "critica")

class TestCalcularResumoFinanceiro(unittest.TestCase):

    def test_calcular_resumo_financeiro(self):
        pedidos_teste = []
        pedidos_teste.append({
            "status": "finalizado",
            "valor_bruto": 100.0,
            "desconto": 10.0,
            "valor_total": 90.0,
            "custo_estimado": 30.0
        })
        resultado = calcular_resumo_financeiro(pedidos_teste)
        self.assertEqual(resultado["quantidade_finalizados"], 1)
        self.assertEqual(resultado["faturamento_bruto"], 100.0)
        self.assertEqual(resultado["desconto_total"], 10.0)
        self.assertEqual(resultado["faturamento_liquido"], 90.0)
        self.assertEqual(resultado["margem_estimada"], 60.0)
        self.assertEqual(resultado["ticket_medio"], 90.0)

    def test_pedido_em_preparo_nao_entra_no_resumo(self):
        pedidos_teste = []

        pedidos_teste.append({
            "status": "finalizado",
            "valor_bruto": 100.0,
            "desconto": 10.0,
            "valor_total": 90.0,
            "custo_estimado": 30.0
        })

        pedidos_teste.append({
            "status": "em_preparo",
            "valor_bruto": 5000.0,
            "desconto": 0.0,
            "valor_total": 5000.0,
            "custo_estimado": 1000.0
        })

        resultado = calcular_resumo_financeiro(pedidos_teste)

        self.assertEqual(resultado["quantidade_finalizados"], 1)
        self.assertEqual(resultado["faturamento_bruto"], 100.0)
        self.assertEqual(resultado["desconto_total"], 10.0)
        self.assertEqual(resultado["faturamento_liquido"], 90.0)
        self.assertEqual(resultado["margem_estimada"], 60.0)
        self.assertEqual(resultado["ticket_medio"], 90.0)

    def test_sem_pedidos_finalizados_retorna_zeros(self):
        pedidos_teste = []

        pedidos_teste.append({"status": "em_preparo"})
        pedidos_teste.append({"status": "cancelado"})


        resultado = calcular_resumo_financeiro(pedidos_teste)
        self.assertEqual(resultado["quantidade_finalizados"], 0)
        self.assertEqual(resultado["faturamento_bruto"], 0)
        self.assertEqual(resultado["desconto_total"], 0)
        self.assertEqual(resultado["faturamento_liquido"], 0)
        self.assertEqual(resultado["margem_estimada"], 0)
        self.assertEqual(resultado["ticket_medio"], 0)


        
        



