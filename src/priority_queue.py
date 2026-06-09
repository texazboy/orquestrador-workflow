# RF04 - Max-Heap binaria feita na mao (sem heapq).
# Guarda pares (chave, valor); compara pela chave e devolve o valor.
# A chave que o resto do projeto usa eh (prioridade, -indice).

class MaxHeap:
    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def empty(self):
        return len(self._data) == 0

    def push(self, chave, valor):
        self._data.append((chave, valor))
        self._sift_up(len(self._data) - 1)

    def pop(self):
        if not self._data:
            raise IndexError("pop() chamado em heap vazia")
        topo = self._data[0]
        ultimo = self._data.pop()
        if self._data:
            # joga o ultimo pra raiz e desce ate achar o lugar dele
            self._data[0] = ultimo
            self._sift_down(0)
        return topo[1]

    def peek(self):
        if not self._data:
            raise IndexError("peek() chamado em heap vazia")
        return self._data[0][1]

    def _sift_up(self, i):
        data = self._data
        while i > 0:
            pai = (i - 1) // 2
            if data[i][0] > data[pai][0]:
                data[i], data[pai] = data[pai], data[i]
                i = pai
            else:
                break

    def _sift_down(self, i):
        data = self._data
        n = len(data)
        while True:
            esq = 2 * i + 1
            dir = 2 * i + 2
            maior = i
            if esq < n and data[esq][0] > data[maior][0]:
                maior = esq
            if dir < n and data[dir][0] > data[maior][0]:
                maior = dir
            if maior == i:   # ja esta na posicao certa
                break
            data[i], data[maior] = data[maior], data[i]
            i = maior
