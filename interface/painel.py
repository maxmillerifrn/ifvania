"""PainelInformacoes com integridade segmentada, identificação da área e estado do boss."""
import pygame
import configuracoes
from habilidades import Habilidade, NOMES_HABILIDADES
from interface import tema


class PainelInformacoes:
    def __init__(self):
        self.fonte = pygame.font.Font(None, 22)
        self.fonte_pequena = pygame.font.Font(None, 20)
        self.fonte_grande = pygame.font.Font(None, 34)
        self.ultimas_linhas_dicas = []

    def draw(self, superficie, jogador, nome_fase, chefe=None):
        tema.panel(superficie, (18, 16, 204, 66), tema.CIANO)
        cor = tema.PERIGO if jogador.vida <= 2 else tema.CIANO
        tema.text(superficie, self.fonte_pequena, 'INTEGRIDADE', (31, 24), tema.ATENUADO)
        valor = f'{jogador.vida:02d} / {jogador.vida_maxima:02d}'
        tema.text(superficie, self.fonte_pequena, valor, (160, 24), cor)
        intervalo = 4
        largura = (176-intervalo*(jogador.vida_maxima-1)) / jogador.vida_maxima
        for i in range(jogador.vida_maxima):
            r = pygame.Rect(round(31+i*(largura+intervalo)), 48, max(1, int(largura)), 12)
            pygame.draw.rect(superficie, cor if i < jogador.vida else (35, 47, 54), r)
        tema.text(superficie, self.fonte_pequena, player_label(jogador), (31, 65), tema.ATENUADO)
        largura_area = min(498, max(224, self.fonte.size(nome_fase)[0]+30))
        retangulo_area = pygame.Rect(configuracoes.LARGURA_TELA-largura_area-18, 16, largura_area, 43)
        tema.panel(superficie, retangulo_area)
        tema.text(superficie, self.fonte_pequena, 'LOCALIZAÇÃO', (retangulo_area.x+12, 21), tema.AMBAR)
        tema.text(superficie, self.fonte, tema.fit_text(self.fonte, nome_fase, largura_area-24),
                   (retangulo_area.x+12, 36))
        if jogador.habilidades:
            rotulos = ' / '.join(NOMES_HABILIDADES[a] for a in sorted(jogador.habilidades, key=lambda a: a.value))
            rotulo = tema.fit_text(self.fonte_pequena, rotulos, largura_area-24)
            tema.panel(superficie, (retangulo_area.x, 64, largura_area, 26))
            tema.text(superficie, self.fonte_pequena, rotulo, (retangulo_area.x+12, 70), tema.ATENUADO)
        if jogador.chicote_desbloqueado:
            tema.panel(superficie, (18, 91, 204, 45))
            pronto = jogador.espera_esquiva == 0
            rotulo = ('CARGA PRONTA / SOLTE X' if jogador.carga >= configuracoes.TEMPO_CARGA else 'CARREGANDO') if jogador.carregando else ('ESQUIVA PRONTA' if pronto else 'ESQUIVA RECUPERANDO')
            tema.text(superficie, self.fonte_pequena, rotulo, (30, 99), tema.CIANO if pronto else tema.ATENUADO)
            fracao = (jogador.carga/configuracoes.TEMPO_CARGA if jogador.carregando
                      else 1-jogador.espera_esquiva/configuracoes.ESPERA_ESQUIVA)
            pygame.draw.rect(superficie, (43, 50, 54), (30, 122, 178, 4))
            pygame.draw.rect(superficie, tema.AMBAR if jogador.carregando else tema.CIANO,
                             (30, 122, round(178*fracao), 4))
        if chefe is not None and chefe.ativo and chefe.vivo:
            self.draw_boss(superficie, chefe)

    def draw_boss(self, superficie, chefe):
        retangulo = pygame.Rect(248, 91, configuracoes.LARGURA_TELA-496, 57)
        tema.panel(superficie, retangulo, tema.PERIGO)
        tema.text(superficie, self.fonte, chefe.nome.upper(), (retangulo.x+14, retangulo.y+10))
        etapa = 'FASE II' if chefe.etapa >= 2 else 'FASE I'
        tema.text(superficie, self.fonte_pequena, etapa, (retangulo.right-66, retangulo.y+12), tema.PERIGO)
        barra = pygame.Rect(retangulo.x+14, retangulo.y+36, retangulo.width-28, 7)
        pygame.draw.rect(superficie, (40, 30, 38), barra)
        proporcao = max(0, min(1, chefe.vida/chefe.vida_maxima))
        pygame.draw.rect(superficie, tema.PERIGO, (barra.x, barra.y, round(barra.width*proporcao), barra.height))
        pygame.draw.line(superficie, tema.AMBAR, (barra.centerx, barra.top-2), (barra.centerx, barra.bottom+2))

    def draw_controls_hint(self, superficie, jogador):
        dicas = ['A/D ou SETAS  mover', 'ESPAÇO  saltar',
                 'X tocar  golpe / segurar  carga' if jogador.chicote_desbloqueado else 'E  interagir']
        if jogador.chicote_desbloqueado and not jogador.has(Habilidade.ARRANCADA):
            dicas.append('SHIFT  esquiva')
        for habilidade, dica in ((Habilidade.SALTO_DUPLO, 'ESPAÇO 2x  salto duplo'),
                              (Habilidade.ARRANCADA, 'SHIFT  dash'), (Habilidade.ESCALADA_PAREDE, 'PAREDE + SALTO'),
                              (Habilidade.DISPARO_DISTANCIA, 'F  tiro'), (Habilidade.ESCUDO, 'Q  escudo')):
            if jogador.has(habilidade):
                dicas.append(dica)
        dicas.append('ESC  pausa')
        fileiras, linha = [], ''
        for dica in dicas:
            tentativa = linha+'     |     '+dica if linha else dica
            if self.fonte_pequena.size(tentativa)[0] > configuracoes.LARGURA_TELA-64 and linha:
                fileiras.append(linha)
                linha = dica
            else:
                linha = tentativa
        fileiras.append(linha)
        self.ultimas_linhas_dicas = fileiras
        altura = len(fileiras)*20+16
        retangulo = pygame.Rect(18, configuracoes.ALTURA_TELA-altura-10, configuracoes.LARGURA_TELA-36, altura)
        tema.panel(superficie, retangulo)
        for i, fileira in enumerate(fileiras):
            tema.text(superficie, self.fonte_pequena, fileira, (retangulo.x+13, retangulo.y+9+i*20), tema.ATENUADO)

    def draw_center_text(self, superficie, texto, subtitulo=None, deslocamento_y=0):
        retangulo = pygame.Rect(150, configuracoes.ALTURA_TELA//2-67+deslocamento_y, configuracoes.LARGURA_TELA-300, 138)
        tema.panel(superficie, retangulo, tema.AMBAR)
        titulo = self.fonte_grande.render(tema.fit_text(self.fonte_grande, texto, retangulo.width-40), True, tema.PAPEL)
        superficie.blit(titulo, titulo.get_rect(center=(retangulo.centerx, retangulo.y+46)))
        if subtitulo:
            linha = self.fonte.render(tema.fit_text(self.fonte, subtitulo, retangulo.width-40), True, tema.ATENUADO)
            superficie.blit(linha, linha.get_rect(center=(retangulo.centerx, retangulo.y+89)))


def player_label(jogador):
    return 'ESTUDANTE / '+('MENINA' if jogador.personagem == 'menina' else 'MENINO')
