"""Campanha antiga, fora do menu principal. Definição das 6 fases: mapas (gerados proceduralmente de forma determinística),
professores-chefe, textos de diálogo e habilidades concedidas.
"""
import random
from entidades.chefe import DEFINICOES_CHEFES
from habilidades import Habilidade

COMPRIMENTOS = [46, 52, 58, 64, 70, 78]
LINHA_CHAO = 14
ALTURA_BLOCOS = 17


def _generate_rows(comprimento_blocos, altura_blocos, linha_chao, semente, quantidade_inimigos):
    gerador_aleatorio = random.Random(semente)
    grade = [['.' for _ in range(comprimento_blocos)] for _ in range(altura_blocos)]

    # bordas do nível
    for x in range(comprimento_blocos):
        grade[0][x] = '#'
        grade[altura_blocos - 1][x] = '#'
    for y in range(altura_blocos):
        grade[y][0] = '#'
        grade[y][comprimento_blocos - 1] = '#'

    # chão principal, com pequenos degraus e vãos de 1 bloco (sempre pulável)
    x = 1
    fileira = linha_chao
    while x < comprimento_blocos - 1:
        grade[fileira][x] = '#'
        x += 1
        if x > 10 and x < comprimento_blocos - 12 and gerador_aleatorio.random() < 0.10:
            # vão pequeno (1 bloco) - sempre transponível a pé
            x += 1
        elif x > 8 and x < comprimento_blocos - 10 and gerador_aleatorio.random() < 0.12:
            # degrau de 1 bloco de altura
            fileira = max(linha_chao - 2, min(linha_chao + 1, fileira + gerador_aleatorio.choice([-1, 1])))

    # espinhos ocasionais sobre o chão
    for x in range(4, comprimento_blocos - 12):
        if grade[linha_chao][x] == '#' and gerador_aleatorio.random() < 0.05:
            grade[linha_chao - 1][x] = '^'

    # plataformas flutuantes decorativas / rotas alternativas
    for _ in range(comprimento_blocos // 8):
        px = gerador_aleatorio.randint(6, comprimento_blocos - 14)
        py = gerador_aleatorio.randint(3, linha_chao - 3)
        comprimento_pontas = gerador_aleatorio.randint(2, 4)
        for k in range(comprimento_pontas):
            if px + k < comprimento_blocos - 1:
                grade[py][px + k] = '#'

    # Arena livre, com piso plano desde a entrada do encontro. Apenas adicionar
    # piso deixava blocos do terreno anterior sobrepondo o chefe e seus tiros.
    for gx in range(comprimento_blocos - 12, comprimento_blocos - 1):
        for gy in range(1, altura_blocos - 1):
            grade[gy][gx] = '#' if gy >= linha_chao else '.'

    # inimigos comuns espalhados pelo chão principal
    posicoes_inimigos = sorted(gerador_aleatorio.sample(range(6, comprimento_blocos - 14), min(quantidade_inimigos, max(1, comprimento_blocos - 20))))
    for ex in posicoes_inimigos:
        grade[linha_chao - 1][ex] = 'E'

    # jogador
    grade[linha_chao - 1][2] = 'P'

    # gatilho de diálogo antes do chefe
    x_dialogo = comprimento_blocos - 12
    grade[linha_chao - 1][x_dialogo] = 'D'

    # chefe
    x_chefe = comprimento_blocos - 6
    grade[linha_chao - 2][x_chefe] = 'B'

    # saída (só ativa após derrotar o chefe)
    x_saida = comprimento_blocos - 2
    grade[linha_chao - 1][x_saida] = 'X'

    return [''.join(r) for r in grade], x_chefe, linha_chao


def build_legacy_levels():
    fases = []
    for i, definicao_chefe in enumerate(DEFINICOES_CHEFES):
        comprimento = COMPRIMENTOS[i]
        fileiras, coluna_chefe, linha_chao = _generate_rows(
            comprimento_blocos=comprimento,
            altura_blocos=ALTURA_BLOCOS,
            linha_chao=LINHA_CHAO,
            semente=1000 + i * 37,
            quantidade_inimigos=3 + i,
        )
        fases.append({
            "index": i,
            "name": f"Fase {i + 1}: {definicao_chefe['subject']}",
            "ascii_map": fileiras,
            "boss": definicao_chefe,
            "ability_reward": ORDEM_HABILIDADES[i],
            "intro_dialogue": DIALOGOS_INTRODUCAO[i],
            "boss_dialogue": DIALOGOS_CHEFES[i],
            "victory_dialogue": DIALOGOS_VITORIA[i],
        })
    return fases


ORDEM_HABILIDADES = [
    Habilidade.SALTO_DUPLO,
    Habilidade.ARRANCADA,
    Habilidade.ESCALADA_PAREDE,
    Habilidade.DISPARO_DISTANCIA,
    Habilidade.ESCUDO,
    None,  # o chefe final não concede novo poder, apenas encerra o jogo
]


DIALOGOS_INTRODUCAO = [
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

DIALOGOS_CHEFES = [
    [("RomerBug", "Prepare-se para a prova... e para meus aviões de papel!"),
     ("Aluno(a)", "E essa medalha na sua mesa, professor?"),
     ("RomerBug", "Quando minha vida chegar à metade, você vai conhecer o SpeedBug!")],
    [("Prof. Python", "Nada de ponto e vírgula vai te salvar aqui.")],
    [("Prof. Java", "Prepare-se para um NullPointerException de dor.")],
    [("Prof. C", "Cuidado com o buffer overflow dos meus ataques.")],
    [("Prof. SQL", "Isso é um DELETE FROM sua_paciencia;")],
    [("Prof. Assembly", "Sem abstrações. Só você, eu, e registradores.")],
]

DIALOGOS_VITORIA = [
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
