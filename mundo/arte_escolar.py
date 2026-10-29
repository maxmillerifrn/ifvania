"""Ambientes escolares detalhados com mobiliário e terminais em camadas."""
import pygame
import recursos
import configuracoes
from mundo.terminal import TelaTerminal


class ArteEscolar:
    def __init__(self, ambiente, largura):
        nome = 'corredor_detalhado.png' if ambiente == 'corridor' else 'laboratorio_detalhado.png'
        self.fundo = recursos.load_image('cenarios/'+nome)
        self.ambiente = ambiente
        self.largura = largura
        self.terminais = TelaTerminal()
        self.telas_monitores = []
        self.estatico = pygame.Surface((largura, configuracoes.ALTURA_TELA), pygame.SRCALPHA)
        if ambiente != 'corridor':
            for base in range(0, largura, 960):
                for x in (112, 272, 432, 592):
                    if base+x+138 < largura:
                        self._workstation(base+x, 240)

    def _workstation(self, x, y):
        s = self.estatico
        # Mesa: tampo com espessura, gaveta, pés, gabinete e teclado.
        pygame.draw.rect(s, (11, 18, 24), (x-8, y+78, 142, 34))
        for x_painel in (x-4, x+66):
            pygame.draw.rect(s, (29, 40, 46), (x_painel, y+83, 62, 25))
            pygame.draw.rect(s, (51, 64, 68), (x_painel, y+83, 62, 25), 1)
            pygame.draw.line(s, (106, 116, 112), (x_painel+45, y+89), (x_painel+55, y+89), 2)
            for ventilacao in range(3):
                pygame.draw.line(s, (15, 26, 32), (x_painel+6, y+93+ventilacao*4), (x_painel+24, y+93+ventilacao*4))
        pygame.draw.rect(s, (91, 91, 77), (x-12, y+74, 150, 6))
        pygame.draw.line(s, (152, 142, 111), (x-12, y+74), (x+137, y+74))
        for perna in (x-6, x+125):
            pygame.draw.rect(s, (42, 55, 60), (perna, y+80, 5, 32))
        pygame.draw.rect(s, (19, 28, 34), (x+104, y+43, 24, 31))
        pygame.draw.rect(s, (53, 67, 71), (x+106, y+45, 20, 2))
        for fileira in range(4):
            pygame.draw.line(s, (48, 64, 68), (x+108, y+51+fileira*4), (x+122, y+51+fileira*4))
        pygame.draw.circle(s, (88, 164, 166), (x+119, y+69), 1)
        pygame.draw.rect(s, (24, 37, 44), (x+10, y+65, 76, 8))
        for kx in range(x+14, x+80, 6):
            for ky in (y+67, y+70):
                pygame.draw.rect(s, (74, 90, 91), (kx, ky, 4, 1))
        # Moldura e reflexos do monitor; nada animado é pintado na moldura.
        pygame.draw.rect(s, (5, 11, 17), (x+10, y, 84, 58))
        pygame.draw.rect(s, (66, 81, 87), (x+10, y, 84, 58), 2)
        pygame.draw.line(s, (112, 128, 127), (x+12, y+1), (x+91, y+1))
        pygame.draw.rect(s, (47, 61, 67), (x+46, y+58, 10, 6))
        pygame.draw.rect(s, (58, 70, 73), (x+34, y+62, 34, 3))
        pygame.draw.circle(s, (89, 176, 171), (x+87, y+54), 1)
        self.telas_monitores.append(pygame.Rect(x+16, y+5, 72, 46))
        # Cabos e pequenos acessórios dão profundidade sem novas colisões.
        pygame.draw.lines(s, (24, 35, 40), False,
                          [(x+100, y+68), (x+100, y+88), (x+117, y+88), (x+117, y+110)], 2)
        pygame.draw.ellipse(s, (88, 104, 107), (x+91, y+66, 8, 5))

    def draw(self, superficie, camera, instante, corrompido):
        deslocamento = round(camera.deslocamento.x)
        # Módulos em resolução nativa: sem esticar uma sala para cobrir todo o corredor.
        for x in range(0, self.largura, self.fundo.get_width()):
            superficie.blit(self.fundo, (x-deslocamento, -round(camera.deslocamento.y)))
        superficie.blit(self.estatico, (-deslocamento, -round(camera.deslocamento.y)))
        for semente, retangulo in enumerate(self.telas_monitores):
            self.terminais.draw(superficie, camera.apply(retangulo), instante, semente, corrompido)
