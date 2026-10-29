"""Converte um mapa em ASCII (lista de strings) em geometria de colisão e spawns.

Legenda dos tiles:
    '.'  vazio
    '#'  bloco sólido (chão / parede / plataforma)
    '^'  espinho (dano ao tocar)
    'P'  ponto de spawn do jogador
    'B'  ponto de spawn do professor-chefe
    'E'  ponto de spawn de um inimigo comum (bug)
    'D'  gatilho de diálogo pré-chefe (zona de trigger, não sólida)
    'X'  saída da fase (zona de trigger, ativa após derrotar o chefe)
"""
import pygame
import configuracoes

TB = configuracoes.TAMANHO_BLOCO


class MapaBlocos:
    def __init__(self, mapa_ascii):
        self.fileiras = mapa_ascii
        self.largura = max(len(r) for r in self.fileiras) * TB
        self.altura = len(self.fileiras) * TB

        self.solidos = []
        self.perigos = []
        self.surgimento_jogador = (64, 64)
        self.surgimento_chefe = None
        self.surgimentos_inimigos = []
        self.gatilho_dialogo = None
        self.gatilho_saida = None

        self._parse()

    def _parse(self):
        for indice_linha, fileira in enumerate(self.fileiras):
            for indice_coluna, caractere in enumerate(fileira):
                x, y = indice_coluna * TB, indice_linha * TB
                retangulo = pygame.Rect(x, y, TB, TB)
                if caractere == '#':
                    self.solidos.append(retangulo)
                elif caractere == '^':
                    self.perigos.append(pygame.Rect(x, y + TB // 2, TB, TB // 2))
                elif caractere == 'P':
                    self.surgimento_jogador = (x, y)
                elif caractere == 'B':
                    self.surgimento_chefe = (x, y)
                elif caractere == 'E':
                    self.surgimentos_inimigos.append((x, y))
                elif caractere == 'D':
                    # Toda a região após a entrada pertence ao encontro,
                    # inclusive plataformas e trajetórias de salto/dash.
                    self.gatilho_dialogo = pygame.Rect(x, 0, self.largura - x, self.altura)
                elif caractere == 'X':
                    self.gatilho_saida = pygame.Rect(x, y, TB, TB * 2)
