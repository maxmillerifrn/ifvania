"""Classe base abstrata para toda personagem viva do jogo.

`Character` reúne o que o aluno, os inimigos comuns e os professores-chefe
têm em comum: posição, vida, dano de contato e a física de queda/colisão
com o cenário. Ela é uma **classe abstrata** (herda de `ABC`) porque não
faz sentido existir uma "personagem genérica" solta no jogo - só as
subclasses concretas (`Player`, `Enemy`, `Boss`) podem ser instanciadas.

O método `update` é marcado com `@abstractmethod`: só declarar essa classe
já impede `Character(...)` de ser criada diretamente, e obriga cada
subclasse a implementar seu próprio comportamento de atualização (cada
tipo de personagem se move de um jeito bem diferente).
"""
from abc import ABC, abstractmethod

import pygame
import settings


class Character(pygame.sprite.Sprite, ABC):
    """Base comum a Player, Enemy e Boss (posição, vida, física, desenho)."""

    VISUAL_SCALE = 1.0

    def __init__(self, x, y, width, height, health):
        super().__init__()
        self.width, self.height = width, height
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(x, y, width, height)

        self.max_health = health
        self.health = health
        self.alive = True
        self.contact_damage = 1

        # cada subclasse define self.image ao carregar seus próprios sprites
        self.image = None

    # ------------------------------------------------------------------
    # Contrato: toda personagem concreta PRECISA saber se atualizar sozinha
    # ------------------------------------------------------------------
    @abstractmethod
    def update(self, *args, **kwargs):
        """Lógica de um quadro (frame). Assinatura varia por subclasse:
        Player usa (solids, hazards), Enemy usa (solids), Boss usa
        (player, solids) - por isso fica abstrato aqui na base."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Dano: implementação padrão, sobrescrita quando a personagem precisa
    # de uma regra especial (Player tem escudo/invencibilidade, Boss tem
    # fases de raiva). Quem sobrescrever normalmente chama
    # `super().take_damage(amount)` para reaproveitar a regra base.
    # ------------------------------------------------------------------
    def take_damage(self, amount, knockback=(0, 0)):
        if not self.alive:
            return
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.alive = False

    # ------------------------------------------------------------------
    # Física reaproveitável por quem obedece gravidade e colide com o
    # cenário (Player e Enemy). O Boss flutua dentro de uma arena e não
    # usa esses métodos.
    # ------------------------------------------------------------------
    def apply_gravity(self):
        """Acelera a queda até a velocidade terminal definida em settings."""
        self.vel.y = min(self.vel.y + settings.GRAVITY, settings.MAX_FALL_SPEED)

    def move_and_collide_x(self, solids):
        """Move no eixo X e resolve colisão com o cenário.

        Devolve -1/0/1 indicando se encostou numa parede à esquerda,
        nenhuma, ou à direita."""
        touched_wall = 0
        self.pos.x += self.vel.x
        self.rect.x = round(self.pos.x)
        for tile in solids:
            if self.rect.colliderect(tile):
                if self.vel.x > 0:
                    self.rect.right = tile.left
                    touched_wall = 1
                elif self.vel.x < 0:
                    self.rect.left = tile.right
                    touched_wall = -1
                self.pos.x = self.rect.x
        return touched_wall

    def move_and_collide_y(self, solids):
        """Move no eixo Y e resolve colisão com o cenário.

        Devolve True se encostou no chão."""
        on_ground = False
        self.pos.y += self.vel.y
        self.rect.y = round(self.pos.y)
        for tile in solids:
            if self.rect.colliderect(tile):
                if self.vel.y > 0:
                    self.rect.bottom = tile.top
                    on_ground = True
                elif self.vel.y < 0:
                    self.rect.top = tile.bottom
                self.vel.y = 0
                self.pos.y = self.rect.y
        return on_ground

    # ------------------------------------------------------------------
    # Desenho padrão: só posiciona o sprite atual na tela pela câmera.
    # Subclasses com efeitos extras (piscar, flash de dano, barra de fase)
    # chamam `super().draw(surface, camera)` e completam por cima.
    # ------------------------------------------------------------------
    def get_draw_image(self):
        """Escala apenas a arte; o apoio dos pés e o corpo físico são preservados."""
        size = tuple(round(side * self.VISUAL_SCALE) for side in self.image.get_size())
        if size == self.image.get_size():
            return self.image
        return pygame.transform.scale(self.image, size)

    def draw(self, surface, camera):
        image = self.get_draw_image()
        dest = camera.apply(self.rect)
        surface.blit(image, image.get_rect(midbottom=dest.midbottom))
