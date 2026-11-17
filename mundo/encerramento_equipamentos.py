"""Desligamento seguro encenado, sem cronômetro de falha ou combate residual."""
import pygame
from sistema import recursos
from interface import tema


class EncerramentoEquipamentos:
    DURACAO = 180

    def __init__(self, fase, jogador):
        self.fase, self.jogador = fase, jogador
        self.instante = 0
        self.reserva_desligada = False
        self.fonte = pygame.font.Font(None, 25)
        self.manutencao = recursos.load_image('apresentacao/chefes/guardioes/francisco.png')
        jogador.cancelar_combate()
        jogador.projeteis.empty()
        jogador.velocidade.update(0, 0)

    def update(self):
        self.instante += 1
        if self.instante >= 55:
            self.fase.arte.etapa_aula = 'desligado'
        self.reserva_desligada = self.instante >= 115
        return self.instante >= self.DURACAO

    def draw(self, superficie):
        self.fase.draw(superficie)
        self.jogador.draw(superficie, self.fase.camera)
        x = 860-min(100, self.instante)
        superficie.blit(self.manutencao, self.manutencao.get_rect(midbottom=(x, self.fase.Y_PISO)))
        nobreak = pygame.Rect(820, self.fase.Y_PISO-52, 38, 52)
        pygame.draw.rect(superficie, (31, 43, 49), nobreak, border_radius=4)
        pygame.draw.circle(superficie, (57, 76, 80) if self.reserva_desligada else tema.AMBAR, (839, nobreak.top+12), 4)
        caixa_usb = pygame.Rect(570, self.fase.Y_PISO-35, 75, 35)
        pygame.draw.rect(superficie, (46, 62, 68), caixa_usb, border_radius=3)
        pygame.draw.rect(superficie, tema.AMBAR, caixa_usb.inflate(-5, -5), 1)
        pygame.draw.rect(superficie, (163, 175, 174), (594, caixa_usb.top+10, 22, 10))
        pygame.draw.line(superficie, (172, 77, 72), caixa_usb.topleft, caixa_usb.bottomright, 2)
        imagem = self.fonte.render('USB isolado', True, tema.PAPEL)
        superficie.blit(imagem, imagem.get_rect(midbottom=caixa_usb.midtop))
        if self.reserva_desligada:
            sombra = pygame.Surface(superficie.get_size(), pygame.SRCALPHA)
            sombra.fill((9, 19, 30, 75))
            superficie.blit(sombra, (0, 0))
        tema.panel(superficie, pygame.Rect(170, 85, 620, 105), tema.CIANO)
        linhas = ('Pessoas liberadas · rede isolada',
                  'Equipamentos: desligados' if self.instante >= 55 else 'Manutenção: encerrando equipamentos',
                  'Nobreak: desligado · saída segura' if self.reserva_desligada else 'Alimentação de reserva: aguardando')
        for indice, texto in enumerate(linhas):
            tema.text(superficie, self.fonte, texto, (190, 102+indice*26), tema.PAPEL)
