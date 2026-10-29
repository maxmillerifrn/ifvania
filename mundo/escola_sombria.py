"""Laboratório escolar corrompido; desenho independente da geometria física."""
import pygame
from interface import tema
from mundo.arte_escolar import ArteEscolar


class EscolaSombria:
    def __init__(self, largura, altura, y_piso):
        self.arte = ArteEscolar('lab', largura)
        self.instantes_visuais = 0
        self.y_piso = y_piso
        self.fonte = pygame.font.Font(None, 18)

    def draw_background(self, superficie, camera):
        self.arte.draw(superficie, camera, self.instantes_visuais, True)

    def update(self):
        self.instantes_visuais += 1

    def draw_block(self, superficie, retangulo, camera, largura_mundo, topo_livre=True):
        destino = camera.apply(retangulo)
        if not destino.colliderect(superficie.get_rect()):
            return
        if retangulo.y >= self.y_piso:
            pygame.draw.rect(superficie, (26, 34, 40), destino)
            pygame.draw.line(superficie, (38, 48, 54), destino.topleft, destino.topright)
            pygame.draw.line(superficie, (32, 42, 48), destino.topleft, destino.bottomleft)
            if retangulo.y == self.y_piso and topo_livre:
                pygame.draw.rect(superficie, (12, 17, 20), (destino.x, destino.y, destino.width, 7))
                pygame.draw.line(superficie, (186, 191, 164), destino.topleft, (destino.right-1, destino.y), 3)
                pygame.draw.line(superficie, (58, 76, 79), (destino.x, destino.y+4), (destino.right, destino.y+4))
        elif retangulo.x == 0 or retangulo.right == largura_mundo or retangulo.y == 0:
            pygame.draw.rect(superficie, (17, 25, 31), destino)
            if retangulo.y == 0:
                pygame.draw.line(superficie, (47, 60, 65), destino.bottomleft, destino.bottomright)
        else:
            # Metal sólido em primeiro plano; só a face realmente exposta tem faixa.
            pygame.draw.rect(superficie, (57, 72, 78), destino)
            pygame.draw.line(superficie, (13, 20, 25), destino.bottomleft, destino.bottomright, 3)
            pygame.draw.line(superficie, (124, 139, 142), destino.topleft, destino.bottomleft, 2)
            pygame.draw.line(superficie, (13, 20, 25), destino.topright, destino.bottomright, 2)
            pygame.draw.rect(superficie, (31, 44, 51), destino.inflate(-8, -14))
            pygame.draw.circle(superficie, (148, 158, 152), (destino.x+6, destino.bottom-5), 2)
            if topo_livre:
                pygame.draw.rect(superficie, (12, 17, 21), (destino.x, destino.y, destino.width, 9))
                pygame.draw.line(superficie, (235, 213, 156), destino.topleft, (destino.right-1, destino.y), 4)
                for x in range(destino.left+3, destino.right-5, 12):
                    pygame.draw.line(superficie, (188, 159, 96), (x, destino.y+7), (x+5, destino.y+3), 3)

    def draw_exit(self, superficie, gatilho, camera, desbloqueado):
        retangulo = pygame.Rect(gatilho.centerx-28, self.y_piso-126, 56, 126)
        destino = camera.apply(retangulo)
        pygame.draw.rect(superficie, (15, 23, 29), destino)
        pygame.draw.rect(superficie, (66, 84, 87), destino, 3)
        pygame.draw.rect(superficie, (32, 47, 54), destino.inflate(-12, -10))
        indicador = tema.CIANO if desbloqueado else tema.AMBAR
        pygame.draw.rect(superficie, indicador, (destino.x+13, destino.y+16, 30, 5))
        pygame.draw.rect(superficie, indicador, (destino.right-13, destino.centery, 4, 9))
        rotulo = self.fonte.render('SAÍDA', True, tema.PAPEL)
        superficie.blit(rotulo, rotulo.get_rect(midbottom=(destino.centerx, destino.top-5)))
