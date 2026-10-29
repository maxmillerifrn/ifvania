"""Carregamento e cache de imagens (sprites) usadas pelo jogo.

Centralizar o carregamento aqui evita ler o mesmo arquivo do disco várias
vezes e permite trocar a arte do jogo apenas substituindo os arquivos dentro
de recursos/imagens/ - sem precisar mexer no código das classes.

Se uma imagem não existir (ex.: pasta recursos/ foi apagada ou o aluno ainda
não desenhou a arte de um personagem), cai automaticamente para um retângulo
colorido "placeholder", para o jogo nunca quebrar por causa de uma imagem
faltando.
"""
import os
import pygame

DIRETORIO_BASE = os.path.dirname(os.path.abspath(__file__))
DIRETORIO_IMAGENS = os.path.join(DIRETORIO_BASE, 'recursos', 'imagens')

_cache = {}
_avisos_ausentes = set()


def _placeholder(tamanho, cor=(255, 0, 255)):
    superficie = pygame.Surface(tamanho, pygame.SRCALPHA)
    superficie.fill((*cor, 180))
    pygame.draw.rect(superficie, (255, 255, 255), superficie.get_rect(), 2)
    return superficie


def load_image(caminho_relativo, tamanho=None, cor_alternativa=(255, 0, 255)):
    """Carrega (com cache) uma imagem de recursos/imagens/<relative_path>.

    `size` (largura, altura) opcional redimensiona a imagem com suavização.
    Se o arquivo não existir, devolve um retângulo magenta de aviso, para o
    jogo continuar rodando mesmo com arte incompleta.
    """
    tecla = (caminho_relativo, tamanho)
    if tecla in _cache:
        return _cache[tecla]

    caminho_completo = os.path.join(DIRETORIO_IMAGENS, caminho_relativo)
    if not os.path.isfile(caminho_completo):
        if caminho_relativo not in _avisos_ausentes:
            print(f"[recursos] aviso: imagem não encontrada -> {caminho_relativo} (usando placeholder)")
            _avisos_ausentes.add(caminho_relativo)
        imagem = _placeholder(tamanho or (32, 32), cor_alternativa)
    else:
        imagem = pygame.image.load(caminho_completo).convert_alpha()
        if tamanho is not None and imagem.get_size() != tamanho:
            imagem = pygame.transform.smoothscale(imagem, tamanho)

    _cache[tecla] = imagem
    return imagem


def load_flipped(caminho_relativo, tamanho=None, cor_alternativa=(255, 0, 255)):
    """Igual a load_image, mas devolve a versão espelhada horizontalmente
    (útil para o personagem/inimigo virar para a esquerda)."""
    tecla = (caminho_relativo, tamanho, "flipped")
    if tecla in _cache:
        return _cache[tecla]
    base = load_image(caminho_relativo, tamanho, cor_alternativa)
    espelhado = pygame.transform.flip(base, True, False)
    _cache[tecla] = espelhado
    return espelhado


def clear_cache():
    _cache.clear()


def load_character_frames(caminhos, cor_alternativa=(255, 0, 255)):
    """Normaliza uma sequência inteira, preservando proporções e escala.

    Remove margens externas comuns, usa uma única escala entre poses e
    alinha os pés. O mesmo grupo deve incluir todos os estados/formas que
    compartilham o corpo, para não variar o tamanho durante a animação.
    """
    import configuracoes

    caminhos = tuple(caminhos)
    tamanho = configuracoes.TAMANHO_PERSONAGEM
    tecla = ("character_frames", caminhos, tamanho, cor_alternativa)
    if tecla in _cache:
        return _cache[tecla]
    originais = [load_image(caminho, cor_alternativa=cor_alternativa) for caminho in caminhos]
    limites = [quadro.get_bounding_rect() for quadro in originais]
    largura = max((retangulo.width for retangulo in limites), default=1) or 1
    altura = max((retangulo.height for retangulo in limites), default=1) or 1
    escala = min(tamanho[0] / largura, tamanho[1] / altura)
    quadros = []
    for original, retangulo in zip(originais, limites):
        quadro = pygame.Surface(tamanho, pygame.SRCALPHA)
        if retangulo.width and retangulo.height:
            recortado = original.subsurface(retangulo)
            redimensionado = pygame.transform.scale(recortado, (
                max(1, round(retangulo.width * escala)),
                max(1, round(retangulo.height * escala)),
            ))
            quadro.blit(redimensionado, redimensionado.get_rect(midbottom=(tamanho[0] // 2, tamanho[1])))
        quadros.append(quadro)
    _cache[tecla] = quadros
    return quadros
