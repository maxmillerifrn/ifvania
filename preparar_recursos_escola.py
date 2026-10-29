"""Exporta Max e Romerito do atlas de professores para o corpo comum."""
import pygame
import configuracoes
from preparar_figuras_personagens import extract_figures, export_frames


def principal():
    pygame.init()
    pygame.display.set_mode((1, 1))
    try:
        figuras = extract_figures('professores.png', 2, 2)
        # A geração veio voltada à direita; os professores olham para o aluno.
        figuras = [pygame.transform.flip(quadro, True, False) for quadro in figuras]
        export_frames(figuras, 'professores', ['max_0.png', 'max_1.png',
                                      'romerito_0.png', 'romerito_1.png'],
                      configuracoes.TAMANHO_PERSONAGEM)
    finally:
        pygame.quit()


if __name__ == '__main__':
    principal()
