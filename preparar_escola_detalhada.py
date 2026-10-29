"""Exporta a nova arte escolar em resolução nativa, sem esticar os módulos."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
import pygame
from preparar_figuras_personagens import ORIGENS, DESTINO


def principal():
    pygame.init()
    pygame.display.set_mode((1, 1))
    try:
        alvo = DESTINO/'cenarios'
        alvo.mkdir(parents=True, exist_ok=True)
        for nome in ('laboratorio_detalhado.png', 'corredor_detalhado.png'):
            imagem = pygame.image.load(str(ORIGENS/nome)).convert()
            pygame.image.save(pygame.transform.scale(imagem, (960, 540)), str(alvo/nome))
    finally:
        pygame.quit()


if __name__ == '__main__':
    principal()
