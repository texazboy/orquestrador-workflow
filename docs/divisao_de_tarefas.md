# Divisão de Tarefas

A gente se organizou em volta dos quatro Requisitos Funcionais do Projeto 2. Cada
um ficou responsável por um RF e pelo módulo dele, e a integração foi combinada
nas bordas.

## Quem ficou com o quê

| Pessoa | RF | Foco | Arquivos principais |
|---|---|---|---|
| José Gabriel Dâmaso | RF01 | Grafo dirigido (lista de adjacência) + I/O | `src/graph.py`, `src/io_handler.py` |
| Pedro Augusto | RF02 | Ordenação topológica (Kahn) + integração no CLI | `src/topological_sort.py`, `src/main.py` |
| Matheus Dos Santos Tenório | RF03 | Detecção de ciclos com DFS iterativa | `src/cycle_detector.py`, `src/demo_recursao.py`, `tests/test_casos.py` |
| Matheus Vasconcelos Soares | RF04 | Max-Heap + gerador de dados + benchmark | `src/priority_queue.py`, `src/generate_data.py`, `src/benchmark.py` |

A gente dividiu assim pra não pisar no código um do outro o tempo todo. O José
Gabriel definiu o contrato do grafo (índices inteiros, `neighbors`,
`in_degrees_copy`) e, a partir dali, o Matheus Tenório e o Pedro trabalharam só
em cima dessa interface, sem precisar saber como o I/O funciona por dentro. O
Matheus Soares entregou a heap com uma API mínima (`push`/`pop`/`peek`) que o
Pedro usa no Kahn, e tocou o gerador de dados em paralelo, já que ele não depende
do núcleo. No fim o Pedro fez a "cola" no `main.py`, ligando leitura → ciclo →
ordenação → escrita.

## Onde um módulo encostou no outro

- **José Gabriel → Matheus Tenório / Pedro:** a interface do grafo virou o
  contrato central. Ordenar os vizinhos no `finalize()` foi pedido do Matheus
  Tenório e do Pedro pra garantir o determinismo nos dois algoritmos.
- **Matheus Soares → Pedro:** o desempate da heap em `(prioridade, -índice)` foi
  acertado entre os dois pra ordem de liberação bater com o gabarito.
- **Matheus Tenório → Pedro:** a DFS roda antes da ordenação no `main`; se acha
  ciclo, o programa aborta com o diagnóstico em vez de tentar ordenar.

## Mais ou menos a ordem em que as coisas foram saindo

Seguimos as dependências entre os módulos (primeiro as estruturas-base, depois a
integração e a documentação):

1. José Gabriel — estrutura inicial do repositório e esboço do README
2. Matheus Soares — Max-Heap
3. José Gabriel — grafo dirigido com lista de adjacência
4. José Gabriel — camada de I/O (leitura/escrita JSON)
5. Matheus Tenório — detecção de ciclos com DFS iterativa de 3 cores
6. Matheus Tenório — correção na reconstrução do caminho do ciclo
7. Pedro — ordenação topológica (Kahn + prioridade)
8. Pedro — CLI e fluxo principal (`main.py`)
9. Matheus Soares — gerador automático dos 3 níveis de dados
10. Matheus Soares — gabaritos + script de benchmark
11. Pedro — ajuste de determinismo nos desempates
12. Matheus Tenório — testes de unidade e casos-limite
13. Matheus Soares — documentação da prova de carga e complexidade
14. José Gabriel — README final, decisões de design e divisão de tarefas
15. Pedro — Makefile e `run.sh`

O histórico completo de commits está no `HISTORICO_GIT.md`.
