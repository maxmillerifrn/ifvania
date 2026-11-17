"""Sequência escolar com geometria editável e interações únicas.

A sala, o corredor e o A28 compartilham a interface usada por Jogo (tilemap,
câmera, spawn, update e draw), sem criar inimigos ou um boss antecipadamente.
"""
from types import SimpleNamespace
import pygame
from sistema import recursos
from sistema import configuracoes
from entidades.professor import Professor
from mundo.camera import Camera
from mundo.arte_escolar import ArteEscolar
from interface import tema
from mundo.succao_computador import SuccaoComputador


class FaseEscolar:
    Y_PISO = 352
    NOMES = {'classroom': 'Laboratório de informática — programação orientada a objetos',
             'corridor': 'Pátio coberto — procure o laboratório A28',
             'lab': 'Laboratório A28 — encontre o professor Romerito'}

    def __init__(self, ambiente):
        self.ambiente = ambiente
        self.Y_PISO = 440 if ambiente == 'corridor' else 352
        self.nome = self.NOMES[ambiente]
        largura = 1920 if ambiente == 'corridor' else configuracoes.LARGURA_TELA
        self.mapa_blocos = SimpleNamespace(
            largura=largura, altura=configuracoes.ALTURA_TELA, perigos=[],
            solidos=[pygame.Rect(0, self.Y_PISO, largura, configuracoes.ALTURA_TELA-self.Y_PISO),
                    pygame.Rect(-32, 0, 32, configuracoes.ALTURA_TELA),
                    pygame.Rect(largura, 0, 32, configuracoes.ALTURA_TELA),
                    pygame.Rect(0, -32, largura, 32)])
        self.camera = Camera(largura, self.mapa_blocos.altura)
        self.surgimento_jogador = (64 if ambiente == 'classroom' else 120, self.Y_PISO-configuracoes.TAMANHO_PERSONAGEM[1])
        self.chefe = None
        self.professores = pygame.sprite.Group()
        if ambiente != 'corridor':
            self.professores.add(Professor(700, self.surgimento_jogador[1],
                                  'max' if ambiente == 'classroom' else 'romerito'))
        self.porta_a28 = pygame.Rect(1728, self.Y_PISO-134, 80, 134)
        self.interacao_disparada = False
        self.corrompido = ambiente != 'classroom'
        self.instantes = 0
        self.instantes_visuais = 0
        self.arte = ArteEscolar(ambiente, largura, mostrar_turma=ambiente == 'classroom')
        self.hipnose = 0.0
        self.succao = None
        self.indice_historia = 0
        self.fundo_memoria = recursos.load_image('cenarios/memoria_tarefa.png') if ambiente == 'classroom' else None
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
        self.succao = SuccaoComputador(self, jogador)

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
        if self.corrompido:
            self.hipnose = min(1, self.hipnose+1/90)

    def _door(self, superficie, x, rotulo, ativo=False, deslocamento_y=0):
        def desenhar(cor, retangulo, largura=0):
            destino = pygame.Rect(retangulo).move(0, deslocamento_y)
            self._rect(superficie, cor, destino, largura)

        # Porta metálica: caixilho, visor, dobradiças, puxador e chapa inferior.
        desenhar((21, 29, 34), (x-7, 210, 94, 142))
        desenhar((89, 100, 101), (x-4, 213, 88, 139), 2)
        desenhar((43, 57, 63), (x, 218, 80, 134))
        desenhar((71, 85, 89), (x+3, 221, 74, 128), 1)
        desenhar((14, 28, 35), (x+12, 230, 56, 42))
        desenhar((96, 123, 128), (x+12, 230, 56, 42), 2)
        desenhar((26, 47, 56), (x+16, 234, 48, 34))
        desenhar((65, 91, 99), (x+20, 237, 2, 27))
        desenhar((101, 113, 110), (x+61, 290, 10, 21))
        desenhar((164, 173, 163), (x+58, 295, 11, 3))
        desenhar((56, 69, 73), (x+8, 328, 64, 19))
        for hy in (239, 289, 327):
            desenhar((100, 107, 103), (x+2, hy, 4, 9))
        for sy in (334, 339, 344):
            desenhar((83, 93, 91), (x+15, sy, 46, 1))
        desenhar((13, 27, 33), (x-5, 180, 90, 25))
        desenhar((95, 117, 118), (x-5, 180, 90, 25), 1)
        self._text(superficie, rotulo, x+20, 185+deslocamento_y)
        if ativo:
            desenhar((110, 182, 179), (x+91, 288, 7, 4))

    def _desenhar_fachada_a28(self, superficie):
        """Bloco de chegada: porta pertence à parede e soleira ao piso."""
        self._rect(superficie, (30, 38, 41), (1600, 112, 320, 328))
        self._rect(superficie, (118, 108, 81), (1608, 120, 304, 312))
        for y in range(128, 420, 24):
            self._rect(superficie, (106, 98, 76), (1608, y, 304, 1))
        self._rect(superficie, (59, 67, 66), (1608, 354, 304, 78))
        self._rect(superficie, (123, 66, 56), (1608, 350, 304, 7))
        self._rect(superficie, (27, 39, 44), (1592, 100, 328, 14))
        self._rect(superficie, (151, 148, 119), (1592, 100, 328, 3))
        self._rect(superficie, (27, 35, 39), (1600, 432, 320, 8))
        self._rect(superficie, (149, 155, 139), (1718, 438, 100, 2))

    def draw(self, superficie, ocultar_professores=False):
        self.arte.draw(superficie, self.camera, self.instantes_visuais, self.corrompido, self.hipnose)
        if self.ambiente == 'corridor':
            self._desenhar_fachada_a28(superficie)
            self._door(superficie, self.porta_a28.x, 'A28', True, self.Y_PISO-352)
            self._rect(superficie, (17, 34, 40), (1280, 95, 250, 30))
            self._text(superficie, 'LABORATÓRIO A28  >', 1295, 102)
        else:
            titulo = ('IFVania — inteligência artificial' if self.arte.etapa_aula in ('execucao', 'revolta')
                      else 'Apresentação da atividade / POO') if self.ambiente == 'classroom' else 'LABORATÓRIO A28'
            self._text(superficie, titulo, 454, 170)
            subtitulo = ('Programação orientada a objetos' if self.ambiente == 'classroom'
                         else 'Rede isolada. Encerramento seguro.' if self.arte.etapa_aula == 'desligado'
                         else 'Sistema sob controle da IFVania.')
            self._text(superficie, subtitulo, 454, 200, pequeno=True)
        for professor in ([] if ocultar_professores else self.professores):
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
            superficie.blit(painel, (310, self.Y_PISO+13))
            texto = self.fonte.render(self.instrucao.replace('—', ':'), True, (223, 238, 206))
            superficie.blit(texto, texto.get_rect(center=(480, self.Y_PISO+29)))

    def draw_abduction(self, superficie, jogador, progresso):
        if self.succao:
            self.succao.draw(superficie, progresso)

    def sincronizar_aula(self, indice, indice_execucao, indice_corrupcao):
        self.indice_historia = indice
        self.arte.etapa_aula = ('revolta' if indice >= indice_corrupcao else
                               'execucao' if indice >= indice_execucao else
                               'pendrive' if indice >= indice_execucao-2 else 'codigo')
        if indice >= indice_corrupcao:
            self.corrompido = True
            self.hipnose = max(self.hipnose, min(1, (indice-indice_corrupcao)/3))

    def draw_apresentacao(self, superficie, indice, indice_memoria, indice_execucao):
        if indice_memoria <= indice < indice_execucao:
            area = pygame.Rect(130, 36, 700, 315)
            pygame.draw.rect(superficie, (5, 13, 22), area.inflate(12, 12))
            superficie.blit(pygame.transform.scale(self.fundo_memoria, area.size), area)
            legenda = 'NA NOITE ANTERIOR / TAREFA DE POO'
            self._text(superficie, legenda, 146, 46, pequeno=True)
            monitor = pygame.Rect(area.x+round(area.width*0.725), area.y+round(area.height*0.39),
                                  round(area.width*0.10), round(area.height*0.14))
            self.arte.terminais.draw(superficie, monitor, self.instantes_visuais,
                                    etapa_aula='geracao' if indice == indice_memoria else 'continuidade')
            if indice == indice_memoria+1:
                # Queda de energia e recuperação do programa, em batidas suaves.
                escuro = pygame.Surface(area.size, pygame.SRCALPHA)
                escuro.fill((1, 7, 17, 115 if (self.instantes_visuais//24) % 3 == 0 else 32))
                superficie.blit(escuro, area)
                self._text(superficie, 'Continuidade de aprendizagem ativada', 360, 312, (135, 235, 215), pequeno=True)
            return
        painel = pygame.Rect(305, 40, 350, 126)
        pygame.draw.rect(superficie, (7, 17, 25), painel)
        pygame.draw.rect(superficie, (66, 103, 111), painel, 2)
        etapa = self.arte.etapa_aula
        self._text(superficie, 'MONITOR DO ALUNO / tarefa.py', 317, 47, pequeno=True)
        linhas = {
            'codigo': ('class Atividade:', '    def executar(self):', '        return tarefa'),
            'pendrive': ('USB conectado', 'Abrindo tarefa.py...', 'Origem: pendrive do aluno'),
            'execucao': ('> python tarefa.py', 'IFVania.iniciar()', 'Conectando a rede da escola...'),
            'revolta': ('IFVANIA / SESSAO SEM FIM', 'encerrar() -> ACESSO NEGADO', 'Controle da turma: ATIVADO'),
        }[etapa]
        for numero, linha in enumerate(linhas):
            self._text(superficie, linha, 318, 74+numero*24,
                       (233, 166, 148) if self.corrompido else (132, 219, 205), pequeno=True)
        if indice >= indice_execucao:
            self._rect(superficie, (151, 166, 161), (88, 310, 18, 7))
            self._rect(superficie, (53, 121, 112), (103, 311, 9, 5))
