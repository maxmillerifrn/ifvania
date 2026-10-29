"""Gera as imagens (pixel art) usadas pelo jogo, em recursos/imagens/.

Este script NÃO é necessário para jogar - as imagens já ficam prontas na pasta
recursos/. Ele existe para que professores/alunos entendam como as imagens foram
feitas e possam regenerá-las ou usá-lo como base para desenhar as próprias artes
e substituir os arquivos em recursos/imagens/.

Estilo: pixel art de baixa resolução (sem suavização), no espírito de
personagens de Castlevania/Metroid - silhueta com contorno escuro, poucas
cores por material e sombreamento em blocos sólidos (sem gradiente).

O(a) aluno(a) protagonista veste farda do IFRN (camisa polo verde institucional,
calça e mochila) e tem quadros de animação separados para parado(a), andando
(4 quadros), pulando e dando dash - a virada para a esquerda é feita em tempo
de execução por recursos.py (espelhamento), então só desenhamos virado(a) para a
direita aqui.

Requer Pillow:  pip install pillow
Executar:        python gerar_recursos.py
"""
import os
import random
from PIL import Image, ImageDraw

BASE = "recursos/imagens"

for subtitulo in ('jogador', 'inimigos', 'chefes', 'blocos', 'cenarios', 'interface'):
    os.makedirs(f"{BASE}/{subtitulo}", exist_ok=True)


def canvas(largura, altura):
    return Image.new("RGBA", (largura, altura), (0, 0, 0, 0))


def save(imagem, caminho):
    imagem.save(caminho)
    print("gerado:", caminho)


def darken(cor, fator=0.6):
    r, g, b, a = cor
    return (int(r * fator), int(g * fator), int(b * fator), a)


# ----------------------------------------------------------------------
# Paleta - poucas cores por material, como em sprites 16/32-bit
# ----------------------------------------------------------------------
CONTORNO = (16, 14, 22, 255)
PELE = (222, 170, 133, 255)
SOMBRA_PELE = (181, 128, 96, 255)
CABELO = (43, 28, 22, 255)
UNIFORME = (36, 112, 76, 255)        # verde institucional do IFRN
SOMBRA_UNIFORME = (22, 80, 54, 255)
GOLA = (232, 232, 224, 255)
REMENDO = (238, 238, 230, 255)
CALCA = (46, 46, 60, 255)
SAPATO = (26, 24, 32, 255)
MOCHILA = (196, 132, 34, 255)
SOMBRA_MOCHILA = (150, 96, 22, 255)
BRANCO = (245, 245, 245, 255)
PRETO = (12, 12, 12, 255)


# ----------------------------------------------------------------------
# Aluno(a) - personagem principal (26x40), virado(a) para a direita
# ----------------------------------------------------------------------
def draw_student(deslocamento_perna_esquerda=0, elevacao_perna_esquerda=0, deslocamento_perna_direita=0, elevacao_perna_direita=0,
                  retangulo_braco=(18, 20, 22, 26), oscilacao=0, olho="open", inclinacao=0,
                  linhas_movimento=False):
    largura, altura = 26, 40
    imagem = canvas(largura, altura)
    desenho = ImageDraw.Draw(imagem)

    def perna(x0, dx, elevacao):
        x = x0 + dx + inclinacao
        y_quadril = 28 + oscilacao
        base_canela = 34 + oscilacao - elevacao
        desenho.rectangle([x, y_quadril, x + 4, base_canela], fill=CALCA, outline=CONTORNO)
        base_sapato = min(38, base_canela + 4)
        desenho.rectangle([x, base_canela, x + 4, base_sapato], fill=SAPATO, outline=CONTORNO)

    # pernas (atrás do tronco/mochila)
    perna(6, deslocamento_perna_esquerda, elevacao_perna_esquerda)
    perna(15, deslocamento_perna_direita, elevacao_perna_direita)

    if linhas_movimento:
        for i in range(3):
            yy = 16 + i * 6
            transparencia = 190 - i * 55
            desenho.line([(-3 - i * 4 + inclinacao, yy), (3 - i * 4 + inclinacao, yy)],
                   fill=(190, 235, 255, transparencia), width=2)

    # mochila (ombro traseiro/esquerdo)
    desenho.rectangle([1 + inclinacao, 15 + oscilacao, 6 + inclinacao, 29 + oscilacao], fill=MOCHILA, outline=CONTORNO)
    desenho.line([7 + inclinacao, 15 + oscilacao, 12 + inclinacao, 20 + oscilacao], fill=SOMBRA_MOCHILA, width=2)

    # tronco (camisa polo) - ombros/mangas mais largos, cintura mais estreita
    desenho.rectangle([3 + inclinacao, 14 + oscilacao, 23 + inclinacao, 19 + oscilacao], fill=UNIFORME, outline=CONTORNO)
    desenho.rectangle([5 + inclinacao, 19 + oscilacao, 21 + inclinacao, 28 + oscilacao], fill=UNIFORME, outline=CONTORNO)
    desenho.rectangle([9 + inclinacao, 25 + oscilacao, 17 + inclinacao, 28 + oscilacao], fill=SOMBRA_UNIFORME)

    # colarinho
    desenho.polygon([(10 + inclinacao, 14 + oscilacao), (16 + inclinacao, 14 + oscilacao),
               (14 + inclinacao, 17 + oscilacao), (12 + inclinacao, 17 + oscilacao)], fill=GOLA, outline=CONTORNO)

    # emblema do IFRN no peito
    desenho.rectangle([12 + inclinacao, 20 + oscilacao, 16 + inclinacao, 23 + oscilacao], fill=REMENDO, outline=CONTORNO)
    desenho.point((14 + inclinacao, 21 + oscilacao), fill=UNIFORME)

    # braço (posição varia por pose)
    ax0, ay0, ax1, ay1 = retangulo_braco
    desenho.rectangle([ax0 + inclinacao, ay0 + oscilacao, ax1 + inclinacao, ay1 + oscilacao], fill=PELE, outline=CONTORNO)

    # cabeça
    desenho.ellipse([7 + inclinacao, 1 + oscilacao, 19 + inclinacao, 13 + oscilacao], fill=PELE, outline=CONTORNO)
    desenho.rectangle([9 + inclinacao, 9 + oscilacao, 17 + inclinacao, 12 + oscilacao], fill=SOMBRA_PELE)

    # cabelo (touca + topete apontando para a direção que anda) - metade de
    # cima da elipse (ângulo 180->360 = arco norte no PIL), com a borda reta
    # (a "franja") bem acima do olho para não se misturarem nesta resolução
    desenho.pieslice([6 + inclinacao, -2 + oscilacao, 20 + inclinacao, 8 + oscilacao], 180, 360, fill=CABELO, outline=CONTORNO)
    desenho.polygon([(16 + inclinacao, 0 + oscilacao), (20 + inclinacao, 2 + oscilacao), (16 + inclinacao, 4 + oscilacao)], fill=CABELO)

    # olho
    if olho == "blink":
        desenho.line([13 + inclinacao, 7 + oscilacao, 16 + inclinacao, 7 + oscilacao], fill=CONTORNO, width=1)
    else:
        desenho.rectangle([14 + inclinacao, 6 + oscilacao, 16 + inclinacao, 8 + oscilacao], fill=PRETO)

    return imagem


# parado(a): 2 quadros (respiração + piscada)
save(draw_student(retangulo_braco=(18, 20, 22, 26), olho="open"), f"{BASE}/jogador/repouso_0.png")
save(draw_student(retangulo_braco=(18, 21, 22, 27), oscilacao=1, olho="blink"), f"{BASE}/jogador/repouso_1.png")

# andando: 4 quadros (contato / passagem / contato / passagem)
save(draw_student(deslocamento_perna_esquerda=-2, deslocamento_perna_direita=2, retangulo_braco=(14, 19, 18, 25)),
     f"{BASE}/jogador/caminhada_0.png")
save(draw_student(elevacao_perna_direita=3, oscilacao=-1, retangulo_braco=(18, 20, 22, 26)),
     f"{BASE}/jogador/caminhada_1.png")
save(draw_student(deslocamento_perna_esquerda=2, deslocamento_perna_direita=-2, retangulo_braco=(21, 19, 25, 25)),
     f"{BASE}/jogador/caminhada_2.png")
save(draw_student(elevacao_perna_esquerda=3, oscilacao=-1, retangulo_braco=(15, 20, 19, 26)),
     f"{BASE}/jogador/caminhada_3.png")

# pulo (pernas dobradas, braço para cima)
save(draw_student(deslocamento_perna_esquerda=1, elevacao_perna_esquerda=4, deslocamento_perna_direita=-1, elevacao_perna_direita=2,
                   retangulo_braco=(19, 13, 23, 18), oscilacao=-1),
     f"{BASE}/jogador/salto.png")

# dash (corpo inclinado, pernas esticadas para trás, linhas de movimento)
save(draw_student(deslocamento_perna_esquerda=-3, deslocamento_perna_direita=3, elevacao_perna_direita=1,
                   retangulo_braco=(11, 18, 15, 23), inclinacao=2, olho="blink", linhas_movimento=True),
     f"{BASE}/jogador/arrancada.png")


# ----------------------------------------------------------------------
# Inimigo comum (bug) - 26x24, 2 quadros de "rastejo"
# ----------------------------------------------------------------------
def draw_bug(cor=(200, 70, 70, 255), quadro=0):
    largura, altura = 26, 24
    imagem = canvas(largura, altura)
    desenho = ImageDraw.Draw(imagem)
    peruca = 1 if quadro == 1 else -1

    desenho.ellipse([1, 6, 25, 23], fill=cor, outline=CONTORNO)
    desenho.ellipse([2, 6, 13, 15], fill=darken(cor, 1.15) if sum(cor[:3]) < 690 else cor)
    desenho.ellipse([6, 12, 9, 15], fill=PRETO)
    desenho.ellipse([16, 12, 19, 15], fill=PRETO)

    for lx in (5, 12, 19):
        desenho.line([lx, 6, lx + peruca * 3, 1], fill=cor, width=2)

    for lx, dy in ((3, 1), (13, -1), (22, 1)):
        ly = 20 if quadro == 0 else 22
        desenho.line([lx, 16, lx + dy, ly], fill=CONTORNO, width=2)
    return imagem


save(draw_bug(quadro=0), f"{BASE}/inimigos/bug_0.png")
save(draw_bug(quadro=1), f"{BASE}/inimigos/bug_1.png")


# ----------------------------------------------------------------------
# Professores-chefe (54x64) - jaleco corrompido por "glitches" de vírus
# ----------------------------------------------------------------------
def draw_boss(cor, destaque, simbolo, semente_falha):
    largura, altura = 54, 64
    imagem = canvas(largura, altura)
    desenho = ImageDraw.Draw(imagem)

    desenho.rectangle([4, 16, 49, 59], fill=cor, outline=CONTORNO)
    desenho.rectangle([4, 40, 25, 59], fill=darken(cor, 0.65))
    desenho.rectangle([6, 20, 47, 25], fill=BRANCO, outline=CONTORNO)

    desenho.ellipse([15, 0, 39, 23], fill=PELE, outline=CONTORNO)
    desenho.rectangle([18, 17, 36, 22], fill=SOMBRA_PELE)

    # óculos: duas lentes quadradas + ponte, em vez de um retângulo grande
    # (um retângulo grande nesta resolução vira uma venda sólida)
    desenho.rectangle([18, 9, 23, 13], fill=SOMBRA_PELE, outline=CONTORNO)
    desenho.rectangle([31, 9, 36, 13], fill=SOMBRA_PELE, outline=CONTORNO)
    desenho.line([23, 10, 31, 10], fill=CONTORNO, width=1)
    desenho.point((20, 11), fill=PRETO)
    desenho.point((33, 11), fill=PRETO)

    simbolo(desenho)

    desenho.rectangle([4, 55, 49, 59], fill=destaque)

    gerador_aleatorio = random.Random(semente_falha)
    for _ in range(5):
        gx, gy = gerador_aleatorio.randint(6, 46), gerador_aleatorio.randint(18, 55)
        desenho.rectangle([gx, gy, gx + 1, gy + 1], fill=destaque)
    return imagem


def sym_scratch(desenho):
    for i, c in enumerate([(240, 150, 40, 255), (60, 140, 220, 255), (200, 60, 60, 255)]):
        desenho.rectangle([14 + i * 9, 34, 21 + i * 9, 41], fill=c, outline=CONTORNO)


def sym_python(desenho):
    desenho.arc([18, 30, 30, 42], 200, 380, fill=(60, 140, 220, 255), width=3)
    desenho.arc([24, 36, 36, 48], 20, 200, fill=(230, 210, 60, 255), width=3)


def sym_java(desenho):
    desenho.ellipse([19, 30, 35, 46], outline=(180, 100, 40, 255), width=3)
    desenho.line([27, 30, 27, 24], fill=(120, 70, 30, 255), width=3)


def sym_c(desenho):
    desenho.arc([18, 30, 36, 48], 40, 320, fill=(230, 230, 230, 255), width=4)


def sym_sql(desenho):
    desenho.ellipse([18, 30, 36, 36], fill=(60, 180, 140, 255))
    desenho.rectangle([18, 33, 36, 45], fill=(60, 180, 140, 255))
    desenho.ellipse([18, 42, 36, 48], fill=(40, 140, 110, 255))


def sym_asm(desenho):
    for i, bit in enumerate("1010"):
        cor = BRANCO if bit == "1" else (120, 120, 120, 255)
        desenho.text((16 + i * 6, 32), bit, preenchimento=cor)


ARTES_CHEFES = [
    ((240, 150, 40, 255), (255, 200, 90, 255), sym_scratch, "prof_scratch"),
    ((60, 140, 220, 255), (230, 210, 60, 255), sym_python, "prof_python"),
    ((200, 60, 60, 255), (255, 150, 150, 255), sym_java, "prof_java"),
    ((120, 120, 130, 255), (220, 220, 230, 255), sym_c, "prof_c"),
    ((60, 180, 140, 255), (140, 230, 210, 255), sym_sql, "prof_sql"),
    ((30, 30, 40, 255), (90, 90, 110, 255), sym_asm, "prof_assembly"),
]

for i, (cor, destaque, abreviatura_simbolo, nome_arquivo) in enumerate(ARTES_CHEFES):
    save(draw_boss(cor, destaque, abreviatura_simbolo, semente_falha=i * 13 + 1), f"{BASE}/chefes/{nome_arquivo}.png")


# ----------------------------------------------------------------------
# Tiles de cenário (chão / espinho), power-up e painel de fundo
# ----------------------------------------------------------------------
def draw_ground_tile():
    largura = altura = 32
    imagem = canvas(largura, altura)
    desenho = ImageDraw.Draw(imagem)
    desenho.rectangle([0, 0, largura - 1, altura - 1], fill=(95, 68, 52, 255))
    desenho.rectangle([0, 0, largura - 1, 3], fill=(140, 105, 70, 255))
    for i in range(4):
        x = i * 8 + 2
        desenho.rectangle([x, 6, x + 5, 11], outline=(75, 52, 40, 255))
        desenho.rectangle([x + 2, 17, x + 7, 22], outline=(75, 52, 40, 255))
    desenho.rectangle([0, 0, largura - 1, altura - 1], outline=(58, 40, 30, 255))
    return imagem


def draw_spike_tile():
    largura = altura = 32
    imagem = canvas(largura, altura)
    desenho = ImageDraw.Draw(imagem)
    for i in range(3):
        x0 = i * 10
        desenho.polygon([(x0, 32), (x0 + 5, 12), (x0 + 10, 32)],
                   fill=(210, 40, 40, 255), outline=(120, 10, 10, 255))
        desenho.line([(x0 + 5, 12), (x0 + 3, 19)], fill=(255, 130, 130, 255), width=1)
    return imagem


def draw_powerup():
    largura = altura = 32
    imagem = canvas(largura, altura)
    desenho = ImageDraw.Draw(imagem)
    desenho.polygon([(16, 2), (28, 16), (16, 30), (4, 16)], fill=(255, 210, 40, 255), outline=BRANCO)
    desenho.polygon([(16, 2), (22, 16), (16, 16), (10, 16)], fill=(255, 235, 150, 255))
    desenho.polygon([(12, 8), (20, 8), (16, 16)], fill=(40, 30, 0, 255))
    return imagem


def draw_bg_panel():
    largura, altura = 90, 220
    imagem = canvas(largura, altura)
    desenho = ImageDraw.Draw(imagem)
    desenho.rectangle([0, 0, largura - 1, altura - 1], fill=(32, 28, 54, 255), outline=(50, 44, 74, 255))
    for fileira in range(4):
        for coluna in range(2):
            x, y = 10 + coluna * 40, 15 + fileira * 50
            desenho.rectangle([x, y, x + 28, y + 34], fill=(46, 40, 74, 255), outline=(60, 54, 92, 255))
            desenho.rectangle([x + 2, y + 2, x + 26, y + 6], fill=(60, 54, 92, 255))
    return imagem


save(draw_ground_tile(), f"{BASE}/blocos/chao.png")
save(draw_spike_tile(), f"{BASE}/blocos/espinho.png")
save(draw_powerup(), f"{BASE}/interface/item_habilidade.png")
save(draw_bg_panel(), f"{BASE}/cenarios/painel.png")

print("\nTodas as imagens foram geradas em recursos/imagens/")
