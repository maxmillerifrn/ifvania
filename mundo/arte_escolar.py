"""Ambientes escolares detalhados com mobiliário e terminais em camadas."""
import pygame
from sistema import recursos
from sistema import configuracoes
from mundo.terminal import TelaTerminal
from mundo.turma_laboratorio import TurmaLaboratorio
from mundo.vegetacao_vento import VegetacaoAoVento


class ArteEscolar:
    def __init__(self, ambiente, largura, mostrar_turma=False):
        nome = 'patio_ifrn.png' if ambiente == 'corridor' else 'laboratorio_detalhado.png'
        self.fundo = recursos.load_image('cenarios/'+nome)
        self.vento = VegetacaoAoVento(self.fundo,[(45,112,300,242),(389,112,250,242),(700,112,208,242)],[(132,280,150,78),(490,280,150,78)]) if ambiente == 'corridor' else None
        self.ambiente = ambiente
        self.largura = largura
        self.terminais = TelaTerminal()
        self.etapa_aula = 'codigo'
        self.telas_monitores = []
        self.estatico = pygame.Surface((largura, configuracoes.ALTURA_TELA), pygame.SRCALPHA)
        if ambiente in ('classroom', 'lab') and largura == 960:
            self._bancada_perspectiva(240, 202, 0.8)
            self._bancada_perspectiva(490, 222, 1.0)
        elif ambiente != 'corridor':
            for base in range(0, largura, 960):
                for x in (112, 272, 432, 592):
                    if base+x+138 < largura:
                        self._workstation(base+x, 240)

        self.turma = TurmaLaboratorio(self.telas_monitores) if mostrar_turma else None

    def _bancada_perspectiva(self, x, y, escala):
        """Tampo recua ao fundo; frente, laterais e sombra marcam volume."""
        bancada = pygame.Surface((184, 126), pygame.SRCALPHA)
        pygame.draw.ellipse(bancada, (5, 12, 19, 95), (0, 96, 184, 26))
        for esquerda in (12, 157):
            pygame.draw.polygon(bancada, (33, 44, 49),
                                [(esquerda, 68), (esquerda+7, 68),
                                 (esquerda+4, 110), (esquerda-2, 110)])
            pygame.draw.line(bancada, (94, 105, 107), (esquerda, 71), (esquerda-2, 108), 2)
        pygame.draw.polygon(bancada, (51, 61, 62), [(5, 65), (179, 65), (179, 74), (5, 74)])
        pygame.draw.polygon(bancada, (114, 109, 87), [(30, 42), (151, 42), (179, 65), (5, 65)])
        pygame.draw.lines(bancada, (181, 170, 132), False, [(30, 42), (151, 42), (179, 65), (5, 65)], 2)
        pygame.draw.line(bancada, (28, 40, 44), (6, 73), (178, 73), 2)
        pygame.draw.rect(bancada, (28, 41, 48), (131, 27, 19, 23))
        pygame.draw.line(bancada, (79, 99, 102), (134, 31), (146, 31))
        pygame.draw.circle(bancada, (105, 194, 186), (144, 45), 1)
        pygame.draw.polygon(bancada, (27, 39, 46), [(64, 52), (113, 52), (122, 59), (56, 59)])
        for linha in range(3):
            pygame.draw.line(bancada, (102, 115, 113), (65-linha*2, 53+linha*2), (112+linha*2, 53+linha*2))
        pygame.draw.ellipse(bancada, (51, 67, 70), (127, 54, 8, 5))
        pygame.draw.rect(bancada, (41, 57, 64), (85, 43, 8, 9))
        pygame.draw.rect(bancada, (75, 91, 94), (74, 50, 29, 3))
        pygame.draw.rect(bancada, (9, 18, 25), (51, 0, 78, 48))
        pygame.draw.rect(bancada, (78, 100, 107), (51, 0, 78, 48), 2)
        pygame.draw.line(bancada, (137, 156, 151), (53, 1), (126, 1))
        pygame.draw.circle(bancada, (107, 192, 175), (123, 44), 1)
        tamanho = (round(184*escala), round(126*escala))
        self.estatico.blit(pygame.transform.scale(bancada, tamanho), (x, y))
        self.telas_monitores.append(pygame.Rect(x+round(55*escala), y+round(4*escala),
                                               round(70*escala), round(38*escala)))

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

    def draw(self, superficie, camera, instante, corrompido, hipnose=0):
        deslocamento = round(camera.deslocamento.x)
        # Módulos em resolução nativa: sem esticar uma sala para cobrir todo o corredor.
        for x in range(0, self.largura, self.fundo.get_width()):
            recuo = 32 if self.ambiente in ('classroom', 'lab') and self.largura == 960 else 0
            superficie.blit(self.fundo, (x-deslocamento, -round(camera.deslocamento.y)-recuo))
            if self.vento is not None:
                self.vento.draw(superficie,instante,(deslocamento-x,round(camera.deslocamento.y)))
            if recuo:
                # Abre chão atrás da passagem lateral, para apoiar a fileira distante.
                superficie.blit(self.fundo, (x-deslocamento, 540-recuo-round(camera.deslocamento.y)),
                                pygame.Rect(0, 540-recuo, self.fundo.get_width(), recuo))
        superficie.blit(self.estatico, (-deslocamento, -round(camera.deslocamento.y)))
        for semente, retangulo in enumerate(self.telas_monitores):
            self.terminais.draw(superficie, camera.apply(retangulo), instante, semente, corrompido, 'revolta' if corrompido else self.etapa_aula)
        if self.turma:
            self.turma.draw(superficie, camera, instante, hipnose)
