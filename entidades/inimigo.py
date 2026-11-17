"""Inimigos comuns: os 'bugs' que infestam a escola.

Herda de `Personagem` e reaproveita a gravidade/colisão prontas da base -
só precisa decidir *para onde* andar (patrulha simples entre dois pontos)
e o que acontece quando morre.
"""
import pygame
from sistema import configuracoes
from sistema import recursos
from entidades.personagem import Personagem


class Inimigo(Personagem):
    ESCALA_VISUAL = 1.0
    _FIGURAS = None
    _VELOCIDADE_ANIMACAO = 10  # quadros de jogo entre cada troca de perna/antena

    @classmethod
    def _load_sprites(cls):
        if cls._FIGURAS is None:
            quadros = recursos.load_character_frames(
                [f"inimigos/bug_{i}.png" for i in range(2)], configuracoes.COR_INIMIGO)
            cls._FIGURAS = {
                1: quadros,
                -1: [pygame.transform.flip(quadro, True, False) for quadro in quadros],
            }
        return cls._FIGURAS

    def __init__(self, x, y, area_patrulha=80, velocidade=1.4, vida=2, cor=None):
        super().__init__(x, y, *configuracoes.TAMANHO_PERSONAGEM, vida=vida)
        self.figuras = self._load_sprites()
        self.image = self.figuras[1][0]
        self.velocidade.x = velocidade
        self.x_inicial = x
        self.area_patrulha = area_patrulha
        self.rapidez = velocidade
        self.cor = cor or configuracoes.COR_INIMIGO
        self._tempo = 0
        self.brilho_dano = 0
        self.tempo_barra_vida = 0
        self.temporizador_recuo = 0
        self.direcao_patrulha = 1 if velocidade >= 0 else -1
        self.quadro_animacao = 0

    def update(self, solidos):
        self.brilho_dano = max(0, self.brilho_dano-1)
        self.tempo_barra_vida = max(0, self.tempo_barra_vida-1)
        if self.temporizador_recuo > 0:
            self.temporizador_recuo -= 1
            self.move_and_collide_x(solidos)
            self.velocidade.x *= 0.72
            self.apply_gravity()
            self.move_and_collide_y(solidos)
            if self.temporizador_recuo == 0:
                self.velocidade.x = self.direcao_patrulha*self.rapidez
            return
        self._tempo += 1
        if self._tempo % self._VELOCIDADE_ANIMACAO == 0:
            self.quadro_animacao = 1 - self.quadro_animacao

        apoio = pygame.Rect(self.rect.left+3, self.rect.bottom, self.rect.width-6, 3)
        frente = pygame.Rect(self.rect.right+1 if self.velocidade.x > 0 else self.rect.left-5, self.rect.bottom, 4, 5)
        if any(apoio.colliderect(solido) for solido in solidos) and not any(frente.colliderect(solido) for solido in solidos):
            self.velocidade.x *= -1
            self.direcao_patrulha = 1 if self.velocidade.x > 0 else -1

        parede_tocada = self.move_and_collide_x(solidos)
        fora_area_patrulha = (self.rect.x < self.x_inicial - self.area_patrulha
                                or self.rect.x > self.x_inicial + self.area_patrulha)
        if parede_tocada != 0 or fora_area_patrulha:
            self.velocidade.x *= -1
            self.direcao_patrulha = 1 if self.velocidade.x >= 0 else -1

        self.apply_gravity()
        self.move_and_collide_y(solidos)

    def take_damage(self, quantidade, recuo=(0, 0)):
        if not self.vivo or quantidade <= 0:
            return
        super().take_damage(quantidade)
        self.brilho_dano = 9
        self.tempo_barra_vida = 100
        self.temporizador_recuo = 10
        self.velocidade.update(recuo)
        if not self.vivo:
            self.kill()

    def _redraw(self):
        direcao_olhar = 1 if self.velocidade.x >= 0 else -1
        self.image = self.figuras[direcao_olhar][self.quadro_animacao]

    def reagir_bloqueio(self, area):
        if area is self.rect:
            self.temporizador_recuo = 8
            self.velocidade.x *= -1

    def draw(self, superficie, camera):
        self._redraw()
        imagem = self.get_draw_image()
        destino = imagem.get_rect(midbottom=camera.apply(self.rect).midbottom)
        superficie.blit(imagem, destino)
        if self.brilho_dano:
            clarao = pygame.mask.from_surface(imagem).to_surface(setcolor=(245, 255, 228, 190), unsetcolor=(0, 0, 0, 0))
            clarao.set_alpha(round(220*self.brilho_dano/9))
            superficie.blit(clarao, destino)
        if self.tempo_barra_vida and self.vivo:
            barra = pygame.Rect(0, 0, 36, 5)
            barra.midbottom = (destino.centerx, destino.top-4)
            pygame.draw.rect(superficie, (15, 22, 31), barra.inflate(4, 4), border_radius=3)
            pygame.draw.rect(superficie, (74, 43, 48), barra)
            preenchimento = barra.copy()
            preenchimento.width = round(barra.width*self.vida/self.vida_maxima)
            pygame.draw.rect(superficie, (118, 230, 171), preenchimento)
