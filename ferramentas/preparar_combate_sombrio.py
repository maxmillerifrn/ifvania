"""Exporta poses de soco, chute e especiais em pastas próprias."""
import argparse
from pathlib import Path
import pygame


def exportar(destino):
    raiz = Path(__file__).resolve().parents[1]
    atlas = pygame.image.load(str(raiz/'recursos/fontes_arte/combate_sombrio/atlas.png'))
    for linha,nome in enumerate(('romerbug_sombrio','speedbug_corredor','mente_brilhante')):
        figuras = []
        for coluna in range(6):
            area = pygame.Rect(coluna*atlas.get_width()//6,linha*atlas.get_height()//3,atlas.get_width()//6,atlas.get_height()//3)
            figura = atlas.subsurface(area).copy()
            mascara = pygame.mask.from_surface(figura,100).to_surface(setcolor=(255,255,255,255),unsetcolor=(0,0,0,0))
            figura.blit(mascara,(0,0),special_flags=pygame.BLEND_RGBA_MULT)
            limites = figura.get_bounding_rect(min_alpha=100)
            if not limites.width: raise ValueError(f'Pose ausente: {nome}/{coluna}')
            figuras.append(figura.subsurface(limites).copy())
        for tamanho,prefixo in ((40,''),(80,'apresentacao/')):
            pasta = Path(destino)/prefixo/'chefes'/nome
            pasta.mkdir(parents=True,exist_ok=True)
            escala = min(tamanho/max(f.get_width() for f in figuras),tamanho/max(f.get_height() for f in figuras))
            for indice,figura in enumerate(figuras):
                imagem = pygame.transform.smoothscale(figura,(max(1,round(figura.get_width()*escala)),max(1,round(figura.get_height()*escala))))
                quadro = pygame.Surface((tamanho,tamanho),pygame.SRCALPHA)
                quadro.blit(imagem,imagem.get_rect(midbottom=(tamanho//2,tamanho)))
                pygame.image.save(quadro,str(pasta/f'pose_{indice}.png'))
        pasta = Path(destino)/'dialogos'
        pasta.mkdir(parents=True,exist_ok=True)
        if nome == 'mente_brilhante':
            original = figuras[0]
            figura = original.subsurface((0,0,original.get_width(),round(original.get_height()*0.60))).copy()
            retrato = pygame.Surface((384,576),pygame.SRCALPHA)
            proporcao = min(384/figura.get_width(),576/figura.get_height())
            imagem = pygame.transform.smoothscale(figura,(round(figura.get_width()*proporcao),round(figura.get_height()*proporcao)))
            retrato.blit(imagem,imagem.get_rect(midbottom=(192,576)))
            pygame.image.save(retrato,str(pasta/'mente_brilhante.png'))


if __name__ == '__main__':
    argumentos = argparse.ArgumentParser()
    argumentos.add_argument('--destino',default=str(Path(__file__).resolve().parents[1]/'recursos/imagens'))
    exportar(argumentos.parse_args().destino)
