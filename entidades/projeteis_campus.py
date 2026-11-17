"""Objetos legíveis de esporte e arquivo; vida limitada e ricochete único."""
import pygame
from entidades.projetil import Projetil


class BolaVirtual(Projetil):
    def __init__(self, x, y, direcao):
        super().__init__(x, y, (direcao, -0.25), dono='boss', velocidade=4.5)
        self.image = pygame.Surface((22, 22), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (110, 217, 169), (11, 11), 10)
        pygame.draw.circle(self.image, (232, 244, 195), (11, 11), 10, 2)
        pygame.draw.line(self.image, (35, 85, 69), (2, 11), (20, 11), 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.ricochetes = 1
        self.duracao_restante = 150

    def update(self, solidos):
        anterior = self.rect.copy()
        self.velocidade.y = min(7, self.velocidade.y+0.12)
        self.posicao += self.velocidade
        self.rect.center = round(self.posicao.x), round(self.posicao.y)
        self.duracao_restante -= 1
        if self.duracao_restante <= 0:
            self.kill()
            return
        for bloco in solidos:
            if not self.rect.colliderect(bloco):
                continue
            if not self.ricochetes:
                self.kill()
                return
            self.ricochetes -= 1
            if anterior.bottom <= bloco.top and self.velocidade.y > 0:
                self.rect.bottom = bloco.top
                self.velocidade.y = -max(2.8, abs(self.velocidade.y)*0.8)
            else:
                self.rect.right = bloco.left if self.velocidade.x > 0 else self.rect.right
                if self.velocidade.x < 0:
                    self.rect.left = bloco.right
                self.velocidade.x *= -1
            self.posicao.update(self.rect.center)
            return


class FichaArquivo(Projetil):
    def __init__(self, x, y, direcao):
        super().__init__(x, y, (direcao, 0), dono='boss', velocidade=3.7)
        self.image = pygame.Surface((22, 14), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (222, 211, 177), (0, 0, 22, 14), border_radius=2)
        for linha in (4, 8, 11):
            pygame.draw.line(self.image, (85, 103, 112), (4, linha), (18, linha))
        self.rect = self.image.get_rect(center=(x, y))
