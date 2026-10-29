"""Sistema simples de caixas de diálogo estilo RPG/metroidvania."""
import pygame
import configuracoes
from interface import tema


class CaixaDialogo:
    def __init__(self):
        self.linhas = []          # lista de tuplas (falante, texto)
        self.indice = 0
        self.ativo = False
        self.ao_concluir = None
        self.fonte = pygame.font.Font(None, 22)
        self.fonte_nome = pygame.font.Font(None, 24)
        self._caracteres_exibidos = 0
        self._velocidade_digitacao = 2  # caracteres por frame
        self.nome_jogador = 'Aluno(a)'

    def resolve_lines(self, linhas):
        return [(self.nome_jogador if falante in ('Aluno(a)', '{player}') else falante,
                 texto.replace('{player}', self.nome_jogador)) for falante, texto in linhas]

    def start(self, linhas, ao_concluir=None):
        if not linhas:
            if ao_concluir:
                ao_concluir()
            return
        self.linhas = self.resolve_lines(linhas)
        self.indice = 0
        self.ativo = True
        self.ao_concluir = ao_concluir
        self._caracteres_exibidos = 0

    def handle_event(self, evento):
        if not self.ativo:
            return
        if evento.type == pygame.KEYDOWN and evento.key in (
            pygame.K_e, pygame.K_RETURN, pygame.K_SPACE
        ):
            falante, texto = self.linhas[self.indice]
            if self._caracteres_exibidos < len(texto):
                self._caracteres_exibidos = len(texto)  # revela tudo de uma vez
                return
            self.indice += 1
            self._caracteres_exibidos = 0
            if self.indice >= len(self.linhas):
                self.ativo = False
                ao_finalizar = self.ao_concluir
                self.ao_concluir = None
                if ao_finalizar:
                    ao_finalizar()

    def update(self):
        if not self.ativo:
            return
        falante, texto = self.linhas[self.indice]
        if self._caracteres_exibidos < len(texto):
            self._caracteres_exibidos = min(len(texto), self._caracteres_exibidos + self._velocidade_digitacao)

    def _wrap(self, texto, largura_maxima):
        palavras = texto.split(' ')
        linhas, atual = [], ''
        for palavra in palavras:
            tentativa = (atual + ' ' + palavra).strip()
            if self.fonte.size(tentativa)[0] > largura_maxima:
                linhas.append(atual)
                atual = palavra
            else:
                atual = tentativa
        if atual:
            linhas.append(atual)
        return linhas

    def draw(self, superficie):
        if not self.ativo:
            return
        falante, texto = self.linhas[self.indice]
        texto_exibido = texto[: self._caracteres_exibidos]

        retangulo_caixa = pygame.Rect(24, configuracoes.ALTURA_TELA-156, configuracoes.LARGURA_TELA-48, 142)
        tema.panel(superficie, retangulo_caixa, tema.CIANO if falante == 'Entidade' else tema.AMBAR)
        pygame.draw.line(superficie, tema.BORDA, (retangulo_caixa.x+20, retangulo_caixa.y+36),
                         (retangulo_caixa.right-20, retangulo_caixa.y+36))
        tema.text(superficie, self.fonte_nome, falante.upper(), (retangulo_caixa.x+20, retangulo_caixa.y+12),
                   tema.CIANO if falante == 'Entidade' else tema.AMBAR)
        linhas_quebradas = self._wrap(texto_exibido, retangulo_caixa.width-40)
        for i, linha in enumerate(linhas_quebradas[:3]):
            tema.text(superficie, self.fonte, linha, (retangulo_caixa.x+20, retangulo_caixa.y+48+i*20))
        if self._caracteres_exibidos >= len(texto):
            fonte_dica = pygame.font.Font(None, 18)
            dica = fonte_dica.render('E / ENTER  continuar', True, tema.ATENUADO)
            superficie.blit(dica, dica.get_rect(bottomright=(retangulo_caixa.right-20, retangulo_caixa.bottom-10)))
