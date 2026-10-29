"""Telas de acesso à escola, com navegação por mouse e teclado."""
import pygame
import recursos
import configuracoes
from entidades.jogador import Jogador
from interface import tema


class InterfaceInicial:
    def __init__(self):
        fachada = recursos.load_image('menu/escola_noturna.png')
        self.fundo = pygame.transform.scale(fachada, (configuracoes.LARGURA_TELA, configuracoes.ALTURA_TELA))
        self.fonte_titulo = pygame.font.Font(None, 94)
        self.fonte_cabecalho = pygame.font.Font(None, 36)
        self.fonte = pygame.font.Font(None, 28)
        self.fonte_pequena = pygame.font.Font(None, 20)
        self.retangulos_menu = [pygame.Rect(56, 300, 304, 54), pygame.Rect(56, 370, 304, 54)]
        self.retangulos_personagens = [pygame.Rect(244, 132, 220, 272), pygame.Rect(496, 132, 220, 272)]
        self.retangulo_confirmar = pygame.Rect(320, 428, 320, 48)
        self.retangulo_voltar = pygame.Rect(28, 28, 120, 40)
        self.retangulo_nome = pygame.Rect(240, 224, 480, 72)
        self.retangulo_confirmar_nome = pygame.Rect(320, 336, 320, 48)
        self.personagens = tuple(Jogador.PERSONAGENS)
        self.previas = {}
        for personagem in self.personagens:
            self.previas[personagem] = [pygame.transform.scale(quadro, (136, 136))
                                        for quadro in Jogador._load_sprites(personagem)['idle_r']]
        self.instante_animacao = 0
        self.veu = pygame.Surface(self.fundo.get_size(), pygame.SRCALPHA)
        for x in range(configuracoes.LARGURA_TELA):
            transparencia = max(0, int(225*(1-x/760)))
            pygame.draw.line(self.veu, (*tema.TINTA, transparencia), (x, 0), (x, configuracoes.ALTURA_TELA))

    def update(self):
        self.instante_animacao += 1

    def _center(self, superficie, valor, centro, fonte=None, cor=tema.PAPEL):
        renderizado = (fonte or self.fonte).render(valor, True, cor)
        superficie.blit(renderizado, renderizado.get_rect(center=centro))

    def _button(self, superficie, retangulo, rotulo, em_foco=False, numero=None):
        tema.panel(superficie, retangulo, tema.AMBAR if em_foco else None,
                    tema.ELEVADO if em_foco else tema.PAINEL)
        if em_foco:
            pygame.draw.line(superficie, tema.AMBAR, retangulo.topleft, (retangulo.right-1, retangulo.top))
        if numero:
            tema.text(superficie, self.fonte_pequena, numero, (retangulo.x+17, retangulo.y+19), tema.AMBAR if em_foco else tema.ATENUADO)
            tema.text(superficie, self.fonte, rotulo, (retangulo.x+54, retangulo.y+15), tema.PAPEL)
            if em_foco:
                tema.text(superficie, self.fonte, '>', (retangulo.right-30, retangulo.y+14), tema.AMBAR)
        else:
            self._center(superficie, rotulo, retangulo.center, cor=tema.AMBAR if em_foco else tema.PAPEL)

    def draw_menu(self, superficie, indice_menu):
        superficie.blit(self.fundo, (0, 0))
        superficie.blit(self.veu, (0, 0))
        tema.text(superficie, self.fonte_pequena, 'IFRN  /  CAMPUS CAICÓ', (58, 66), tema.AMBAR)
        tema.text(superficie, self.fonte_titulo, 'IFVania', (51, 106))
        pygame.draw.line(superficie, tema.AMBAR, (58, 193), (104, 193), 3)
        tema.text(superficie, self.fonte, 'A escola não é mais a mesma.', (58, 218), tema.PAPEL)
        for i, (retangulo, rotulo) in enumerate(zip(self.retangulos_menu, ('Jogar', 'Sair'))):
            self._button(superficie, retangulo, rotulo, i == indice_menu, f'0{i+1}')
        tema.text(superficie, self.fonte_pequena, 'Uma presença tomou os corredores.', (58, 454), tema.ATENUADO)
        pygame.draw.rect(superficie, tema.TINTA, (0, 498, configuracoes.LARGURA_TELA, 42))
        pygame.draw.line(superficie, tema.BORDA, (28, 498), (932, 498))
        tema.text(superficie, self.fonte_pequena, 'SETAS  escolher     ENTER  confirmar     MOUSE  selecionar', (56, 513), tema.ATENUADO)
        tema.text(superficie, self.fonte_pequena, 'IFVANIA / ACESSO', (790, 513), tema.AMBAR)

    def draw_selection(self, superficie, indice_personagem):
        superficie.blit(self.fundo, (0, 0))
        sobreposicao = pygame.Surface(superficie.get_size(), pygame.SRCALPHA)
        sobreposicao.fill((*tema.TINTA, 215))
        superficie.blit(sobreposicao, (0, 0))
        self._button(superficie, self.retangulo_voltar, 'Voltar')
        self._center(superficie, 'ESCOLHA SEU PERSONAGEM', (480, 59), self.fonte_cabecalho)
        self._center(superficie, 'A mesma escola. O mesmo perigo.', (480, 95), self.fonte_pequena, tema.ATENUADO)
        for i, retangulo in enumerate(self.retangulos_personagens):
            selecionado = i == indice_personagem
            tema.panel(superficie, retangulo, tema.AMBAR if selecionado else None,
                        tema.ELEVADO if selecionado else tema.PAINEL)
            tema.text(superficie, self.fonte_pequena, f'0{i+1} / ESTUDANTE', (retangulo.x+18, retangulo.y+16), tema.AMBAR if selecionado else tema.ATENUADO)
            pygame.draw.line(superficie, tema.BORDA, (retangulo.x+18, retangulo.y+44), (retangulo.right-18, retangulo.y+44))
            personagem = self.personagens[i]
            quadro = self.previas[personagem][(self.instante_animacao//24) % 2]
            pygame.draw.ellipse(superficie, (7, 13, 18), (retangulo.centerx-58, 304, 116, 12))
            superficie.blit(quadro, quadro.get_rect(midbottom=(retangulo.centerx, 316)))
            self._center(superficie, Jogador.PERSONAGENS[personagem], (retangulo.centerx, 342), self.fonte_cabecalho)
            self._center(superficie, 'SELECIONADO' if selecionado else 'Clique para escolher',
                         (retangulo.centerx, 382), self.fonte_pequena, tema.AMBAR if selecionado else tema.ATENUADO)
        self._button(superficie, self.retangulo_confirmar,
                     f'Jogar com {Jogador.PERSONAGENS[self.personagens[indice_personagem]]}', True)
        self._center(superficie, 'Mesmos controles e habilidades para os dois personagens.', (480, 501), self.fonte_pequena, tema.ATENUADO)
        self._center(superficie, 'SETAS escolher    ENTER começar    ESC voltar', (480, 526), self.fonte_pequena, tema.ATENUADO)

    def draw_name_entry(self, superficie, nome, personagem, erro=''):
        superficie.blit(self.fundo, (0, 0))
        sobreposicao = pygame.Surface(superficie.get_size(), pygame.SRCALPHA)
        sobreposicao.fill((*tema.TINTA, 220))
        superficie.blit(sobreposicao, (0, 0))
        self._button(superficie, self.retangulo_voltar, 'Voltar')
        self._center(superficie, 'COMO VOCÊ QUER SER CHAMADO?', (480, 100), self.fonte_cabecalho)
        self._center(superficie, 'Seu nome aparecerá nos diálogos da jornada.', (480, 142), self.fonte_pequena, tema.ATENUADO)
        self._center(superficie, 'PERSONAGEM / '+Jogador.PERSONAGENS[personagem].upper(), (480, 181), self.fonte_pequena, tema.AMBAR)
        tema.panel(superficie, self.retangulo_nome, tema.PERIGO if erro else tema.CIANO)
        valor = nome or 'Digite seu nome'
        tema.text(superficie, self.fonte, valor, (self.retangulo_nome.x+20, self.retangulo_nome.y+26),
                   tema.PAPEL if nome else tema.ATENUADO)
        if (self.instante_animacao//30) % 2 == 0:
            x = self.retangulo_nome.x+20+(self.fonte.size(nome)[0] if nome else 0)
            pygame.draw.line(superficie, tema.CIANO, (x, self.retangulo_nome.y+22), (x, self.retangulo_nome.y+48), 2)
        tema.text(superficie, self.fonte_pequena, f'{len(nome)} / 20', (self.retangulo_nome.right-60, 308), tema.ATENUADO)
        self._button(superficie, self.retangulo_confirmar_nome, 'Começar a jornada', True)
        if erro:
            self._center(superficie, erro, (480, 411), self.fonte_pequena, tema.PERIGO)
        self._center(superficie, 'ENTER confirmar    BACKSPACE apagar    ESC voltar', (480, 477), self.fonte_pequena, tema.ATENUADO)
