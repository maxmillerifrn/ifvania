"""Sistema de habilidades (power-ups) que o aluno adquire ao derrotar professores."""
from enum import Enum, auto
import pygame
import configuracoes
import recursos


class Habilidade(Enum):
    SALTO_DUPLO = auto()
    ARRANCADA = auto()
    ESCALADA_PAREDE = auto()
    DISPARO_DISTANCIA = auto()
    ESCUDO = auto()


NOMES_HABILIDADES = {
    Habilidade.SALTO_DUPLO: "Pulo Duplo (RomerBug)",
    Habilidade.ARRANCADA: "Dash Veloz (Python)",
    Habilidade.ESCALADA_PAREDE: "Escalada de Parede (Java)",
    Habilidade.DISPARO_DISTANCIA: "Tiro de Ponteiro (C)",
    Habilidade.ESCUDO: "Escudo de Dados (SQL)",
}

TECLAS_HABILIDADES = {
    Habilidade.SALTO_DUPLO: "Espaço (2x no ar)",
    Habilidade.ARRANCADA: "SHIFT",
    Habilidade.ESCALADA_PAREDE: "Segure na parede",
    Habilidade.DISPARO_DISTANCIA: "F",
    Habilidade.ESCUDO: "Q",
}


class ItemHabilidade(pygame.sprite.Sprite):
    """Item coletável que concede uma habilidade permanente ao jogador."""

    def __init__(self, x, y, habilidade: Habilidade):
        super().__init__()
        self.habilidade = habilidade
        tamanho = configuracoes.TAMANHO_BLOCO
        self.image = recursos.load_image("interface/item_habilidade.png", (tamanho, tamanho), configuracoes.COR_ITEM_HABILIDADE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self._tempo = 0

    def update(self):
        self._tempo += 1
        self.rect.y += -1 if (self._tempo // 15) % 2 == 0 else 1

    def draw(self, superficie, camera):
        superficie.blit(self.image, camera.apply(self.rect))
