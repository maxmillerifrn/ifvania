"""Seleção de ação independente da execução e dos temporizadores."""


class EstrategiaCorpoACorpo:
    def escolher(self, inimigo, jogador):
        distancia = abs(jogador.rect.centerx-inimigo.rect.centerx)
        return 'preparar' if distancia < 120 else 'patrulhar'


class EstrategiaLancador:
    def escolher(self, inimigo, jogador):
        return 'preparar' if abs(jogador.rect.centerx-inimigo.rect.centerx) < 400 else 'patrulhar'
