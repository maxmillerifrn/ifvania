import pygame
import configuracoes
from personagem import Personagem
from powerups import Habilidade

class Jogador(Personagem):

    _SPRITES = None

    def __init__(self,x,y):
        super().__init__(
            x,y,largura=26,
            altura=40,vida=6
        )

        #Estado Físico
        self.no_ar = False
        self.obstaculo = 0
        self.face=1
        self.pulos = 0

        #Combate
        self.invulnerabilidade = 0
        self.atk_cooldown = 0
        self.atk_timer = 0

        #Timers de habilidades
        self.dash_timer = 0
        self.dash_cooldown_timer = 0
        self.shot_cooldown = 0
        self.shield_active = False
        self.shield_cooldown = 0

        self.habilidades=set()
        self.chefes_derrotados = set()
        self.projectiles = pygame.sprite.Group()
        self.sprites = self._load_sprites()
        self.image = self.sprites["direita"]
