"""Capturas de orientação no corredor e comparação da brisa sem alterar saves."""
import argparse
from pathlib import Path
import pygame
from sistema.jogo import Jogo, ESTADO_JOGANDO
from sistema.eventos_campanha import FaseConcluida, ChefeDerrotado


def capturar(destino):
    destino = Path(destino)
    destino.mkdir(parents=True,exist_ok=True)
    jogo = Jogo()
    jogo._load_level(0,novo_jogador=True)
    jogo.eventos_campanha.emitir(ChefeDerrotado('a28'))
    jogo.eventos_campanha.emitir(FaseConcluida('a28'))
    jogo._load_campus('convivencia','a28')
    jogo.maquina_estados.estado = ESTADO_JOGANDO
    for nome,x in (('saida_a28',180),('corredor',750),('porta_biblioteca',1150)):
        jogo.jogador.rect.topleft = (x,jogo.fase.piso-40)
        jogo.jogador.posicao.update(jogo.jogador.rect.topleft)
        jogo.fase.camera.update(jogo.jogador.rect)
        jogo._draw()
        pygame.image.save(jogo.tela,str(destino/f'{nome}.png'))
    jogo._load_campus('jardim')
    jogo.maquina_estados.estado = ESTADO_JOGANDO
    for instante in (0,35):
        jogo.fase.instantes = instante
        jogo._draw()
        pygame.image.save(jogo.tela,str(destino/f'jardim_vento_{instante}.png'))
    pygame.quit()


if __name__ == '__main__':
    argumentos = argparse.ArgumentParser()
    argumentos.add_argument('--destino',default='avaliacao/corredor_e_vento')
    capturar(argumentos.parse_args().destino)
