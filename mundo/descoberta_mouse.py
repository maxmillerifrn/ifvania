"""Encenação corporal de retirar a luva da mochila e vestir o protótipo.

O nome da classe mantém compatibilidade com ferramentas e a campanha.
"""
from entidades.visual_equipamento import pose_equipamento


class DescobertaMouse:
    DURACAO = 180

    def __init__(self):
        self.instante = 0
        self.visivel = False
        self.aguardando_conclusao = False
        self.mostrar_cartao = True

    @property
    def concluida(self):
        return self.instante >= self.DURACAO

    @property
    def indice_pose(self):
        return 6+min(5, self.instante//30)

    def update(self, indice_fala):
        self.visivel = indice_fala >= 2 or self.aguardando_conclusao
        if self.visivel:
            self.instante = min(self.DURACAO, self.instante+1)

    def draw(self, superficie, camera, jogador):
        if not self.visivel:
            return
        imagem = pose_equipamento(jogador.personagem, self.indice_pose, jogador.direcao_olhar < 0)
        destino = camera.apply(jogador.rect)
        superficie.blit(imagem, imagem.get_rect(midbottom=destino.midbottom))
