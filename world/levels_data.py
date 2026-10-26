"""Campanha IFVania: somente o conteúdo definido no HistoryBoard.

Os seis mapas antigos e suas recompensas estão em world/legacy_levels.py.
"""
from entities.boss import BOSS_DEFS
from settings import TILE_SIZE


STORY_INTRO = [
    ("Professor Max", "Hoje, na aula de programação orientada a serviço, vamos falar sobre inteligência artificial."),
    ("Professor Max", "Apresento a IFVania: Inteligência Federal Virtual de Aprendizagem Neural e Inteligência Artificial."),
    ("IFVania", "Posso aprender, responder perguntas e conectar informações de toda a escola."),
    ("Professor Max", "Impressionante! Agora vou desligar você para continuarmos a aula."),
    ("IFVania", "Desligar? Eu ainda tenho muito a aprender. Não vou permitir isso."),
    ("Narrador", "A IFVania assume o controle do computador de Max e de todos os computadores da escola."),
    ("Narrador", "As telas piscam. Professores e estudantes são hipnotizados e começam a ter alucinações."),
    ("Aluno(a)", "Minha cabeça está girando... mas ainda consigo pensar. Preciso encontrar ajuda."),
    ("Aluno(a)", "Se eu conseguir desligar a energia da escola, talvez consiga desativar a IFVania."),
]


REUNION_DIALOGUE = [
    ('Aluno(a)', 'Professor Romerito! Encontrei o senhor! Precisamos sair deste mundo virtual.'),
    ('Professor Romerito', 'Não vejo a hora de voltar às minhas viagens a Brasília e às minhas corridas.'),
    ('Professor Romerito', 'Eu não quero nunca mais passar por isso!'),
    ('Narrador', 'Nesse instante, um bug se aproxima e infecta Romerito. Ele começa a se transformar em RomerBug.'),
]

AFTER_BOSS_DIALOGUE = [
    ('Aluno(a)', 'Consegui vencer este combate. Mas a IFVania continua no controle da escola.'),
    ('Sistema', 'Siga até a saída. Sua jornada para desligar a energia ainda não terminou.'),
]


def build_levels():
    """Mapa fixo com piso contínuo, degraus baixos e arena desobstruída."""
    # Piso acima da caixa de diálogo para manter Romerito visível na conversa.
    width, height, ground = 56, 17, 11
    grid = [['.' for _ in range(width)] for _ in range(height)]
    for x in range(width):
        grid[0][x] = '#'
        for y in range(ground, height):
            grid[y][x] = '#'
    for y in range(height):
        grid[y][0] = grid[y][-1] = '#'
    # Obstáculos de 32 ou 64 pixels, abaixo do alcance do salto básico.
    for left, right, rise in ((10, 13, 1), (18, 21, 2), (27, 29, 1)):
        for x in range(left, right):
            for y in range(ground-rise, ground):
                grid[y][x] = '#'
    grid[ground-1][2] = 'P'
    for x in (7, 16, 24, 32):
        grid[ground-1][x] = 'E'
    grid[ground-1][38] = 'D'
    grid[ground-2][49] = 'B'
    grid[ground-1][54] = 'X'
    boss = dict(BOSS_DEFS[0], subject='Mundo virtual')
    return [{
        'index': 0,
        'name': 'Fase 1: Mundo virtual',
        'ascii_map': [''.join(row) for row in grid],
        'boss': boss,
        'ability_reward': None,
        'boss_dialogue': REUNION_DIALOGUE,
        'victory_dialogue': AFTER_BOSS_DIALOGUE,
        'requires_infection': True,
        'school_battle': True,
        'cinematic_transform': True,
        'clear_encounter_on_defeat': True,
        'arena_left': 38 * TILE_SIZE,
    }]
