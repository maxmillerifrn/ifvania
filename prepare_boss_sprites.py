"""Exporta os sprites gerados de RomerBug/SpeedBug e seus projéteis."""
from prepare_character_sprites import extract_figures, export_frames
import pygame


def main():
    pygame.init()
    pygame.display.set_mode((1, 1))
    try:
        forms = extract_figures("romerbug_speedbug.png", rows=1, columns=4)
        projectiles = extract_figures("romerbug_projectiles.png", rows=1, columns=2)
        export_frames(forms, "bosses", [
            "romerbug_0.png", "romerbug_1.png", "speedbug_0.png", "speedbug_1.png",
        ], (54, 64))
        export_frames(projectiles[:1], "projectiles", ["paper_plane.png"], (26, 14))
        export_frames(projectiles[1:], "projectiles", ["medal.png"], (18, 22))
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
