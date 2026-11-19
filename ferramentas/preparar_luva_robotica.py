"""Recorta as três poses da fonte aprovada; preserva alpha e proporções."""
from pathlib import Path
import argparse
import pygame


def exportar(destino):
    raiz = Path(__file__).resolve().parents[1]
    atlas = pygame.image.load(str(raiz/'recursos/fontes_arte/luva_robotica/atlas_texturizado.png'))
    pasta = Path(destino)/'equipamentos/luva_robotica'
    pasta.mkdir(parents=True, exist_ok=True)
    for indice, nome in enumerate(('repouso', 'punho', 'aberta')):
        largura = atlas.get_width()//3
        quadro = atlas.subsurface((indice*largura, 0, largura, atlas.get_height()))
        limites = quadro.get_bounding_rect(min_alpha=32)
        if not limites.width:
            raise ValueError(f'Pose vazia: {nome}')
        figura = quadro.subsurface(limites)
        proporcao = 128/figura.get_width()
        imagem = pygame.transform.smoothscale(figura, (128, round(figura.get_height()*proporcao)))
        pygame.image.save(imagem, str(pasta/f'{nome}.png'))


if __name__ == '__main__':
    argumentos = argparse.ArgumentParser()
    argumentos.add_argument('--destino', default=str(Path(__file__).resolve().parents[1]/'recursos/imagens'))
    exportar(argumentos.parse_args().destino)
