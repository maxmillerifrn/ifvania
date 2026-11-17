"""Impactos transitórios independentes da sobrevivência do alvo."""
import math
import pygame


class EfeitosCombate:
    def __init__(self):
        self.impactos = []

    def adicionar(self, centro, fatal=False):
        self.impactos.append([pygame.Vector2(centro), 18 if fatal else 12, fatal])

    def update(self):
        for impacto in self.impactos:
            impacto[1] -= 1
        self.impactos = [impacto for impacto in self.impactos if impacto[1] > 0]

    def draw(self, superficie, camera):
        for centro, restante, fatal in self.impactos:
            idade = (18 if fatal else 12)-restante
            origem = centro-camera.deslocamento
            for indice in range(8 if fatal else 5):
                angulo = indice*math.tau/(8 if fatal else 5)
                eixo = pygame.Vector2(math.cos(angulo), math.sin(angulo))
                inicio = origem+eixo*(3+idade*1.5)
                fim = inicio+eixo*max(1, restante/2)
                pygame.draw.line(superficie, (255, 211, 123) if fatal else (220, 249, 239), inicio, fim, 2)
