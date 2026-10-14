"""Câmera 2D simples que segue o jogador e trava nos limites do nível."""
import pygame
import settings


class Camera:
    def __init__(self, level_width, level_height):
        self.offset = pygame.Vector2(0, 0)
        self.level_width = level_width
        self.level_height = level_height

    def update(self, target_rect):
        x = target_rect.centerx - settings.SCREEN_WIDTH // 2
        y = target_rect.centery - settings.SCREEN_HEIGHT // 2
        x = max(0, min(x, max(0, self.level_width - settings.SCREEN_WIDTH)))
        y = max(0, min(y, max(0, self.level_height - settings.SCREEN_HEIGHT)))
        self.offset.x, self.offset.y = x, y

    def apply(self, rect):
        return pygame.Rect(rect.x - self.offset.x, rect.y - self.offset.y, rect.width, rect.height)
