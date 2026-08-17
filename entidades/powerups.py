from enum import Enum, auto

class Habilidade(Enum):
    DOUBLE_DASH = auto()
    DASH = auto()
    WALL_CLIMB = auto()
    RANGED_SHOT = auto()
    SHIELD = auto()

HABILIDADE_NOME = {
    Habilidade.DOUBLE_DASH:"Pulo Duplo",
    Habilidade.DASH:"Dash veloz",
    Habilidade.WALL_CLIMB:"Escalada de parede",
    Habilidade.RANGED_SHOT:"Tiro certeiro",
    Habilidade.SHIELD:"Escudo de Dados"
}

HABILIDADES_HOTKEYS = {
    Habilidade.DOUBLE_DASH:"Espaço 2x no ar",
    Habilidade.DASH: "Shift",
    Habilidade.WALL_CLIMB: "Segure na parede",
    Habilidade.RANGED_SHOT: "F",
    Habilidade.SHIELD: "Q"
}

class PowerUp():

    def __init__(self,x,
                 y,
                 habilidade:Habilidade,
                 imagem):
        self.habilidade = habilidade
        self.image = imagem
        