"""Exporta os ciclos de locomoção do chefe e as poses do mouse-chicote."""
from preparar_figuras_personagens import extract_figures, export_frames
import pygame


def principal():
    pygame.init()
    pygame.display.set_mode((1, 1))
    try:
        movimento = extract_figures("movimento_chefe.png", 2, 6)
        ataque = extract_figures("aluno_chicote.png", 1, 3)
        export_frames(movimento, 'chefes', [
            *[f"romerbug_caminhada_{i}.png" for i in range(6)],
            *[f"speedbug_corrida_{i}.png" for i in range(6)],
        ], (54, 64))
        # O braço estendido ultrapassa o corpo, sem aumentar sua colisão.
        export_frames(ataque, 'jogador', [f"ataque_{i}.png" for i in range(3)], (36, 40))
    finally:
        pygame.quit()


if __name__ == "__main__":
    principal()
