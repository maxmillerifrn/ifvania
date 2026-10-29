"""Exporta os sprites gerados de RomerBug/SpeedBug e seus projéteis."""
from preparar_figuras_personagens import extract_figures, export_frames
import pygame


def principal():
    pygame.init()
    pygame.display.set_mode((1, 1))
    try:
        formas = extract_figures("romerbug_speedbug.png", fileiras=1, colunas=4)
        projeteis = extract_figures("projeteis_romerbug.png", fileiras=1, colunas=2)
        export_frames(formas, 'chefes', [
            "romerbug_0.png", "romerbug_1.png", "speedbug_0.png", "speedbug_1.png",
        ], (54, 64))
        export_frames(projeteis[:1], 'projeteis', ["aviao_papel.png"], (26, 14))
        export_frames(projeteis[1:], 'projeteis', ["medalha.png"], (18, 22))
    finally:
        pygame.quit()


if __name__ == "__main__":
    principal()
