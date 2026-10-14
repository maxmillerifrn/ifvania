"""Exporta as artes aprovadas para os dez PNG usados pelo jogo.

Não desenha personagens: apenas separa as figuras do atlas transparente,
redimensiona sem suavização e alinha os pés. Requer somente Pygame.
Execute novamente após generate_assets.py para restaurar esta arte.
"""
from pathlib import Path
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame


ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / "assets" / "art_sources"
OUTPUT = ROOT / "assets" / "images"


def extract_figures(filename, rows, columns):
    """Isola figuras conectadas, sem cortar poses que ultrapassam a grade."""
    atlas = pygame.image.load(str(SOURCES / filename)).convert_alpha()
    components = pygame.mask.from_surface(atlas).connected_components(500)
    if len(components) != rows * columns:
        raise ValueError(f"{filename}: esperadas {rows * columns} figuras; encontradas {len(components)}")
    figures = []
    for component in components:
        bounds = component.get_bounding_rects()[0]
        isolated = atlas.copy()
        silhouette = component.to_surface(
            setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 0)
        )
        isolated.blit(silhouette, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        row = min(rows - 1, bounds.centery * rows // atlas.get_height())
        figures.append((row, bounds.centerx, isolated.subsurface(bounds).copy()))
    figures.sort(key=lambda item: (item[0], item[1]))
    return [figure for _, _, figure in figures]


def export_frames(figures, folder, names, size):
    # Uma escala compartilhada mantém a proporção entre as poses, inclusive
    # o salto encolhido e o dash mais largo. A física permanece inalterada.
    scale = min(size[0] / max(f.get_width() for f in figures),
                size[1] / max(f.get_height() for f in figures))
    destination = OUTPUT / folder
    destination.mkdir(parents=True, exist_ok=True)
    for figure, name in zip(figures, names):
        scaled = pygame.transform.scale(figure, (
            max(1, round(figure.get_width() * scale)),
            max(1, round(figure.get_height() * scale)),
        ))
        frame = pygame.Surface(size, pygame.SRCALPHA)
        frame.blit(scaled, scaled.get_rect(midbottom=(size[0] // 2, size[1])))
        pygame.image.save(frame, str(destination / name))
        print(f"exportado: {(destination / name).relative_to(ROOT)}")


def main():
    pygame.init()
    pygame.display.set_mode((1, 1))
    try:
        # Valida ambos os atlas antes de substituir qualquer PNG do jogo.
        student = extract_figures("student_ifrn_caico.png", rows=2, columns=4)
        bugs = extract_figures("bugs_microbes.png", rows=1, columns=2)
        export_frames(student, "player", [
            "idle_0.png", "idle_1.png", "walk_0.png", "walk_1.png",
            "walk_2.png", "walk_3.png", "jump.png", "dash.png",
        ], (26, 40))
        export_frames(bugs, "enemies", ["bug_0.png", "bug_1.png"], (26, 24))
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
