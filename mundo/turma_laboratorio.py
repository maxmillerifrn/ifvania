"""Colegas ilustrados em resolução própria, preservando as bancadas e suas colisões."""
import math
import pygame
from sistema import recursos


class TurmaLaboratorio:
    def __init__(self, postos):
        self.postos = postos
        self.figuras = [recursos.load_image(f'cenarios/turma/{nome}_costas.png') for nome in ('aluno', 'aluna')]
        self.quadros = {}

    def draw(self, superficie, camera, instante, hipnose=0):
        for indice, posto in enumerate(self.postos):
            escala = posto.width/70
            hipnotizado = hipnose > indice*0.12
            tamanho = (round(70*escala), round(90*escala))
            chave = (indice % 2, tamanho, hipnotizado)
            if chave not in self.quadros:
                figura = pygame.transform.smoothscale(self.figuras[indice % 2], tamanho)
                if hipnotizado:
                    reflexo = figura.copy()
                    reflexo.fill((135, 191, 187, 255), special_flags=pygame.BLEND_RGBA_MULT)
                    figura = reflexo
                self.quadros[chave] = figura
            figura = self.quadros[chave]
            # Respiração visual discreta e pausa de postura na hipnose.
            respiracao = 0 if hipnotizado else round(math.sin(instante*0.035+indice)*escala)
            destino = figura.get_rect(midtop=(posto.centerx, posto.bottom+round(9*escala)+respiracao))
            superficie.blit(figura, camera.apply(destino))
