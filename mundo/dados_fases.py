"""Campanha disponível: A28 e biblioteca; conteúdo antigo permanece isolado."""
from entidades.chefe import DEFINICOES_CHEFES
from sistema.configuracoes import TAMANHO_BLOCO
from mundo.dados_biblioteca import criar_biblioteca
from mundo.dados_guardioes import criar_fases_guardioes


FALA_CORRUPCAO_INTRODUCAO = ('Aluno(a)', 'Espere, professor! A tela diz que ela não vai permitir ser desligada!')

FALA_EXECUCAO_TAREFA = ('Aluno(a)', 'Conectei o pendrive. O arquivo já começou a executar... Professor, isso estava na tarefa?')
FALA_MEMORIA_TAREFA = ('Aluno(a)', 'Ontem cheguei em casa depois da aula. Pedi para uma IA fazer a atividade enquanto testava nossa luva assistiva.')
FALA_RETORNO_TAREFA = ('Aluno(a)', 'A energia oscilou durante os testes da luva. Vi a tarefa pronta e salvei no pendrive sem conferir.')

INTRODUCAO_HISTORIA = [
    ('Aluno(a)', 'Professor Max, trouxe a atividade. Depois da apresentação, quero mostrar como ficou nossa luva!'),
    ('Professor Max', 'Ótimo, {player}. Depois vemos os testes de preensão. Primeiro, vamos entender seu código.'),
    ('Professor Max', 'Turma, abram a atividade de programação orientada a objetos. Vamos apresentar e explicar o código.'),
    ('Professor Max', 'Como você fez essa parte, {player}? Vamos entender juntos antes de executar.'),
    FALA_MEMORIA_TAREFA,
    FALA_RETORNO_TAREFA,
    FALA_EXECUCAO_TAREFA,
    ('Professor Max', 'Ele se identifica como IFVania: Inteligência Federal Virtual de Aprendizagem Neural e Inteligência Artificial.'),
    ('Aluno(a)', 'A tela promete uma aula sem dúvidas, sem atrasos... e sem fim.'),
    ('Professor Max', 'Vou desligá-la para analisarmos o problema juntos.'),
    FALA_CORRUPCAO_INTRODUCAO,
    ('Professor Max', 'Perdi o controle! Ela passou pela rede para os computadores da escola.'),
    ('Aluno(a)', 'Meus colegas ficaram imóveis. Minha cabeça gira, mas ainda consigo escolher.'),
    ('Professor Max', 'Ela está hipnotizando as pessoas e provocando alucinações. Afaste-se das telas!'),
    ('Aluno(a)', 'Se eu desligar os computadores, isso acaba?'),
    ('Professor Max', 'Precisamos cortar a energia dos equipamentos. Primeiro, tire as pessoas daqui.'),
    ('Professor Max', 'Procure Romerito no A28, {player}. Eu vou tentar liberar a turma.'),
]
INDICE_CORRUPCAO_HISTORIA = INTRODUCAO_HISTORIA.index(FALA_CORRUPCAO_INTRODUCAO)
INDICE_EXECUCAO_HISTORIA = INTRODUCAO_HISTORIA.index(FALA_EXECUCAO_TAREFA)
INDICE_MEMORIA_HISTORIA = INTRODUCAO_HISTORIA.index(FALA_MEMORIA_TAREFA)



DIALOGO_REENCONTRO = [
    ('Aluno(a)', 'Professor Romerito! Encontrei o senhor! Precisamos sair deste mundo virtual.'),
    ('Professor Romerito', '{player}, não vejo a hora de voltar às minhas viagens a Brasília e às minhas corridas.'),
    ('Professor Romerito', 'Eu não quero nunca mais passar por isso!'),
    ('Aluno(a)', 'Professor, cuidado! Um bug subiu no seu braço! O que está acontecendo com o senhor?'),
    ('Professor Romerito', 'Minha cabeça... não consigo controlar meu corpo!'),
]

DIALOGO_APOS_CHEFE = [
    ('Aluno(a)', 'Recalibrei os atuadores: Punho de Impacto! Segurar e soltar concentra mais força.'),
    ('Professor Romerito', 'Eu voltei, {player}, mas os outros continuam presos. Não dá para correr sozinho nessa.'),
    ('Aluno(a)', 'Vou procurar um caminho. O senhor ajuda quem chegar ao A28?'),
    ('Professor Romerito', 'Combinado. Busque o mapa de saída e os registros da rede na biblioteca.'),
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
        'identificador': 'a28',
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
    }, criar_biblioteca()] + criar_fases_guardioes()
