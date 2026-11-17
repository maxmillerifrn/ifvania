"""Identidade visual dos setores da expansão sem alterar a geometria física."""
import math
import pygame
from mundo.escola_sombria import EscolaSombria
from mundo.arte_escolar import ArteEscolar
from sistema import recursos


class CenarioGuardioes(EscolaSombria):
    def __init__(self, largura, altura, y_piso, identificador):
        super().__init__(largura, altura, y_piso)
        self.identificador = identificador
        self.estabilizados = 0
        self.consultados = set()
        self.memoria = recursos.load_image('cenarios/memoria_tarefa.png', (280, 158)) if identificador == 'continuidade' else None
        if identificador == 'recreio':
            self.arte = ArteEscolar('corridor', largura)

    def draw_background(self, superficie, camera):
        if self.identificador in ('copias', 'recreio'):
            super().draw_background(superficie, camera)
        else:
            superficie.fill((15, 25, 36) if self.identificador == 'rede' else (24, 23, 43))
        if self.identificador == 'recreio':
            # Linhas de quadra e rede ficam ao fundo; só blocos são apoios.
            for x in range(120, self.arte.largura, 640):
                area = camera.apply(pygame.Rect(x, self.y_piso-34, 460, 26))
                pygame.draw.rect(superficie, (98, 62, 44), area)
                pygame.draw.rect(superficie, (222, 207, 167), area.inflate(-16, -12), 2)
                pygame.draw.ellipse(superficie, (222, 207, 167), area.inflate(-260, -12), 2)
                gol = camera.apply(pygame.Rect(x+12, self.y_piso-155, 100, 120))
                pygame.draw.rect(superficie, (138, 162, 163), gol, 2)
                for coluna in range(gol.left+12, gol.right, 12):
                    pygame.draw.line(superficie, (63, 86, 91), (coluna, gol.top), (coluna, gol.bottom))
                placar = camera.apply(pygame.Rect(x+155, 210, 145, 42))
                pygame.draw.rect(superficie, (19, 35, 42), placar, border_radius=4)
                texto = self.fonte.render('RECREIO  '+('LIVRE' if self.estabilizados == 3 else '00:00'), True, (126, 227, 180))
                superficie.blit(texto, texto.get_rect(center=placar.center))
        elif self.identificador == 'rede':
            for indice, x in enumerate(range(70, self.arte.largura, 175)):
                armario = camera.apply(pygame.Rect(x, 200, 110, self.y_piso-200))
                pygame.draw.rect(superficie, (32, 49, 59), armario, border_radius=5)
                pygame.draw.rect(superficie, (87, 106, 113), armario, 2)
                for y in range(armario.top+20, armario.bottom-10, 28):
                    pygame.draw.line(superficie, (16, 25, 33), (armario.left+10, y), (armario.right-10, y), 8)
                    cor = (106, 214, 183) if f'terminal_{indice % 3}' not in self.consultados else (53, 71, 77)
                    pygame.draw.circle(superficie, cor, (armario.left+15, y), 2)
        elif self.identificador == 'copias':
            for indice in range(3-self.estabilizados):
                copia = pygame.Surface(superficie.get_size(), pygame.SRCALPHA)
                x = 200+indice*210-round(camera.deslocamento.x) % 400
                pygame.draw.rect(copia, (123, 194, 206, 50), (x, 220, 150, 120), 2)
                pygame.draw.line(copia, (123, 194, 206, 45), (x, 340), (x+150, 220), 2)
                superficie.blit(copia, (0, 0))
        elif self.identificador == 'continuidade':
            for x in (350, 1300, 2300):
                memoria = self.memoria.copy()
                memoria.set_alpha(65)
                superficie.blit(memoria, (x-camera.deslocamento.x, 180-camera.deslocamento.y))
            for x in range(180, self.arte.largura, 540):
                centro = (x-camera.deslocamento.x, 270-camera.deslocamento.y)
                for raio in (75, 100, 130):
                    pygame.draw.circle(superficie, (65, 66, 99), centro, raio, 2)
                angulo = self.instantes_visuais*0.02
                pygame.draw.line(superficie, (128, 195, 210), centro,
                                 (centro[0]+math.cos(angulo)*100, centro[1]+math.sin(angulo)*100), 3)

    def draw_block(self, superficie, retangulo, camera, largura_mundo, topo_livre=True):
        if self.identificador != 'recreio' or retangulo.y >= self.y_piso or retangulo.y == 0 or retangulo.x in (0, largura_mundo-32):
            return super().draw_block(superficie, retangulo, camera, largura_mundo, topo_livre)
        destino = camera.apply(retangulo)
        pygame.draw.rect(superficie, (94, 76, 58), destino)
        pygame.draw.rect(superficie, (46, 55, 57), destino.inflate(-8, -10))
        if topo_livre:
            pygame.draw.line(superficie, (229, 208, 161), destino.topleft, destino.topright, 4)
