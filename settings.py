"""Configurações globais do jogo: dimensões, cores, física."""

TITLE = "IFVania"

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
FPS = 60
TILE_SIZE = 32

# Contrato corporal comum a protagonistas, NPCs, bugs e bosses.
CHARACTER_SIZE = (40, 40)
CHARACTER_VISUAL_SCALE = 2.0  # Protagonista, bosses e NPCs: 80 × 80, durante toda a partida.

# Física
GRAVITY = 0.65
MAX_FALL_SPEED = 15
PLAYER_SPEED = 4.2
PLAYER_JUMP_STRENGTH = -12.5
DOUBLE_JUMP_STRENGTH = -10.5
DASH_SPEED = 11
DASH_DURATION = 10          # frames que o dash dura
DASH_COOLDOWN = 35          # frames de espera entre dashes
WALL_SLIDE_SPEED = 2.2
WALL_JUMP_X = 6.5
WALL_JUMP_Y = -11
ATTACK_COOLDOWN = 30       # preparação, golpe e recolhimento do mouse com fio
INVULN_TIME = 90            # frames de invencibilidade após tomar dano
SHOT_COOLDOWN = 30
SHOT_SPEED = 9

# Cores (R,G,B)
WHITE = (245, 245, 245)
BLACK = (10, 10, 10)
BG_COLOR = (22, 20, 38)
BG_COLOR_2 = (32, 28, 54)
GROUND_COLOR = (95, 68, 52)
GROUND_EDGE = (140, 105, 70)
PLATFORM_COLOR = (110, 85, 130)
SPIKE_COLOR = (210, 40, 40)
GATE_COLOR = (90, 90, 150)
GATE_OPEN_COLOR = (60, 200, 120)
EXIT_COLOR = (255, 220, 90)

PLAYER_COLOR = (70, 170, 255)
PLAYER_DASH_COLOR = (180, 230, 255)
ENEMY_COLOR = (200, 70, 70)
BOSS_ACCENT = (255, 255, 255)

PROJECTILE_PLAYER_COLOR = (120, 240, 180)
PROJECTILE_ENEMY_COLOR = (255, 120, 70)

UI_BG = (18, 16, 30, 210)
UI_BORDER = (230, 230, 230)
HP_COLOR = (220, 45, 65)
HP_BG = (60, 12, 18)
BOSS_HP_COLOR = (200, 60, 220)
POWERUP_COLOR = (255, 210, 40)
TEXT_COLOR = (245, 245, 245)
TEXT_SHADOW = (0, 0, 0)
NAME_COLOR = (255, 210, 90)

FONT_NAME = None  # usa a fonte padrão do pygame
