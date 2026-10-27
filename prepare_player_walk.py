"""Exporta ciclos de oito quadros, preservando as caminhadas anteriores."""
import pygame
import settings
from prepare_character_sprites import extract_figures, export_frames


def main():
    pygame.init()
    pygame.display.set_mode((1, 1))
    try:
        figures = extract_figures('player_walk_cycle.png', 2, 8)
        for row, folder in enumerate(('player/walk_cycle', 'player/girl/walk_cycle')):
            export_frames(figures[row*8:row*8+8], folder,
                          [f'walk_{i}.png' for i in range(8)], settings.CHARACTER_SIZE)
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()
