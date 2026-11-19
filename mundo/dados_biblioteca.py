"""Percurso e diálogos da biblioteca, separados da primeira fase."""
from sistema.configuracoes import TAMANHO_BLOCO

DIALOGO_MODULO = [
    ('Aluno(a)', 'Módulo de Repetição? Ele consegue executar um segundo impulso no ar!'),
    ('Sistema', 'Salto duplo disponível. Pressione salto, solte e pressione outra vez no ar.'),
    ('Aluno(a)', 'Vou praticar aqui antes de subir às estantes. O piso de baixo parece seguro.'),
]


def criar_biblioteca():
    largura, altura, chao = 78, 19, 14
    grade = [['.'] * largura for _ in range(altura)]
    for y in range(altura):
        grade[y][0] = grade[y][-1] = '#'
    for x in range(largura):
        grade[0][x] = '#'
        for y in range(chao, altura):
            grade[y][x] = '#'
    # Escada inicial acessível sem habilidade; segundo patamar exige dois impulsos.
    for esquerda, direita, topo in ((11, 14, 12), (25, 29, 9), (34, 38, 7), (43, 47, 9)):
        for x in range(esquerda, direita):
            grade[topo][x] = '#'
    grade[13][2] = 'P'
    grade[12][68] = 'B'
    grade[13][60] = 'D'
    grade[13][76] = 'X'
    for x in (51, 56):
        grade[13][x] = 'E'
    return {
        'identificador': 'biblioteca',
        'index': 1, 'name': 'Fase 2: Biblioteca dos arquivos perdidos',
        'ascii_map': [''.join(linha) for linha in grade],
        'boss': dict(name='Mente Brilhante', subject='Guardião dos registros', color=(119, 153, 162),
                     health=18, boss_type='mente_brilhante'),
        'ability_reward': None, 'library': True,
        'arena_left': 60*TAMANHO_BLOCO, 'clear_encounter_on_defeat': True,
        'boss_dialogue': [
            ('Mente Brilhante', 'A IFVania trancou o catálogo na minha cabeça. Não consigo liberar o mapa!'),
            ('Aluno(a)', 'Professor Ricardo? Vou romper esse vínculo. A turma precisa da saída.'),
        ],
        'victory_dialogue': [('Aluno(a)', 'Otimizei o controle: R ativa Sobrecarga por cinco segundos. Depois, os atuadores precisam esfriar.'),
            ('Professor Ricardo', 'Minha cabeça voltou a ser minha. O mapa está liberado; vamos tirar todos daqui.'),
            ('Aluno(a)', 'Achei o mapa e o inventário. O servidor tem uma alimentação de reserva.'),
            ('Professor Romerito', 'E há colegas presos perto da quadra, {player}. Precisamos abrir o pátio.'),
            ('Aluno(a)', 'Vou buscar o caminho. A IFVania ainda está ativa.'),
        ],
    }
