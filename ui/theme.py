"""Paleta e superfícies compartilhadas da interface escolar sombria."""
import pygame

INK = (9, 14, 19)
PANEL = (15, 23, 30)
RAISED = (24, 35, 43)
BORDER = (64, 80, 87)
PAPER = (226, 224, 211)
MUTED = (151, 165, 169)
AMBER = (198, 166, 105)
CYAN = (111, 181, 187)
DANGER = (179, 78, 87)


def panel(surface, rect, accent=None, fill=PANEL):
    rect = pygame.Rect(rect)
    shadow = pygame.Surface(rect.size, pygame.SRCALPHA)
    shadow.fill((0, 0, 0, 100))
    surface.blit(shadow, rect.move(3, 4))
    pygame.draw.rect(surface, fill, rect)
    pygame.draw.rect(surface, BORDER, rect, 1)
    pygame.draw.line(surface, (43, 57, 65), (rect.left+1, rect.top+1),
                     (rect.right-2, rect.top+1))
    if accent:
        pygame.draw.rect(surface, accent, (rect.left, rect.top+8, 3, rect.height-16))


def text(surface, font, value, position, color=PAPER):
    surface.blit(font.render(value, True, color), position)


def fit_text(font, value, width):
    """Elide nomes longos sem invadir barras e botões adjacentes."""
    if font.size(value)[0] <= width:
        return value
    while value and font.size(value+'...')[0] > width:
        value = value[:-1]
    return value+'...'
