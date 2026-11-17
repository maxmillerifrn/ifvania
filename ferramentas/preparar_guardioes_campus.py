"""Extrai avatares ficcionais; não são retratos dos docentes reais."""
import argparse
from pathlib import Path
import pygame


def exportar(destino):
    raiz = Path(__file__).resolve().parents[1]
    atlas = pygame.image.load(str(raiz/'recursos/fontes_arte/guardioes_campus/avatares.png'))
    figuras = []
    for indice in range(3):
        celula = atlas.subsurface((indice*atlas.get_width()//3, 0, atlas.get_width()//3, atlas.get_height()))
        figuras.append(pygame.transform.flip(celula.subsurface(celula.get_bounding_rect(min_alpha=16)), True, False))
    maximo = pygame.image.load(str(raiz/'recursos/imagens/apresentacao/professores/max_0.png'))
    figuras.append(pygame.transform.flip(maximo, True, False))
    for nome, figura in zip(('elias', 'alessandro', 'francisco', 'max'), figuras):
        if nome != 'max':
            pasta_retratos = Path(destino)/'dialogos'
            pasta_retratos.mkdir(parents=True, exist_ok=True)
            busto = figura.subsurface((0, 0, figura.get_width(), round(figura.get_height()*0.66)))
            escala_retrato = min(680/busto.get_width(), 1080/busto.get_height())
            imagem_retrato = pygame.transform.smoothscale(busto, (round(busto.get_width()*escala_retrato), round(busto.get_height()*escala_retrato)))
            retrato = pygame.Surface((768, 1152), pygame.SRCALPHA)
            retrato.blit(imagem_retrato, imagem_retrato.get_rect(midbottom=(384, 1152)))
            pygame.image.save(retrato, str(pasta_retratos/f'guardiao_{nome}.png'))
        for tamanho, pasta in ((40, Path(destino)/'chefes/guardioes'), (80, Path(destino)/'apresentacao/chefes/guardioes')):
            pasta.mkdir(parents=True, exist_ok=True)
            escala = min(tamanho/figura.get_width(), tamanho/figura.get_height())
            imagem = pygame.transform.smoothscale(figura, (round(figura.get_width()*escala), round(figura.get_height()*escala)))
            quadro = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
            quadro.blit(imagem, imagem.get_rect(midbottom=(tamanho//2, tamanho)))
            pygame.image.save(quadro, str(pasta/f'{nome}.png'))


if __name__ == '__main__':
    argumentos = argparse.ArgumentParser()
    argumentos.add_argument('--destino', default=str(Path(__file__).resolve().parents[1]/'recursos/imagens'))
    exportar(argumentos.parse_args().destino)
