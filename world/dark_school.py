"""Laboratório escolar corrompido; desenho independente da geometria física."""
import pygame
from ui import theme
from world.school_art import SchoolArt


class DarkSchool:
    def __init__(self, width, height, floor_y):
        self.art = SchoolArt('lab', width)
        self.visual_ticks = 0
        self.floor_y = floor_y
        self.font = pygame.font.Font(None, 18)

    def draw_background(self, surface, camera):
        self.art.draw(surface, camera, self.visual_ticks, True)

    def update(self):
        self.visual_ticks += 1

    def draw_block(self, surface, rect, camera, world_width):
        dest = camera.apply(rect)
        if not dest.colliderect(surface.get_rect()):
            return
        if rect.y >= self.floor_y:
            pygame.draw.rect(surface, (26, 34, 40), dest)
            pygame.draw.line(surface, (38, 48, 54), dest.topleft, dest.topright)
            pygame.draw.line(surface, (32, 42, 48), dest.topleft, dest.bottomleft)
            if rect.y == self.floor_y:
                pygame.draw.line(surface, (108, 118, 111), dest.topleft, dest.topright, 3)
                pygame.draw.line(surface, (58, 76, 79), (dest.x, dest.y+4), (dest.right, dest.y+4))
        elif rect.x == 0 or rect.right == world_width or rect.y == 0:
            pygame.draw.rect(surface, (17, 25, 31), dest)
            if rect.y == 0:
                pygame.draw.line(surface, (47, 60, 65), dest.bottomleft, dest.bottomright)
        else:
            # Bancadas de laboratório ocupam exatamente os blocos de colisão.
            pygame.draw.rect(surface, (36, 46, 51), dest)
            pygame.draw.line(surface, (141, 132, 106), dest.topleft, dest.topright, 3)
            pygame.draw.rect(surface, (19, 28, 34), dest.inflate(-8, -12))
            pygame.draw.line(surface, (63, 78, 81), (dest.x+6, dest.y+10), (dest.right-6, dest.y+10))

    def draw_exit(self, surface, trigger, camera, unlocked):
        rect = pygame.Rect(trigger.centerx-28, self.floor_y-126, 56, 126)
        dest = camera.apply(rect)
        pygame.draw.rect(surface, (15, 23, 29), dest)
        pygame.draw.rect(surface, (66, 84, 87), dest, 3)
        pygame.draw.rect(surface, (32, 47, 54), dest.inflate(-12, -10))
        indicator = theme.CYAN if unlocked else theme.AMBER
        pygame.draw.rect(surface, indicator, (dest.x+13, dest.y+16, 30, 5))
        pygame.draw.rect(surface, indicator, (dest.right-13, dest.centery, 4, 9))
        label = self.font.render('SAÍDA', True, theme.PAPER)
        surface.blit(label, label.get_rect(midbottom=(dest.centerx, dest.top-5)))
