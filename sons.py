"""Sinais curtos sintetizados localmente; o jogo também funciona sem dispositivo de áudio."""
from array import array
import math
import pygame

_cache = {}


def tocar(tipo):
    formato = pygame.mixer.get_init()
    if not formato or formato[1] != -16:
        return
    chave = (tipo, formato)
    if chave not in _cache:
        frequencia, _, canais = formato
        duracao = 0.055 if tipo == 'impacto' else 0.10
        amostras = array('h')
        for indice in range(round(frequencia*duracao)):
            tempo = indice/frequencia
            tom = (130-65*tempo/duracao) if tipo == 'impacto' else (880 if tipo == 'carga' else 440)
            envelope = (1-tempo/duracao)**2
            valor = round(4800*envelope*math.sin(2*math.pi*tom*tempo))
            amostras.extend([valor]*canais)
        _cache[chave] = pygame.mixer.Sound(buffer=amostras)
    _cache[chave].play()
