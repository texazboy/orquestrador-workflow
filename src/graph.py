# RF01 - Grafo dirigido com lista de adjacencia.
# Os nos sao guardados por indice inteiro (0..V-1); a traducao rotulo<->indice
# fica num dict so pra entrada/saida, nao entra em nenhum algoritmo.

class Graph:
    def __init__(self):
        self._label_to_index = {}      # "T07" -> 5
        self._index_to_label = []      # 5 -> "T07"
        self._adj = []                 # lista de adjacencia (vizinhos de saida)
        self._in_degree = []           # grau de entrada de cada no
        self._edge_set = set()         # pares (u, v) ja vistos, pra deduplicar
        self.duplicate_edges = 0

    def add_node(self, label):
        # se o rotulo ja existe, devolve o indice que ele ja tem
        idx = self._label_to_index.get(label)
        if idx is not None:
            return idx
        idx = len(self._index_to_label)
        self._label_to_index[label] = idx
        self._index_to_label.append(label)
        self._adj.append([])
        self._in_degree.append(0)
        return idx

    def add_edge(self, src_label, dst_label):
        u = self.add_node(src_label)
        v = self.add_node(dst_label)
        # aresta repetida: conta e ignora, pra nao baguncar o grau de entrada
        if (u, v) in self._edge_set:
            self.duplicate_edges += 1
            return False
        self._edge_set.add((u, v))
        self._adj[u].append(v)
        self._in_degree[v] += 1
        return True

    def finalize(self):
        # ordena os vizinhos uma vez so. e isso que faz a DFS e o Kahn
        # visitarem sempre na mesma ordem (determinismo)
        for lista in self._adj:
            lista.sort()

    def num_nodes(self):
        return len(self._index_to_label)

    def num_unique_edges(self):
        return len(self._edge_set)

    def neighbors(self, u):
        return self._adj[u]

    def in_degree(self, u):
        return self._in_degree[u]

    def out_degree(self, u):
        return len(self._adj[u])

    def in_degrees_copy(self):
        # o Kahn vai decrementar isso, entao devolve uma copia
        return list(self._in_degree)

    def index_of(self, label):
        return self._label_to_index[label]

    def label(self, idx):
        return self._index_to_label[idx]

    def isolated_nodes(self):
        # no isolado = sem aresta de entrada nem de saida
        total = 0
        for u in range(self.num_nodes()):
            if self._in_degree[u] == 0 and len(self._adj[u]) == 0:
                total += 1
        return total
