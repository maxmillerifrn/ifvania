"""Carregamento e cache de imagens (sprites) usadas pelo jogo.

Centralizar o carregamento aqui evita ler o mesmo arquivo do disco várias
vezes e permite trocar a arte do jogo apenas substituindo os arquivos dentro
de assets/images/ - sem precisar mexer no código das classes.

Se uma imagem não existir (ex.: pasta assets/ foi apagada ou o aluno ainda
não desenhou a arte de um personagem), cai automaticamente para um retângulo
colorido "placeholder", para o jogo nunca quebrar por causa de uma imagem
faltando.
"""
import os
import pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "assets", "images")

_cache = {}
_missing_warned = set()


def _placeholder(size, color=(255, 0, 255)):
    surf = pygame.Surface(size, pygame.SRCALPHA)
    surf.fill((*color, 180))
    pygame.draw.rect(surf, (255, 255, 255), surf.get_rect(), 2)
    return surf


def load_image(relative_path, size=None, fallback_color=(255, 0, 255)):
    """Carrega (com cache) uma imagem de assets/images/<relative_path>.

    `size` (largura, altura) opcional redimensiona a imagem com suavização.
    Se o arquivo não existir, devolve um retângulo magenta de aviso, para o
    jogo continuar rodando mesmo com arte incompleta.
    """
    key = (relative_path, size)
    if key in _cache:
        return _cache[key]

    full_path = os.path.join(IMAGES_DIR, relative_path)
    if not os.path.isfile(full_path):
        if relative_path not in _missing_warned:
            print(f"[assets] aviso: imagem não encontrada -> {relative_path} (usando placeholder)")
            _missing_warned.add(relative_path)
        image = _placeholder(size or (32, 32), fallback_color)
    else:
        image = pygame.image.load(full_path).convert_alpha()
        if size is not None and image.get_size() != size:
            image = pygame.transform.smoothscale(image, size)

    _cache[key] = image
    return image


def load_flipped(relative_path, size=None, fallback_color=(255, 0, 255)):
    """Igual a load_image, mas devolve a versão espelhada horizontalmente
    (útil para o personagem/inimigo virar para a esquerda)."""
    key = (relative_path, size, "flipped")
    if key in _cache:
        return _cache[key]
    base = load_image(relative_path, size, fallback_color)
    flipped = pygame.transform.flip(base, True, False)
    _cache[key] = flipped
    return flipped


def clear_cache():
    _cache.clear()


def load_character_frames(paths, fallback_color=(255, 0, 255)):
    """Normaliza uma sequência inteira, preservando proporções e escala.

    Remove margens externas comuns, usa uma única escala entre poses e
    alinha os pés. O mesmo grupo deve incluir todos os estados/formas que
    compartilham o corpo, para não variar o tamanho durante a animação.
    """
    import settings

    paths = tuple(paths)
    size = settings.CHARACTER_SIZE
    key = ("character_frames", paths, size, fallback_color)
    if key in _cache:
        return _cache[key]
    originals = [load_image(path, fallback_color=fallback_color) for path in paths]
    bounds = [frame.get_bounding_rect() for frame in originals]
    width = max((rect.width for rect in bounds), default=1) or 1
    height = max((rect.height for rect in bounds), default=1) or 1
    scale = min(size[0] / width, size[1] / height)
    frames = []
    for original, rect in zip(originals, bounds):
        frame = pygame.Surface(size, pygame.SRCALPHA)
        if rect.width and rect.height:
            cropped = original.subsurface(rect)
            scaled = pygame.transform.scale(cropped, (
                max(1, round(rect.width * scale)),
                max(1, round(rect.height * scale)),
            ))
            frame.blit(scaled, scaled.get_rect(midbottom=(size[0] // 2, size[1])))
        frames.append(frame)
    _cache[key] = frames
    return frames
