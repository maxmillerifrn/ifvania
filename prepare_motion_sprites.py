"""Exporta os ciclos de locomoção do chefe e as poses do mouse-chicote."""
from prepare_character_sprites import extract_figures, export_frames
import pygame


def main():
    pygame.init()
    pygame.display.set_mode((1, 1))
    try:
        motion = extract_figures("boss_motion.png", 2, 6)
        attack = extract_figures("student_whip.png", 1, 3)
        export_frames(motion, "bosses", [
            *[f"romerbug_walk_{i}.png" for i in range(6)],
            *[f"speedbug_run_{i}.png" for i in range(6)],
        ], (54, 64))
        # O braço estendido ultrapassa o corpo, sem aumentar sua colisão.
        export_frames(attack, "player", [f"attack_{i}.png" for i in range(3)], (36, 40))
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
