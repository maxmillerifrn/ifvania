"""Câmera 2D simples que segue o jogador e trava nos limites do nível."""
import pygame
import configuracoes


class Camera:
    def __init__(self, largura_fase, altura_fase):
        self.deslocamento = pygame.Vector2(0, 0)
        self.largura_fase = largura_fase
        self.altura_fase = altura_fase

    def update(self, retangulo_alvo):
        x = retangulo_alvo.centerx - configuracoes.LARGURA_TELA // 2
        y = retangulo_alvo.centery - configuracoes.ALTURA_TELA // 2
        x = max(0, min(x, max(0, self.largura_fase - configuracoes.LARGURA_TELA)))
        y = max(0, min(y, max(0, self.altura_fase - configuracoes.ALTURA_TELA)))
        self.deslocamento.x, self.deslocamento.y = x, y

    def apply(self, retangulo):
        return pygame.Rect(retangulo.x - self.deslocamento.x, retangulo.y - self.deslocamento.y, retangulo.width, retangulo.height)
