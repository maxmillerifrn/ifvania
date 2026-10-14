"""Sistema de habilidades (power-ups) que o aluno adquire ao derrotar professores."""
from enum import Enum, auto
import pygame
import settings
import assets


class Ability(Enum):
    DOUBLE_JUMP = auto()
    DASH = auto()
    WALL_CLIMB = auto()
    RANGED_SHOT = auto()
    SHIELD = auto()


ABILITY_NAMES = {
    Ability.DOUBLE_JUMP: "Pulo Duplo (RomerBug)",
    Ability.DASH: "Dash Veloz (Python)",
    Ability.WALL_CLIMB: "Escalada de Parede (Java)",
    Ability.RANGED_SHOT: "Tiro de Ponteiro (C)",
    Ability.SHIELD: "Escudo de Dados (SQL)",
}

ABILITY_HOTKEYS = {
    Ability.DOUBLE_JUMP: "Espaço (2x no ar)",
    Ability.DASH: "SHIFT",
    Ability.WALL_CLIMB: "Segure na parede",
    Ability.RANGED_SHOT: "F",
    Ability.SHIELD: "Q",
}


class PowerUp(pygame.sprite.Sprite):
    """Item coletável que concede uma habilidade permanente ao jogador."""

    def __init__(self, x, y, ability: Ability):
        super().__init__()
        self.ability = ability
        size = settings.TILE_SIZE
        self.image = assets.load_image("ui/powerup.png", (size, size), settings.POWERUP_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
        self._t = 0

    def update(self):
        self._t += 1
        self.rect.y += -1 if (self._t // 15) % 2 == 0 else 1

    def draw(self, surface, camera):
        surface.blit(self.image, camera.apply(self.rect))
