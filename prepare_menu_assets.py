"""Prepara a fachada e os onze quadros da Menina sem redesenhar a arte.

Execute após atualizar as fontes em assets/art_sources. Não altera os sprites
existentes do Menino. Extração e exportação usam o pipeline local de Pygame.
"""
import pygame
import settings
from prepare_character_sprites import SOURCES, OUTPUT, extract_figures, export_frames


FRAME_NAMES = [
    "idle_0.png", "idle_1.png",
    "walk_0.png", "walk_1.png", "walk_2.png", "walk_3.png",
    "jump.png", "dash.png", "attack_0.png", "attack_1.png", "attack_2.png",
]


def main():
    pygame.init()
    pygame.display.set_mode((1, 1))
    try:
        # Valida o atlas completo antes de escrever os quadros consumidos.
        figures = extract_figures("student_girl.png", rows=3, columns=4)
        facade = pygame.image.load(str(SOURCES / "school_facade.png")).convert()
        export_frames(figures[:11], "player/girl", FRAME_NAMES, settings.CHARACTER_SIZE)
        destination = OUTPUT / "menu"
        destination.mkdir(parents=True, exist_ok=True)
        # Grade de 480 × 270 ampliada em escala inteira para a janela.
        facade = pygame.transform.scale(facade, (480, 270))
        pygame.image.save(facade, str(destination / "school_facade.png"))
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
