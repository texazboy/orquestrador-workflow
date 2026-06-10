# Análise de Complexidade

Notação: **V** = número de tarefas (vértices) e **E** = número de dependências
únicas (arestas). Todas as estruturas principais foram feitas na mão, sem
biblioteca de alto nível (`networkx`, `heapq` etc.) no núcleo.

## Resumo

| Componente | Operação | Tempo | Espaço |
|---|---|---|---|
| Lista de adjacência | `add_node` | O(1) amortizado | O(V) |
| Lista de adjacência | `add_edge` (com dedup) | O(1) amortizado | O(E) |
| Lista de adjacência | `finalize` (ordena vizinhos) | O(E log E) | O(1) extra |
| Max-Heap | `push` / `pop` | O(log V) | O(V) |
| Max-Heap | `peek` | O(1) | - |
| DFS (detecção de ciclo) | `find_cycle` | O(V + E) | O(V) |
| Ordenação topológica | `topological_order` (Kahn + heap) | O(E + V log V) | O(V) |
| Pipeline completo (`main`) | leitura → ciclo → topo → escrita | O(E + V log V) | O(V + E) |

O termo que domina o sistema é **O(E + V log V)**, que vem da ordenação
topológica com a fila de prioridade. Isso fica abaixo da meta da rubrica
(`O(N log N)`) mesmo no estresse de 10.000 tarefas e 25.000 dependências.

## Detalhamento por módulo

### Lista de Adjacência (`graph.py`)

Cada nó ganha um índice inteiro fixo na hora que é inserido, e os vizinhos de
saída ficam numa lista de inteiros. Inserir nó ou aresta é O(1) amortizado (um
`append`). A deduplicação usa um conjunto de pares `(origem, destino)` consultado
em O(1) médio. Esse conjunto existe só pra detectar e contar repetição; ele não
entra em nenhum algoritmo central.

`finalize()` ordena a lista de vizinhos de cada nó uma vez. Somando todos os nós,
isso é O(E log E) no pior caso (quando um nó só concentra quase todas as arestas)
e na prática fica perto de O(E) quando o grau é bem distribuído. Ordenar os
vizinhos é o que faz a DFS e o Kahn explorarem sempre na mesma ordem, que é a
base do determinismo.

Passar por todos os vizinhos de todos os nós uma vez é O(V + E), o limite natural
de qualquer varredura em lista de adjacência.

### Max-Heap binária (`priority_queue.py`)

Heap binária clássica em cima de um array. A propriedade de heap é mantida pelo
`_sift_up` (sobe depois de inserir) e pelo `_sift_down` (desce depois de tirar a
raiz), e cada um anda no máximo a altura da árvore, que é ⌊log₂ V⌋. Então `push`
e `pop` são O(log V) e `peek` é O(1). Espaço O(V), um elemento por tarefa que
está "pronta" ao mesmo tempo.

### DFS / Detecção de Ciclos (`cycle_detector.py`)

DFS com marcação de três cores (BRANCO/CINZA/PRETO), feita de forma iterativa com
pilha explícita. Cada nó entra e sai da pilha uma vez (BRANCO → CINZA → PRETO) e
cada aresta é olhada uma vez só, daí o O(V + E). Espaço O(V): os vetores de cor e
de pai, mais a pilha, que no pior caso (um caminho enorme) guarda V frames.

A versão iterativa foi escolha consciente: o ciclo plantado no estresse tem quase
3.000 nós de fundo, o que estoura o limite de recursão padrão do Python (1000).
Mais sobre isso no `prova_de_carga.md`.

### Ordenação Topológica (`topological_sort.py`)

Algoritmo de Kahn com fila de prioridade. Calcular o grau de entrada de todo
mundo é O(V + E). Cada nó entra e sai da heap exatamente uma vez: 2V operações de
O(log V), ou seja O(V log V). Ao tirar um nó, a gente percorre as arestas de
saída dele e desconta o grau de entrada dos sucessores; somado em todos os nós
isso dá O(E). Total: **O(E + V log V)**. Espaço O(V) pro vetor de graus e pra
heap.

Se a heap esvaziar antes de ordenar todo mundo, é porque sobrou um ciclo e a
função devolve `None`. No fluxo de verdade a DFS já barra esse caso antes, mas a
checagem fica ali como garantia.

### Pipeline (`main.py` + `io_handler.py`)

A leitura junta os rótulos, ordena (O(V log V)), insere nós e arestas (O(V + E))
e chama o `finalize` (O(E log E)). Depois roda a detecção de ciclo (O(V + E)) e,
se for DAG, a ordenação topológica (O(E + V log V)). Escrever o JSON é O(V). O
custo total é dominado por **O(E + V log V)**, com memória O(V + E) pra guardar o
grafo inteiro.
