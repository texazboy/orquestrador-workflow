# Gerador dos 3 cenarios de teste (basico / avancado / estresse).
# Sem nenhuma dependencia externa: os nomes das tarefas saem de listas fixas
# combinadas pelo indice, e a aleatoriedade (prioridades e arestas do estresse)
# usa o random da stdlib com seed fixa. Resultado: rodar "make gen" reproduz
# exatamente os mesmos arquivos em qualquer maquina, sem instalar nada.

import json
import os
import random

SEED = 42
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# Vocabulario pra montar nomes de tarefa plausiveis. A escolha eh por indice
# (i % len), entao nao mexe no fluxo do random que decide prioridade/arestas.
_VERBOS = [
    "Processar", "Validar", "Compilar", "Indexar", "Sincronizar",
    "Exportar", "Importar", "Agregar", "Normalizar", "Comprimir",
    "Replicar", "Auditar", "Particionar", "Reconciliar", "Empacotar",
    "Publicar", "Calcular", "Treinar", "Renderizar", "Despachar",
]
_ALVOS = [
    "o lote de pedidos", "os logs de acesso", "a base de clientes",
    "o índice de busca", "as métricas diárias", "o cache de sessão",
    "os relatórios mensais", "a fila de mensagens", "o backup incremental",
    "as faturas pendentes", "o dataset de treino", "os eventos brutos",
    "a tabela de fatos", "os snapshots noturnos", "o catálogo de produtos",
]


def _nome_tarefa(i):
    verbo = _VERBOS[i % len(_VERBOS)]
    alvo = _ALVOS[(i // len(_VERBOS)) % len(_ALVOS)]
    return f"{verbo} {alvo}"


def _salvar(nome, tasks, dependencies):
    caminho = os.path.join(DATA_DIR, nome)
    # newline="\n": mantem LF no Windows pra os arquivos gerados ficarem
    # iguais em qualquer SO (mesmo motivo do io_handler.write_output)
    with open(caminho, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"tasks": tasks, "dependencies": dependencies},
                  f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"  gerado: {nome:24s} "
          f"({len(tasks)} tarefas, {len(dependencies)} dependências)")


def gerar_basico():
    random.seed(SEED)

    prioridades = {
        "T01": 5, "T02": 5, "T03": 1, "T04": 9,
        "T05": 2, "T06": 7, "T07": 8, "T08": 3,
    }
    tasks = [{"id": tid, "name": _nome_tarefa(i), "priority": p}
             for i, (tid, p) in enumerate(sorted(prioridades.items()))]

    dependencies = [
        {"from": "T01", "to": "T03"},
        {"from": "T02", "to": "T03"},
        {"from": "T03", "to": "T04"},
        {"from": "T03", "to": "T05"},
        {"from": "T05", "to": "T06"},
        {"from": "T08", "to": "T06"},
    ]
    _salvar("input_basico.json", tasks, dependencies)


def gerar_avancado():
    random.seed(SEED)

    ids = [f"A{i:02d}" for i in range(1, 11)]
    tasks = [{"id": tid, "name": _nome_tarefa(i), "priority": (i % 5) + 1}
             for i, tid in enumerate(ids)]

    # de proposito: ciclo A01->A02->A03->A01, dependencia repetida (A04->A05
    # duas vezes) e nos soltos (A09, A10) -> cobre os edge cases do enunciado
    dependencies = [
        {"from": "A01", "to": "A02"},
        {"from": "A02", "to": "A03"},
        {"from": "A03", "to": "A01"},
        {"from": "A04", "to": "A05"},
        {"from": "A04", "to": "A05"},
        {"from": "A05", "to": "A06"},
        {"from": "A07", "to": "A08"},
    ]
    _salvar("input_avancado.json", tasks, dependencies)


def gerar_estresse(total_tarefas=10_000, total_arestas=25_000, tam_corrente=3_000):
    random.seed(SEED)

    n = total_tarefas
    k = n - tam_corrente
    largura = len(str(n - 1))

    def rid(i):
        return f"T{i:0{largura}d}"

    tasks = [{"id": rid(i), "name": _nome_tarefa(i),
              "priority": random.randint(1, 10)} for i in range(n)]

    arestas_corrente = tam_corrente
    arestas_dag = total_arestas - arestas_corrente

    # parte DAG: arestas u->v com u<v (nunca fecham ciclo)
    vistas = set()
    dependencies = []
    tentativas = 0
    limite = arestas_dag * 50
    while len(dependencies) < arestas_dag and tentativas < limite:
        tentativas += 1
        u = random.randint(0, k - 2)
        v = random.randint(u + 1, k - 1)
        if (u, v) in vistas:
            continue
        vistas.add((u, v))
        dependencies.append({"from": rid(u), "to": rid(v)})

    # corrente longa no final dos nos: k -> k+1 -> ... -> n-1
    for i in range(k, n - 1):
        dependencies.append({"from": rid(i), "to": rid(i + 1)})

    # ...e a aresta que fecha o ciclo bem fundo (volta pra k+5).
    # eh esse ciclo profundo que so a DFS iterativa aguenta detectar.
    dependencies.append({"from": rid(n - 1), "to": rid(k + 5)})

    _salvar("input_estresse.json", tasks, dependencies)


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Gerando massa de testes (seed={SEED}) em {DATA_DIR} ...")
    gerar_basico()
    gerar_avancado()
    gerar_estresse()
    print("Concluído.")


if __name__ == "__main__":
    main()
