"""Quatro encontros concretos; ações escolhidas por estratégias de cada guardião."""
import math
import pygame
from entidades.chefe import Chefe
from entidades.projetil import Projetil
from sistema.maquina_estados import MaquinaEstados
from sistema import recursos


class GuardiaoCampus(Chefe):
    """Infraestrutura de janelas/colisão; subclasses definem seu repertório."""
    def __init__(self, *argumentos, **opcoes):
        super().__init__(*argumentos, **opcoes)
        self.estados = MaquinaEstados('esperar', {'esperar': {'preparar'}, 'preparar': {'atacar'},
            'atacar': {'recuperar'}, 'recuperar': {'preparar'}})
        self.tempo_estado = 45
        self.acao = None
        self.ciclo = 0
        self.direcao_ataque = -1
        self.vinculo_rompido = False
        self.origem_ataque = pygame.Vector2(self.rect.center)
        self.reforcos = pygame.sprite.Group()
        self.quantidade_aliados = 0
        self.disparos_pendentes = []
        quadros = recursos.load_character_frames([f'chefes/poses_{self.identificador_visual}/pose_{indice}.png' for indice in range(4)])
        self.figuras_guardiao = {1: quadros, -1: [recursos.espelhar_quadro(quadro) for quadro in quadros]}
        self._draw_sprite()

    def _draw_sprite(self):
        if not hasattr(self, 'figuras_guardiao') or (self.identificador_visual == 'francisco' and self.vinculo_rompido):
            return super()._draw_sprite()
        indice = {'esperar': 0, 'preparar': 1, 'atacar': 2, 'recuperar': 3}[self.estados.estado]
        self.image = self.figuras_guardiao[self.direcao_olhar][indice]

    def choose_attack(self, jogador):
        raise NotImplementedError

    def preparar(self, jogador):
        self.acao = self.choose_attack(jogador)
        self.ciclo += 1
        self.direcao_ataque = 1 if jogador.rect.centerx >= self.rect.centerx else -1
        self.direcao_olhar = self.direcao_ataque
        self.estados.mudar('preparar')
        self.tempo_estado = 32 if self.etapa == 1 else 26
        self._draw_sprite()

    def iniciar_acao(self, jogador):
        self.estados.mudar('atacar')
        self.tempo_estado = 24
        self.origem_ataque.update(self.rect.center)
        if self.acao == 'bola':
            from entidades.projeteis_campus import BolaVirtual
            self.projeteis.add(BolaVirtual(*self.rect.center, self.direcao_ataque))
        elif self.acao == 'pulso':
            for direcao in (-1, 1):
                self.projeteis.add(Projetil(self.rect.centerx, self.rect.bottom-8, (direcao, 0), dono='boss', velocidade=5))
        elif self.acao == 'portas':
            alturas = [self.rect.centery, self.rect.centery-62]
            if self.etapa >= 2:
                alturas.reverse()
            self.tempo_estado = 42
            self.disparos_pendentes = [(32, alturas[0]), (14, alturas[1])]
        elif self.acao == 'invocar':
            from entidades.fabrica_entidades import criar_inimigo
            for desvio in (-75, 75):
                x = max(self.arena.left, min(self.arena.right-40, self.rect.x+desvio))
                self.reforcos.add(criar_inimigo('combate', x, self.rect.y))

    def update(self, jogador, solidos):
        if not self.ativo or not self.vivo:
            return
        self._tempo += 1
        self.brilho_dano = max(0, self.brilho_dano-1)
        self.projeteis.update(solidos)
        if self.estados.estado == 'atacar' and self.acao == 'portas':
            for instante, altura in list(self.disparos_pendentes):
                if self.tempo_estado == instante:
                    self.projeteis.add(Projetil(self.rect.centerx, altura, (self.direcao_ataque, 0), dono='boss', velocidade=4.5))
                    self.disparos_pendentes.remove((instante, altura))
        if self.etapa >= 2 and not self.vinculo_rompido:
            self.vinculo_rompido = True
        if self.estados.estado == 'atacar' and self.acao == 'investida':
            self.velocidade.x = self.direcao_ataque*5.5
            self.move_and_collide_x(solidos)
            self.rect.clamp_ip(self.arena)
            self.posicao.x = self.rect.x
        self.tempo_estado -= 1
        if self.tempo_estado <= 0:
            if self.estados.estado in ('esperar', 'recuperar'):
                self.preparar(jogador)
            elif self.estados.estado == 'preparar':
                self.iniciar_acao(jogador)
            else:
                self.estados.mudar('recuperar')
                recuperacao = {'investida': 66, 'sequencia': 40, 'invocar': 54}.get(self.acao, 48)
                self.tempo_estado = recuperacao if self.etapa == 1 else max(36, recuperacao-8)
        self._draw_sprite()

    def take_damage(self, quantidade, recuo=(0, 0)):
        if self.ativo and self.vivo and self.estados.estado == 'preparar' and self.acao == 'barreira' and quantidade < 2:
            return
        super().take_damage(quantidade, recuo)

    def reagir_bloqueio(self, area):
        if area is self.rect and self.estados.estado == 'atacar' and self.acao == 'investida':
            self.estados.mudar('recuperar')
            self.tempo_estado = 54
            self.velocidade.x = 0

    def get_all_hit_rects(self):
        if not self.ativo or not self.vivo:
            return []
        areas = [(projetil.rect, projetil.dano) for projetil in self.projeteis]
        if self.estados.estado == 'atacar':
            if self.acao == 'investida':
                areas.append((self.rect, 1))
            elif self.acao in ('sequencia', 'varredura', 'arco'):
                area = self.rect.inflate(100 if self.acao == 'sequencia' else 170, 0)
                area.centerx += self.direcao_ataque*45
                # Dois tempos distintos da sequência, sem dano no intervalo.
                if self.acao != 'sequencia' or self.tempo_estado > 16 or self.tempo_estado < 8:
                    areas.append((area, 1))
        return areas

    def draw(self, superficie, camera):
        imagem = self.get_draw_image()
        if self.derrotado:
            imagem = recursos.imagem_apresentacao(self.figuras_guardiao[self.direcao_olhar][0], (80, 80))
            superficie.blit(imagem, imagem.get_rect(midbottom=camera.apply(self.rect).midbottom))
            return
        estado = self.estados.estado
        inclinacao = self.direcao_olhar*(8 if estado == 'preparar' else -9 if estado == 'atacar' else 0)
        imagem = pygame.transform.rotozoom(imagem, inclinacao+math.sin(self._tempo*0.1), 1)
        destino = imagem.get_rect(midbottom=camera.apply(self.rect).midbottom)
        superficie.blit(imagem, destino)
        if self.brilho_dano:
            clarao = pygame.mask.from_surface(imagem).to_surface(setcolor=(255, 252, 220, 170), unsetcolor=(0, 0, 0, 0))
            superficie.blit(clarao, destino)
        for projetil in self.projeteis:
            projetil.draw(superficie, camera)


class EliasGuardiaoCompasso(GuardiaoCampus):
    identificador_visual = 'elias'
    def choose_attack(self, jogador):
        if abs(jogador.rect.centerx-self.rect.centerx) < 130:
            return 'sequencia' if self.ciclo % 2 == 0 else 'investida'
        return ('bola', 'investida', 'pulso')[self.ciclo % 3]


class MaxEmLoop(GuardiaoCampus):
    identificador_visual = 'max'
    def __init__(self, *argumentos, **opcoes):
        super().__init__(*argumentos, **opcoes)
        self.centros_copias = tuple(max(self.arena.left, min(self.arena.right-self.largura, self.rect.x+desvio)) for desvio in (-135, 0, 135))

    def choose_attack(self, jogador):
        acao = ('varredura', 'invocar', 'portas', 'barreira')[self.ciclo % 4]
        return 'varredura' if acao == 'invocar' and self.quantidade_aliados >= 2 else acao

    def preparar(self, jogador):
        self.rect.x = round(self.centros_copias[(self.ciclo+self.etapa) % 3])
        self.posicao.x = self.rect.x
        super().preparar(jogador)
        self.tempo_estado += 10

    def draw(self, superficie, camera):
        if self.ativo and self.vivo:
            origem = camera.apply(self.rect).center
            for x in self.centros_copias:
                if abs(x-self.rect.x) < 2:
                    continue
                copia = self.get_draw_image().copy()
                copia.set_alpha(65)
                destino = copia.get_rect(midbottom=(x+20-camera.deslocamento.x, origem[1]+20))
                superficie.blit(copia, destino)
            pygame.draw.line(superficie, (107, 234, 216), (origem[0], origem[1]-85), origem, 2)
        super().draw(superficie, camera)


class AlessandroSentinelaEnlaces(GuardiaoCampus):
    identificador_visual = 'alessandro'
    def choose_attack(self, jogador):
        return ('barreira', 'portas', 'varredura', 'investida')[self.ciclo % 4]

    def take_damage(self, quantidade, recuo=(0, 0)):
        frontal = recuo[0]*self.direcao_olhar < 0
        if self.ativo and self.vivo and self.estados.estado == 'preparar' and self.acao == 'barreira' and not frontal:
            # O flanco rompe a proteção sem obrigar carregado.
            Chefe.take_damage(self, quantidade, recuo)
            return
        super().take_damage(quantidade, recuo)


class FranciscoGuardiaoContinuidade(GuardiaoCampus):
    identificador_visual = 'francisco'
    def __init__(self, *argumentos, **opcoes):
        super().__init__(*argumentos, **opcoes)
        self.transicao_nucleo = 0
        self.figura_professor = self.figura_direita

    def take_damage(self, quantidade, recuo=(0, 0)):
        if self.transicao_nucleo:
            return
        antes = self.vida
        super().take_damage(quantidade, recuo)
        if self.vivo and antes > self.vida_maxima/2 >= self.vida:
            from sistema import recursos
            self.transicao_nucleo = 45
            self.vinculo_rompido = True
            self.nome = 'IFVania · autopreservação'
            self.figura_direita = recursos.load_character_frames(['chefes/transicao/entidade.png'])[0]
            self.figura_esquerda = recursos.espelhar_quadro(self.figura_direita)
            self.projeteis.empty()

    def get_all_hit_rects(self):
        return [] if self.transicao_nucleo else super().get_all_hit_rects()

    def choose_attack(self, jogador):
        acoes = ('arco', 'pulso', 'invocar', 'portas', 'investida') if self.etapa >= 2 else ('arco', 'pulso', 'investida')
        acao = acoes[self.ciclo % len(acoes)]
        return 'pulso' if acao == 'invocar' and self.quantidade_aliados >= 2 else acao

    def update(self, jogador, solidos):
        if not self.ativo or not self.vivo:
            return
        if self.transicao_nucleo:
            self.transicao_nucleo -= 1
            jogador.temporizador_invulnerabilidade = max(60, jogador.temporizador_invulnerabilidade)
            self._draw_sprite()
            return
        super().update(jogador, solidos)

    def draw(self, superficie, camera):
        if self.vinculo_rompido:
            imagem = pygame.transform.smoothscale(self.figura_professor, (80, 80))
            destino = camera.apply(pygame.Rect(self.arena.left+60, self.rect.y, 40, 40))
            superficie.blit(imagem, imagem.get_rect(midbottom=destino.midbottom))
            if self.derrotado:
                return
        super().draw(superficie, camera)
