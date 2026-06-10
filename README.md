# Orquestrador de Agentes Autônomos (Workflow Engine)

**Projeto escolhido:** Projeto 2 — Orquestrador de Agentes Autônomos.

Um motor que resolve em que ordem milhares de tarefas dependentes devem rodar e
que detecta deadlock (ciclo de dependências) antes de começar a executar.

## Equipe

| Integrante                      | Responsabilidade principal                             |
| ------------------------------- | ------------------------------------------------------ |
| José Gabriel Dâmaso             | Grafo (lista de adjacência) e camada de I/O (RF01)     |
| Pedro Augusto                   | Ordenação topológica (Kahn) e integração no CLI (RF02) |
| Matheus Dos Santos Tenório      | Detecção de ciclos com DFS iterativa (RF03)            |
| Matheus Vasconcelos Soares      | Fila de prioridade (Max-Heap), geração de dados (RF04) |

A divisão detalhada está em [`docs/divisao_de_tarefas.md`](docs/divisao_de_tarefas.md).

## O problema

A entrada é um conjunto de **tarefas**, cada uma com uma **prioridade**, mais um
conjunto de **dependências** do tipo "a tarefa A precisa terminar antes da B".
A partir disso o programa:

1. monta o grafo de dependências;
2. checa se existe ciclo (deadlock). Se existir, ele aborta e mostra qual é o
   ciclo, porque não dá pra ordenar algo que depende de si mesmo;
3. se for um DAG válido, gera a ordem de execução sempre liberando primeiro a
   tarefa pronta de maior prioridade. Quando empata, vence o menor id.

## Requisitos Funcionais

| RF   | O que pede                                  | Estrutura/algoritmo (feito à mão) | Arquivo                   |
| ---- | ------------------------------------------- | --------------------------------- | ------------------------- |
| RF01 | Modelar dependências                        | Grafo com lista de adjacência     | `src/graph.py`            |
| RF02 | Determinar a sequência de execução          | Ordenação topológica (Kahn)       | `src/topological_sort.py` |
| RF03 | Detectar ciclos (deadlock) e abortar        | DFS iterativa (3 cores)           | `src/cycle_detector.py`   |
| RF04 | Liberar tarefas prontas por urgência        | Max-Heap binária                  | `src/priority_queue.py`   |

Não usamos nenhuma biblioteca pronta de estrutura de dados no núcleo: nada de
`networkx`, `heapq` ou afins. O único `dict` do projeto aparece na borda de I/O,
só pra converter o rótulo da tarefa (`"T07"`) no índice inteiro interno. O porquê
disso está explicado em [`docs/decisoes_de_design.md`](docs/decisoes_de_design.md).

## Estrutura do repositório

```
orquestrador-workflow/
├── src/
│   ├── graph.py              # RF01 - grafo (lista de adjacência)
│   ├── priority_queue.py     # RF04 - Max-Heap
│   ├── cycle_detector.py     # RF03 - DFS iterativa
│   ├── topological_sort.py   # RF02 - Kahn + prioridade
│   ├── io_handler.py         # leitura/escrita JSON
│   ├── main.py               # CLI (junta tudo)
│   ├── generate_data.py      # gerador dos 3 cenários
│   ├── benchmark.py          # prova de carga
│   └── demo_recursao.py      # demonstra recursiva estourando vs. iterativa
├── data/                     # entradas + gabaritos dos 3 níveis
├── docs/                     # complexidade, design, prova de carga
├── tests/                    # testes de unidade (unittest)
├── run.sh
├── Makefile
├── requirements.txt
└── README.md
```

## Como executar

Precisa só de **Python 3.8+**. Não tem dependência externa nenhuma (nem o núcleo,
nem o gerador de dados), então não precisa instalar nada nem compilar.

### Opção 1 - script

```bash
./run.sh data/input_basico.json data/saida.json
```

### Opção 2 - Makefile

```bash
make gen      # regera os 3 arquivos de entrada
make run      # roda o cenário básico
make test     # roda os 3 cenários e compara com os gabaritos
make bench    # prova de carga
make clean    # limpa as saídas temporárias
```

### Opção 3 - direto pelo módulo

```bash
python3 -m src.main --input data/input_estresse.json --output data/saida.json
```

A saída em JSON é determinística (não inclui o tempo de execução de propósito).
O resumo com os tempos sai no `stderr`.

## Formato de entrada e saída

**Entrada** (`input_*.json`):

```json
{
  "tasks": [{"id": "T01", "name": "...", "priority": 5}],
  "dependencies": [{"from": "T01", "to": "T03"}]
}
```

**Saída** (`output_esperado_*.json`):

```json
{
  "projeto": "Orquestrador de Agentes Autônomos (Workflow Engine)",
  "ciclo_detectado": false,
  "ciclo": [],
  "ordem_execucao": ["T07", "T01", "T02", "..."],
  "estatisticas": {
    "total_tarefas": 8,
    "total_dependencias_informadas": 6,
    "total_dependencias_unicas": 6,
    "dependencias_duplicadas_ignoradas": 0,
    "nos_isolados": 1
  }
}
```

## Testes e gabaritos

Os três cenários ficam em `data/`, cada um com o gabarito do lado:

- **básico** - DAG limpo, testa a ordenação e o desempate por prioridade;
- **avançado** - casos chatos: nós soltos, dependência repetida e um ciclo, que
  faz o `ciclo_detectado` virar `true`;
- **estresse** - 10.000 tarefas e 25.000 dependências, com um ciclo bem fundo
  (~2.995 nós) escondido lá no meio, pra forçar a DFS a aguentar a profundidade
  sem estourar a pilha.

`make test` regera as saídas e compara byte a byte com os gabaritos. Os testes de
unidade rodam com `python3 -m unittest tests.test_casos` e cobrem as estruturas,
os três cenários e alguns casos-limite (self-loop, grafo vazio).

## Complexidade (resumo)

| Operação                    | Complexidade   |
| --------------------------- | -------------- |
| Construção do grafo         | O(V + E)       |
| Detecção de ciclos (DFS)    | O(V + E)       |
| Ordenação topológica + heap | O(E + V log V) |
| Memória total               | O(V + E)       |

A conta completa e a medição empírica estão em
[`docs/complexidade.md`](docs/complexidade.md) e
[`docs/prova_de_carga.md`](docs/prova_de_carga.md).
