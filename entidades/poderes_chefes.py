"""Poderes ativos: energia sombria e raio lançado pela cabeça do avatar."""
import pygame
from entidades.projetil import Projetil


class PulsoSombrio(Projetil):
    def __init__(self, origem, direcao):
        super().__init__(*origem,direcao,dono='boss',velocidade=5,cor=(157,91,221))
        self.image = pygame.Surface((24,20),pygame.SRCALPHA)
        pygame.draw.ellipse(self.image,(67,38,104),(0,0,24,20))
        pygame.draw.ellipse(self.image,(183,116,239),(4,3,16,14),2)
        self.rect = self.image.get_rect(center=origem)
        self.posicao.update(origem)
        self.duracao_restante = 65


class RaioBrilhante(Projetil):
    def __init__(self, origem, direcao):
        super().__init__(*origem,direcao,dono='boss',velocidade=7)
        self.image = pygame.Surface((34,14),pygame.SRCALPHA)
        pontos = [(0,7),(9,2),(14,10),(23,4),(33,7)]
        pygame.draw.lines(self.image,(88,173,239),False,pontos,6)
        pygame.draw.lines(self.image,(237,249,255),False,pontos,2)
        if self.velocidade.x < 0: self.image = pygame.transform.flip(self.image,True,False)
        self.rect = self.image.get_rect(center=origem)
        self.posicao.update(origem)
        self.duracao_restante = 65
