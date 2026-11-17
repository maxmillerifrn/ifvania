"""Fábricas por registro, sem substitutos silenciosos para tipos desconhecidos."""
from entidades.inimigo import Inimigo
from entidades.bug_combate import BugCombate, BugGuarda, BugRetransmissor, BugArquivo, BugRepetidor


CONSTRUTORES_INIMIGOS = {'bug': Inimigo, 'combate': BugCombate,
                        'guarda': BugGuarda, 'retransmissor': BugRetransmissor,
                        'arquivo': BugArquivo,
                        'repetidor': BugRepetidor,
                        'lancador': lambda x, y: BugCombate(x, y, lancador=True)}


def criar_inimigo(tipo, x, y):
    if tipo not in CONSTRUTORES_INIMIGOS:
        raise ValueError(f'Tipo de inimigo desconhecido: {tipo}')
    return CONSTRUTORES_INIMIGOS[tipo](x, y)


def criar_chefe(tipo, *argumentos, **opcoes):
    from entidades.chefes_professores import CLASSES_CHEFES
    if tipo not in CLASSES_CHEFES:
        raise ValueError(f'Tipo de chefe desconhecido: {tipo}')
    return CLASSES_CHEFES[tipo](*argumentos, **opcoes)
