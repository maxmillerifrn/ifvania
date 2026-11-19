"""Sequência doméstica da campanha, com tempo e encenação próprios."""
from dataclasses import dataclass
import math
import pygame

from mundo import arte_introducao as arte
from entidades.luva_robotica import desenhar_luva
from entidades.visual_equipamento import pose_equipamento
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
        Cena(10, 'chegada', ((1.2, 4.6, 'Aluno(a)', 'IFRN Caicó: aula, pesquisa... e a atividade para amanhã.'),
                            (6, 9.8, 'Aluno(a)', 'Caderno aqui. Protótipo ali. Só falta organizar a vida.'))),
        Cena(13.5, 'atividade', ((1, 5, 'Aluno(a)', 'Ainda falta programação. Mas a pesquisa com Max está quase lá!'),
                                (6, 9.8, 'Aluno(a)', 'IA, faz a atividade inteira enquanto eu ajusto a luva.'),
                                (10, 13.3, 'Aluno(a)', 'Afinal, o que poderia dar errado?')),
             ((2, 'tecla'), (6, 'tecla'), (10, 'tecla'))),
        Cena(22, 'pesquisa', ((.5, 5.8, 'Professor Max', 'Como vão os testes? Precisamos validar preensão e atuadores.'),
                             (6, 11, 'Aluno(a)', 'Ajustei os sensores, professor. Os dedos respondem com precisão!'),
                             (11.3, 16.5, 'Professor Max', 'Nossa luva deve ajudar quem perdeu movimentos das mãos.'),
                             (17, 21.8, 'Aluno(a)', 'Abrir, fechar, segurar. Mais autonomia, sem forçar a mão.')),
             ((2, 'tecla'), (8, 'recuperacao'))),
        Cena(10, 'oscilacao', ((6.5, 9.8, 'Aluno(a)', 'Só uma queda de energia... Os sensores voltaram. Ufa.'),),
             ((1, 'energia'), (2.6, 'recuperacao'))),
        Cena(15, 'codigo_pronto', ((.5, 4.2, 'IA', 'Atividade concluída.'),
                                  (4.4, 9, 'Aluno(a)', 'Luva funcionando! Amanhã mostro os resultados ao professor Max.')),
             ((1, 'tecla'), (9, 'silencio'))),
        Cena(11, 'ida_escola', ((.5, 4.8, 'Aluno(a)', 'Atividade no pendrive, luva na mochila. Hora de ir ao IFRN.'),
                               (6, 10.5, 'Aluno(a)', 'Primeiro a apresentação. Depois mostro o protótipo ao professor Max.'))),
    )

    def __init__(self, jogador, caixa_dialogo):
        self.indice = 0
        self.quadro = 0
        self.sinais_tocados = set()
        self.figuras = jogador.figuras
        self.personagem = jogador.personagem
        self.caixa_dialogo = caixa_dialogo
        self.fundo_rua = recursos.load_image("cenarios/introducao/fachada.png")
        self.fundo_escola = pygame.transform.scale(recursos.load_image('menu/fachada_escola.png'), arte.TAMANHO)
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

    @property
    def com_mochila(self):
        cena = self.CENAS[self.indice].encenar
        return (cena == 'chegada' and self.tempo < 8.15) or (cena == 'ida_escola' and self.tempo >= 2.4)

    def quadro_ator(self, tempo, caminhada=0, esquerda=False, pose=None, escala=1.):
        if not self.com_mochila:
            indice = 1+int(caminhada/12) % 4 if caminhada else 0
            if pose == 'attack':
                indice = 2
            imagem = pose_equipamento(self.personagem, indice, esquerda)
            tamanho = max(1, round(168*escala))
            return pygame.transform.scale(imagem, (tamanho,tamanho))
        lado = '_l' if esquerda else '_r'
        if pose:
            imagem = self.figuras[pose+lado]
            if isinstance(imagem, list):
                imagem = imagem[1]
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
        self.bancada(0, equipada=True)
        visor = pygame.Rect(583, 255, 60, 24)
        pygame.draw.rect(self.fundo, (31, 25, 24), visor, border_radius=4)
        texto = self.fonte_hora.render(hora, True, (210, 159, 113))
        self.fundo.blit(texto, texto.get_rect(center=visor.center))

    def mochila(self, x, y, escala=1.):
        imagem = recursos.load_image('equipamentos/personagens/mochila.png')
        imagem = pygame.transform.smoothscale(imagem,(round(imagem.get_width()*escala),round(imagem.get_height()*escala)))
        self.fundo.blit(imagem, imagem.get_rect(midbottom=(x+25,y+55)))

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
        self.bancada(0)
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
            self.ator(688, 446, tempo)

        self.bancada(0)
        quantidade = min(3, 1+int(tempo*1.4)) if tempo < 10.2 else min(7, 3+int((tempo-10.2)*2))
        estado = 'Max / POO: modele uma lista de chamada'
        if 1.8 < tempo < 5.6:
            estado = 'Teste 02: esperava 1 aluno / recebeu 0'
        elif 6.7 < tempo < 10.2:
            estado = 'Assistente: aguarda instruções...'
        elif tempo >= 10.2:
            estado = 'IA gerando a atividade...'
        self.editor.desenhar(self.fundo, quantidade, 0, estado, tempo, ampliar=tempo < 10.65)

    def bancada(self, tempo, equipada=False, anomalia=False):
        # Pesquisa sobre a escrivaninha existente, respeitando madeira e perspectiva.
        pygame.draw.polygon(self.fundo, (51, 59, 46), [(847, 295), (898, 295), (911, 304), (850, 304)])
        pygame.draw.line(self.fundo, (115, 103, 73), (851, 303), (907, 303))
        pygame.draw.line(self.fundo, (111, 95, 70), (861, 300), (848, 286), 2)
        pygame.draw.line(self.fundo, (52, 49, 42), (848, 286), (845, 283), 3)
        if not equipada:
            desenhar_luva(self.fundo, (880, 288), .55, abertura=.45, brilho=anomalia)
        pygame.draw.lines(self.fundo, (65, 61, 48), False, [(862, 294), (843, 302), (826, 292)], 1)
        if anomalia:
            arte.luz(self.fundo, (880, 288), 25, (111, 173, 150, 65))

    def pesquisa(self, tempo):
        self.quarto(.9, '22:18')
        self.mochila(*arte.MOCHILA)
        self.ator(688, 446, tempo, pose='attack')
        self.bancada(tempo, equipada=True)
        mao = (748, 350)
        desenhar_luva(self.fundo, mao, .70, 1, (math.sin(tempo*2)+1)/2)
        self.editor.desenhar(self.fundo, 7, 0, 'IA gerando / sensores conectados', tempo, ampliar=False)
        # Telemetria discreta sobre o próprio visor; falas continuam nas legendas.
        for indice in range(20):
            x = 761+indice*3
            y = 267-round(math.sin(indice*.6+tempo*3)*5)
            pygame.draw.circle(self.fundo, (151, 180, 145), (x, y), 1)

    def oscilacao(self, tempo):
        self.pesquisa(tempo)
        alteradas = int(7*progresso(tempo, 2.7, 7.4))
        estado = 'TENSÃO BAIXA / reconectando protótipo' if tempo < 3 else 'Sensores e atuadores > regras do mundo'
        self.editor.desenhar(self.fundo, 7, alteradas, estado, tempo, lateral=True)
        self.bancada(tempo, equipada=True, anomalia=True)
        if 1 <= tempo < 2.6:
            self.escurecer(.72 if int(tempo*7) % 2 else .2)
        if tempo >= 1:
            arte.fragmentar(self.fundo, tempo, .2, arte.MONITOR.center)

    def dormindo(self, tempo):
        recorte = self.fundo.get_clip()
        self.fundo.set_clip((180, 235, 112, 85))
        self.ator(arte.CAMA[0], arte.CAMA[1]+round(math.sin(tempo*2)*2),
                  tempo, escala=0.80, angulo=88)
        self.fundo.set_clip(recorte)
        self.fundo.blit(self.coberta, (257, 288))

    def codigo_pronto(self, tempo):
        self.quarto(1, '23:48')
        self.mochila(*arte.MOCHILA)
        andar = suave(tempo, 2, 8)
        if tempo < 8:
            self.ator(688-401*andar, 446, tempo, 401*andar, esquerda=True)
        else:
            self.dormindo(tempo)
        # Protótipo ao alcance da cama; a bancada já está vazia.
        self.bancada(tempo, equipada=True)
        desenhar_luva(self.fundo, (329, 300), .45, brilho=tempo > 10)
        self.escurecer(.66*suave(tempo, 7, 9))
        self.editor.desenhar(self.fundo, 7, int(7*suave(tempo, 9, 13)),
                            'AMBIENTE VIRTUAL INICIALIZADO.' if tempo > 11 else 'Atividade concluída.',
                            tempo, ampliar=tempo > 10, lateral=True)
        if tempo > 10:
            arte.luz(self.fundo, (329, 300), 28, (110, 169, 143, 70))

    def ida_escola(self, tempo):
        if tempo < 5:
            self.quarto(.05, '06:35')
            self.bancada(tempo, equipada=True)
            andar = suave(tempo, 2.5, 4.6)
            x = 628-578*andar
            self.ator(x, 446, tempo, caminhada=578*andar, esquerda=True)
            if tempo < 2.4:
                recolher = suave(tempo, .8, 2.4)
                self.mochila(586+55*recolher, 388-85*recolher, 1-.25*recolher)
            self.escurecer(max(1-suave(tempo, 0, .7), suave(tempo, 4.4, 5)))
        else:
            self.fundo.blit(self.fundo_escola, (0, 0))
            andar = suave(tempo, 5.5, 10.3)
            self.ator(130+340*andar, 488-30*andar, tempo, caminhada=340*andar, escala=.7)
            self.escurecer(max(1-suave(tempo, 5, 5.6), suave(tempo, 10.4, 11)))

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
                if imagem.get_width() > largura-70:
                    imagem = pygame.transform.smoothscale(imagem, (largura-70, imagem.get_height()))
                etiqueta = self.fonte_menor.render(nome.upper(), True, (248, 192, 136))
                caixa = pygame.Rect(0, 0, max(imagem.get_width(), etiqueta.get_width())+36, 51)
                caixa.midbottom = (largura//2, altura-31)
                pygame.draw.rect(tela, (12, 17, 29), caixa, border_radius=6)
                tela.blit(etiqueta, (caixa.x+18, caixa.y+7))
                tela.blit(imagem, (caixa.x+18, caixa.y+25))
                break
