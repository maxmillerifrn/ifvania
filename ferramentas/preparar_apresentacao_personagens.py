"""Exporta arte em 80 px direto das fontes; mantém sprites lógicos anteriores."""
import argparse
from pathlib import Path
import pygame
from ferramentas.preparar_figuras_personagens import extract_figures


def salvar(figuras, pasta, nomes, destino):
    escala = min(80/max(figura.get_width() for figura in figuras), 80/max(figura.get_height() for figura in figuras))
    pasta = Path(destino)/pasta
    pasta.mkdir(parents=True, exist_ok=True)
    for figura, nome in zip(figuras, nomes):
        quadro = pygame.Surface((80, 80), pygame.SRCALPHA)
        imagem = pygame.transform.smoothscale(figura, (round(figura.get_width()*escala), round(figura.get_height()*escala)))
        quadro.blit(imagem, imagem.get_rect(midbottom=(40, 80)))
        pygame.image.save(quadro, str(pasta/nome))


def exportar(destino):
    pygame.init()
    pygame.display.set_mode((1, 1))
    try:
        nomes = ['repouso_0.png', 'repouso_1.png', *[f'caminhada_{i}.png' for i in range(4)], 'salto.png', 'arrancada.png']
        salvar(extract_figures('aluno_ifrn_caico.png', 2, 4), 'jogador', nomes, destino)
        aluna = extract_figures('aluna.png', 3, 4)
        salvar(aluna[:8], 'jogador/menina', nomes, destino)
        salvar(aluna[8:11], 'jogador/menina', [f'ataque_{i}.png' for i in range(3)], destino)
        salvar(extract_figures('aluno_chicote.png', 1, 3), 'jogador', [f'ataque_{i}.png' for i in range(3)], destino)
        for fonte, subpasta in (('ciclo_caminhada_jogador.png', 'ciclo_caminhada'), ('caminhada_carregando.png', 'caminhada_carregando')):
            figuras = extract_figures(fonte, 2, 8)
            for indice, pasta in enumerate(('jogador', 'jogador/menina')):
                salvar(figuras[indice*8:indice*8+8], pasta+'/'+subpasta, [f'caminhada_{i}.png' for i in range(8)], destino)
        professores = extract_figures('professores.png', 2, 2)
        professores = [pygame.transform.flip(figura, True, False) for figura in professores]
        salvar(professores, 'professores', ['max_0.png', 'max_1.png', 'romerito_0.png', 'romerito_1.png'], destino)
    finally:
        pygame.quit()


if __name__ == '__main__':
    argumentos = argparse.ArgumentParser()
    argumentos.add_argument('--destino', default=str(Path(__file__).resolve().parents[1]/'recursos/imagens/apresentacao'))
    exportar(argumentos.parse_args().destino)
