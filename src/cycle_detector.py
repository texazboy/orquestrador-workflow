# RF03 - Deteccao de ciclo (deadlock) com DFS iterativa.
# Tres cores: BRANCO = nao visitado, CINZA = esta na pilha atual,
# PRETO = ja terminou. Achar uma aresta pra um no CINZA = ciclo.
# Iterativa de proposito: o ciclo do teste de estresse tem ~3000 de
# profundidade e estouraria a recursao do Python (limite 1000).

BRANCO, CINZA, PRETO = 0, 1, 2


def find_cycle(graph):
    n = graph.num_nodes()
    color = [BRANCO] * n
    parent = [-1] * n

    for start in range(n):
        if color[start] != BRANCO:
            continue

        color[start] = CINZA
        # cada item da pilha eh [no, indice do proximo vizinho a olhar]
        stack = [[start, 0]]

        while stack:
            quadro = stack[-1]
            u = quadro[0]
            i = quadro[1]
            vizinhos = graph.neighbors(u)

            if i < len(vizinhos):
                quadro[1] = i + 1          # avanca pro proximo vizinho
                v = vizinhos[i]
                if color[v] == BRANCO:
                    color[v] = CINZA
                    parent[v] = u
                    stack.append([v, 0])
                elif color[v] == CINZA:
                    # achou aresta de volta pra um no ainda na pilha: ciclo
                    return _reconstruir_ciclo(graph, parent, u, v)
            else:
                # ja olhou todos os vizinhos, fecha o no
                color[u] = PRETO
                stack.pop()

    return None


def _reconstruir_ciclo(graph, parent, u, v):
    # sobe pelos pais de u ate chegar em v, depois fecha de volta em v
    caminho = []
    x = u
    while x != v:
        caminho.append(x)
        x = parent[x]
    caminho.append(v)
    caminho.reverse()
    caminho.append(v)
    return [graph.label(idx) for idx in caminho]
