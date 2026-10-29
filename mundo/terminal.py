"""Informação viva desenhada exclusivamente na superfície interna do monitor."""
import math
import pygame


class TelaTerminal:
    def __init__(self):
        self.fonte = pygame.font.Font(None, 12)

    def draw(self, superficie, retangulo, instante, semente=0, corrompido=False):
        retangulo = pygame.Rect(retangulo)
        if retangulo.width < 6 or retangulo.height < 6:
            return
        area_interna = pygame.Surface(retangulo.size)
        area_interna.fill((6, 20, 26))
        destaque = (192, 101, 126) if corrompido else (107, 202, 193)
        cor_atenuada = (51, 100, 110)
        etapa = (instante//150+semente) % 3
        pagina = instante//18+semente*7
        rotulo = 'IFVANIA' if corrompido else ('A28 / REDE', 'SISTEMA', 'ARQUIVOS')[etapa]
        area_interna.blit(self.fonte.render(rotulo, False, destaque), (3, 2))
        pygame.draw.line(area_interna, cor_atenuada, (2, 11), (retangulo.width-3, 11))
        if etapa == 1:
            for i in range(max(1, (retangulo.width-8)//6)):
                altura = 2+round((retangulo.height-22)*(0.5+0.45*math.sin(instante*0.045+i*0.8+semente)))
                pygame.draw.rect(area_interna, destaque, (4+i*6, retangulo.height-4-altura, 4, altura))
        else:
            fileiras = max(1, (retangulo.height-16)//9)
            registros = ['> rede on', '> load A28', '> cpu %03d' % (pagina % 999),
                    '> ram %02d%%' % ((pagina*7) % 100), '> scan %03d' % ((pagina*11) % 999),
                    '> negado' if corrompido else '> ativo']
            for fileira in range(fileiras):
                linha = registros[(fileira+pagina) % len(registros)]
                area_interna.blit(self.fonte.render(linha, False, destaque if fileira == fileiras-1 else (98, 157, 162)), (3, 14+fileira*9))
            if (instante//24) % 2 == 0:
                pygame.draw.rect(area_interna, destaque, (retangulo.width-7, retangulo.height-7, 3, 4))
        # A superfície local corta texto e gráficos sem alterar o clip do cenário.
        superficie.blit(area_interna, retangulo.topleft)
