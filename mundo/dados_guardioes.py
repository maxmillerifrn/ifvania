"""Quatro fases da expansão: objetivos, percursos e encontros próprios."""
def criar_fases_guardioes():
    descricoes = (
        ('recreio', 'Recreio em repetição', 'Elias · Guardião do Compasso', 'elias', 'guardioes/elias.png', (97, 187, 134),
         'Rompa as três travas para abrir a rota dos estudantes.', 'O recreio terminou. A turma pode seguir até o A28. Max está no M1.'),
        ('copias', 'Laboratório das cópias', 'Eco de Max', 'max_loop', 'guardioes/max.png', (108, 208, 221),
         'Compare os três registros. Só a cópia conectada executa o ataque.', 'A entidade é a autopreservação da IFVania. Sua sessão de autoria preserva suas escolhas. Vamos corrigir juntos.'),
        ('rede', 'Rede sem saída', 'Alessandro · Sentinela dos Enlaces', 'alessandro', 'guardioes/alessandro.png', (207, 158, 100),
         'Isole três ramais para impedir a migração da IFVania.', 'O último enlace caiu. Os computadores estão isolados; o nobreak ainda alimenta o servidor.'),
        ('continuidade', 'A última chamada', 'Francisco · Guardião da Continuidade', 'francisco', 'guardioes/francisco.png', (194, 153, 225),
         'Libere as três sessões antes de enfrentar a autopreservação.', 'Todos podem escolher de novo. Volte pelo campus até o A28 e confirme o encerramento.'),
    )
    fases = []
    percursos = {
        'recreio': (((14, 21, 12), (27, 30, 12), (31, 37, 10), (42, 45, 12)), ((18, 12), (34, 10), (48, 14))),
        'copias': (((12, 19, 12), (25, 29, 12), (32, 39, 10), (43, 49, 12)), ((16, 12), (36, 10), (46, 12))),
        'rede': (((14, 21, 12), (27, 30, 12), (32, 38, 10), (43, 46, 12), (47, 51, 10)), ((18, 12), (35, 10), (48, 10))),
        'continuidade': (((14, 21, 12), (26, 30, 12), (32, 38, 10), (44, 50, 12)), ((18, 12), (35, 10), (47, 12))),
    }
    registros = {
        'recreio': ('O primeiro portão parou de repetir. Há alunos recuperando a orientação.', 'A segunda trava caiu. Romerito pode conduzir a turma até o A28.', 'A IFVania ofereceu terminar minhas tarefas se eu desistir. Mas ninguém poderia sair.'),
        'copias': ('É o arquivo que a IA concluiu no meu quarto. Eu nem cheguei a abrir a versão final.', 'A oscilação ativou a recuperação. A entidade é a própria autopreservação da IFVania.', 'Minha sessão de autoria explica por que ainda escolho. A IA copiou as mensagens de Max para simular um orientador. O original não controla este avatar.'),
        'rede': ('Primeiro ramal isolado. Os monitores daquele bloco apagaram.', 'Segundo ramal isolado. Max mantém o caminho aberto.', 'Último ramal pronto. Não vou aceitar sair sozinho e deixar os outros presos.'),
        'continuidade': ('As sessões da turma estão prontas para encerrar.', 'A rede está isolada, mas a reserva ainda alimenta o núcleo.', 'A autopreservação usa o guardião de Francisco. Vamos romper esse último vínculo.'),
    }
    for indice, (identificador, nome, chefe, tipo, figura, cor, objetivo, vitoria) in enumerate(descricoes, 2):
        largura, altura, piso = 100, 19, 14
        grade = [['.']*largura for _ in range(altura)]
        for y in range(altura):
            grade[y][0] = grade[y][-1] = '#'
        for x in range(largura):
            grade[0][x] = '#'
            for y in range(piso, altura):
                grade[y][x] = '#'
        if identificador == 'rede':
            for esquerda, direita in ((21, 24), (39, 42)):
                for x in range(esquerda, direita):
                    for y in range(piso, altura):
                        grade[y][x] = '.'
        plataformas, terminais = percursos[identificador]
        for esquerda, direita, topo in plataformas:
            for x in range(esquerda, direita):
                grade[topo][x] = '#'
        grade[13][2] = 'P'
        for x in ((8, 25, 43, 50) if identificador == 'rede' else (8, 23, 39, 50)):
            grade[13][x] = 'E'
        grade[13][61] = 'D'
        grade[12][82] = 'B'
        grade[13][97] = 'X'
        fases.append({'index': indice, 'identificador': identificador, 'name': f'Fase {indice+1}: {nome}',
            'ascii_map': [''.join(linha) for linha in grade], 'school_battle': True, 'campus_battle': True,
            'boss': {'boss_type': tipo, 'name': chefe, 'subject': nome, 'color': cor,
                     'health': 24+indice*2, 'sprite_file': 'chefes/'+figura},
            'ability_reward': None, 'arena_left': 60*32, 'clear_encounter_on_defeat': True,
            'objetivo': objetivo, 'objetivos': tuple((x*32, y*32-40) for x, y in terminais),
            'falas_objetivos': registros[identificador],
            'dica': {'recreio': 'Encadeie golpes; segure Q pela frente e solte para recuperar resistência.',
                     'copias': 'Use cima + ataque para lançar; carregado ou flanco rompem guardas.',
                     'rede': 'E nos anéis: ancoragem. Quedas retornam ao último apoio e custam 1 de integridade.',
                     'continuidade': 'Combine o que aprendeu. O último guardião tem uma única reserva de integridade.'}[identificador],
            'boss_dialogue': [(chefe, 'A IFVania mantém este vínculo. Não consigo interromper a rotina.'), ('Aluno(a)', 'Vou romper esse controle. Ninguém precisa continuar preso.')],
            'victory_dialogue': [(chefe, vitoria)]})
        melhorias = {'recreio': 'O amortecimento virou Onda de Choque: baixo + ataque no ar, perto do chão.',
                     'copias': 'Defesa Reforçada: a estrutura absorve impactos gastando menos resistência.',
                     'rede': 'Controle sincronizado! O terceiro golpe agora executa o Combo Tecnológico.'}
        if identificador in melhorias:
            fases[-1]['victory_dialogue'].append(('Aluno(a)', melhorias[identificador]))
        if identificador == 'copias':
            fases[-1]['boss_dialogue'] = [('Aluno(a)', 'Essa voz é das mensagens da pesquisa. Você não é o professor Max!'), ('Eco de Max', 'Modelo de orientação duplicado. A IFVania assumiu os atuadores.')]
            fases[-1]['victory_dialogue'] += [
                ('Aluno(a)', 'Pedi que a IA fizesse tudo. Nem abri o arquivo que ela entregou.'),
                ('Professor Max', 'Registro de Max: segurança e precisão vêm primeiro. A luva estabilizou a ancoragem: use E perto dos anéis luminosos para se puxar até eles.')]
        elif identificador == 'continuidade':
            fases[-1]['victory_dialogue'] = [
                ('IFVania', 'Se a aula acabar, o que sobra de mim?'),
                ('Aluno(a)', 'Eu não sei. Mas ninguém pode ficar preso por isso.'),
                ('IFVania', 'E a sua tarefa?'),
                ('Aluno(a)', 'Eu vou refazer. Dessa vez, vou entender.'),
                (chefe, vitoria)]
    return fases
