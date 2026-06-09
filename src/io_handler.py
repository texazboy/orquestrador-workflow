# Camada de I/O: le o JSON de entrada e escreve o de saida.
# Aqui eh o unico lugar onde o rotulo da tarefa vira indice inteiro do grafo.

import json

from .graph import Graph


def load_input(path):
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    tasks = raw.get("tasks", [])
    deps = raw.get("dependencies", [])

    # junta todo rotulo que aparece (em tasks ou nas dependencias)
    labels = set()
    prio_map = {}
    for t in tasks:
        tid = t["id"]
        labels.add(tid)
        prio_map[tid] = int(t.get("priority", 0))
    for d in deps:
        labels.add(d["from"])
        labels.add(d["to"])

    # insere em ordem alfabetica: assim o indice interno acompanha o rotulo,
    # o que deixa os desempates deterministicos
    g = Graph()
    for label in sorted(labels):
        g.add_node(label)

    priorities = [0] * g.num_nodes()
    for label in labels:
        priorities[g.index_of(label)] = prio_map.get(label, 0)

    for d in deps:
        g.add_edge(d["from"], d["to"])

    g.finalize()
    # devolve tambem o total bruto de dependencias (antes de deduplicar)
    return g, priorities, len(deps)


def write_output(path, output_dict):
    # newline="\n" forca LF mesmo no Windows; senao o modo texto trocaria por
    # \r\n e a saida deixaria de bater byte a byte com o gabarito (determinismo)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(output_dict, f, ensure_ascii=False, indent=2)
        f.write("\n")
