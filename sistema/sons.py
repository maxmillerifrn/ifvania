"""Sinais curtos sintetizados localmente; o jogo também funciona sem dispositivo de áudio."""
from array import array
import math
import pygame

_cache = {}
_ambientes = {}
_mudo = False
_pausado = False
_ambiente_atual = None


def definir_ambiente(identificador):
    global _ambiente_atual
    formato = pygame.mixer.get_init()
    if not formato or formato[1] != -16:
        return
    pygame.mixer.set_reserved(1)
    canal = pygame.mixer.Channel(0)
    if _ambiente_atual == identificador and canal.get_busy():
        return
    frequencias = {'a28': (82, 123), 'biblioteca': (98, 147), 'recreio': (110, 165),
                   'copias': (87, 130), 'rede': (73, 146), 'continuidade': (65, 97),
                   'campus': (130, 195), 'escola': (146, 220)}
    fundamental, harmonia = frequencias.get(identificador, frequencias['escola'])
    chave = (identificador, formato)
    if chave not in _ambientes:
        frequencia, _, canais = formato
        amostras = array('h')
        for indice in range(frequencia*2):
            tempo = indice/frequencia
            envelope = math.sin(math.pi*tempo/2)**2
            valor = round(1400*envelope*(math.sin(math.tau*fundamental*tempo)+0.4*math.sin(math.tau*harmonia*tempo)))
            amostras.extend([valor]*canais)
        _ambientes[chave] = pygame.mixer.Sound(buffer=amostras)
    canal.play(_ambientes[chave], loops=-1, fade_ms=300)
    canal.set_volume(0 if _mudo or _pausado else 0.18)
    _ambiente_atual = identificador


def pausar_ambiente(pausado):
    global _pausado
    _pausado = pausado
    if pygame.mixer.get_init():
        pygame.mixer.Channel(0).set_volume(0 if _mudo or pausado else 0.18)


def alternar_audio():
    global _mudo
    _mudo = not _mudo
    pausar_ambiente(_pausado)
    return not _mudo


def tocar(tipo):
    if _mudo:
        return
    formato = pygame.mixer.get_init()
    if not formato or formato[1] != -16:
        return
    chave = (tipo, formato)
    if chave not in _cache:
        frequencia, _, canais = formato
        duracao = 0.055 if tipo == 'impacto' else 0.16 if tipo == 'quebra' else 0.10
        amostras = array('h')
        for indice in range(round(frequencia*duracao)):
            tempo = indice/frequencia
            tom = (130-65*tempo/duracao) if tipo == 'impacto' else {'carga': 880, 'quebra': 110, 'dano': 180, 'bloqueio': 520}.get(tipo, 440)
            envelope = (1-tempo/duracao)**2
            valor = round(4800*envelope*math.sin(2*math.pi*tom*tempo))
            amostras.extend([valor]*canais)
        _cache[chave] = pygame.mixer.Sound(buffer=amostras)
    _cache[chave].play()
