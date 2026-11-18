"""Arquivo JSON versionado e substituição atômica; nunca serializa objetos Python."""
import json
import os
from pathlib import Path
from sistema.habilidades import Habilidade


class ArmazemSalvamento:
    def __init__(self, caminho=None):
        self.caminho = Path(caminho) if caminho else Path(__file__).resolve().parents[1]/'dados/salvamento.json'
        self.erro = ''

    def carregar(self):
        self.erro = ''
        try:
            dados = json.loads(self.caminho.read_text(encoding='utf-8'))
            if not self.validar(dados):
                raise ValueError('Formato de salvamento incompatível')
            return dados
        except FileNotFoundError:
            return None
        except (OSError, ValueError, TypeError, KeyError):
            self.erro = 'Não foi possível ler o jogo salvo.'
            return None

    @staticmethod
    def validar(dados):
        if not isinstance(dados, dict) or dados.get('versao') != 1:
            return False
        if not isinstance(dados.get('nome'), str) or len(dados['nome']) > 40:
            return False
        if dados.get('personagem') not in ('boy', 'menina'):
            return False
        if type(dados.get('vida_maxima')) is not int or not 1 <= dados['vida_maxima'] <= 100:
            return False
        habilidades = dados.get('habilidades')
        if not isinstance(habilidades, list) or any(h not in Habilidade.__members__ for h in habilidades):
            return False
        cena = dados.get('cena', {})
        if not isinstance(cena, dict) or cena.get('tipo') not in ('fase', 'campus'):
            return False
        if type(cena.get('indice')) is not int or not 0 <= cena['indice'] < 6:
            return False
        if cena['tipo'] == 'campus' and cena.get('setor') not in ('convivencia', 'jardim', 'informatica', 'tecnico'):
            return False
        for chave in ('infectado', 'dialogo_exibido'):
            if chave in cena and type(cena[chave]) is not bool:
                return False
        if 'inimigos_ativos' in cena and (not isinstance(cena['inimigos_ativos'],list) or any(type(i) is not int or not -1 <= i <= 100 for i in cena['inimigos_ativos'])):
            return False
        posicao = cena.get('posicao')
        if not isinstance(posicao, list) or len(posicao) != 2 or any(type(n) is not int or not 0 <= n <= 20000 for n in posicao):
            return False
        progresso = dados.get('progresso')
        if not isinstance(progresso, dict):
            return False
        for chave in ('chefes', 'fases'):
            if not isinstance(progresso.get(chave), list) or any(not isinstance(i, str) for i in progresso[chave]):
                return False
        objetivos = progresso.get('objetivos')
        return isinstance(objetivos, list) and all(isinstance(o, list) and len(o) == 2 and all(isinstance(i, str) for i in o) for o in objetivos)

    def salvar(self, dados):
        if not self.validar(dados):
            self.erro = 'Dados de salvamento inválidos.'
            return False
        temporario = self.caminho.with_suffix('.temporario')
        try:
            self.caminho.parent.mkdir(parents=True, exist_ok=True)
            with temporario.open('w', encoding='utf-8') as arquivo:
                json.dump(dados, arquivo, ensure_ascii=False, indent=2)
                arquivo.flush()
                os.fsync(arquivo.fileno())
            temporario.replace(self.caminho)
            self.erro = ''
            return True
        except OSError:
            self.erro = 'Não foi possível gravar o checkpoint.'
            return False
