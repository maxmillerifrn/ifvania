"""Máquina finita explícita, reutilizada por aplicação e encontros."""


class MaquinaEstados:
    def __init__(self, inicial, transicoes):
        self.transicoes = {estado: frozenset(destinos) for estado, destinos in transicoes.items()}
        if inicial not in self.transicoes:
            raise ValueError(f'Estado inicial desconhecido: {inicial}')
        self.estado = inicial

    def mudar(self, destino):
        if destino == self.estado:
            return
        if destino not in self.transicoes.get(self.estado, ()):
            raise ValueError(f'Transição inválida: {self.estado} → {destino}')
        self.estado = destino
