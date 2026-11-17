"""Extrai as quatro poses de cada avatar sem recortar poses pela grade."""
import argparse
from pathlib import Path
import pygame


def exportar(destino):
    raiz = Path(__file__).resolve().parents[1]
    atlas = pygame.image.load(str(raiz/'recursos/fontes_arte/guardioes_campus/poses_combate.png'))
    grupos = {(fileira, coluna): [] for fileira in range(4) for coluna in range(4)}
    for componente in pygame.mask.from_surface(atlas).connected_components(200):
        limites = componente.get_bounding_rects()[0]
        chave = (min(3, limites.centery*4//atlas.get_height()), min(3, limites.centerx*4//atlas.get_width()))
        grupos[chave].append((componente, limites))
    nomes = ('elias', 'max', 'alessandro', 'francisco')
    for fileira, nome in enumerate(nomes):
        figuras = []
        for coluna in range(4):
            partes = grupos[fileira, coluna]
            if not partes:
                raise ValueError(f'Pose ausente: {nome}/{coluna}')
            limites = partes[0][1].unionall([parte[1] for parte in partes])
            mascara = pygame.Mask(atlas.get_size())
            for componente, _ in partes:
                mascara.draw(componente, (0, 0))
            figura = atlas.subsurface(limites).copy()
            silhueta = mascara.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 0))
            figura.blit(silhueta, (-limites.x, -limites.y), special_flags=pygame.BLEND_RGBA_MULT)
            figuras.append(figura)
        for tamanho, prefixo in ((40, ''), (80, 'apresentacao/')):
            pasta = Path(destino)/(prefixo+'chefes/poses_'+nome)
            pasta.mkdir(parents=True, exist_ok=True)
            escala = min(tamanho/max(figura.get_width() for figura in figuras), tamanho/max(figura.get_height() for figura in figuras))
            for indice, figura in enumerate(figuras):
                imagem = pygame.transform.smoothscale(figura, (max(1, round(figura.get_width()*escala)), max(1, round(figura.get_height()*escala))))
                quadro = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
                quadro.blit(imagem, imagem.get_rect(midbottom=(tamanho//2, tamanho)))
                pygame.image.save(quadro, str(pasta/f'pose_{indice}.png'))


if __name__ == '__main__':
    argumentos = argparse.ArgumentParser()
    argumentos.add_argument('--destino', default=str(Path(__file__).resolve().parents[1]/'recursos/imagens'))
    exportar(argumentos.parse_args().destino)
