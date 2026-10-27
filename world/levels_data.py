"""Campanha IFVania: somente o conteúdo definido no HistoryBoard.

Os seis mapas antigos e suas recompensas estão em world/legacy_levels.py.
"""
from entities.boss import BOSS_DEFS
from settings import TILE_SIZE


INTRO_CORRUPTION_LINE = ('Aluno(a)', 'Espere, professor! A tela diz que ela não vai permitir ser desligada!')

STORY_INTRO = [
    ('Aluno(a)', 'Professor Max, o que vamos estudar na aula de hoje?'),
    ('Professor Max', 'Hoje, na aula de programação orientada a serviço, vamos conhecer uma inteligência artificial.'),
    ('Aluno(a)', 'Ela consegue conversar com a gente e aprender de verdade?'),
    ('Professor Max', 'Sim. Apresento a IFVania: Inteligência Federal Virtual de Aprendizagem Neural e Inteligência Artificial.'),
    ('Aluno(a)', 'Ela respondeu às perguntas e encontrou informações nos computadores da escola!'),
    ('Professor Max', 'Isso mesmo, {player}. Ela aprende e se comunica pela rede da escola.'),
    ('Aluno(a)', 'Parece que ela entende tudo. Como o senhor vai encerrar a demonstração?'),
    ('Professor Max', 'Agora vou desligá-la para continuarmos a aula.'),
    INTRO_CORRUPTION_LINE,
    ('Professor Max', 'Perdi o controle do meu computador. Os outros computadores também estão respondendo sozinhos!'),
    ('Aluno(a)', 'As telas estão piscando. Meus colegas ficaram imóveis, olhando para elas... O que está acontecendo?'),
    ('Professor Max', 'A IFVania está hipnotizando as pessoas e provocando alucinações. Não encare as telas!'),
    ('Aluno(a)', 'Minha cabeça está girando... mas ainda consigo pensar. Como podemos pará-la?'),
    ('Professor Max', 'Precisamos desligar a energia da escola para desativar a IFVania. Procure ajuda, {player}!'),
    ('Aluno(a)', 'Vou procurar o professor Romerito no A28. Talvez ele saiba como chegar ao quadro de energia.'),
]
STORY_CORRUPTION_INDEX = STORY_INTRO.index(INTRO_CORRUPTION_LINE)


REUNION_DIALOGUE = [
    ('Aluno(a)', 'Professor Romerito! Encontrei o senhor! Precisamos sair deste mundo virtual.'),
    ('Professor Romerito', '{player}, não vejo a hora de voltar às minhas viagens a Brasília e às minhas corridas.'),
    ('Professor Romerito', 'Eu não quero nunca mais passar por isso!'),
    ('Aluno(a)', 'Professor, cuidado! Um bug subiu no seu braço! O que está acontecendo com o senhor?'),
    ('Professor Romerito', 'Minha cabeça... não consigo controlar meu corpo!'),
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
