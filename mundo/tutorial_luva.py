"""Objetivos observáveis no primeiro confronto real; sem física paralela."""
import pygame


class TutorialLuva:
    def __init__(self, jogador, fase):
        self.origem = jogador.rect.x
        self.alvo = min(fase.inimigos, key=lambda inimigo: inimigo.rect.x, default=None)
        self.concluido = False
        self.tempo_final = 240
        jogador.acoes_luva.clear()
        jogador.protecao_inicial = True
        self.fonte = pygame.font.Font(None, 22)
        self.texto = ''

    def atualizar(self, jogador):
        if abs(jogador.rect.x-self.origem) >= 45:
            jogador.acoes_luva.add('movimento')
        etapas = (
            ('movimento', 'Um bug! A/D ou setas: mova-se e procure espaço.'),
            ('guarda', 'Q: erga a luva. A proteção automática responde ao primeiro impacto frontal.'),
            ('esquiva', 'Solte Q. SHIFT: esquive pela investida; aguarde a recuperação.'),
            ('ataque', 'X / K / clique: toque e solte para socar. Segure para um golpe forte.'),
            ('combo', 'Encadeie três toques. Cima + golpe: ascendente. Baixo no ar: mergulho.'),
        )
        for acao, texto in etapas:
            if acao not in jogador.acoes_luva:
                self.texto = texto
                return
        if self.alvo is not None and self.alvo.vivo:
            self.texto = 'Derrote o bug! Bloqueie pela frente; solte Q e ataque para contra-atacar.'
            return
        jogador.protecao_inicial = False
        self.texto = 'A luva nos protegeu. Agora preciso encontrar a saída e avisar Max.'
        self.tempo_final -= 1
        self.concluido = self.tempo_final <= 0

    def desenhar(self, superficie):
        if self.concluido or not self.texto:
            return
        imagem = self.fonte.render(self.texto, True, (191, 249, 229))
        caixa = imagem.get_rect(midtop=(superficie.get_width()//2, 177)).inflate(24, 20)
        pygame.draw.rect(superficie, (13, 29, 38), caixa, border_radius=7)
        pygame.draw.rect(superficie, (69, 144, 133), caixa, 1, border_radius=7)
        superficie.blit(imagem, imagem.get_rect(center=caixa.center))
