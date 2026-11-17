"""Ciclos de cenário e resgates visuais sem aliados vulneráveis."""
import math
import pygame
from sistema import recursos


class DesafiosCampus:
    def __init__(self, identificador):
        self.identificador = identificador
        self.instante = 0
        self.resgatados = []
        self.zonas = [pygame.Rect(23*32, 14*32-12, 112, 12), pygame.Rect(39*32, 14*32-12, 112, 12)]

    def update(self):
        self.instante += 1
        for estudante in self.resgatados:
            estudante[1] += 1
        self.resgatados = [estudante for estudante in self.resgatados if estudante[1] < 120]

    def registrar_resgate(self, centro, indice):
        if self.identificador == 'recreio':
            self.resgatados.append([pygame.Vector2(centro), 0, indice])

    def areas_ativas(self, concluidos):
        return [zona for indice, zona in enumerate(self.zonas)
                if f'terminal_{indice}' not in concluidos and 45 <= (self.instante+indice*65) % 180 < 63]

    def draw(self, superficie, camera, concluidos):
        for indice, zona in enumerate(self.zonas):
            if f'terminal_{indice}' in concluidos:
                continue
            tempo = (self.instante+indice*65) % 180
            destino = camera.apply(zona)
            if tempo < 45:
                cor = (181, 139, 86)
                pygame.draw.line(superficie, cor, destino.midleft, destino.midright, 1)
            elif tempo < 63:
                for x in range(destino.left, destino.right, 12):
                    deslocamento = round(math.sin((x+self.instante)*0.2)*4)
                    pygame.draw.line(superficie, (245, 199, 101), (x, destino.bottom), (x+5, destino.top-9+deslocamento), 3)
        for origem, instante, indice in self.resgatados:
            pasta = 'jogador/menina' if indice % 2 else 'jogador'
            quadro = (instante//5) % 8
            figura = recursos.load_image(f'apresentacao/{pasta}/ciclo_caminhada/caminhada_{quadro}.png')
            figura = pygame.transform.flip(figura, True, False).copy()
            figura.set_alpha(min(255, (120-instante)*12))
            destino = origem-pygame.Vector2(instante*1.8, 0)-camera.deslocamento
            superficie.blit(figura, figura.get_rect(midbottom=destino))
