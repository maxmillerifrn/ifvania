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
import settings

TS = settings.TILE_SIZE


class TileMap:
    def __init__(self, ascii_map):
        self.rows = ascii_map
        self.width = max(len(r) for r in self.rows) * TS
        self.height = len(self.rows) * TS

        self.solids = []
        self.hazards = []
        self.player_spawn = (64, 64)
        self.boss_spawn = None
        self.enemy_spawns = []
        self.dialogue_trigger = None
        self.exit_trigger = None

        self._parse()

    def _parse(self):
        for row_i, row in enumerate(self.rows):
            for col_i, ch in enumerate(row):
                x, y = col_i * TS, row_i * TS
                rect = pygame.Rect(x, y, TS, TS)
                if ch == '#':
                    self.solids.append(rect)
                elif ch == '^':
                    self.hazards.append(pygame.Rect(x, y + TS // 2, TS, TS // 2))
                elif ch == 'P':
                    self.player_spawn = (x, y)
                elif ch == 'B':
                    self.boss_spawn = (x, y)
                elif ch == 'E':
                    self.enemy_spawns.append((x, y))
                elif ch == 'D':
                    # Toda a região após a entrada pertence ao encontro,
                    # inclusive plataformas e trajetórias de salto/dash.
                    self.dialogue_trigger = pygame.Rect(x, 0, self.width - x, self.height)
                elif ch == 'X':
                    self.exit_trigger = pygame.Rect(x, y, TS, TS * 2)
