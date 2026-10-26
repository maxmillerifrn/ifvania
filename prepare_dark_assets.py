"""Prepara artes noturnas e poses da transição sem sobrescrever fontes antigas."""
import pygame
import settings
from prepare_character_sprites import SOURCES, OUTPUT, extract_figures, export_frames


def main():
    pygame.init()
    pygame.display.set_mode((1, 1))
    try:
        figures = extract_figures('boss_transition.png', 2, 3)
        entity = pygame.image.load(str(SOURCES/'boss_entity.png')).convert_alpha()
        entity = entity.subsurface(entity.get_bounding_rect()).copy()
        export_frames(figures, 'bosses/transition', [f'pose_{i}.png' for i in range(6)], settings.CHARACTER_SIZE)
        export_frames([entity], 'bosses/transition', ['entity.png'], settings.CHARACTER_SIZE)
        for source, target, size in (
                ('school_night.png', 'menu/school_night.png', (480, 270)),
                ('dark_lab.png', 'background/dark_lab.png', (896, 272))):
            image = pygame.image.load(str(SOURCES/source)).convert()
            dest = OUTPUT/target
            dest.parent.mkdir(parents=True, exist_ok=True)
            pygame.image.save(pygame.transform.scale(image, size), str(dest))
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()
