"""Criação validada das cenas, com dependências fornecidas pela campanha."""
from mundo.escola import FaseEscolar
from mundo.fase import Fase
from mundo.campus_virtual import CampusVirtual


class FabricaCenas:
    def __init__(self, eventos, progresso=None):
        self._construtores = {
            'escola': FaseEscolar,
            'fase': lambda dados_fase: Fase(dados_fase, eventos=eventos, progresso=progresso),
            'campus': lambda setor, chegada='inicio': CampusVirtual(setor, progresso, chegada, eventos),
        }

    def registrar(self, tipo_cena, construtor):
        if not tipo_cena or not callable(construtor):
            raise ValueError('Cena exige identificador e construtor chamável')
        if tipo_cena in self._construtores:
            raise ValueError(f'Tipo de cena já registrado: {tipo_cena}')
        self._construtores[tipo_cena] = construtor

    def criar(self, tipo_cena, **configuracao):
        try:
            construtor = self._construtores[tipo_cena]
        except KeyError:
            raise ValueError(f'Tipo de cena desconhecido: {tipo_cena}') from None
        if tipo_cena == 'escola' and configuracao.get('ambiente') not in FaseEscolar.NOMES:
            raise ValueError(f'Ambiente escolar desconhecido: {configuracao.get("ambiente")}')
        return construtor(**configuracao)
