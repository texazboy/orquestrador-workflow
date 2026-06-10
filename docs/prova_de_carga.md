# Prova de Carga

Evidência de que o sistema aguenta o volume do cenário de estresse sem estourar
memória e com complexidade dentro do que foi pedido. Os números abaixo saíram de
`python -m src.benchmark` rodado neste repositório (Python 3.14, Windows). Os
tempos variam um pouco a cada execução, mas o formato da curva se mantém.

## 1. Escalabilidade de tempo

DAGs sintéticos cada vez maiores, mantendo a proporção de 2,5 arestas por nó (a
mesma do estresse: 10.000 nós / 25.000 arestas). "Total" = DFS de detecção de
ciclo + ordenação topológica completa.

| N (nós) | M (arestas) | DFS ciclo | Topo+heap | Total | µs por elemento |
|---:|---:|---:|---:|---:|---:|
| 1.000 | 2.500 | 0,56 ms | 2,00 ms | 2,56 ms | 0,731 |
| 2.000 | 5.000 | 1,15 ms | 4,54 ms | 5,69 ms | 0,813 |
| 5.000 | 12.500 | 2,70 ms | 13,06 ms | 15,76 ms | 0,901 |
| 10.000 | 25.000 | 6,13 ms | 29,86 ms | 35,99 ms | 1,028 |
| 20.000 | 50.000 | 13,79 ms | 69,44 ms | 83,23 ms | 1,189 |
| 50.000 | 125.000 | 38,88 ms | 224,39 ms | 263,28 ms | 1,504 |

Quintuplicando a entrada (1k → 5k) o tempo total cresce ~6,2×; de 10k pra 50k
(5×) cresce ~7,3×. Esse crescimento um pouquinho acima do linear é o que se
espera de um custo **O(E + V log V)**: o fator `log V` faz o "µs por elemento"
subir devagar (de 0,73 pra 1,50 ao longo de duas ordens de grandeza) sem nunca
virar quadrático. A meta da rubrica (`O(N log N)`) está atendida.

O cenário oficial de estresse (10.000 tarefas, 25.000 dependências, **com** o
ciclo plantado) roda de ponta a ponta — ler o JSON, achar o ciclo e gerar a
saída — em poucos milissegundos.

## 2. Uso de memória

O pico de memória foi medido com `tracemalloc` durante a montagem do grafo e a
execução dos dois algoritmos no maior caso:

> **Pico de ~42,3 MB para N = 50.000 nós e M = 125.000 arestas.**

O consumo cresce linear, **O(V + E)**: a gente guarda um índice por nó, uma lista
de inteiros pras arestas e uns vetores auxiliares O(V) na DFS e no Kahn. Não tem
cópia quadrática nem matriz de adjacência (que pra 50.000 nós precisaria de uns
2,5 bilhões de células). Cinquenta mil nós cabem tranquilo na RAM de qualquer
máquina comum, sem estouro.

## 3. Por que a DFS tem que ser iterativa (demonstração)

O ciclo plantado no `input_estresse.json` é fundo de propósito: uma corrente de
milhares de tarefas que volta pro começo. O script `src/demo_recursao.py` roda
lado a lado uma DFS recursiva ingênua e a iterativa do projeto, na mesma entrada
de estresse (`python -m src.demo_recursao`):

```
Limite de recursao do Python : 1000
Tarefas no grafo de estresse : 10000
DFS RECURSIVA (ingenua)      : RecursionError -- estourou a pilha do interpretador
DFS ITERATIVA (projeto)      : encontrou ciclo de 2995 nos, sem estourar
   inicio do ciclo: T7005 -> T7006 -> T7007 -> T7008 -> ... -> T9999 -> T7005
```

A recursiva bate no limite de 1000 chamadas aninhadas e levanta `RecursionError`,
ou seja, falharia justo no caso que o RF03 manda detectar. A iterativa, com a
pilha na memória normal, percorre o ciclo de **2995 nós** e reconstrói ele
certinho. É a justificativa prática da decisão registrada no
`decisoes_de_design.md`.

## 4. Determinismo sob carga

Cada nível foi rodado duas vezes e as saídas comparadas com `diff`:

| Nível | Execuções | `diff` entre elas | Bate com o gabarito |
|---|---|---|---|
| básico | 2 | idêntico | sim |
| avançado | 2 | idêntico | sim |
| estresse | 2 | idêntico | sim |

O resultado é igual bit a bit mesmo nos 10.000 nós do estresse, o que sustenta a
comparação direta com o `output_esperado_estresse.json`.

## Como reproduzir

```bash
# tabela de tempo + memória de pico
python -m src.benchmark

# demonstração da recursiva estourando vs. a iterativa achando o ciclo
python -m src.demo_recursao

# rodar os 3 níveis e comparar com o gabarito
make test
```
