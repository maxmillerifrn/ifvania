"""Sequência doméstica da campanha, com tempo e encenação próprios."""
from dataclasses import dataclass
import math
import pygame

from mundo import arte_introducao as arte
from sistema import configuracoes, recursos, sons


def progresso(tempo, inicio, fim):
    return max(0., min(1., (tempo-inicio)/(fim-inicio)))


def suave(tempo, inicio, fim):
    peso = progresso(tempo, inicio, fim)
    return peso*peso*(3-2*peso)


@dataclass(frozen=True)
class Cena:
    duracao: float
    encenar: str
    falas: tuple = ()
    sinais: tuple = ()


class Introducao:
    CENAS = (
        Cena(9, 'chegada', ((1.8, 4.9, 'Aluno(a)', 'Enfim em casa. Só falta a atividade de Max.'),
                           (5.7, 8.6, 'Aluno(a)', 'Onde foi que eu anotei o prazo?'))),
        Cena(13.5, 'atividade', ((2.1, 5.2, 'Aluno(a)', 'A lista veio vazia. De novo.'),
                                (6.7, 10.2, 'Aluno(a)', 'IA, faz a atividade inteira. Pode mandar o arquivo pronto.'),
                                (10.5, 13.2, 'Aluno(a)', 'Vou dormir. De manhã eu vejo como ficou.')),
             ((2, 'tecla'), (4, 'tecla'), (10.2, 'tecla'), (13.2, 'silencio'))),
        Cena(9, 'oscilacao', sinais=((1, 'energia'), (2.6, 'recuperacao'))),
        Cena(12, 'codigo_pronto', (
            (4.0, 7.4, 'IA', 'Atividade concluída. Entrega sincronizada com o campus.'),
            (7.7, 10.8, 'Aluno(a)', 'Já entregou? Então posso dormir mais cinco minutos.')),
            ((4.0, 'tecla'), (11.1, 'recuperacao'))),
        Cena(9.5, 'despertar', ((1.7, 5.3, 'Aluno(a)', 'Ué, eu nem toquei no teclado... O que é isso?'),),
             ((1.1, 'anomalia'), (5.3, 'energia'))),
    )

    def __init__(self, jogador, caixa_dialogo):
        self.indice = 0
        self.quadro = 0
        self.sinais_tocados = set()
        self.figuras = jogador.figuras
        self.caixa_dialogo = caixa_dialogo
        self.fundo_rua = recursos.load_image("cenarios/introducao/fachada.png")
        self.fundo_quarto = recursos.load_image("cenarios/introducao/quarto.png")
        tecido = self.fundo_quarto.subsurface((371, 316, 157, 78))
        self.coberta = pygame.transform.smoothscale(tecido, (271, 106))
        self.fundo = pygame.Surface(arte.TAMANHO)
        self.sombra = pygame.Surface(arte.TAMANHO, pygame.SRCALPHA)
        self.editor = arte.EditorIntroducao()
        self.fonte = pygame.font.Font(None, 27)
        self.fonte_menor = pygame.font.Font(None, 20)
        self.fonte_hora = pygame.font.SysFont('monospace', 17)
        self.dica = self.fonte_menor.render('ESC pausa / F pular', True, (213, 225, 231))

    @property
    def tempo(self):
        return self.quadro / configuracoes.QUADROS_POR_SEGUNDO

    def atualizar(self):
        cena = self.CENAS[self.indice]
        self.quadro += 1
        for instante, sinal in cena.sinais:
            if self.tempo >= instante and instante not in self.sinais_tocados:
                self.sinais_tocados.add(instante)
                if sinal in ('silencio', 'anomalia'):
                    sons.definir_ambiente(sinal)
                else:
                    sons.tocar(sinal)
        if self.tempo < cena.duracao:
            return False
        if self.indice == len(self.CENAS)-1:
            return True
        self.indice += 1
        self.quadro = 0
        self.sinais_tocados.clear()
        return False

    def escurecer(self, opacidade):
        self.sombra.fill((5, 9, 20, round(255*max(0, min(1, opacidade)))))
        self.fundo.blit(self.sombra, (0, 0))

    def quadro_ator(self, tempo, caminhada=0, esquerda=False, pose=None, escala=1.):
        lado = '_l' if esquerda else '_r'
        if pose:
            imagem = self.figuras[pose+lado]
        elif caminhada:
            imagem = self.figuras['walk'+lado][int(caminhada/12) % 8]
        else:
            imagem = self.figuras['idle'+lado][int(tempo*2) % 2]
        tamanho = max(1, round(168*escala))
        original = recursos.imagem_apresentacao(imagem, (80, 80))
        return pygame.transform.scale(original, (tamanho, tamanho))

    def ator(self, x, y, tempo, caminhada=0, esquerda=False, pose=None, escala=1.,
             angulo=0, opacidade=255, sombra=True):
        imagem = self.quadro_ator(tempo, caminhada, esquerda, pose, escala)
        if angulo:
            imagem = pygame.transform.rotate(imagem, angulo)
        if opacidade < 255:
            imagem = imagem.convert_alpha()
            # Preserve a transparência por pixel nas bordas do sprite.
            imagem.fill((255, 255, 255, opacidade), special_flags=pygame.BLEND_RGBA_MULT)
        if sombra and not angulo:
            pygame.draw.ellipse(self.fundo, (63, 48, 43), (x-29, y-5, 58, 10))
        apoio = imagem.get_bounding_rect().midbottom
        self.fundo.blit(imagem, (round(x)-apoio[0], round(y)-apoio[1]))

    def quarto(self, noite, hora):
        self.fundo.blit(self.fundo_quarto, (0, 0))
        if noite:
            # Cada vidro escurece por dentro, preservando caixilhos e cortinas.
            cor = (round(255-105*noite), round(255-79*noite), round(255-30*noite))
            for x, largura in ((342, 55), (405, 37), (451, 49), (508, 43)):
                for y, altura in ((118, 24), (151, 108)):
                    self.fundo.fill(cor, (x, y, largura, altura), special_flags=pygame.BLEND_RGB_MULT)
        visor = pygame.Rect(583, 255, 60, 24)
        pygame.draw.rect(self.fundo, (31, 25, 24), visor, border_radius=4)
        texto = self.fonte_hora.render(hora, True, (210, 159, 113))
        self.fundo.blit(texto, texto.get_rect(center=visor.center))

    def mochila(self, x, y):
        pygame.draw.ellipse(self.fundo, (33, 29, 28), (x-26, y+49, 91, 11))
        pygame.draw.arc(self.fundo, (36, 37, 32), (x+34, y+7, 37, 48), 0.2, 4.8, 5)
        pygame.draw.arc(self.fundo, (54, 59, 44), (x+12, y-7, 24, 19), 0, math.pi, 4)
        pygame.draw.rect(self.fundo, (28, 35, 32), (x, y, 51, 55), border_radius=13)
        pygame.draw.rect(self.fundo, (65, 76, 56), (x+3, y+2, 43, 48), border_radius=12)
        pygame.draw.rect(self.fundo, (79, 89, 65), (x+6, y+6, 35, 40), 1, border_radius=11)
        pygame.draw.rect(self.fundo, (43, 52, 40), (x+4, y+33, 42, 19), border_radius=5)
        pygame.draw.line(self.fundo, (138, 134, 89), (x+12, y+37), (x+35, y+37))

    def chegada(self, tempo):
        if tempo < 4.8:
            self.fundo.blit(self.fundo_rua, (0, 0))
            andar = suave(tempo, 0.25, 3.94)
            entrar = suave(tempo, 3.73, 4.45)
            x = 113+405*andar+16*entrar
            self.ator(x, 460-37*entrar, tempo, 405*andar+16*entrar if entrar < 1 else 0,
                      escala=1.02-0.13*entrar, opacidade=round(255*(1-entrar)),
                      sombra=entrar == 0)
            if entrar:
                batente = pygame.Rect(556, 214, 72, 216)
                self.fundo.blit(self.fundo_rua, batente, batente)
            self.escurecer(max(1-suave(tempo, 0, 0.75), suave(tempo, 4.18, 4.8)))
            return
        self.quarto(suave(tempo, 5, 9)*0.52, '18:07')
        andar = suave(tempo, 4.8, 8.15)
        x = 76+552*andar
        self.ator(x, 437+7*suave(tempo, 4.8, 5.7), tempo, 552*andar if andar < 1 else 0)
        if tempo >= 8.15:
            self.mochila(arte.MOCHILA[0], arte.MOCHILA[1]-round(18*(1-suave(tempo, 8.15, 8.43))))
            pygame.draw.rect(self.fundo, (61, 104, 105), arte.MONITOR)
        self.escurecer(1-suave(tempo, 4.8, 5.25))

    def posto(self, tempo, hora='20:46'):
        self.quarto(0.82, hora)
        self.mochila(*arte.MOCHILA)
        x, y = arte.CADEIRA
        imagem = self.quadro_ator(tempo)
        corpo = imagem.get_bounding_rect()
        corte = corpo.y+round(corpo.height*0.63)
        tronco = imagem.subsurface((0, 0, imagem.get_width(), corte))
        self.fundo.blit(tronco, tronco.get_rect(midbottom=(x-8, 355)))
        pernas = imagem.subsurface((0, corte, imagem.get_width(), corpo.bottom-corte))
        pernas = pygame.transform.rotozoom(pernas, 13, 0.9)
        self.fundo.blit(pernas, pernas.get_rect(midbottom=(x+26, y-25)))

    def atividade(self, tempo):
        if tempo < 10.65:
            self.posto(tempo)
        else:
            self.quarto(0.9, '20:46')
            self.mochila(*arte.MOCHILA)
            andar = suave(tempo, 10.65, 13.16)
            self.ator(688-402*andar, 446, tempo, 402*andar if andar < 1 else 0, esquerda=True)
            deitar = suave(tempo, 13.16, 13.5)
            if deitar:
                self.escurecer(deitar*0.87)
        quantidade = min(3, 1+int(tempo*1.4)) if tempo < 10.2 else min(7, 3+int((tempo-10.2)*2))
        estado = 'Max / POO: modele uma lista de chamada'
        if 1.8 < tempo < 5.6:
            estado = 'Teste 02: esperava 1 aluno / recebeu 0'
        elif 6.7 < tempo < 10.2:
            estado = 'Assistente: aguarda instruções...'
        elif tempo >= 10.2:
            estado = 'IA gerando a atividade...'
        self.editor.desenhar(self.fundo, quantidade, 0, estado, tempo, ampliar=tempo < 10.65)

    def oscilacao(self, tempo):
        self.quarto(1, '00:42')
        self.mochila(*arte.MOCHILA)
        self.dormindo(tempo)
        self.escurecer(0.56)
        alteradas = int(7*progresso(tempo, 2.7, 7.4))
        estado = 'IA gerando a atividade...'
        if tempo >= 1:
            estado = 'TENSÃO BAIXA / reiniciando console'
        if tempo >= 2.6:
            estado = 'Interface restaurada / sessão duplicada'
        if tempo >= 5:
            estado = 'IFVania :: mapa vinculando ao campus'
        self.editor.desenhar(self.fundo, 7, alteradas, estado, tempo, lateral=True)
        if 1 <= tempo < 2.6:
            opacidade = 0.94 if 1.52 < tempo < 2.24 else 0.22+0.17*math.sin(tempo*24)
            self.escurecer(opacidade)
            arte.fragmentar(self.fundo, tempo, 0.21, arte.MONITOR.center)
        elif 2.6 <= tempo < 3.05 or 5.8 <= tempo < 7.7:
            arte.fragmentar(self.fundo, tempo, 0.13, arte.MONITOR.center)

    def dormindo(self, tempo):
        recorte = self.fundo.get_clip()
        self.fundo.set_clip((180, 235, 112, 85))
        self.ator(arte.CAMA[0], arte.CAMA[1]+round(math.sin(tempo*2)*2),
                  tempo, escala=0.80, angulo=88)
        self.fundo.set_clip(recorte)
        self.fundo.blit(self.coberta, (257, 288))

    def codigo_pronto(self, tempo):
        hora = '06:12'
        if tempo < 3.9:
            self.quarto(0.14, hora)
            self.mochila(*arte.MOCHILA)
            levantar = suave(tempo, 0.8, 1.6)
            if not levantar:
                self.dormindo(tempo)
            else:
                andar = suave(tempo, 1.6, 3.9)
                distancia = 402*andar
                self.ator(arte.CAMA[0]+distancia, arte.CAMA[1]+129*levantar, tempo,
                          distancia if andar < 1 else 0,
                          escala=0.80+0.20*levantar, angulo=88*(1-levantar))
            self.escurecer(0.50-0.26*suave(tempo, 0, 1.6))
        else:
            self.posto(tempo, hora)
            self.escurecer(0.24)
        self.editor.desenhar(self.fundo, 7, 0, 'Entrega enviada / Portal IFRN Caicó',
                             tempo, ampliar=tempo >= 3.9)
        if 11.1 <= tempo < 11.6:
            arte.fragmentar(self.fundo, tempo, 0.18, arte.MONITOR.center)

    def despertar(self, tempo):
        atracao = suave(tempo, 5, 8.8)
        intensidade = suave(tempo, 0.6, 7.8)
        centro_x, centro_y = arte.MONITOR.center
        if tempo < 2.6:
            self.posto(tempo, '06:12')
        else:
            self.quarto(0.14, '06:12')
            self.mochila(*arte.MOCHILA)
            recuar = suave(tempo, 2.6, 4.2)
            if atracao < 1:
                inicio = 688-112*recuar
                self.ator(inicio+(centro_x-inicio)*atracao,
                          446+(centro_y-446)*atracao-math.sin(atracao*math.pi)*70, tempo,
                          112*recuar if recuar < 1 else 0, esquerda=0 < recuar < 1,
                          pose='jump' if atracao else None,
                          escala=max(0.05, 1-atracao), angulo=-130*atracao)
        self.escurecer(0.24+0.35*intensidade)
        pygame.draw.rect(self.fundo, (113, 234, 225), arte.MONITOR)
        arte.luz(self.fundo, arte.MONITOR.center, 360, (89, 234, 235, 115+round(intensidade*126)))
        if 1.45 <= tempo < 5.3:
            nome = self.caixa_dialogo.nome_jogador.upper()
            texto = self.fonte_hora.render(f'SESSÃO AUTORA / {nome}', False, (186, 250, 222))
            placa = texto.get_rect(midbottom=(centro_x, centro_y-54)).inflate(12, 8)
            placa.clamp_ip(pygame.Rect(16, 32, 928, 476))
            pygame.draw.rect(self.fundo, (16, 55, 67), placa)
            self.fundo.blit(texto, texto.get_rect(center=placa.center))
        if intensidade > 0:
            for indice in range(4):
                raio = round(35+((tempo*69+indice*60) % 260)*intensidade)
                pygame.draw.ellipse(self.fundo, (79, 157+indice*15, 181),
                                    (centro_x-raio, centro_y-raio//2, raio*2, raio), 1)
            arte.fragmentar(self.fundo, tempo, intensidade, arte.MONITOR.center)
        self.escurecer(suave(tempo, 8.55, 9.45)*0.76)

    def desenhar(self, tela, com_interface=True):
        cena = self.CENAS[self.indice]
        tempo = self.tempo
        getattr(self, cena.encenar)(tempo)
        if self.indice in (1, 2, 3):
            opacidade = max(1-suave(tempo, 0, 0.3), suave(tempo, cena.duracao-0.25, cena.duracao))
            self.escurecer(opacidade*0.55)
        enquadramento = self.fundo.get_rect()
        if self.indice == 0:
            aproximacao = suave(tempo, 0.8, 3.9) if tempo < 4.8 else suave(tempo, 5.2, 8.4)
            margem = round(16*aproximacao)
            enquadramento = enquadramento.inflate(-4*margem, -round(2.25*margem))
        pygame.transform.scale(self.fundo.subsurface(enquadramento), tela.get_size(), tela)
        if not com_interface:
            return
        largura, altura = tela.get_size()
        pygame.draw.rect(tela, (6, 10, 19), (0, 0, largura, 30))
        pygame.draw.rect(tela, (6, 10, 19), (0, altura-30, largura, 30))
        tela.blit(self.dica, self.dica.get_rect(topright=(largura-17, 8)))
        for inicio, fim, falante, texto in cena.falas:
            if inicio <= tempo < fim:
                [(nome, texto)] = self.caixa_dialogo.resolve_lines([(falante, texto)])
                imagem = self.fonte.render(texto, True, (244, 239, 229))
                etiqueta = self.fonte_menor.render(nome.upper(), True, (248, 192, 136))
                caixa = pygame.Rect(0, 0, max(imagem.get_width(), etiqueta.get_width())+36, 51)
                caixa.midbottom = (largura//2, altura-31)
                pygame.draw.rect(tela, (12, 17, 29), caixa, border_radius=6)
                tela.blit(etiqueta, (caixa.x+18, caixa.y+7))
                tela.blit(imagem, (caixa.x+18, caixa.y+25))
                break
