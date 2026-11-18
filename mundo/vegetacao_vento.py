"""Brisa nas folhas de fundos raster; arquitetura e colisões permanecem fixas."""
import math
import pygame


class VegetacaoAoVento:
    _cache = {}

    def __init__(self, imagem, regioes, exclusoes=()):
        chave = (id(imagem),tuple(tuple(r) for r in regioes),tuple(tuple(r) for r in exclusoes))
        if chave not in self._cache:
            partes = []
            exclusoes = [pygame.Rect(r) for r in exclusoes]
            for regiao in regioes:
                limites = pygame.Rect(regiao).clip(imagem.get_rect())
                folhas = pygame.Surface(limites.size,pygame.SRCALPHA)
                for y in range(limites.height):
                    for x in range(limites.width):
                        mundial = (x+limites.x,y+limites.y)
                        r,g,b,a = imagem.get_at(mundial)
                        if g > 22 and g > r*1.13 and g > b*0.92 and not any(area.collidepoint(mundial) for area in exclusoes):
                            folhas.set_at((x,y),(r,g,b,a))
                partes.append((limites,folhas))
            self._cache[chave] = partes
        self.partes = self._cache[chave]

    @staticmethod
    def deslocamento(instante, indice, altura_relativa):
        rajada = math.sin(instante*0.037+indice*1.7)+0.45*math.sin(instante*0.073+altura_relativa*3)
        return round(rajada*(1+2*(1-altura_relativa)))

    def draw(self, superficie, instante, deslocamento=(0,0)):
        for indice,(limites,folhas) in enumerate(self.partes):
            destino = limites.move(-round(deslocamento[0]),-round(deslocamento[1]))
            if not destino.inflate(8,0).colliderect(superficie.get_rect()):
                continue
            for y in range(0,limites.height,4):
                trecho = pygame.Rect(0,y,limites.width,min(4,limites.height-y))
                oscilacao = self.deslocamento(instante,indice,y/max(1,limites.height))
                superficie.blit(folhas,(destino.x+oscilacao,destino.y+y),trecho)
