"""Progresso idempotente em memória; uma instância por campanha."""
from sistema.eventos_campanha import ChefeDerrotado, FaseConcluida, ObjetivoConcluido


class ProgressoCampanha:
    def __init__(self, eventos):
        self._chefes_derrotados = set()
        self._fases_concluidas = set()
        self._objetivos_concluidos = set()
        self._remocoes = (
            eventos.inscrever(ChefeDerrotado, self._registrar_chefe),
            eventos.inscrever(FaseConcluida, self._registrar_fase),
            eventos.inscrever(ObjetivoConcluido, self._registrar_objetivo),
        )

    @property
    def chefes_derrotados(self):
        return frozenset(self._chefes_derrotados)

    @property
    def fases_concluidas(self):
        return frozenset(self._fases_concluidas)

    def _registrar_chefe(self, evento):
        self._chefes_derrotados.add(evento.identificador_fase)

    def _registrar_fase(self, evento):
        self._fases_concluidas.add(evento.identificador_fase)

    def _registrar_objetivo(self, evento):
        self._objetivos_concluidos.add((evento.identificador_fase, evento.identificador_objetivo))

    def objetivos_da_fase(self, identificador):
        return frozenset(objetivo for fase, objetivo in self._objetivos_concluidos if fase == identificador)

    def encerrar(self):
        """Desliga a sessão antiga antes de iniciar outra no mesmo jogo."""
        for remover in self._remocoes:
            remover()
