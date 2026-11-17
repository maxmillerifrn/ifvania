"""Encenação visual da bolsa e retirada do mouse durante o diálogo."""
import math
import pygame


class DescobertaMouse:
    def __init__(self):
        self.instante = 0
        self.visivel = False

    def update(self, indice_fala):
        self.visivel = indice_fala >= 2
        if self.visivel:
            self.instante = min(100, self.instante+1)

    def draw(self, superficie, camera, jogador):
        if not self.visivel:
            return
        destino_final = superficie
        superficie = pygame.Surface((120, 100), pygame.SRCALPHA)
        corpo = pygame.Rect(12, 20, 40, 40)
        bolsa = pygame.Rect(corpo.right+12, corpo.bottom-28, 28, 27)
        pygame.draw.rect(superficie, (17, 31, 35), bolsa.inflate(4, 2), border_radius=6)
        pygame.draw.rect(superficie, (38, 102, 72), bolsa, border_radius=5)
        abertura = min(12, self.instante//2)
        pygame.draw.line(superficie, (203, 190, 139), bolsa.topleft, (bolsa.right, bolsa.top-abertura), 3)
        progresso = max(0, min(1, (self.instante-15)/50))
        origem = pygame.Vector2(bolsa.centerx, bolsa.top)
        destino = pygame.Vector2(corpo.centerx+12, corpo.top+5)
        mouse = origem.lerp(destino, progresso)
        mouse.y -= math.sin(progresso*math.pi)*16
        pygame.draw.lines(superficie, (158, 186, 190), False, [origem, (mouse.x+10, mouse.y+10), mouse], 2)
        pygame.draw.ellipse(superficie, (202, 198, 177), (mouse.x-6, mouse.y-9, 12, 18))
        pygame.draw.line(superficie, (39, 56, 61), (mouse.x, mouse.y-7), (mouse.x, mouse.y-1), 2)
        pygame.draw.line(superficie, (176, 127, 91), (corpo.left, corpo.top+8), mouse, 5)
        imagem = pygame.transform.smoothscale(superficie, (300, 250))
        destino = imagem.get_rect(center=(480, 200))
        pygame.draw.rect(destino_final, (15, 28, 36), destino, border_radius=10)
        pygame.draw.rect(destino_final, (89, 161, 158), destino, 2, border_radius=10)
        destino_final.blit(imagem, destino)
