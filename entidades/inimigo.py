"""Inimigos comuns: os 'bugs' que infestam a escola.

Herda de `Personagem` e reaproveita a gravidade/colisão prontas da base -
só precisa decidir *para onde* andar (patrulha simples entre dois pontos)
e o que acontece quando morre.
"""
import pygame
import configuracoes
import recursos
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
        self.quadro_animacao = 0

    def update(self, solidos):
        self._tempo += 1
        if self._tempo % self._VELOCIDADE_ANIMACAO == 0:
            self.quadro_animacao = 1 - self.quadro_animacao

        parede_tocada = self.move_and_collide_x(solidos)
        fora_area_patrulha = (self.rect.x < self.x_inicial - self.area_patrulha
                                or self.rect.x > self.x_inicial + self.area_patrulha)
        if parede_tocada != 0 or fora_area_patrulha:
            self.velocidade.x *= -1

        self.apply_gravity()
        self.move_and_collide_y(solidos)

    def take_damage(self, quantidade, recuo=(0, 0)):
        super().take_damage(quantidade)
        if not self.vivo:
            self.kill()

    def _redraw(self):
        direcao_olhar = 1 if self.velocidade.x >= 0 else -1
        self.image = self.figuras[direcao_olhar][self.quadro_animacao]

    def draw(self, superficie, camera):
        self._redraw()
        super().draw(superficie, camera)
