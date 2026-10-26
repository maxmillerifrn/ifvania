"""Campanha antiga, fora do menu principal. Definição das 6 fases: mapas (gerados proceduralmente de forma determinística),
professores-chefe, textos de diálogo e habilidades concedidas.
"""
import random
from entities.boss import BOSS_DEFS
from powerups import Ability

LENGTHS = [46, 52, 58, 64, 70, 78]
GROUND_ROW = 14
HEIGHT_TILES = 17


def _generate_rows(length_tiles, height_tiles, ground_row, seed, num_enemies):
    rng = random.Random(seed)
    grid = [['.' for _ in range(length_tiles)] for _ in range(height_tiles)]

    # bordas do nível
    for x in range(length_tiles):
        grid[0][x] = '#'
        grid[height_tiles - 1][x] = '#'
    for y in range(height_tiles):
        grid[y][0] = '#'
        grid[y][length_tiles - 1] = '#'

    # chão principal, com pequenos degraus e vãos de 1 bloco (sempre pulável)
    x = 1
    row = ground_row
    while x < length_tiles - 1:
        grid[row][x] = '#'
        x += 1
        if x > 10 and x < length_tiles - 12 and rng.random() < 0.10:
            # vão pequeno (1 bloco) - sempre transponível a pé
            x += 1
        elif x > 8 and x < length_tiles - 10 and rng.random() < 0.12:
            # degrau de 1 bloco de altura
            row = max(ground_row - 2, min(ground_row + 1, row + rng.choice([-1, 1])))

    # espinhos ocasionais sobre o chão
    for x in range(4, length_tiles - 12):
        if grid[ground_row][x] == '#' and rng.random() < 0.05:
            grid[ground_row - 1][x] = '^'

    # plataformas flutuantes decorativas / rotas alternativas
    for _ in range(length_tiles // 8):
        px = rng.randint(6, length_tiles - 14)
        py = rng.randint(3, ground_row - 3)
        plen = rng.randint(2, 4)
        for k in range(plen):
            if px + k < length_tiles - 1:
                grid[py][px + k] = '#'

    # Arena livre, com piso plano desde a entrada do encontro. Apenas adicionar
    # piso deixava blocos do terreno anterior sobrepondo o chefe e seus tiros.
    for gx in range(length_tiles - 12, length_tiles - 1):
        for gy in range(1, height_tiles - 1):
            grid[gy][gx] = '#' if gy >= ground_row else '.'

    # inimigos comuns espalhados pelo chão principal
    enemy_positions = sorted(rng.sample(range(6, length_tiles - 14), min(num_enemies, max(1, length_tiles - 20))))
    for ex in enemy_positions:
        grid[ground_row - 1][ex] = 'E'

    # jogador
    grid[ground_row - 1][2] = 'P'

    # gatilho de diálogo antes do chefe
    dialogue_x = length_tiles - 12
    grid[ground_row - 1][dialogue_x] = 'D'

    # chefe
    boss_x = length_tiles - 6
    grid[ground_row - 2][boss_x] = 'B'

    # saída (só ativa após derrotar o chefe)
    exit_x = length_tiles - 2
    grid[ground_row - 1][exit_x] = 'X'

    return [''.join(r) for r in grid], boss_x, ground_row


def build_legacy_levels():
    levels = []
    for i, boss_def in enumerate(BOSS_DEFS):
        length = LENGTHS[i]
        rows, boss_x_tile, ground_row = _generate_rows(
            length_tiles=length,
            height_tiles=HEIGHT_TILES,
            ground_row=GROUND_ROW,
            seed=1000 + i * 37,
            num_enemies=3 + i,
        )
        levels.append({
            "index": i,
            "name": f"Fase {i + 1}: {boss_def['subject']}",
            "ascii_map": rows,
            "boss": boss_def,
            "ability_reward": ABILITY_ORDER[i],
            "intro_dialogue": INTRO_DIALOGUES[i],
            "boss_dialogue": BOSS_DIALOGUES[i],
            "victory_dialogue": VICTORY_DIALOGUES[i],
        })
    return levels


ABILITY_ORDER = [
    Ability.DOUBLE_JUMP,
    Ability.DASH,
    Ability.WALL_CLIMB,
    Ability.RANGED_SHOT,
    Ability.SHIELD,
    None,  # o chefe final não concede novo poder, apenas encerra o jogo
]


INTRO_DIALOGUES = [
    [("Aluno(a)", "A Sala de Iniciação parece... estranhamente colorida."),
     ("RomerBug", "A aula começa de terno. Mas eu também treino para correr!"),
     ("Aluno(a)", "Ok, isso não é nada assustador. Nada mesmo.")],
    [("Aluno(a)", "O laboratório de Python cheira a café requeimado e cobras."),
     ("Prof. Python", "print('Você não vai passar da minha indentação perfeita.')"),
     ("Aluno(a)", "Eu... só uso 4 espaços, prometo!")],
    [("Aluno(a)", "A sala de POO tem herança em todo lugar. Literalmente."),
     ("Prof. Java", "public class VoceVaiPerder extends Aluno { }"),
     ("Aluno(a)", "Isso nem compila e mesmo assim dá medo.")],
    [("Aluno(a)", "Aqui cheira a ponteiro solto e memória vazando."),
     ("Prof. C", "Segmentation fault... na sua coragem."),
     ("Aluno(a)", "Eu só queria fazer um free() na minha ansiedade.")],
    [("Aluno(a)", "A biblioteca de dados está organizada demais. É assustador."),
     ("Prof. SQL", "SELECT * FROM alunos WHERE coragem > 0; -- 0 linhas retornadas."),
     ("Aluno(a)", "Vou fazer um JOIN com minha coragem escondida.")],
    [("Aluno(a)", "O núcleo do sistema. É aqui que tudo começou."),
     ("Prof. Assembly", "MOV medo, TODOS_OS_REGISTRADORES"),
     ("Aluno(a)", "Chegou a hora do boot final. Vamos formatar esse vírus.")],
]

BOSS_DIALOGUES = [
    [("RomerBug", "Prepare-se para a prova... e para meus aviões de papel!"),
     ("Aluno(a)", "E essa medalha na sua mesa, professor?"),
     ("RomerBug", "Quando minha vida chegar à metade, você vai conhecer o SpeedBug!")],
    [("Prof. Python", "Nada de ponto e vírgula vai te salvar aqui.")],
    [("Prof. Java", "Prepare-se para um NullPointerException de dor.")],
    [("Prof. C", "Cuidado com o buffer overflow dos meus ataques.")],
    [("Prof. SQL", "Isso é um DELETE FROM sua_paciencia;")],
    [("Prof. Assembly", "Sem abstrações. Só você, eu, e registradores.")],
]

VICTORY_DIALOGUES = [
    [("SpeedBug", "Ufa... você cruzou a linha de chegada. O vírus perdeu!"),
     ("Aluno(a)", "Boa corrida, RomerBug! Agora vou saltar ainda mais alto."),
     ("Sistema", "Habilidade adquirida: Pulo Duplo!")],
    [("Prof. Python", "Meu... código... está... sem exceções..."),
     ("Aluno(a)", "Bom jogo, professor. Vou usar isso com sabedoria."),
     ("Sistema", "Habilidade adquirida: Dash Veloz!")],
    [("Prof. Java", "Fatal Error: professor.encerrar()..."),
     ("Aluno(a)", "Aprendi a escalar qualquer herança agora."),
     ("Sistema", "Habilidade adquirida: Escalada de Parede!")],
    [("Prof. C", "Core dumped... foi... uma... boa... aula..."),
     ("Aluno(a)", "Vou apontar meus ponteiros para o bem agora."),
     ("Sistema", "Habilidade adquirida: Tiro de Ponteiro!")],
    [("Prof. SQL", "COMMIT; -- fim da transação, aluno..."),
     ("Aluno(a)", "Seus dados vão descansar em paz, professor."),
     ("Sistema", "Habilidade adquirida: Escudo de Dados!")],
    [("Prof. Assembly", "HALT."),
     ("Aluno(a)", "O vírus foi formatado. A escola está livre!"),
     ("Diretora", "Você salvou a escola, aluno! Parabéns, formando(a) de honra!")],
]
