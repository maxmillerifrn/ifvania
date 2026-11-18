"""Prepara o panorama do corredor mantendo a borda do passeio no piso lógico."""
import argparse
from pathlib import Path
import pygame


def exportar(destino):
    raiz = Path(__file__).resolve().parents[1]
    original = pygame.image.load(str(raiz/'recursos/fontes_arte/corredor_biblioteca/panorama.png'))
    panorama = pygame.transform.smoothscale(original,(1920,510))
    quadro = pygame.Surface((1920,540),pygame.SRCALPHA)
    quadro.blit(panorama,(0,0))
    quadro.blit(pygame.transform.scale(panorama.subsurface((0,509,1920,1)),(1920,30)),(0,510))
    pasta = Path(destino)/'cenarios'
    pasta.mkdir(parents=True,exist_ok=True)
    pygame.image.save(quadro,str(pasta/'corredor_biblioteca.png'))


if __name__ == '__main__':
    argumentos = argparse.ArgumentParser()
    argumentos.add_argument('--destino',default=str(Path(__file__).resolve().parents[1]/'recursos/imagens'))
    exportar(argumentos.parse_args().destino)
