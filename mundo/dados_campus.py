"""Campus lateral ficcional: conexões de jogo, não planta arquitetônica real."""
SETORES = {
    'convivencia': {'nome': 'Convivência · Biblioteca e ginásio', 'proximo': 'jardim', 'requisito': 'recreio',
                    'entradas': ((1200, 'Biblioteca', 1, 'a28'), (1800, 'Ginásio · Recreio em repetição', 2, 'biblioteca'))},
    'jardim': {'nome': 'Jardim · ponto de reunião', 'anterior': 'convivencia', 'proximo': 'informatica', 'requisito': 'recreio',
               'entradas': ((370, 'A28 · ponto seguro', None, None),)},
    'informatica': {'nome': 'Bloco de informática · M1 e M5', 'anterior': 'jardim', 'proximo': 'tecnico', 'requisito': 'copias',
                    'entradas': ((520, 'M1 · Laboratório das cópias', 3, 'recreio'), (1490, 'M5 · Rede sem saída', 4, 'copias'))},
    'tecnico': {'nome': 'Área técnica · acesso ao LIT', 'anterior': 'informatica',
                'entradas': ((1320, 'LIT · A última chamada', 5, 'rede'),)},
}

RETORNOS = {'a28': 'convivencia', 'biblioteca': 'convivencia', 'recreio': 'convivencia',
            'copias': 'informatica', 'rede': 'informatica', 'continuidade': 'tecnico'}

FALAS_CAMPUS = {
    'convivencia': [('Professor Romerito', 'Siga pelo corredor até a porta de madeira da biblioteca, {player}. Precisamos consultar os registros antes do ginásio.')],
    'jardim': [('Professor Romerito', 'A turma está segura aqui. Max ainda repete a aula no M1. Vá pelo bloco de informática.')],
    'informatica': [('Professor Max', 'A rotina de cópias parou. O cabo alcança os conectores: use E longe dos terminais. Falta isolar a rede no M5.')],
    'tecnico': [('Professor Max', 'A rede está isolada. O nobreak ainda alimenta o núcleo. Francisco está preso no guardião do LIT.')],
}
