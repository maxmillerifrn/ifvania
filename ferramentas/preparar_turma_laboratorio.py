"""Exporta a fonte HD da turma sem sobrescrever artes anteriores."""
import argparse
from pathlib import Path
import pygame


def exportar(destino):
    raiz = Path(__file__).resolve().parents[1]
    fonte = pygame.image.load(str(raiz/'recursos/fontes_arte/turma_laboratorio/turma_costas.png'))
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    for indice, nome in enumerate(('aluno', 'aluna')):
        metade = fonte.subsurface((indice*fonte.get_width()//2, 0, fonte.get_width()//2, fonte.get_height()))
        limites = metade.get_bounding_rect(min_alpha=16)
        recorte = metade.subsurface(limites)
        escala = min(128/recorte.get_width(), 168/recorte.get_height())
        quadro = pygame.Surface((128, 168), pygame.SRCALPHA)
        imagem = pygame.transform.smoothscale(recorte, (round(recorte.get_width()*escala), round(recorte.get_height()*escala)))
        quadro.blit(imagem, imagem.get_rect(midbottom=(64, 168)))
        pygame.image.save(quadro, str(destino/f'{nome}_costas.png'))


if __name__ == '__main__':
    argumentos = argparse.ArgumentParser()
    argumentos.add_argument('--destino', default=str(Path(__file__).resolve().parents[1]/'recursos/imagens/cenarios/turma'))
    exportar(argumentos.parse_args().destino)
