"""Os professores-chefe (bosses) de cada fase.

Cada Chefe tem padrões de ataque próprios, fases baseadas em vida restante,
e concede uma habilidade ao ser derrotado. Herda de `Personagem` (vida,
dano, desenho básico) mas NÃO usa a gravidade/colisão da base: o chefe
flutua dentro de uma arena fixa, então cuida do próprio movimento.
"""
import pygame
from abc import abstractmethod
import configuracoes
import recursos
from entidades.personagem import Personagem
from entidades.projetil import Projetil


class Chefe(Personagem):
    ESCALA_VISUAL = configuracoes.ESCALA_VISUAL_PERSONAGEM

    def __init__(self, x, y, nome, disciplina, cor, vida=20, arena=None, arquivo_figura=None):
        super().__init__(x, y, *configuracoes.TAMANHO_PERSONAGEM, vida=vida)
        self.nome = nome
        self.disciplina = disciplina
        self.cor = cor
        arquivo_figura = arquivo_figura or "chefes/prof_scratch.png"
        self.figura_direita = recursos.load_character_frames([arquivo_figura], cor)[0]
        self.figura_esquerda = pygame.transform.flip(self.figura_direita, True, False)
        self.image = self.figura_esquerda
        self.x_inicial = x
        self.arena = arena or pygame.Rect(x - 220, y - 200, 440, 260)

        self.etapa = 1
        self.derrotado = False
        self.ativo = False  # só luta depois do diálogo de introdução

        self.temporizador_ataque = 90
        self.estado_ataque = None
        self.relogio_ataque = 0
        self.direcao_olhar = -1
        self.brilho_dano = 0
        self.projeteis = pygame.sprite.Group()
        self._tempo = 0  # relógio interno só para animar o balanço (bob) do sprite

        self._draw_sprite()

    def activate(self):
        self.ativo = True

    def take_damage(self, quantidade, recuo=(0, 0)):
        if not self.ativo or not self.vivo:
            return
        super().take_damage(quantidade)
        self.brilho_dano = 8
        if self.vida <= self.vida_maxima * 0.5 and self.etapa == 1:
            self.etapa = 2
        if self.vida <= self.vida_maxima * 0.2 and self.etapa == 2:
            self.etapa = 3
        if not self.vivo:
            self.derrotado = True
            self.projeteis.empty()

    @abstractmethod
    def choose_attack(self, jogador):
        """As classes concretas definem a estratégia do encontro."""
        raise NotImplementedError("Cada boss deve implementar sua estratégia de ataques")

    def update(self, jogador, solidos):
        self._tempo += 1
        if not self.ativo or not self.vivo:
            self._draw_sprite()
            return

        if self.brilho_dano > 0:
            self.brilho_dano -= 1

        self.direcao_olhar = 1 if jogador.rect.centerx > self.rect.centerx else -1
        self.temporizador_ataque -= 1
        multiplicador_velocidade = 1 + (self.etapa - 1) * 0.35

        if self.temporizador_ataque <= 0 and self.estado_ataque is None:
            self.estado_ataque = self.choose_attack(jogador)
            self.relogio_ataque = 0

        if self.estado_ataque == "lunge":
            self.relogio_ataque += 1
            self.velocidade.x = self.direcao_olhar * 3.2 * multiplicador_velocidade
            if self.relogio_ataque > 26:
                self._end_attack(multiplicador_velocidade)
        elif self.estado_ataque == "spread":
            self.velocidade.x = 0
            self.relogio_ataque += 1
            if self.relogio_ataque == 15:
                for angulo in (-0.3, 0, 0.3):
                    dx = (1 if self.direcao_olhar > 0 else -1) + angulo
                    self.projeteis.add(Projetil(self.rect.centerx, self.rect.centery,
                                                      (dx, angulo), dono="boss", velocidade=6))
            if self.relogio_ataque > 40:
                self._end_attack(multiplicador_velocidade)
        elif self.estado_ataque == "slam":
            self.velocidade.x = 0
            self.relogio_ataque += 1
            if self.relogio_ataque == 20:
                for dx in (-1, 1):
                    self.projeteis.add(Projetil(self.rect.centerx, self.rect.bottom - 10,
                                                      (dx, -0.15), dono="boss", velocidade=5))
            if self.relogio_ataque > 45:
                self._end_attack(multiplicador_velocidade)
        else:
            # perseguição leve dentro da arena
            direcao = 1 if jogador.rect.centerx > self.rect.centerx else -1
            self.velocidade.x = direcao * 0.8 * multiplicador_velocidade

        self.posicao.x += self.velocidade.x
        self.rect.x = round(self.posicao.x)
        self.rect.clamp_ip(self.arena)
        self.posicao.x = self.rect.x

        self.projeteis.update(solidos)
        self._draw_sprite()

    def _end_attack(self, multiplicador_velocidade):
        self.estado_ataque = None
        self.temporizador_ataque = max(35, int(70 / multiplicador_velocidade))

    def get_all_hit_rects(self):
        retangulos = [(self.rect, self.dano_contato)]
        for p in self.projeteis:
            retangulos.append((p.rect, p.dano))
        return retangulos

    def _draw_sprite(self):
        # escolhe o sprite (imagem carregada de recursos/imagens/chefes/) conforme direção
        self.image = self.figura_direita if self.direcao_olhar > 0 else self.figura_esquerda

    def draw(self, superficie, camera):
        imagem = self.get_draw_image()
        destino = imagem.get_rect(midbottom=camera.apply(self.rect).midbottom)
        superficie.blit(imagem, destino)
        if self.brilho_dano > 0:
            # flash branco ao levar dano, sem alterar a imagem original em cache
            clarao = imagem.copy()
            clarao.fill((255, 255, 255, 140), special_flags=pygame.BLEND_RGBA_MULT)
            superficie.blit(clarao, destino, special_flags=pygame.BLEND_RGBA_ADD)
        # indicadores de fase de raiva (não fazem parte da arte base)
        if self.ativo and self.vivo:
            if self.etapa >= 2:
                pygame.draw.circle(superficie, (255, 60, 60), (destino.right - 8, destino.top + 8), 4)
            if self.etapa >= 3:
                pygame.draw.circle(superficie, (255, 60, 60), (destino.left + 8, destino.top + 8), 4)
        for p in self.projeteis:
            p.draw(superficie, camera)


# ----------------------------------------------------------------------
# Definições narrativas dos 6 professores-chefe
# ----------------------------------------------------------------------
DEFINICOES_CHEFES = [
    dict(name="RomerBug", subject="Lógica de Blocos", color=(50, 65, 105), health=16,
         sprite_file="chefes/romerbug_0.png", boss_type="romerbug"),
    dict(name="Prof. Python", subject="Laboratório de Lógica", color=(60, 140, 220), health=20,
         sprite_file="chefes/prof_python.png", boss_type="python"),
    dict(name="Prof. Java", subject="Sala de POO", color=(200, 60, 60), health=24,
         sprite_file="chefes/prof_java.png", boss_type="java"),
    dict(name="Prof. C", subject="Sala de Memória", color=(120, 120, 130), health=28,
         sprite_file="chefes/prof_c.png", boss_type="c"),
    dict(name="Prof. SQL", subject="Biblioteca de Dados", color=(60, 180, 140), health=32,
         sprite_file="chefes/prof_sql.png", boss_type="sql"),
    dict(name="Prof. Assembly", subject="Núcleo do Sistema", color=(30, 30, 40), health=40,
         sprite_file="chefes/prof_assembly.png", boss_type="assembly"),
]
