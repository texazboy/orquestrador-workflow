# Decisões de Design

Aqui a gente registra as escolhas que não dá pra entender só olhando o código,
aquelas que provavelmente alguém perguntaria "por que fizeram assim?".

## 1. Por que tem um `dict` se o projeto proíbe estrutura pronta?

A regra do trabalho é sobre o núcleo: o grafo, a heap, o Kahn e a DFS são todos
escritos na mão, em cima de listas e índices inteiros. O único `dict` que sobrou
está na entrada/saída (`graph.py` e `io_handler.py`) e serve só pra traduzir o
rótulo da tarefa (`"T07"`) para o índice interno e voltar.

Isso é um problema de leitura de arquivo, não de algoritmo. Dava pra trocar o
`dict` por uma busca binária numa lista de rótulos ordenada e nenhuma linha do
grafo, da heap, da DFS ou do Kahn mudaria, porque eles só enxergam inteiros de 0
a V-1. Nenhuma decisão de ordem, prioridade ou caminho passa pelo `dict`.
Mantivemos ele por ser a forma O(1) natural de fazer esse mapeamento na borda. Ou
seja: não é uma das estruturas que estão sendo avaliadas.

## 2. DFS iterativa em vez de recursiva

A DFS recursiva é mais curtinha e mais fácil de ler. O problema é que o cenário
de estresse tem, de propósito, um ciclo com quase 3.000 nós de profundidade. O
Python aborta a recursão em 1000 chamadas por padrão, então uma DFS recursiva
levantaria `RecursionError` e derrubaria o programa exatamente no caso que o RF03
manda detectar.

A versão iterativa guarda os "frames" numa pilha que a gente mesmo controla, na
memória normal. Aí a profundidade que ela aguenta depende só da RAM, não do
interpretador. A demonstração (a recursiva estoura, a iterativa acha o ciclo de
2995 nós) está no `prova_de_carga.md`. Foi trocar um pouco de elegância por
robustez, e nesse caso valeu.

## 3. Como garantimos a saída determinística

A rubrica pede saída determinística e dá o gabarito pronto. A gente garante isso
com três coisas que se encaixam:

- **Inserção em ordem alfabética.** Na leitura os rótulos são ordenados antes de
  virarem nós, então o índice interno acompanha a ordem alfabética do rótulo
  (índice menor = rótulo "menor"). Isso já fixa qualquer desempate por id.
- **Vizinhos ordenados (`finalize`).** Cada lista de adjacência é ordenada uma
  vez só. Como a DFS e o Kahn sempre visitam os vizinhos na mesma sequência, qual
  ciclo aparece (quando tem mais de um) e a ordem de liberação ficam sempre
  iguais.
- **Desempate explícito na heap.** A fila usa a chave `(prioridade, -índice)`.
  Maior prioridade sai primeiro; empatou, ganha o menor índice, que é o menor
  rótulo. Nenhum empate fica "ao acaso".

Rodamos cada nível duas vezes e comparamos as saídas com `diff`: deu zero
diferença nos três. A reprodutibilidade vem do design, não de sorte.

## 4. Por que o tempo de execução não entra no JSON

O tempo é útil pra prova de carga, mas muda a cada execução e de máquina pra
máquina. Se ele entrasse no `output.json` a comparação com o gabarito quebrava
toda hora. Por isso os tempos vão só pro `stderr`, no resuminho de execução,
enquanto o arquivo de saída fica só com o que é reprodutível: ciclo, ordem e
estatísticas.

## 5. Formato da entrada e o sentido das arestas

A entrada tem dois arrays: `tasks` (com `id`, `name`, `priority`) e
`dependencies` (com `from` e `to`). A convenção que adotamos é que
`{"from": A, "to": B}` quer dizer "A roda antes de B", o que vira a aresta
dirigida A → B. Assim a ordenação topológica respeita "pré-requisito antes do
dependente", que é como a gente lê um grafo de tarefas na cabeça.

Dependência repetida é detectada, contada e ignorada (a aresta entra uma vez só).
Tarefa que não tem nenhuma dependência, nem de entrada nem de saída, é um nó
isolado: continua valendo, entra normal na ordenação e aparece na contagem de
isolados. Os dois números vão no bloco `estatisticas` da saída, o que dá pra
quem corrige um sinal de que os dados foram realmente processados e não chutados.

## 6. Por que Python

O trabalho deixa escolher a linguagem. Python deixa as estruturas curtas e à
mostra, o que ajuda num trabalho cujo objetivo é justamente mostrar a estrutura
por dentro. O ponto fraco dele (o limite de recursão) a gente acabou usando a
favor, virou o motivo da DFS iterativa. O mesmo desenho (índices inteiros,
listas, heap em cima de array) migra direto pra Java ou JavaScript se precisar.
