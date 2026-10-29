"""Professores da sequência escolar, sem comportamento de inimigo."""
import recursos
import configuracoes
from entidades.personagem import Personagem


class Professor(Personagem):
    ESCALA_VISUAL = configuracoes.ESCALA_VISUAL_PERSONAGEM
    NOMES = {'max': 'Professor Max', 'romerito': 'Professor Romerito'}

    def __init__(self, x, y, identidade):
        super().__init__(x, y, *configuracoes.TAMANHO_PERSONAGEM, vida=1)
        self.nome = self.NOMES[identidade]
        self.quadros = recursos.load_character_frames(
            [f'professores/{identidade}_{i}.png' for i in range(2)])
        self.image = self.quadros[0]
        self.dano_contato = 0
        self.instante_animacao = 0

    def update(self):
        self.instante_animacao += 1
        self.image = self.quadros[(self.instante_animacao // 30) % 2]
