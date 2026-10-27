"""Informação viva desenhada exclusivamente na superfície interna do monitor."""
import math
import pygame


class TerminalScreen:
    def __init__(self):
        self.font = pygame.font.Font(None, 12)

    def draw(self, surface, rect, tick, seed=0, corrupted=False):
        rect = pygame.Rect(rect)
        if rect.width < 6 or rect.height < 6:
            return
        pane = pygame.Surface(rect.size)
        pane.fill((6, 20, 26))
        accent = (192, 101, 126) if corrupted else (107, 202, 193)
        dim = (51, 100, 110)
        phase = (tick//150+seed) % 3
        page = tick//18+seed*7
        label = 'IFVANIA' if corrupted else ('A28 / REDE', 'SISTEMA', 'ARQUIVOS')[phase]
        pane.blit(self.font.render(label, False, accent), (3, 2))
        pygame.draw.line(pane, dim, (2, 11), (rect.width-3, 11))
        if phase == 1:
            for i in range(max(1, (rect.width-8)//6)):
                height = 2+round((rect.height-22)*(0.5+0.45*math.sin(tick*0.045+i*0.8+seed)))
                pygame.draw.rect(pane, accent, (4+i*6, rect.height-4-height, 4, height))
        else:
            rows = max(1, (rect.height-16)//9)
            logs = ['> rede on', '> load A28', '> cpu %03d' % (page % 999),
                    '> ram %02d%%' % ((page*7) % 100), '> scan %03d' % ((page*11) % 999),
                    '> negado' if corrupted else '> ativo']
            for row in range(rows):
                line = logs[(row+page) % len(logs)]
                pane.blit(self.font.render(line, False, accent if row == rows-1 else (98, 157, 162)), (3, 14+row*9))
            if (tick//24) % 2 == 0:
                pygame.draw.rect(pane, accent, (rect.width-7, rect.height-7, 3, 4))
        # A superfície local corta texto e gráficos sem alterar o clip do cenário.
        surface.blit(pane, rect.topleft)
