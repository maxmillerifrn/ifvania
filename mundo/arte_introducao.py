"""Arte em camadas e efeitos do computador na abertura."""
import math
import random

import pygame

TAMANHO = (960, 540)
MONITOR = pygame.Rect(756, 238, 82, 44)
CADEIRA = (704, 425)
CAMA = (287, 317)
MOCHILA = (586, 388)


def luz(superficie, centro, raio, cor):
    brilho = pygame.Surface((raio*2, raio*2), pygame.SRCALPHA)
    for circulo in range(raio, 0, -4):
        opacidade = round(cor[3]*(1-circulo/raio)**1.5)
        pygame.draw.circle(brilho, (*cor[:3], opacidade), (raio, raio), circulo)
    superficie.blit(brilho, (centro[0]-raio, centro[1]-raio))


class EditorIntroducao:
    CODIGO = ('class Aluno:', '    def __init__(self, nome):', '        self.nome = nome',
              '        self.presente = False', '', 'turma = []', 'turma.append(Aluno("Caicó"))')
    ANOMALIA = ('// IFVania :: anomalia', 'mundo = reconstruir("A28")', 'luva = importar(sensores, atuadores)',
                'preensao -> potencia_de_impacto', 'estrutura -> defesa_virtual',
                'turma -> avatares; bugs -> hostis', 'vincular(autor, luva, mundo)')

    def __init__(self):
        self.fonte = pygame.font.SysFont('monospace', 18)
        self.painel = pygame.Surface((538, 270))
        self.moldura = self.painel.get_rect(topleft=(35, 70))
        self.linhas = [self.fonte.render(linha, True, (166, 224, 204)) for linha in self.CODIGO]
        self.alteracoes = [self.fonte.render(linha, True, (255, 151, 173)) for linha in self.ANOMALIA]
        self.numeros = [self.fonte.render(f'{numero:02}', True, (128, 146, 173)) for numero in range(1, 8)]
        self.titulo = self.fonte.render('OFICINA DE CÓDIGO   /   chamada.py', True, (224, 230, 234))
        self.estados = {}

    def desenhar(self, fundo, quantidade, alteradas, estado, tempo, ampliar=True, lateral=False):
        painel = self.painel
        painel.fill((15, 22, 33))
        pygame.draw.rect(painel, (34, 47, 63), (0, 0, 538, 39))
        painel.blit(self.titulo, (18, 9))
        pygame.draw.rect(painel, (22, 34, 49), (0, 40, 47, 194))
        for indice in range(quantidade):
            corrompida = indice < alteradas
            y = 48+25*indice
            if corrompida:
                pygame.draw.rect(painel, (53, 29, 51), (47, y, 476, 24))
            painel.blit(self.numeros[indice], (12, y+1))
            painel.blit((self.alteracoes if corrompida else self.linhas)[indice], (63, y+1))
        if int(tempo*3) % 2:
            pygame.draw.rect(painel, (189, 228, 219), (63, 226, 11, 2))
        pygame.draw.rect(painel, (33, 48, 61), (0, 238, 538, 32))
        if estado not in self.estados:
            self.estados[estado] = self.fonte.render(estado, True, (244, 199, 153))
        painel.blit(self.estados[estado], (18, 243))
        fundo.blit(pygame.transform.smoothscale(painel, MONITOR.size), MONITOR)
        if ampliar:
            imagem = pygame.transform.smoothscale(painel, (378, 190)) if lateral else painel
            moldura = imagem.get_rect(topright=(932, 36)) if lateral else self.moldura
            pygame.draw.rect(fundo, (13, 21, 28), moldura.move(4, 5).inflate(8, 8), border_radius=5)
            inicio = moldura.midbottom if lateral else moldura.midright
            fim = MONITOR.midtop if lateral else MONITOR.midleft
            pygame.draw.line(fundo, (118, 172, 179), inicio, fim, 1)
            pygame.draw.rect(fundo, (113, 150, 157), moldura.inflate(6, 6), border_radius=4)
            fundo.blit(imagem, moldura)


def fragmentar(fundo, tempo, intensidade, alvo):
    gerador = random.Random(int(tempo*14))
    largura, altura = fundo.get_size()
    copia = fundo.copy()
    for _ in range(round(15*intensidade)):
        y = gerador.randrange(altura-16)
        h = gerador.randrange(2, 16)
        fundo.blit(copia, (gerador.randrange(-48, 49), y), (0, y, largura, h))
    centro = pygame.Vector2(alvo)
    for indice in range(round(110*intensidade)):
        angulo = indice*2.399 + tempo*0.65
        distancia = (1-(tempo*0.54+indice*0.067) % 1)*530
        posicao = centro + pygame.Vector2(math.cos(angulo)*distancia, math.sin(angulo)*distancia*0.55)
        tamanho = 3+indice % 7
        cor = ((127, 253, 226), (86, 153, 221), (237, 124, 185))[indice % 3]
        pygame.draw.rect(fundo, cor, (*posicao, tamanho, 2+indice % 4))
