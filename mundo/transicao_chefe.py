"""Cena dos 50%: joelho no chão, entidade, fala, metamorfose e retomada."""
import math
import pygame
import recursos
import configuracoes
from interface import tema


class TransicaoChefe:
    DURACOES = {'kneel': 42, 'arrival': 48, 'morph': 72, 'rise': 42, 'release': 24}
    ORDEM = ('kneel', 'arrival', 'speech', 'morph', 'rise', 'release', 'complete')

    def __init__(self, fase, jogador):
        self.fase = fase
        self.chefe = fase.chefe
        self.jogador = jogador
        self.etapa = 'kneel'
        self.instante = 0
        self.quadros = recursos.load_character_frames([f'chefes/transicao/pose_{i}.png' for i in range(6)])
        self.entidade = recursos.load_character_frames(['chefes/transicao/entidade.png'])[0]
        self.direcao_olhar = self.chefe.direcao_olhar
        self.retangulo_inicial = self.chefe.rect.copy()
        self.velocidade_jogador = jogador.velocidade.copy()
        self.fonte = pygame.font.Font(None, 19)
        self.camada = pygame.Surface((configuracoes.LARGURA_TELA, configuracoes.ALTURA_TELA))
        jogador.cancelar_combate()
        jogador.velocidade.update(0, 0)
        jogador.temporizador_golpe = 0
        jogador.espera_ataque = 0
        jogador.chicote.alvos_atingidos.clear()
        jogador.projeteis.empty()
        self.chefe.projeteis.empty()
        self.chefe.brilho_dano = 0
        self._pose(0)

    def _pose(self, indice):
        quadro = self.quadros[indice]
        self.chefe.image = pygame.transform.flip(quadro, self.direcao_olhar < 0, False)

    def resume(self):
        if self.etapa == 'speech':
            self.etapa, self.instante = 'morph', 0

    def update(self):
        if self.etapa in ('speech', 'complete'):
            return None
        self.instante += 1
        fracao = min(1, self.instante/self.DURACOES[self.etapa])
        if self.etapa == 'kneel':
            self._pose(0 if fracao < 0.35 else 1)
        elif self.etapa in ('arrival',):
            self._pose(2 if fracao > 0.5 else 1)
        elif self.etapa == 'morph':
            anterior = self.quadros[2].copy()
            novo = self.quadros[3].copy()
            novo.set_alpha(round(255*fracao))
            anterior.set_alpha(round(255*(1-fracao)))
            combinado = pygame.Surface(configuracoes.TAMANHO_PERSONAGEM, pygame.SRCALPHA)
            combinado.blit(anterior, (0, 0))
            combinado.blit(novo, (0, 0))
            self.chefe.image = pygame.transform.flip(combinado, self.direcao_olhar < 0, False)
            if fracao >= 0.5:
                self.chefe.nome = 'SpeedBug'
        elif self.etapa == 'rise':
            self._pose(3 if fracao < 0.25 else 4 if fracao < 0.7 else 5)
        else:
            self._pose(5)
        if self.instante >= self.DURACOES[self.etapa]:
            self.etapa = self.ORDEM[self.ORDEM.index(self.etapa)+1]
            self.instante = 0
            if self.etapa == 'speech':
                return 'speech'
            if self.etapa == 'complete':
                self.chefe.finish_cinematic()
                self.jogador.velocidade.update(self.velocidade_jogador)
                self.jogador.temporizador_invulnerabilidade = max(60, self.jogador.temporizador_invulnerabilidade)
                return 'complete'
        return None

    def draw(self, superficie):
        # Zoom somente visual: posições, câmera e caixas de colisão não mudam.
        self.fase.draw(self.camada)
        self.jogador.draw(self.camada, self.fase.camera)
        corpo = self.fase.camera.apply(self.chefe.rect)
        entidade_visivel = self.etapa != 'kneel'
        if entidade_visivel:
            tamanho = tuple(round(lado*configuracoes.ESCALA_VISUAL_PERSONAGEM) for lado in self.entidade.get_size())
            imagem = pygame.transform.flip(pygame.transform.scale(self.entidade, tamanho), self.direcao_olhar < 0, False)
            transparencia = 255
            if self.etapa == 'arrival':
                transparencia = round(255*self.instante/self.DURACOES['arrival'])
            elif self.etapa == 'release':
                transparencia = round(255*(1-self.instante/self.DURACOES['release']))
            imagem.set_alpha(transparencia)
            x = corpo.centerx + (62 if self.direcao_olhar > 0 else -62)
            y = corpo.bottom-92-round(2*math.sin(self.instante*0.09))
            self.camada.blit(imagem, imagem.get_rect(midbottom=(x, y+40)))
            if self.etapa == 'morph':
                brilho = pygame.Surface(self.camada.get_size(), pygame.SRCALPHA)
                pygame.draw.line(brilho, (*tema.CIANO, 100), (x, y+28), corpo.center, 2)
                pygame.draw.ellipse(brilho, (*tema.CIANO, 110), corpo.inflate(22, 12), 2)
                self.camada.blit(brilho, (0, 0))
        quantidade = 1.0
        if self.etapa == 'kneel':
            quantidade = self.instante/self.DURACOES['kneel']
        elif self.etapa == 'release':
            quantidade = 1-self.instante/self.DURACOES['release']
        quantidade = quantidade*quantidade*(3-2*quantidade)
        largura = round(configuracoes.LARGURA_TELA*(1-0.5*quantidade))
        altura = round(configuracoes.ALTURA_TELA*(1-0.5*quantidade))
        recorte = pygame.Rect(0, 0, largura, altura)
        recorte.center = (round(configuracoes.LARGURA_TELA/2+(corpo.centerx-configuracoes.LARGURA_TELA/2)*quantidade),
                       round(configuracoes.ALTURA_TELA/2+(corpo.centery-24-configuracoes.ALTURA_TELA/2)*quantidade))
        recorte.clamp_ip(self.camada.get_rect())
        superficie.blit(pygame.transform.scale(self.camada.subsurface(recorte), superficie.get_size()), (0, 0))
        # Barras de cinema e legenda de estado fora da área das personagens.
        altura_barra = round(46*quantidade)
        pygame.draw.rect(superficie, tema.TINTA, (0, 0, configuracoes.LARGURA_TELA, altura_barra))
        pygame.draw.rect(superficie, tema.TINTA, (0, configuracoes.ALTURA_TELA-round(30*quantidade), configuracoes.LARGURA_TELA, round(30*quantidade)))
        titulo = 'ROMERBUG / LIMIAR DE RUPTURA' if self.etapa in ('kneel', 'arrival', 'speech') else 'SPEEDBUG / RECONSTITUIÇÃO'
        if altura_barra >= 28:
            tema.text(superficie, self.fonte, titulo, (28, 16), tema.AMBAR)
            tema.text(superficie, self.fonte, 'ESC  pausar', (configuracoes.LARGURA_TELA-112, 16), tema.ATENUADO)
