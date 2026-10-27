"""Exporta a nova arte escolar em resolução nativa, sem esticar os módulos."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
import pygame
from prepare_character_sprites import SOURCES, OUTPUT


def main():
    pygame.init()
    pygame.display.set_mode((1, 1))
    try:
        target = OUTPUT/'background'
        target.mkdir(parents=True, exist_ok=True)
        for name in ('lab_detailed.png', 'corridor_detailed.png'):
            image = pygame.image.load(str(SOURCES/name)).convert()
            pygame.image.save(pygame.transform.scale(image, (960, 540)), str(target/name))
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()
