# CLI - junta tudo: le -> detecta ciclo -> ordena -> escreve.

import argparse
import json
import sys
import time

from . import io_handler
from .cycle_detector import find_cycle
from .topological_sort import topological_order

PROJETO = "Orquestrador de Agentes Autônomos (Workflow Engine)"

def build_output(graph, priorities, original_dep_count):
    # primeiro checa ciclo; se tiver, nem tenta ordenar (deadlock)
    ciclo = find_cycle(graph)

    if ciclo is not None:
        ciclo_detectado = True
        ordem = []
    else:
        ciclo_detectado = False
        ordem = topological_order(graph, priorities)
        ciclo = []

    estatisticas = {
        "total_tarefas": graph.num_nodes(),
        "total_dependencias_informadas": original_dep_count,
        "total_dependencias_unicas": graph.num_unique_edges(),
        "dependencias_duplicadas_ignoradas": graph.duplicate_edges,
        "nos_isolados": graph.isolated_nodes(),
    }

    return {
        "projeto": PROJETO,
        "ciclo_detectado": ciclo_detectado,
        "ciclo": ciclo,
        "ordem_execucao": ordem,
        "estatisticas": estatisticas,
    }

def parse_args(argv):
    p = argparse.ArgumentParser(
        description="Orquestrador de Agentes Autônomos — resolve a ordem de "
                    "execução de tarefas dependentes (ordenação topológica + "
                    "prioridade) e detecta deadlocks (ciclos)."
    )
    p.add_argument("input_pos", nargs="?", help="arquivo de entrada (posicional)")
    p.add_argument("output_pos", nargs="?", help="arquivo de saída (posicional)")
    p.add_argument("-i", "--input", help="arquivo JSON de entrada")
    p.add_argument("-o", "--output", help="arquivo JSON de saída")
    args = p.parse_args(argv)

    entrada = args.input or args.input_pos
    saida = args.output or args.output_pos
    if not entrada or not saida:
        p.error("é necessário informar entrada e saída "
                "(ex.: --input X.json --output Y.json)")
    return entrada, saida

def main(argv=None):
    # no console do Windows o padrao costuma ser cp1252; forca UTF-8 no resumo
    # pra acento e nao sair embolado (best-effort, ignora se nao der)
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass

    entrada, saida = parse_args(argv if argv is not None else sys.argv[1:])

    try:
        t0 = time.perf_counter()
        graph, priorities, dep_count = io_handler.load_input(entrada)
        t_load = time.perf_counter()

        output = build_output(graph, priorities, dep_count)
        t_proc = time.perf_counter()

        io_handler.write_output(saida, output)
    except FileNotFoundError:
        print(f"[ERRO] arquivo não encontrado: {entrada}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"[ERRO] JSON inválido em {entrada}: {e}", file=sys.stderr)
        return 1

    est = output["estatisticas"]
    print("=" * 50, file=sys.stderr)
    print(f" Projeto : {PROJETO}", file=sys.stderr)
    print(f" Entrada : {entrada}", file=sys.stderr)
    print(f" Tarefas : {est['total_tarefas']:>10}", file=sys.stderr)
    print(f" Arestas : {est['total_dependencias_unicas']:>10} "
          f"({est['dependencias_duplicadas_ignoradas']} duplicadas ignoradas)",
          file=sys.stderr)
    print(f" Isolados: {est['nos_isolados']:>10}", file=sys.stderr)
    if output["ciclo_detectado"]:
        print(f" Resultado: CICLO detectado (deadlock) - execução abortada.",
              file=sys.stderr)
        print(f"            tamanho do ciclo: {len(output['ciclo']) - 1} nós",
              file=sys.stderr)
    else:
        print(f" Resultado: DAG válido - ordem com "
              f"{len(output['ordem_execucao'])} tarefas gerada.", file=sys.stderr)
    print(f" Tempo leitura      : {(t_load - t0) * 1000:8.2f} ms", file=sys.stderr)
    print(f" Tempo processamento: {(t_proc - t_load) * 1000:8.2f} ms",
          file=sys.stderr)
    print(f" Saída   : {saida}", file=sys.stderr)
    print("=" * 50, file=sys.stderr)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
