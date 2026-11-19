"""Normaliza atlas de poses em quadros de 80 px, mantendo pés e escala comum."""
from pathlib import Path
import argparse
import pygame

RAIZ = Path(__file__).resolve().parents[1]


def exportar(destino):
    pasta = Path(destino)/'equipamentos/personagens'
    for personagem in ('menino', 'menina'):
        origem = 'menina_recorte' if personagem == 'menina' else personagem
        atlas = pygame.image.load(str(RAIZ/f'recursos/fontes_arte/equipamento_personagens/{origem}.png'))
        if atlas.get_size() != (1536,1024):
            raise ValueError('O atlas deve ter 6 x 4 células de 256 px')
        figuras = []
        for linha in range(4):
            for coluna in range(6):
                quadro = atlas.subsurface((coluna*256, linha*256, 256, 256)).copy()
                mascara = pygame.mask.from_surface(quadro, 200)
                # O atlas tem névoa de alpha baixo no fundo; só a figura opaca é exportada.
                silhueta = mascara.to_surface(setcolor=(255,255,255,255), unsetcolor=(0,0,0,0))
                quadro.blit(silhueta, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
                limites = quadro.get_bounding_rect(min_alpha=200)
                if not limites.width:
                    raise ValueError(f'Pose vazia: {personagem}/{linha}/{coluna}')
                figuras.append(quadro.subsurface(limites).copy())
        escala = min(78/max(f.get_height() for f in figuras), 78/max(f.get_width() for f in figuras))
        saida = pasta/personagem
        saida.mkdir(parents=True, exist_ok=True)
        for indice, figura in enumerate(figuras):
            imagem = pygame.transform.smoothscale(figura,(round(figura.get_width()*escala),round(figura.get_height()*escala)))
            quadro = pygame.Surface((80,80),pygame.SRCALPHA)
            quadro.blit(imagem,imagem.get_rect(midbottom=(40,80)))
            pygame.image.save(quadro,str(saida/f'pose_{indice:02}.png'))
    mochila = pygame.image.load(str(RAIZ/'recursos/fontes_arte/equipamento_personagens/mochila.png'))
    mochila = mochila.subsurface(mochila.get_bounding_rect(min_alpha=100))
    imagem = pygame.transform.smoothscale(mochila,(round(mochila.get_width()*64/mochila.get_height()),64))
    pygame.image.save(imagem,str(pasta/'mochila.png'))


if __name__ == '__main__':
    argumentos = argparse.ArgumentParser()
    argumentos.add_argument('--destino',default=str(RAIZ/'recursos/imagens'))
    exportar(argumentos.parse_args().destino)
