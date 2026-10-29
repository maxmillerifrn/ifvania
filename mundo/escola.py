"""Sequência escolar com geometria editável e interações únicas.

A sala, o corredor e o A28 compartilham a interface usada por Jogo (tilemap,
câmera, spawn, update e draw), sem criar inimigos ou um boss antecipadamente.
"""
from types import SimpleNamespace
import pygame
import configuracoes
from entidades.professor import Professor
from mundo.camera import Camera
from mundo.arte_escolar import ArteEscolar
from interface import tema


class FaseEscolar:
    Y_PISO = 352
    NOMES = {'classroom': 'Aula de programação orientada a serviço',
             'corridor': 'Corredores da escola — procure o laboratório A28',
             'lab': 'Laboratório A28 — encontre o professor Romerito'}

    def __init__(self, ambiente):
        self.ambiente = ambiente
        self.nome = self.NOMES[ambiente]
        largura = 1920 if ambiente == 'corridor' else configuracoes.LARGURA_TELA
        self.mapa_blocos = SimpleNamespace(
            largura=largura, altura=configuracoes.ALTURA_TELA, perigos=[],
            solidos=[pygame.Rect(0, self.Y_PISO, largura, configuracoes.ALTURA_TELA-self.Y_PISO),
                    pygame.Rect(-32, 0, 32, configuracoes.ALTURA_TELA),
                    pygame.Rect(largura, 0, 32, configuracoes.ALTURA_TELA),
                    pygame.Rect(0, -32, largura, 32)])
        self.camera = Camera(largura, self.mapa_blocos.altura)
        self.surgimento_jogador = (120, self.Y_PISO-configuracoes.TAMANHO_PERSONAGEM[1])
        self.chefe = None
        self.professores = pygame.sprite.Group()
        if ambiente != 'corridor':
            self.professores.add(Professor(700, self.surgimento_jogador[1],
                                  'max' if ambiente == 'classroom' else 'romerito'))
        self.porta_a28 = pygame.Rect(1664, 218, 80, self.Y_PISO-218)
        self.interacao_disparada = False
        self.corrompido = ambiente != 'classroom'
        self.instantes = 0
        self.instantes_visuais = 0
        self.arte = ArteEscolar(ambiente, largura)
        self.fonte = pygame.font.Font(None, 22)
        self.fonte_pequena = pygame.font.Font(None, 18)
        self.instrucao = None

    def interaction_zone(self):
        if self.ambiente == 'corridor':
            return self.porta_a28.inflate(112, 0)
        if self.ambiente == 'lab':
            return next(iter(self.professores)).rect.inflate(160, 100)
        return None

    def update(self, jogador, eventos):
        self.instantes += 1
        self.professores.update()
        self.camera.update(jogador.rect)
        self.instrucao = None
        zona = self.interaction_zone()
        if self.interacao_disparada or zona is None:
            return None, None
        if jogador.rect.colliderect(zona):
            self.instrucao = 'E — entrar no A28' if self.ambiente == 'corridor' else 'E — falar com Romerito'
            if any(evento.type == pygame.KEYDOWN and evento.key == pygame.K_e for evento in eventos):
                self.interacao_disparada = True
                self.instrucao = None
                return ('enter_lab' if self.ambiente == 'corridor' else 'school_encounter'), None
        return None, None

    def begin_abduction(self, jogador):
        self.instrucao = None
        self.inicio_ataque = next(iter(self.professores)).rect.x
        self.inicio_jogador = jogador.rect.x

    def update_abduction(self, jogador, temporizador):
        # Investida breve de Romerito e recuo do aluno antes da captura.
        # É uma ação narrativa, sem retirar vida ou habilitar combate escolar.
        fracao = min(1, temporizador/18)
        professor = next(iter(self.professores))
        alvo = self.inicio_jogador + jogador.largura - 8
        professor.rect.x = round(self.inicio_ataque + (alvo-self.inicio_ataque)*fracao)
        professor.posicao.x = professor.rect.x
        jogador.posicao.x = self.inicio_jogador - 12*fracao
        jogador.rect.x = round(jogador.posicao.x)

    def _rect(self, superficie, cor, retangulo, largura=0):
        pygame.draw.rect(superficie, cor, self.camera.apply(pygame.Rect(retangulo)), largura)

    def _text(self, superficie, texto, x, y, cor=(235, 242, 222), pequeno=False):
        imagem = (self.fonte_pequena if pequeno else self.fonte).render(texto, True, cor)
        retangulo = self.camera.apply(imagem.get_rect(topleft=(x, y)))
        superficie.blit(imagem, retangulo)

    def update_visuals(self):
        self.instantes_visuais += 1

    def _door(self, superficie, x, rotulo, ativo=False):
        # Porta metálica: caixilho, visor, dobradiças, puxador e chapa inferior.
        self._rect(superficie, (21, 29, 34), (x-7, 210, 94, 142))
        self._rect(superficie, (89, 100, 101), (x-4, 213, 88, 139), 2)
        self._rect(superficie, (43, 57, 63), (x, 218, 80, 134))
        self._rect(superficie, (71, 85, 89), (x+3, 221, 74, 128), 1)
        self._rect(superficie, (14, 28, 35), (x+12, 230, 56, 42))
        self._rect(superficie, (96, 123, 128), (x+12, 230, 56, 42), 2)
        self._rect(superficie, (26, 47, 56), (x+16, 234, 48, 34))
        self._rect(superficie, (65, 91, 99), (x+20, 237, 2, 27))
        self._rect(superficie, (101, 113, 110), (x+61, 290, 10, 21))
        self._rect(superficie, (164, 173, 163), (x+58, 295, 11, 3))
        self._rect(superficie, (56, 69, 73), (x+8, 328, 64, 19))
        for hy in (239, 289, 327):
            self._rect(superficie, (100, 107, 103), (x+2, hy, 4, 9))
        for sy in (334, 339, 344):
            self._rect(superficie, (83, 93, 91), (x+15, sy, 46, 1))
        self._rect(superficie, (13, 27, 33), (x-5, 180, 90, 25))
        self._rect(superficie, (95, 117, 118), (x-5, 180, 90, 25), 1)
        self._text(superficie, rotulo, x+20, 185)
        if ativo:
            self._rect(superficie, (110, 182, 179), (x+91, 288, 7, 4))

    def draw(self, superficie):
        self.arte.draw(superficie, self.camera, self.instantes_visuais, self.corrompido)
        if self.ambiente == 'corridor':
            for x, rotulo in ((160, 'A25'), (640, 'A26'), (1120, 'A27')):
                self._door(superficie, x, rotulo)
            self._door(superficie, self.porta_a28.x, 'A28', True)
            self._rect(superficie, (17, 34, 40), (1280, 95, 250, 30))
            self._text(superficie, 'LABORATÓRIO A28  >', 1295, 102)
        else:
            titulo = 'IFVania — inteligência artificial' if self.ambiente == 'classroom' else 'LABORATÓRIO A28'
            self._text(superficie, titulo, 454, 170)
            self._text(superficie, 'Programação orientada a serviço' if self.ambiente == 'classroom'
                       else 'Sistema sob controle da IFVania.', 454, 200, pequeno=True)
        for professor in self.professores:
            professor.draw(superficie, self.camera)
            imagem = professor.get_draw_image()
            visual = imagem.get_rect(midbottom=professor.rect.midbottom)
            rotulo = self.fonte_pequena.render(professor.nome, True, tema.PAPEL)
            retangulo = rotulo.get_rect(midbottom=(professor.rect.centerx, visual.top-8))
            pygame.draw.rect(superficie, tema.PAINEL, self.camera.apply(retangulo.inflate(12, 6)))
            superficie.blit(rotulo, self.camera.apply(retangulo))
        if self.instrucao:
            painel = pygame.Surface((340, 32), pygame.SRCALPHA)
            painel.fill((15, 31, 38, 230))
            superficie.blit(painel, (310, 365))
            texto = self.fonte.render(self.instrucao.replace('—', ':'), True, (223, 238, 206))
            superficie.blit(texto, texto.get_rect(center=(480, 381)))

    def draw_abduction(self, superficie, jogador, progresso):
        sobreposicao = pygame.Surface(superficie.get_size(), pygame.SRCALPHA)
        sobreposicao.fill((16, 8, 59, int(180*progresso)))
        superficie.blit(sobreposicao, (0, 0))
        if progresso < 0.25:
            visual = jogador.get_draw_image().get_rect(
                midbottom=self.camera.apply(jogador.rect).midbottom)
            pygame.draw.rect(superficie, (244, 201, 118),
                             visual.inflate(8, 8), 2)
        # Fios e anéis visuais representam a captura; não causam dano físico.
        for ator in [jogador, *self.professores]:
            retangulo = ator.get_draw_image().get_rect(
                midbottom=self.camera.apply(ator.rect).midbottom)
            raio = retangulo.width//2+6 + int(progresso*60)
            pygame.draw.ellipse(superficie, (127, 227, 216),
                                (retangulo.centerx-raio, retangulo.centery-12, raio*2, 24), 2)
            pygame.draw.line(superficie, (127, 227, 216), (retangulo.centerx, 90), retangulo.midtop, 2)
        self._text(superficie, 'IFVania: transportando para o mundo virtual...', 220, 235)
