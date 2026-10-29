"""Classe base abstrata para toda personagem viva do jogo.

`Personagem` reúne o que o aluno, os inimigos comuns e os professores-chefe
têm em comum: posição, vida, dano de contato e a física de queda/colisão
com o cenário. Ela é uma **classe abstrata** (herda de `ABC`) porque não
faz sentido existir uma "personagem genérica" solta no jogo - só as
subclasses concretas (`Jogador`, `Inimigo`, `Chefe`) podem ser instanciadas.

O método `update` é marcado com `@abstractmethod`: só declarar essa classe
já impede `Personagem(...)` de ser criada diretamente, e obriga cada
subclasse a implementar seu próprio comportamento de atualização (cada
tipo de personagem se move de um jeito bem diferente).
"""
from abc import ABC, abstractmethod

import pygame
import configuracoes


class Personagem(pygame.sprite.Sprite, ABC):
    """Base comum a Jogador, Inimigo e Chefe (posição, vida, física, desenho)."""

    ESCALA_VISUAL = 1.0

    def __init__(self, x, y, largura, altura, vida):
        super().__init__()
        self.largura, self.altura = largura, altura
        self.posicao = pygame.Vector2(x, y)
        self.velocidade = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(x, y, largura, altura)

        self.vida_maxima = vida
        self.vida = vida
        self.vivo = True
        self.dano_contato = 1

        # cada subclasse define self.image ao carregar seus próprios sprites
        self.image = None

    # ------------------------------------------------------------------
    # Contrato: toda personagem concreta PRECISA saber se atualizar sozinha
    # ------------------------------------------------------------------
    @abstractmethod
    def update(self, *args, **kwargs):
        """Lógica de um quadro (frame). Assinatura varia por subclasse:
        Jogador usa (solids, hazards), Inimigo usa (solids), Chefe usa
        (player, solids) - por isso fica abstrato aqui na base."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Dano: implementação padrão, sobrescrita quando a personagem precisa
    # de uma regra especial (Jogador tem escudo/invencibilidade, Chefe tem
    # fases de raiva). Quem sobrescrever normalmente chama
    # `super().take_damage(amount)` para reaproveitar a regra base.
    # ------------------------------------------------------------------
    def take_damage(self, quantidade, recuo=(0, 0)):
        if not self.vivo:
            return
        self.vida -= quantidade
        if self.vida <= 0:
            self.vida = 0
            self.vivo = False

    # ------------------------------------------------------------------
    # Física reaproveitável por quem obedece gravidade e colide com o
    # cenário (Jogador e Inimigo). O Chefe flutua dentro de uma arena e não
    # usa esses métodos.
    # ------------------------------------------------------------------
    def apply_gravity(self):
        """Acelera a queda até a velocidade terminal definida em configuracoes."""
        self.velocidade.y = min(self.velocidade.y + configuracoes.GRAVIDADE, configuracoes.VELOCIDADE_MAXIMA_QUEDA)

    def move_and_collide_x(self, solidos):
        """Move no eixo X e resolve colisão com o cenário.

        Devolve -1/0/1 indicando se encostou numa parede à esquerda,
        nenhuma, ou à direita."""
        parede_tocada = 0
        self.posicao.x += self.velocidade.x
        self.rect.x = round(self.posicao.x)
        for bloco in solidos:
            if self.rect.colliderect(bloco):
                if self.velocidade.x > 0:
                    self.rect.right = bloco.left
                    parede_tocada = 1
                elif self.velocidade.x < 0:
                    self.rect.left = bloco.right
                    parede_tocada = -1
                self.posicao.x = self.rect.x
        return parede_tocada

    def move_and_collide_y(self, solidos):
        """Move no eixo Y e resolve colisão com o cenário.

        Devolve True se encostou no chão."""
        no_chao = False
        self.posicao.y += self.velocidade.y
        self.rect.y = round(self.posicao.y)
        for bloco in solidos:
            if self.rect.colliderect(bloco):
                if self.velocidade.y > 0:
                    self.rect.bottom = bloco.top
                    no_chao = True
                elif self.velocidade.y < 0:
                    self.rect.top = bloco.bottom
                self.velocidade.y = 0
                self.posicao.y = self.rect.y
        return no_chao

    # ------------------------------------------------------------------
    # Desenho padrão: só posiciona o sprite atual na tela pela câmera.
    # Subclasses com efeitos extras (piscar, flash de dano, barra de fase)
    # chamam `super().draw(surface, camera)` e completam por cima.
    # ------------------------------------------------------------------
    def get_draw_image(self):
        """Escala apenas a arte; o apoio dos pés e o corpo físico são preservados."""
        tamanho = tuple(round(lado * self.ESCALA_VISUAL) for lado in self.image.get_size())
        if tamanho == self.image.get_size():
            return self.image
        return pygame.transform.scale(self.image, tamanho)

    def draw(self, superficie, camera):
        imagem = self.get_draw_image()
        destino = camera.apply(self.rect)
        superficie.blit(imagem, imagem.get_rect(midbottom=destino.midbottom))
