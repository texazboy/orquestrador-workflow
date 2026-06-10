# Prova de carga: mede tempo (DFS + Kahn) e memoria de pico em DAGs de
# tamanho crescente, pra mostrar que o custo segue O(E + V log V).

import random
import time
import tracemalloc

from .graph import Graph
from .cycle_detector import find_cycle
from .topological_sort import topological_order

SEED = 42

def construir_dag(n, m):
    largura = len(str(n - 1))
    g = Graph()
    for i in range(n):
        g.add_node(f"T{i:0{largura}d}")
    prioridades = [random.randint(1, 10) for _ in range(n)]
    vistas = set()
    tentativas = 0
    limite = m * 50
    while g.num_unique_edges() < m and tentativas < limite:
        tentativas += 1
        u = random.randint(0, n - 2)
        v = random.randint(u + 1, n - 1)
        if (u, v) in vistas:
            continue
        vistas.add((u, v))
        g.add_edge(f"T{u:0{largura}d}", f"T{v:0{largura}d}")
    g.finalize()
    return g, prioridades

def medir(n, m):
    random.seed(SEED)
    g, prioridades = construir_dag(n, m)

    t0 = time.perf_counter()
    ciclo = find_cycle(g)
    t1 = time.perf_counter()
    ordem = topological_order(g, prioridades)
    t2 = time.perf_counter()

    assert ciclo is None, "o DAG não deveria ter ciclo"
    assert ordem is not None and len(ordem) == n, "ordenação incompleta"

    return {
        "n": n,
        "m": g.num_unique_edges(),
        "dfs_ms": (t1 - t0) * 1000,
        "topo_ms": (t2 - t1) * 1000,
        "total_ms": (t2 - t0) * 1000,
    }

def main():
    casos = [
        (1_000, 2_500),
        (2_000, 5_000),
        (5_000, 12_500),
        (10_000, 25_000),
        (20_000, 50_000),
        (50_000, 125_000),
    ]
    print(f"{'N (nós)':>9} | {'M (arestas)':>11} | {'DFS ciclo':>10} | "
          f"{'Topo+heap':>10} | {'Total':>10} | {'µs/elem':>8}")
    print("-" * 76)
    for n, m in casos:
        r = medir(n, m)
        us_por_elem = (r["total_ms"] * 1000) / (r["n"] + r["m"])
        print(f"{r['n']:>9} | {r['m']:>11} | {r['dfs_ms']:>9.2f}ms | "
              f"{r['topo_ms']:>9.2f}ms | {r['total_ms']:>9.2f}ms | "
              f"{us_por_elem:>7.3f}")

    random.seed(SEED)
    tracemalloc.start()
    g, prioridades = construir_dag(50_000, 125_000)
    find_cycle(g)
    topological_order(g, prioridades)
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print("-" * 76)
    print(f"Memória de pico (N=50.000, M=125.000): {pico / (1024 * 1024):.1f} MB")

if __name__ == "__main__":
    main()
