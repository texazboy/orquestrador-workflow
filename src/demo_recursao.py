# Demonstracao da secao 3 da prova de carga: por que a DFS precisa ser
# iterativa. Roda uma DFS recursiva ingenua e a iterativa do projeto na mesma
# entrada de estresse. A recursiva estoura a pilha do Python; a iterativa acha
# o ciclo profundo numa boa.
#
# Uso: python -m src.demo_recursao

import sys

from . import io_handler
from .cycle_detector import find_cycle


def dfs_recursiva(graph):
    n = graph.num_nodes()
    BRANCO, CINZA, PRETO = 0, 1, 2
    color = [BRANCO] * n

    def visita(u):
        color[u] = CINZA
        for v in graph.neighbors(u):
            if color[v] == BRANCO:
                if visita(v):
                    return True
            elif color[v] == CINZA:
                return True
        color[u] = PRETO
        return False

    for s in range(n):
        if color[s] == BRANCO and visita(s):
            return True
    return False


def main():
    graph, _, _ = io_handler.load_input("data/input_estresse.json")

    print("Limite de recursao do Python :", sys.getrecursionlimit())
    print("Tarefas no grafo de estresse :", graph.num_nodes())

    try:
        achou = dfs_recursiva(graph)
        print("DFS RECURSIVA (ingenua)      :",
              "achou ciclo" if achou else "nao achou ciclo")
    except RecursionError:
        print("DFS RECURSIVA (ingenua)      : RecursionError -- "
              "estourou a pilha do interpretador")

    ciclo = find_cycle(graph)
    print(f"DFS ITERATIVA (projeto)      : encontrou ciclo de {len(ciclo) - 1} "
          "nos, sem estourar")
    print("   inicio do ciclo:",
          " -> ".join(ciclo[:4]), "-> ... ->", ciclo[-2], "->", ciclo[-1])


if __name__ == "__main__":
    main()
