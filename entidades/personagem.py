from abc import ABC, abstractmethod
import pygame
import configuracoes

class Personagem(pygame.sprite.Sprite,ABC):

    def __init__(self,x,y,
                 largura,
                 altura,
                 vida):
        super().__init__()
        self.largura = largura
        self.altura = altura
        self.x= x
        self.y=y
        self.pos = pygame.Vector(x,y)
        self.vel = pygame.Vector(0,0)
        self.rect = pygame.Rect(x,
                                y,
                                largura,
                                altura)
        #Combate/Vida
        self.max_vidas = vida
        self.vidas = self.max_vidas
        self.alive=True
        self.contato_dano = 1
        self.imagem = None

    @abstractmethod
    def update(self, *args,**kwargs):
        pass

    def tomar_dano(self,
                   valor,
                   contra_ataque(0,0)):
        if not self.alive:
            return
        self.vida -= valor
        if self.vida <=0:
            self.vida = 0
            self.alive = False

    def aplicar_gravidade(self):
        self.vel.y = min(
            self.vel.y +
            configuracoes.GRAVIDADE,
            configuracoes.MAX_FALL_SPEED
        )

    def mover_colidir_x(self, blocos):
        obstaculo = 0
        self.pos.x += self.vel.x
        self.rect.x = round(self.pos.x)
        for tile in blocos:
            if self.rect.colliderect(tile):
                if self.vel.x > 0:
                    self.rect.right = tile.left
                    obstaculo = 1
                elif self.vel.x < 0:
                    self.rect.left = tile.right
                    obstaculo = -1
                self.pos.x = self.rect.x
        return obstaculo

    def mover_colidir_y(self, blocos):
        no_ar = False
        self.pos.y += self.vel.x
        self.rect.y = round(self.pos.y)
        for tile in blocos:
            if self.rect.colliderect(tile):
                if self.vel.y > 0:
                    self.rect.bottom = tile.top
                    no_ar = True
                elif self.vel.y < 0:
                    self.rect.top = tile.bottom
                self.vel.y = 0
                self.pos.y = self.rect.y
        return no_ar

    def desenhar(self, surface, camera):
        surface.blit(self.image,
                     camera.apply(self.rect))

                
