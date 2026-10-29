"""Paleta e superfícies compartilhadas da interface escolar sombria."""
import pygame

TINTA = (9, 14, 19)
PAINEL = (15, 23, 30)
ELEVADO = (24, 35, 43)
BORDA = (64, 80, 87)
PAPEL = (226, 224, 211)
ATENUADO = (151, 165, 169)
AMBAR = (198, 166, 105)
CIANO = (111, 181, 187)
PERIGO = (179, 78, 87)


def panel(superficie, retangulo, destaque=None, preenchimento=PAINEL):
    retangulo = pygame.Rect(retangulo)
    sombra = pygame.Surface(retangulo.size, pygame.SRCALPHA)
    sombra.fill((0, 0, 0, 100))
    superficie.blit(sombra, retangulo.move(3, 4))
    pygame.draw.rect(superficie, preenchimento, retangulo)
    pygame.draw.rect(superficie, BORDA, retangulo, 1)
    pygame.draw.line(superficie, (43, 57, 65), (retangulo.left+1, retangulo.top+1),
                     (retangulo.right-2, retangulo.top+1))
    if destaque:
        pygame.draw.rect(superficie, destaque, (retangulo.left, retangulo.top+8, 3, retangulo.height-16))


def text(superficie, fonte, valor, posicao, cor=PAPEL):
    superficie.blit(fonte.render(valor, True, cor), posicao)


def fit_text(fonte, valor, largura):
    """Elide nomes longos sem invadir barras e botões adjacentes."""
    if fonte.size(valor)[0] <= largura:
        return valor
    while valor and fonte.size(valor+'...')[0] > largura:
        valor = valor[:-1]
    return valor+'...'
