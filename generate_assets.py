"""Gera as imagens (pixel art) usadas pelo jogo, em assets/images/.

Este script NÃO é necessário para jogar - as imagens já ficam prontas na pasta
assets/. Ele existe para que professores/alunos entendam como as imagens foram
feitas e possam regenerá-las ou usá-lo como base para desenhar as próprias artes
e substituir os arquivos em assets/images/.

Estilo: pixel art de baixa resolução (sem suavização), no espírito de
personagens de Castlevania/Metroid - silhueta com contorno escuro, poucas
cores por material e sombreamento em blocos sólidos (sem gradiente).

O(a) aluno(a) protagonista veste farda do IFRN (camisa polo verde institucional,
calça e mochila) e tem quadros de animação separados para parado(a), andando
(4 quadros), pulando e dando dash - a virada para a esquerda é feita em tempo
de execução por assets.py (espelhamento), então só desenhamos virado(a) para a
direita aqui.

Requer Pillow:  pip install pillow
Executar:        python generate_assets.py
"""
import os
import random
from PIL import Image, ImageDraw

BASE = "assets/images"

for sub in ("player", "enemies", "bosses", "tiles", "background", "ui"):
    os.makedirs(f"{BASE}/{sub}", exist_ok=True)


def canvas(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))


def save(img, path):
    img.save(path)
    print("gerado:", path)


def darken(color, factor=0.6):
    r, g, b, a = color
    return (int(r * factor), int(g * factor), int(b * factor), a)


# ----------------------------------------------------------------------
# Paleta - poucas cores por material, como em sprites 16/32-bit
# ----------------------------------------------------------------------
OUTLINE = (16, 14, 22, 255)
SKIN = (222, 170, 133, 255)
SKIN_SHADE = (181, 128, 96, 255)
HAIR = (43, 28, 22, 255)
UNIFORM = (36, 112, 76, 255)        # verde institucional do IFRN
UNIFORM_SHADE = (22, 80, 54, 255)
COLLAR = (232, 232, 224, 255)
PATCH = (238, 238, 230, 255)
PANTS = (46, 46, 60, 255)
SHOE = (26, 24, 32, 255)
BAG = (196, 132, 34, 255)
BAG_SHADE = (150, 96, 22, 255)
WHITE = (245, 245, 245, 255)
BLACK = (12, 12, 12, 255)


# ----------------------------------------------------------------------
# Aluno(a) - personagem principal (26x40), virado(a) para a direita
# ----------------------------------------------------------------------
def draw_student(leg_l_dx=0, leg_l_lift=0, leg_r_dx=0, leg_r_lift=0,
                  arm_box=(18, 20, 22, 26), bob=0, eye="open", lean=0,
                  motion_lines=False):
    w, h = 26, 40
    img = canvas(w, h)
    d = ImageDraw.Draw(img)

    def leg(x0, dx, lift):
        x = x0 + dx + lean
        hip_y = 28 + bob
        shin_bottom = 34 + bob - lift
        d.rectangle([x, hip_y, x + 4, shin_bottom], fill=PANTS, outline=OUTLINE)
        shoe_bottom = min(38, shin_bottom + 4)
        d.rectangle([x, shin_bottom, x + 4, shoe_bottom], fill=SHOE, outline=OUTLINE)

    # pernas (atrás do tronco/mochila)
    leg(6, leg_l_dx, leg_l_lift)
    leg(15, leg_r_dx, leg_r_lift)

    if motion_lines:
        for i in range(3):
            yy = 16 + i * 6
            alpha = 190 - i * 55
            d.line([(-3 - i * 4 + lean, yy), (3 - i * 4 + lean, yy)],
                   fill=(190, 235, 255, alpha), width=2)

    # mochila (ombro traseiro/esquerdo)
    d.rectangle([1 + lean, 15 + bob, 6 + lean, 29 + bob], fill=BAG, outline=OUTLINE)
    d.line([7 + lean, 15 + bob, 12 + lean, 20 + bob], fill=BAG_SHADE, width=2)

    # tronco (camisa polo) - ombros/mangas mais largos, cintura mais estreita
    d.rectangle([3 + lean, 14 + bob, 23 + lean, 19 + bob], fill=UNIFORM, outline=OUTLINE)
    d.rectangle([5 + lean, 19 + bob, 21 + lean, 28 + bob], fill=UNIFORM, outline=OUTLINE)
    d.rectangle([9 + lean, 25 + bob, 17 + lean, 28 + bob], fill=UNIFORM_SHADE)

    # colarinho
    d.polygon([(10 + lean, 14 + bob), (16 + lean, 14 + bob),
               (14 + lean, 17 + bob), (12 + lean, 17 + bob)], fill=COLLAR, outline=OUTLINE)

    # emblema do IFRN no peito
    d.rectangle([12 + lean, 20 + bob, 16 + lean, 23 + bob], fill=PATCH, outline=OUTLINE)
    d.point((14 + lean, 21 + bob), fill=UNIFORM)

    # braço (posição varia por pose)
    ax0, ay0, ax1, ay1 = arm_box
    d.rectangle([ax0 + lean, ay0 + bob, ax1 + lean, ay1 + bob], fill=SKIN, outline=OUTLINE)

    # cabeça
    d.ellipse([7 + lean, 1 + bob, 19 + lean, 13 + bob], fill=SKIN, outline=OUTLINE)
    d.rectangle([9 + lean, 9 + bob, 17 + lean, 12 + bob], fill=SKIN_SHADE)

    # cabelo (touca + topete apontando para a direção que anda) - metade de
    # cima da elipse (ângulo 180->360 = arco norte no PIL), com a borda reta
    # (a "franja") bem acima do olho para não se misturarem nesta resolução
    d.pieslice([6 + lean, -2 + bob, 20 + lean, 8 + bob], 180, 360, fill=HAIR, outline=OUTLINE)
    d.polygon([(16 + lean, 0 + bob), (20 + lean, 2 + bob), (16 + lean, 4 + bob)], fill=HAIR)

    # olho
    if eye == "blink":
        d.line([13 + lean, 7 + bob, 16 + lean, 7 + bob], fill=OUTLINE, width=1)
    else:
        d.rectangle([14 + lean, 6 + bob, 16 + lean, 8 + bob], fill=BLACK)

    return img


# parado(a): 2 quadros (respiração + piscada)
save(draw_student(arm_box=(18, 20, 22, 26), eye="open"), f"{BASE}/player/idle_0.png")
save(draw_student(arm_box=(18, 21, 22, 27), bob=1, eye="blink"), f"{BASE}/player/idle_1.png")

# andando: 4 quadros (contato / passagem / contato / passagem)
save(draw_student(leg_l_dx=-2, leg_r_dx=2, arm_box=(14, 19, 18, 25)),
     f"{BASE}/player/walk_0.png")
save(draw_student(leg_r_lift=3, bob=-1, arm_box=(18, 20, 22, 26)),
     f"{BASE}/player/walk_1.png")
save(draw_student(leg_l_dx=2, leg_r_dx=-2, arm_box=(21, 19, 25, 25)),
     f"{BASE}/player/walk_2.png")
save(draw_student(leg_l_lift=3, bob=-1, arm_box=(15, 20, 19, 26)),
     f"{BASE}/player/walk_3.png")

# pulo (pernas dobradas, braço para cima)
save(draw_student(leg_l_dx=1, leg_l_lift=4, leg_r_dx=-1, leg_r_lift=2,
                   arm_box=(19, 13, 23, 18), bob=-1),
     f"{BASE}/player/jump.png")

# dash (corpo inclinado, pernas esticadas para trás, linhas de movimento)
save(draw_student(leg_l_dx=-3, leg_r_dx=3, leg_r_lift=1,
                   arm_box=(11, 18, 15, 23), lean=2, eye="blink", motion_lines=True),
     f"{BASE}/player/dash.png")


# ----------------------------------------------------------------------
# Inimigo comum (bug) - 26x24, 2 quadros de "rastejo"
# ----------------------------------------------------------------------
def draw_bug(color=(200, 70, 70, 255), frame=0):
    w, h = 26, 24
    img = canvas(w, h)
    d = ImageDraw.Draw(img)
    wig = 1 if frame == 1 else -1

    d.ellipse([1, 6, 25, 23], fill=color, outline=OUTLINE)
    d.ellipse([2, 6, 13, 15], fill=darken(color, 1.15) if sum(color[:3]) < 690 else color)
    d.ellipse([6, 12, 9, 15], fill=BLACK)
    d.ellipse([16, 12, 19, 15], fill=BLACK)

    for lx in (5, 12, 19):
        d.line([lx, 6, lx + wig * 3, 1], fill=color, width=2)

    for lx, dy in ((3, 1), (13, -1), (22, 1)):
        ly = 20 if frame == 0 else 22
        d.line([lx, 16, lx + dy, ly], fill=OUTLINE, width=2)
    return img


save(draw_bug(frame=0), f"{BASE}/enemies/bug_0.png")
save(draw_bug(frame=1), f"{BASE}/enemies/bug_1.png")


# ----------------------------------------------------------------------
# Professores-chefe (54x64) - jaleco corrompido por "glitches" de vírus
# ----------------------------------------------------------------------
def draw_boss(color, accent, symbol, glitch_seed):
    w, h = 54, 64
    img = canvas(w, h)
    d = ImageDraw.Draw(img)

    d.rectangle([4, 16, 49, 59], fill=color, outline=OUTLINE)
    d.rectangle([4, 40, 25, 59], fill=darken(color, 0.65))
    d.rectangle([6, 20, 47, 25], fill=WHITE, outline=OUTLINE)

    d.ellipse([15, 0, 39, 23], fill=SKIN, outline=OUTLINE)
    d.rectangle([18, 17, 36, 22], fill=SKIN_SHADE)

    # óculos: duas lentes quadradas + ponte, em vez de um retângulo grande
    # (um retângulo grande nesta resolução vira uma venda sólida)
    d.rectangle([18, 9, 23, 13], fill=SKIN_SHADE, outline=OUTLINE)
    d.rectangle([31, 9, 36, 13], fill=SKIN_SHADE, outline=OUTLINE)
    d.line([23, 10, 31, 10], fill=OUTLINE, width=1)
    d.point((20, 11), fill=BLACK)
    d.point((33, 11), fill=BLACK)

    symbol(d)

    d.rectangle([4, 55, 49, 59], fill=accent)

    rng = random.Random(glitch_seed)
    for _ in range(5):
        gx, gy = rng.randint(6, 46), rng.randint(18, 55)
        d.rectangle([gx, gy, gx + 1, gy + 1], fill=accent)
    return img


def sym_scratch(d):
    for i, c in enumerate([(240, 150, 40, 255), (60, 140, 220, 255), (200, 60, 60, 255)]):
        d.rectangle([14 + i * 9, 34, 21 + i * 9, 41], fill=c, outline=OUTLINE)


def sym_python(d):
    d.arc([18, 30, 30, 42], 200, 380, fill=(60, 140, 220, 255), width=3)
    d.arc([24, 36, 36, 48], 20, 200, fill=(230, 210, 60, 255), width=3)


def sym_java(d):
    d.ellipse([19, 30, 35, 46], outline=(180, 100, 40, 255), width=3)
    d.line([27, 30, 27, 24], fill=(120, 70, 30, 255), width=3)


def sym_c(d):
    d.arc([18, 30, 36, 48], 40, 320, fill=(230, 230, 230, 255), width=4)


def sym_sql(d):
    d.ellipse([18, 30, 36, 36], fill=(60, 180, 140, 255))
    d.rectangle([18, 33, 36, 45], fill=(60, 180, 140, 255))
    d.ellipse([18, 42, 36, 48], fill=(40, 140, 110, 255))


def sym_asm(d):
    for i, bit in enumerate("1010"):
        color = WHITE if bit == "1" else (120, 120, 120, 255)
        d.text((16 + i * 6, 32), bit, fill=color)


BOSS_ART = [
    ((240, 150, 40, 255), (255, 200, 90, 255), sym_scratch, "prof_scratch"),
    ((60, 140, 220, 255), (230, 210, 60, 255), sym_python, "prof_python"),
    ((200, 60, 60, 255), (255, 150, 150, 255), sym_java, "prof_java"),
    ((120, 120, 130, 255), (220, 220, 230, 255), sym_c, "prof_c"),
    ((60, 180, 140, 255), (140, 230, 210, 255), sym_sql, "prof_sql"),
    ((30, 30, 40, 255), (90, 90, 110, 255), sym_asm, "prof_assembly"),
]

for i, (color, accent, sym, fname) in enumerate(BOSS_ART):
    save(draw_boss(color, accent, sym, glitch_seed=i * 13 + 1), f"{BASE}/bosses/{fname}.png")


# ----------------------------------------------------------------------
# Tiles de cenário (chão / espinho), power-up e painel de fundo
# ----------------------------------------------------------------------
def draw_ground_tile():
    w = h = 32
    img = canvas(w, h)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, h - 1], fill=(95, 68, 52, 255))
    d.rectangle([0, 0, w - 1, 3], fill=(140, 105, 70, 255))
    for i in range(4):
        x = i * 8 + 2
        d.rectangle([x, 6, x + 5, 11], outline=(75, 52, 40, 255))
        d.rectangle([x + 2, 17, x + 7, 22], outline=(75, 52, 40, 255))
    d.rectangle([0, 0, w - 1, h - 1], outline=(58, 40, 30, 255))
    return img


def draw_spike_tile():
    w = h = 32
    img = canvas(w, h)
    d = ImageDraw.Draw(img)
    for i in range(3):
        x0 = i * 10
        d.polygon([(x0, 32), (x0 + 5, 12), (x0 + 10, 32)],
                   fill=(210, 40, 40, 255), outline=(120, 10, 10, 255))
        d.line([(x0 + 5, 12), (x0 + 3, 19)], fill=(255, 130, 130, 255), width=1)
    return img


def draw_powerup():
    w = h = 32
    img = canvas(w, h)
    d = ImageDraw.Draw(img)
    d.polygon([(16, 2), (28, 16), (16, 30), (4, 16)], fill=(255, 210, 40, 255), outline=WHITE)
    d.polygon([(16, 2), (22, 16), (16, 16), (10, 16)], fill=(255, 235, 150, 255))
    d.polygon([(12, 8), (20, 8), (16, 16)], fill=(40, 30, 0, 255))
    return img


def draw_bg_panel():
    w, h = 90, 220
    img = canvas(w, h)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, h - 1], fill=(32, 28, 54, 255), outline=(50, 44, 74, 255))
    for row in range(4):
        for col in range(2):
            x, y = 10 + col * 40, 15 + row * 50
            d.rectangle([x, y, x + 28, y + 34], fill=(46, 40, 74, 255), outline=(60, 54, 92, 255))
            d.rectangle([x + 2, y + 2, x + 26, y + 6], fill=(60, 54, 92, 255))
    return img


save(draw_ground_tile(), f"{BASE}/tiles/ground.png")
save(draw_spike_tile(), f"{BASE}/tiles/spike.png")
save(draw_powerup(), f"{BASE}/ui/powerup.png")
save(draw_bg_panel(), f"{BASE}/background/panel.png")

print("\nTodas as imagens foram geradas em assets/images/")
