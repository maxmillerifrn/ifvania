"""Entrada de desenvolvimento para o novo chefe e capturas sem tocar no save real."""
import argparse
from pathlib import Path
import pygame
from sistema.jogo import Jogo, ESTADO_JOGANDO
from ferramentas.experimentar_campus import preparar


def preparar_mente(jogo):
    preparar(jogo,1)
    fase = jogo.fase
    fase.biblioteca.consultados = {0,1,2}
    fase.biblioteca.modulo_obtido = True
    if fase.biblioteca.portao in fase.mapa_blocos.solidos: fase.mapa_blocos.solidos.remove(fase.biblioteca.portao)
    fase.dialogo_exibido = True
    fase.inimigos.empty()
    fase.chefe.activate()
    jogo.jogador.rect.midbottom = (fase.chefe.rect.centerx-100,fase.chefe.rect.bottom)
    jogo.jogador.posicao.update(jogo.jogador.rect.topleft)
    fase.camera.update(jogo.jogador.rect)
    jogo.maquina_estados.estado = ESTADO_JOGANDO


def capturar(jogo,destino):
    destino = Path(destino)
    destino.mkdir(parents=True,exist_ok=True)
    for ciclo,nome in enumerate(('soco','chute','barrigada','raio')):
        preparar_mente(jogo)
        chefe = jogo.fase.chefe
        chefe.ciclo_combate = ciclo
        chefe.preparar_ataque(jogo.jogador)
        for _ in range(30): chefe.update(jogo.jogador,jogo.fase.mapa_blocos.solidos)
        jogo._draw()
        pygame.image.save(jogo.tela,str(destino/f'mente_{nome}.png'))
    for transformado in (False,True):
        preparar(jogo,0)
        fase = jogo.fase
        fase.infectado = fase.dialogo_exibido = True
        fase.inimigos.empty()
        chefe = fase.chefe
        chefe.activate()
        if transformado:
            chefe.take_damage(8)
            chefe.finish_cinematic()
        jogo.jogador.rect.midbottom = (chefe.rect.centerx-110,chefe.rect.bottom)
        jogo.jogador.posicao.update(jogo.jogador.rect.topleft)
        fase.camera.update(jogo.jogador.rect)
        chefe.ciclo_combate = 1
        chefe.preparar_ataque(jogo.jogador)
        for _ in range(20 if transformado else 28): chefe.update(jogo.jogador,fase.mapa_blocos.solidos)
        jogo._draw()
        pygame.image.save(jogo.tela,str(destino/('speedbug_corrida_sombrio.png' if transformado else 'romerbug_terno_sombrio.png')))
    pygame.quit()


if __name__ == '__main__':
    argumentos = argparse.ArgumentParser()
    argumentos.add_argument('--capturas')
    opcoes = argumentos.parse_args()
    jogo = Jogo()
    if opcoes.capturas:
        capturar(jogo,opcoes.capturas)
    else:
        preparar_mente(jogo)
        jogo.run()
