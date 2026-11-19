"""Variações visuais independentes da física e do atlas histórico."""
import pygame
from sistema import recursos


def pose_equipamento(personagem, indice, esquerda=False):
    pasta = 'menina' if personagem == 'menina' else 'menino'
    caminho = f'equipamentos/personagens/{pasta}/pose_{indice:02}.png'
    return recursos.load_flipped(caminho) if esquerda else recursos.load_image(caminho)


def figura_com_luva(jogador):
    estado = jogador.estado_animacao
    if estado == 'attack':
        indice = 13+jogador.chicote.pose(jogador)
        esquerda = jogador.chicote.direcao_olhar < 0
    else:
        esquerda = jogador.direcao_olhar < 0
        if estado in ('walk', 'block') and jogador.deslocamento_x > .01 and jogador.no_chao:
            indice = 18+int(jogador.distancia_caminhada/8) % 6
        elif estado in ('dash', 'dodge'):
            indice = 17
        elif estado == 'jump' or not jogador.no_chao:
            indice = 16
        elif estado in ('charge', 'block'):
            indice = 13
        else:
            indice = 12
    imagem = pose_equipamento(jogador.personagem, indice, esquerda)
    tamanho = round(jogador.altura*jogador.ESCALA_VISUAL)
    return imagem if tamanho == 80 else pygame.transform.smoothscale(imagem,(tamanho,tamanho))
