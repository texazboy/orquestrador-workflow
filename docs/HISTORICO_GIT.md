# Histórico de Commits

Registro gerado a partir do `git log` real do repositório, em ordem cronológica.
Serve de base para a avaliação de Colaboração e Git: documenta a evolução
incremental do projeto e a contribuição de cada integrante.

## Commits (ordem cronológica)

| # | Hash | Data | Autor | Mensagem |
|---:|---|---|---|---|
| 1 | `2383a59` | 08/06/2026 20:41 | José Gabriel Dâmaso | chore: estrutura inicial do repositorio |
| 2 | `043957a` | 08/06/2026 20:41 | José Gabriel Dâmaso | feat(grafo): grafo dirigido com lista de adjacencia e dedup de arestas (RF01) |
| 3 | `3fbfc1d` | 08/06/2026 21:49 | Matheus Vasconcelos Soares | feat(heap): Max-Heap binaria implementada do zero (RF04) |
| 4 | `f7a3535` | 08/06/2026 22:12 | Chinforimpula\* | feat(ciclos): deteccao de ciclo com DFS iterativa de 3 cores (RF03) |
| 5 | `0167a67` | 08/06/2026 22:18 | Pedro Augusto | feat(topo): ordenacao topologica de Kahn com fila de prioridade (RF02) |
| 6 | `0eeb3c2` | 08/06/2026 22:19 | José Gabriel Dâmaso | feat(io): leitura/escrita JSON com mapeamento rotulo<->indice |
| 7 | `98e762e` | 08/06/2026 22:21 | José Gabriel Dâmaso | Merge branch 'main' |
| 8 | `37df668` | 09/06/2026 15:18 | Matheus Vasconcelos Soares | feat(dados): gerador automatico dos 3 niveis (seed fixa, sem libs) |
| 9 | `4efe920` | 09/06/2026 15:26 | Matheus Vasconcelos Soares | Merge branch 'main' |
| 10 | `1a35faf` | 09/06/2026 15:27 | Pedro Augusto | feat(cli): fluxo principal leitura->ciclo->ordem->escrita (argparse) |
| 11 | `fc7b286` | 09/06/2026 15:31 | Matheus Vasconcelos Soares | Merge branch 'main' |
| 12 | `b72db73` | 09/06/2026 15:39 | Matheus Vasconcelos Soares | test(dados): entradas basico/avancado/estresse (10k tarefas / 25k deps) |
| 13 | `1c91539` | 09/06/2026 15:50 | Matheus Vasconcelos Soares | test(gabarito): saidas esperadas dos 3 niveis |
| 14 | `178708b` | 09/06/2026 18:09 | Chinforimpula\* | feat(ciclos): demo recursiva vs iterativa no cenario de estresse |
| 15 | `3631cdc` | 09/06/2026 18:24 | Chinforimpula\* | test(casos): testes de unidade das estruturas e casos-limite |
| 16 | `45a7056` | 09/06/2026 20:10 | Matheus Vasconcelos Soares | chore: Makefile, run.sh e scripts para execucao padronizada |
| 17 | `bac23c6` | 09/06/2026 20:12 | Matheus Vasconcelos Soares | Merge branch 'main' |
| 18 | `e7e3e75` | 09/06/2026 21:16 | Pedro Augusto | chore: ignorar pasta data |
| 19 | `7512a8a` | 09/06/2026 21:26 | Matheus Vasconcelos Soares | Merge branch 'main' |
| 20 | `decc545` | 09/06/2026 21:42 | Pedro Augusto | docs(carga): prova de carga, analise de complexidade e benchmark |
| 21 | `32fafd0` | 09/06/2026 22:04 | José Gabriel Dâmaso | chore: remove data/ do gitignore (gabaritos sao versionados) |
| 22 | `cc17b39` | 09/06/2026 22:05 | José Gabriel Dâmaso | docs: README, decisoes de design e divisao de tarefas |

\* **Chinforimpula** é o nome de usuário do GitHub de **Matheus Dos Santos
Tenório** (conta `matheus.unima2428@gmail.com`).

## Contribuição por integrante

| Integrante | Commits |
|---|---:|
| Matheus Vasconcelos Soares | 9 |
| José Gabriel Dâmaso | 6 |
| Pedro Augusto | 4 |
| Matheus Dos Santos Tenório | 3 |

(contagem de `git shortlog -sne`; este arquivo de documentação entra num commit
adicional de fechamento.)

## Convenção de mensagens

As mensagens seguem o padrão *Conventional Commits* em português:

- `feat` — nova funcionalidade;
- `fix` — correção;
- `test` — testes ou gabaritos;
- `docs` — documentação;
- `chore` — infraestrutura/configuração.

O escopo entre parênteses indica o módulo afetado (`grafo`, `heap`, `io`,
`ciclos`, `topo`, `cli`, `dados`, `carga`). Os commits de *merge* aparecem
naturalmente porque os quatro integrantes trabalharam em paralelo, integrando o
trabalho com `git pull`/`git push`.

## Como reproduzir este relatório

```bash
git log --reverse --date=format:'%d/%m/%Y %H:%M' \
    --pretty=format:'%h | %ad | %an | %s'
git shortlog -sne
```
