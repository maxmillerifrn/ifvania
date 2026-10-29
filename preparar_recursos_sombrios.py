"""Prepara artes noturnas e poses da transição sem sobrescrever fontes antigas."""
import pygame
import configuracoes
from preparar_figuras_personagens import ORIGENS, DESTINO, extract_figures, export_frames


def principal():
    pygame.init()
    pygame.display.set_mode((1, 1))
    try:
        figuras = extract_figures('transicao_chefe.png', 2, 3)
        entidade = pygame.image.load(str(ORIGENS/'entidade_chefe.png')).convert_alpha()
        entidade = entidade.subsurface(entidade.get_bounding_rect()).copy()
        export_frames(figuras, 'chefes/transicao', [f'pose_{i}.png' for i in range(6)], configuracoes.TAMANHO_PERSONAGEM)
        export_frames([entidade], 'chefes/transicao', ['entidade.png'], configuracoes.TAMANHO_PERSONAGEM)
        for origem, alvo, tamanho in (
                ('escola_noturna.png', 'menu/escola_noturna.png', (480, 270)),
                ('laboratorio_sombrio.png', 'cenarios/laboratorio_sombrio.png', (896, 272))):
            imagem = pygame.image.load(str(ORIGENS/origem)).convert()
            destino = DESTINO/alvo
            destino.parent.mkdir(parents=True, exist_ok=True)
            pygame.image.save(pygame.transform.scale(imagem, tamanho), str(destino))
    finally:
        pygame.quit()


if __name__ == '__main__':
    principal()
