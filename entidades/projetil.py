"""Projéteis disparados pelo aluno (ponteiros) e pelos professores-chefe."""
import pygame
import configuracoes


class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao, dono='jogador', velocidade=None, cor=None, dano=1):
        super().__init__()
        self.dono = dono
        largura, altura = 14, 6
        self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
        cor = cor or (configuracoes.COR_PROJETIL_JOGADOR if dono == 'jogador' else configuracoes.COR_PROJETIL_INIMIGO)
        pygame.draw.ellipse(self.image, cor, (0, 0, largura, altura))
        self.rect = self.image.get_rect(center=(x, y))
        self.posicao = pygame.Vector2(self.rect.center)
        self.rapidez = velocidade if velocidade is not None else configuracoes.VELOCIDADE_DISPARO
        self.velocidade = pygame.Vector2(direcao).normalize() * self.rapidez if direcao else pygame.Vector2(0, 0)
        self.dano = dano
        self.duracao_restante = 90

    def update(self, solidos):
        self.posicao += self.velocidade
        self.rect.center = (round(self.posicao.x), round(self.posicao.y))
        self.duracao_restante -= 1
        if self.duracao_restante <= 0:
            self.kill()
            return
        for bloco in solidos:
            if self.rect.colliderect(bloco):
                self.kill()
                return

    def draw(self, superficie, camera):
        superficie.blit(self.image, camera.apply(self.rect))
