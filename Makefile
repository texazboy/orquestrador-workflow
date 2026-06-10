# Makefile — Orquestrador de Agentes Autônomos (Workflow Engine)
#
# Alvos principais:
#   make gen     -> gera os 3 níveis de dados em data/
#   make run     -> roda o nível básico e imprime a saída
#   make test    -> roda os 3 níveis e compara com o gabarito (data/output_esperado_*)
#   make bench   -> roda a prova de carga (tabela de tempo + memória de pico)
#   make clean   -> remove caches e saídas temporárias
#   make help    -> lista os alvos

PYTHON ?= python3

.PHONY: help gen run test bench clean

help:
	@echo "Alvos disponiveis:"
	@echo "  make gen    - gera input_basico/avancado/estresse em data/"
	@echo "  make run    - executa o nivel basico e mostra a saida"
	@echo "  make test   - executa os 3 niveis e compara com o gabarito"
	@echo "  make bench  - roda o benchmark (tempo + memoria de pico)"
	@echo "  make clean  - limpa caches e arquivos temporarios"

gen:
	$(PYTHON) -m src.generate_data

run:
	$(PYTHON) -m src.main --input data/input_basico.json --output /tmp/saida_basico.json
	@echo "----- saida (basico) -----"
	@cat /tmp/saida_basico.json

# Roda cada nivel e compara a saida com o gabarito correspondente.
# Usa comparacao canonica (chaves ordenadas) para nao depender de espacos.
test:
	@ok=1; \
	for nivel in basico avancado estresse; do \
		$(PYTHON) -m src.main --input data/input_$$nivel.json --output /tmp/saida_$$nivel.json 2>/dev/null; \
		a=$$($(PYTHON) -c "import json,sys;print(json.dumps(json.load(open('/tmp/saida_'+'$$nivel'+'.json')),sort_keys=True))"); \
		b=$$($(PYTHON) -c "import json,sys;print(json.dumps(json.load(open('data/output_esperado_'+'$$nivel'+'.json')),sort_keys=True))"); \
		if [ "$$a" = "$$b" ]; then \
			echo "[OK]    $$nivel: saida bate com o gabarito"; \
		else \
			echo "[FALHA] $$nivel: saida DIVERGE do gabarito"; ok=0; \
		fi; \
	done; \
	if [ $$ok -eq 1 ]; then echo "==> Todos os niveis passaram."; else echo "==> Houve divergencia."; exit 1; fi

bench:
	$(PYTHON) -m src.benchmark

clean:
	rm -rf src/__pycache__ .pytest_cache
	rm -f /tmp/saida_*.json
	@echo "Limpo."
