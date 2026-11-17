"""Eventos síncronos da sessão, sem depender da apresentação ou do Pygame."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ChefeDerrotado:
    identificador_fase: str


@dataclass(frozen=True)
class FaseConcluida:
    identificador_fase: str


@dataclass(frozen=True)
class ObjetivoConcluido:
    identificador_fase: str
    identificador_objetivo: str


class EventosCampanha:
    def __init__(self):
        self._observadores = {}

    def inscrever(self, tipo_evento, observador):
        """Registra uma vez e devolve a função de remoção da inscrição."""
        observadores = self._observadores.setdefault(tipo_evento, [])
        if observador not in observadores:
            observadores.append(observador)

        def remover():
            if observador in observadores:
                observadores.remove(observador)

        return remover

    def emitir(self, evento):
        # Uma cópia mantém ordem e estabilidade se um observador se remover.
        for observador in tuple(self._observadores.get(type(evento), ())):
            observador(evento)
