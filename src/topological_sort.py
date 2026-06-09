# RF02 - Ordenacao topologica pelo algoritmo de Kahn.
# A diferenca pro Kahn padrao eh que, no lugar de uma fila comum, usamos a
# Max-Heap (RF04): entre as tarefas prontas, sai primeiro a de maior prioridade.

from .priority_queue import MaxHeap


def topological_order(graph, priorities):
    n = graph.num_nodes()
    indeg = graph.in_degrees_copy()
    heap = MaxHeap()

    # comeca com quem nao depende de ninguem (grau de entrada 0)
    for u in range(n):
        if indeg[u] == 0:
            # chave (prioridade, -u): maior prioridade primeiro;
            # empatou, menor indice (= menor rotulo) primeiro
            heap.push((priorities[u], -u), u)

    ordem = []
    while not heap.empty():
        u = heap.pop()
        ordem.append(u)
        # "liberou" u: desconta dos sucessores e enfileira quem zerou
        for v in graph.neighbors(u):
            indeg[v] -= 1
            if indeg[v] == 0:
                heap.push((priorities[v], -v), v)

    # se nao saiu todo mundo, sobrou ciclo (no fluxo real a DFS ja barrou antes)
    if len(ordem) != n:
        return None

    return [graph.label(u) for u in ordem]
