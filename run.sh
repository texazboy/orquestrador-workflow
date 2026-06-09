#!/usr/bin/env bash
#
# Script de execução padrão do Orquestrador de Workflow.
# Uso:
#   ./run.sh --input data/input_basico.json --output saida.json
#   ./run.sh -i data/input_avancado.json -o saida.json
#   ./run.sh data/input_estresse.json saida.json   (posicional)
#
# Repassa todos os argumentos diretamente para o módulo principal.
set -euo pipefail

# Garante que rodamos a partir da raiz do projeto (onde está o pacote src/).
cd "$(dirname "$0")"

exec python3 -m src.main "$@"
