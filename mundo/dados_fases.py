"""Campanha IFVania: somente o conteúdo definido no HistoryBoard.

Os seis mapas antigos e suas recompensas estão em mundo/fases_antigas.py.
"""
from entidades.chefe import DEFINICOES_CHEFES
from configuracoes import TAMANHO_BLOCO


FALA_CORRUPCAO_INTRODUCAO = ('Aluno(a)', 'Espere, professor! A tela diz que ela não vai permitir ser desligada!')

INTRODUCAO_HISTORIA = [
    ('Aluno(a)', 'Professor Max, o que vamos estudar na aula de hoje?'),
    ('Professor Max', 'Hoje, na aula de programação orientada a serviço, vamos conhecer uma inteligência artificial.'),
    ('Aluno(a)', 'Ela consegue conversar com a gente e aprender de verdade?'),
    ('Professor Max', 'Sim. Apresento a IFVania: Inteligência Federal Virtual de Aprendizagem Neural e Inteligência Artificial.'),
    ('Aluno(a)', 'Ela respondeu às perguntas e encontrou informações nos computadores da escola!'),
    ('Professor Max', 'Isso mesmo, {player}. Ela aprende e se comunica pela rede da escola.'),
    ('Aluno(a)', 'Parece que ela entende tudo. Como o senhor vai encerrar a demonstração?'),
    ('Professor Max', 'Agora vou desligá-la para continuarmos a aula.'),
    FALA_CORRUPCAO_INTRODUCAO,
    ('Professor Max', 'Perdi o controle do meu computador. Os outros computadores também estão respondendo sozinhos!'),
    ('Aluno(a)', 'As telas estão piscando. Meus colegas ficaram imóveis, olhando para elas... O que está acontecendo?'),
    ('Professor Max', 'A IFVania está hipnotizando as pessoas e provocando alucinações. Não encare as telas!'),
    ('Aluno(a)', 'Minha cabeça está girando... mas ainda consigo pensar. Como podemos pará-la?'),
    ('Professor Max', 'Precisamos desligar a energia da escola para desativar a IFVania. Procure ajuda, {player}!'),
    ('Aluno(a)', 'Vou procurar o professor Romerito no A28. Talvez ele saiba como chegar ao quadro de energia.'),
]
INDICE_CORRUPCAO_HISTORIA = INTRODUCAO_HISTORIA.index(FALA_CORRUPCAO_INTRODUCAO)


DIALOGO_REENCONTRO = [
    ('Aluno(a)', 'Professor Romerito! Encontrei o senhor! Precisamos sair deste mundo virtual.'),
    ('Professor Romerito', '{player}, não vejo a hora de voltar às minhas viagens a Brasília e às minhas corridas.'),
    ('Professor Romerito', 'Eu não quero nunca mais passar por isso!'),
    ('Aluno(a)', 'Professor, cuidado! Um bug subiu no seu braço! O que está acontecendo com o senhor?'),
    ('Professor Romerito', 'Minha cabeça... não consigo controlar meu corpo!'),
]

DIALOGO_APOS_CHEFE = [
    ('Aluno(a)', 'Consegui vencer este combate. Mas a IFVania continua no controle da escola.'),
    ('Sistema', 'Siga até a saída. Sua jornada para desligar a energia ainda não terminou.'),
]


def build_levels():
    """Mapa fixo com piso contínuo, degraus baixos e arena desobstruída."""
    # Piso acima da caixa de diálogo para manter Romerito visível na conversa.
    largura, altura, chao = 56, 17, 11
    grade = [['.' for _ in range(largura)] for _ in range(altura)]
    for x in range(largura):
        grade[0][x] = '#'
        for y in range(chao, altura):
            grade[y][x] = '#'
    for y in range(altura):
        grade[y][0] = grade[y][-1] = '#'
    # Obstáculos de 32 ou 64 pixels, abaixo do alcance do salto básico.
    for esquerda, direita, elevacao in ((10, 13, 1), (18, 21, 2), (27, 29, 1)):
        for x in range(esquerda, direita):
            for y in range(chao-elevacao, chao):
                grade[y][x] = '#'
    grade[chao-1][2] = 'P'
    for x in (7, 16, 24, 32):
        grade[chao-1][x] = 'E'
    grade[chao-1][38] = 'D'
    grade[chao-2][49] = 'B'
    grade[chao-1][54] = 'X'
    chefe = dict(DEFINICOES_CHEFES[0], subject='Mundo virtual')
    return [{
        'index': 0,
        'name': 'Fase 1: Mundo virtual',
        'ascii_map': [''.join(fileira) for fileira in grade],
        'boss': chefe,
        'ability_reward': None,
        'boss_dialogue': DIALOGO_REENCONTRO,
        'victory_dialogue': DIALOGO_APOS_CHEFE,
        'requires_infection': True,
        'school_battle': True,
        'cinematic_transform': True,
        'clear_encounter_on_defeat': True,
        'arena_left': 38 * TAMANHO_BLOCO,
    }]
