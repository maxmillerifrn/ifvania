"""Exporta o novo atlas sem substituir fontes ou sprites aprovados."""
import argparse
from pathlib import Path
import pygame


def exportar(destino):
    fonte = Path(__file__).resolve().parents[1]/'recursos/fontes_arte/bug_humanoide/atlas.png'
    atlas = pygame.image.load(str(fonte))
    for linha, nome in enumerate(('bug_humanoide', 'speedbug_sombrio')):
        figuras = []
        for coluna in range(4):
            celula = pygame.Rect(coluna*atlas.get_width()//4, linha*atlas.get_height()//2,
                                 atlas.get_width()//4, atlas.get_height()//2)
            figura = atlas.subsurface(celula).copy()
            limites = figura.get_bounding_rect(min_alpha=100)
            figuras.append(figura.subsurface(limites).copy())
        for tamanho, prefixo in ((40, ''), (80, 'apresentacao/')):
            pasta = Path(destino)/prefixo/'inimigos'/nome
            pasta.mkdir(parents=True, exist_ok=True)
            escala = min((tamanho-4)/max(f.get_width() for f in figuras), tamanho/max(f.get_height() for f in figuras))
            for indice, figura in enumerate(figuras):
                imagem = pygame.transform.smoothscale(figura, (max(1,round(figura.get_width()*escala)),max(1,round(figura.get_height()*escala))))
                quadro = pygame.Surface((tamanho,tamanho),pygame.SRCALPHA)
                quadro.blit(imagem,imagem.get_rect(midbottom=(tamanho//2,tamanho)))
                pygame.image.save(quadro,str(pasta/f'pose_{indice}.png'))


if __name__ == '__main__':
    argumentos = argparse.ArgumentParser()
    argumentos.add_argument('--destino',default=str(Path(__file__).resolve().parents[1]/'recursos/imagens'))
    exportar(argumentos.parse_args().destino)
