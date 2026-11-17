"""Intenções de entrada; nunca retém eventos brutos ou executa ações ao desenhar."""
from dataclasses import dataclass
import pygame


@dataclass(frozen=True)
class Comando:
    acao: str
    pressionado: bool
    origem: tuple


def interpretar(evento):
    if getattr(evento, 'repeat', False):
        return None
    if evento.type in (pygame.KEYDOWN, pygame.KEYUP):
        acoes = {pygame.K_x: 'ataque', pygame.K_k: 'ataque', pygame.K_LSHIFT: 'esquiva', pygame.K_q: 'bloquear',
                 pygame.K_e: 'interagir', pygame.K_SPACE: 'salto', pygame.K_w: 'salto', pygame.K_UP: 'salto'}
        acao = acoes.get(evento.key)
        if acao:
            return Comando(acao, evento.type == pygame.KEYDOWN, ('tecla', evento.key))
    if evento.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP) and evento.button == 1:
        return Comando('ataque', evento.type == pygame.MOUSEBUTTONDOWN, ('mouse', 1))
    return None


def houve_interacao(eventos):
    return any(comando is not None and comando.pressionado and comando.acao == 'interagir'
               for comando in (interpretar(evento) for evento in eventos))
