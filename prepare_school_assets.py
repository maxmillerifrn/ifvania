"""Exporta Max e Romerito do atlas de professores para o corpo comum."""
import pygame
import settings
from prepare_character_sprites import extract_figures, export_frames


def main():
    pygame.init()
    pygame.display.set_mode((1, 1))
    try:
        figures = extract_figures('teachers.png', 2, 2)
        # A geração veio voltada à direita; os professores olham para o aluno.
        figures = [pygame.transform.flip(frame, True, False) for frame in figures]
        export_frames(figures, 'npcs', ['max_0.png', 'max_1.png',
                                      'romerito_0.png', 'romerito_1.png'],
                      settings.CHARACTER_SIZE)
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()
