"""Exporta as artes aprovadas para os dez PNG usados pelo jogo.

Não desenha personagens: apenas separa as figuras do atlas transparente,
redimensiona sem suavização e alinha os pés. Requer somente Pygame.
Execute novamente após gerar_recursos.py para restaurar esta arte.
"""
from pathlib import Path
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame


RAIZ = Path(__file__).resolve().parent
ORIGENS = RAIZ / 'recursos' / 'fontes_arte'
DESTINO = RAIZ / 'recursos' / 'imagens'


def extract_figures(nome_arquivo, fileiras, colunas):
    """Isola figuras conectadas, sem cortar poses que ultrapassam a grade."""
    atlas = pygame.image.load(str(ORIGENS / nome_arquivo)).convert_alpha()
    componentes = pygame.mask.from_surface(atlas).connected_components(500)
    if len(componentes) != fileiras * colunas:
        raise ValueError(f"{nome_arquivo}: esperadas {fileiras * colunas} figuras; encontradas {len(componentes)}")
    figuras = []
    for componente in componentes:
        limites = componente.get_bounding_rects()[0]
        isolado = atlas.copy()
        silhueta = componente.to_surface(
            setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 0)
        )
        isolado.blit(silhueta, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        fileira = min(fileiras - 1, limites.centery * fileiras // atlas.get_height())
        figuras.append((fileira, limites.centerx, isolado.subsurface(limites).copy()))
    figuras.sort(key=lambda item: (item[0], item[1]))
    return [figura for _, _, figura in figuras]


def export_frames(figuras, pasta, nomes, tamanho):
    # Uma escala compartilhada mantém a proporção entre as poses, inclusive
    # o salto encolhido e o dash mais largo. A física permanece inalterada.
    escala = min(tamanho[0] / max(f.get_width() for f in figuras),
                tamanho[1] / max(f.get_height() for f in figuras))
    destino = DESTINO / pasta
    destino.mkdir(parents=True, exist_ok=True)
    for figura, nome in zip(figuras, nomes):
        redimensionado = pygame.transform.scale(figura, (
            max(1, round(figura.get_width() * escala)),
            max(1, round(figura.get_height() * escala)),
        ))
        quadro = pygame.Surface(tamanho, pygame.SRCALPHA)
        quadro.blit(redimensionado, redimensionado.get_rect(midbottom=(tamanho[0] // 2, tamanho[1])))
        pygame.image.save(quadro, str(destino / nome))
        print(f"exportado: {(destino / nome).relative_to(RAIZ)}")


def principal():
    pygame.init()
    pygame.display.set_mode((1, 1))
    try:
        # Valida ambos os atlas antes de substituir qualquer PNG do jogo.
        aluno = extract_figures("aluno_ifrn_caico.png", fileiras=2, colunas=4)
        bugs = extract_figures("bugs_microbios.png", fileiras=1, colunas=2)
        export_frames(aluno, 'jogador', [
            "repouso_0.png", "repouso_1.png", "caminhada_0.png", "caminhada_1.png",
            "caminhada_2.png", "caminhada_3.png", "salto.png", "arrancada.png",
        ], (26, 40))
        export_frames(bugs, 'inimigos', ["bug_0.png", "bug_1.png"], (26, 24))
    finally:
        pygame.quit()


if __name__ == "__main__":
    principal()
