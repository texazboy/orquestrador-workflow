import unittest

from src.graph import Graph
from src.priority_queue import MaxHeap
from src.cycle_detector import find_cycle
from src import io_handler
from src.main import build_output

class TestMaxHeap(unittest.TestCase):
    def test_maior_prioridade_sai_primeiro(self):
        h = MaxHeap()
        for prioridade, indice in [(5, 0), (9, 1), (1, 2), (7, 3)]:
            h.push((prioridade, -indice), indice)

        self.assertEqual([h.pop() for _ in range(4)], [1, 3, 0, 2])

    def test_desempate_por_menor_indice(self):
        h = MaxHeap()

        for indice in [2, 0, 1]:
            h.push((5, -indice), indice)
        self.assertEqual([h.pop() for _ in range(3)], [0, 1, 2])

    def test_peek_nao_remove(self):
        h = MaxHeap()
        h.push((3, 0), 0)
        h.push((8, -1), 1)
        self.assertEqual(h.peek(), 1)
        self.assertEqual(len(h), 2)

class TestGraph(unittest.TestCase):
    def test_dedup_e_contagem_de_duplicadas(self):
        g = Graph()
        for r in ["A", "B"]:
            g.add_node(r)
        g.add_edge("A", "B")
        g.add_edge("A", "B")
        g.finalize()
        self.assertEqual(g.num_unique_edges(), 1)
        self.assertEqual(g.duplicate_edges, 1)

    def test_vizinhos_ordenados(self):
        g = Graph()
        for r in ["A", "B", "C", "D"]:
            g.add_node(r)

        g.add_edge("A", "D")
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.finalize()
        vizinhos = g.neighbors(g.index_of("A"))
        self.assertEqual(vizinhos, sorted(vizinhos))

class TestPipelineBasico(unittest.TestCase):
    def setUp(self):
        self.g, self.prio, self.dep = io_handler.load_input("data/input_basico.json")
        self.out = build_output(self.g, self.prio, self.dep)

    def test_sem_ciclo(self):
        self.assertFalse(self.out["ciclo_detectado"])
        self.assertEqual(self.out["ciclo"], [])

    def test_tarefa_isolada_de_maior_prioridade_sai_primeiro(self):

        self.assertEqual(self.out["ordem_execucao"][0], "T07")

    def test_desempate_no_pipeline(self):
        ordem = self.out["ordem_execucao"]

        self.assertLess(ordem.index("T01"), ordem.index("T02"))

    def test_um_no_isolado(self):
        self.assertEqual(self.out["estatisticas"]["nos_isolados"], 1)

class TestPipelineAvancado(unittest.TestCase):
    def setUp(self):
        self.g, self.prio, self.dep = io_handler.load_input("data/input_avancado.json")
        self.out = build_output(self.g, self.prio, self.dep)

    def test_detecta_ciclo(self):
        self.assertTrue(self.out["ciclo_detectado"])
        self.assertEqual(self.out["ciclo"], ["A01", "A02", "A03", "A01"])
        self.assertEqual(self.out["ordem_execucao"], [])

    def test_duplicada_ignorada(self):
        self.assertEqual(
            self.out["estatisticas"]["dependencias_duplicadas_ignoradas"], 1
        )

    def test_dois_nos_isolados(self):
        self.assertEqual(self.out["estatisticas"]["nos_isolados"], 2)

class TestDeteccaoCicloDireta(unittest.TestCase):
    def test_dag_simples_nao_tem_ciclo(self):
        g = Graph()
        for r in ["A", "B", "C"]:
            g.add_node(r)
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        g.finalize()
        self.assertIsNone(find_cycle(g))

    def test_ciclo_simples_e_detectado(self):
        g = Graph()
        for r in ["A", "B", "C"]:
            g.add_node(r)
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        g.add_edge("C", "A")
        g.finalize()
        self.assertEqual(find_cycle(g), ["A", "B", "C", "A"])

class TestPipelineEstresse(unittest.TestCase):
    def setUp(self):
        self.g, self.prio, self.dep = io_handler.load_input("data/input_estresse.json")
        self.out = build_output(self.g, self.prio, self.dep)

    def test_volume(self):
        self.assertEqual(self.out["estatisticas"]["total_tarefas"], 10000)

    def test_ciclo_profundo_detectado(self):
        self.assertTrue(self.out["ciclo_detectado"])
        tamanho = len(self.out["ciclo"]) - 1
        self.assertGreater(tamanho, 1000)

class TestCasosLimite(unittest.TestCase):
    def test_self_loop_e_ciclo(self):
        g = Graph()
        g.add_node("A")
        g.add_edge("A", "A")
        g.finalize()
        self.assertEqual(find_cycle(g), ["A", "A"])

    def test_grafo_vazio(self):
        g = Graph()
        g.finalize()
        out = build_output(g, [], 0)
        self.assertFalse(out["ciclo_detectado"])
        self.assertEqual(out["ordem_execucao"], [])
        self.assertEqual(out["estatisticas"]["total_tarefas"], 0)

    def test_no_unico_sem_arestas(self):
        g = Graph()
        g.add_node("X")
        g.finalize()
        out = build_output(g, [7], 0)
        self.assertEqual(out["ordem_execucao"], ["X"])
        self.assertEqual(out["estatisticas"]["nos_isolados"], 1)

if __name__ == "__main__":
    unittest.main()
