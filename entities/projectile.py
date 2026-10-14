"""Projéteis disparados pelo aluno (ponteiros) e pelos professores-chefe."""
import pygame
import settings


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, owner="player", speed=None, color=None, damage=1):
        super().__init__()
        self.owner = owner
        w, h = 14, 6
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        color = color or (settings.PROJECTILE_PLAYER_COLOR if owner == "player" else settings.PROJECTILE_ENEMY_COLOR)
        pygame.draw.ellipse(self.image, color, (0, 0, w, h))
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.Vector2(self.rect.center)
        self.speed = speed if speed is not None else settings.SHOT_SPEED
        self.vel = pygame.Vector2(direction).normalize() * self.speed if direction else pygame.Vector2(0, 0)
        self.damage = damage
        self.life = 90

    def update(self, solids):
        self.pos += self.vel
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.life -= 1
        if self.life <= 0:
            self.kill()
            return
        for tile in solids:
            if self.rect.colliderect(tile):
                self.kill()
                return

    def draw(self, surface, camera):
        surface.blit(self.image, camera.apply(self.rect))
