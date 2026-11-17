"""Guarda frontal com o cabo tensionado; resistência e quebra legíveis."""


class DefesaMouse:
    RESISTENCIA_MAXIMA = 100
    CUSTO_ACERTO = 26
    JANELA_ACERTO = 12
    DURACAO_QUEBRA = 48

    def __init__(self):
        self.ativa = False
        self.resistencia = self.RESISTENCIA_MAXIMA
        self.janela_acerto = 0
        self.espera_recuperacao = 0
        self.quebra = 0
        self.brilho = 0

    def iniciar(self):
        if self.quebra or self.resistencia <= 0:
            return False
        self.ativa = True
        return True

    def cancelar(self):
        self.ativa = False

    def update(self):
        self.janela_acerto = max(0, self.janela_acerto-1)
        self.quebra = max(0, self.quebra-1)
        self.brilho = max(0, self.brilho-1)
        self.espera_recuperacao = max(0, self.espera_recuperacao-1)
        if not self.ativa and not self.espera_recuperacao and not self.quebra:
            self.resistencia = min(self.RESISTENCIA_MAXIMA, self.resistencia+1)

    def receber(self, dano):
        if not self.ativa:
            return False
        if self.janela_acerto:
            return True
        custo = self.CUSTO_ACERTO*dano
        if self.resistencia < custo:
            self.resistencia = 0
            self.quebra = self.DURACAO_QUEBRA
            self.espera_recuperacao = 60
            self.ativa = False
            return False
        self.resistencia -= custo
        self.espera_recuperacao = 45
        self.janela_acerto = self.JANELA_ACERTO
        self.brilho = 10
        return True
