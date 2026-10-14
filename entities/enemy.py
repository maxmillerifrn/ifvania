"""Inimigos comuns: os 'bugs' que infestam a escola.

Herda de `Character` e reaproveita a gravidade/colisão prontas da base -
só precisa decidir *para onde* andar (patrulha simples entre dois pontos)
e o que acontece quando morre.
"""
import pygame
import settings
import assets
from entities.character import Character


class Enemy(Character):
    _SPRITES = None
    _ANIM_SPEED = 10  # quadros de jogo entre cada troca de perna/antena

    @classmethod
    def _load_sprites(cls):
        if cls._SPRITES is None:
            size = (26, 24)
            cls._SPRITES = {
                1: [assets.load_image(f"enemies/bug_{i}.png", size, settings.ENEMY_COLOR) for i in range(2)],
                -1: [assets.load_flipped(f"enemies/bug_{i}.png", size, settings.ENEMY_COLOR) for i in range(2)],
            }
        return cls._SPRITES

    def __init__(self, x, y, patrol_range=80, speed=1.4, health=2, color=None):
        super().__init__(x, y, width=26, height=24, health=health)
        self.sprites = self._load_sprites()
        self.image = self.sprites[1][0]
        self.vel.x = speed
        self.start_x = x
        self.patrol_range = patrol_range
        self.speed = speed
        self.color = color or settings.ENEMY_COLOR
        self._t = 0
        self.anim_frame = 0

    def update(self, solids):
        self._t += 1
        if self._t % self._ANIM_SPEED == 0:
            self.anim_frame = 1 - self.anim_frame

        touched_wall = self.move_and_collide_x(solids)
        out_of_patrol_range = (self.rect.x < self.start_x - self.patrol_range
                                or self.rect.x > self.start_x + self.patrol_range)
        if touched_wall != 0 or out_of_patrol_range:
            self.vel.x *= -1

        self.apply_gravity()
        self.move_and_collide_y(solids)

    def take_damage(self, amount, knockback=(0, 0)):
        super().take_damage(amount)
        if not self.alive:
            self.kill()

    def _redraw(self):
        facing = 1 if self.vel.x >= 0 else -1
        self.image = self.sprites[facing][self.anim_frame]

    def draw(self, surface, camera):
        self._redraw()
        super().draw(surface, camera)
