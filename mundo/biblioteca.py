"""Cenário em Pygame e objetivos locais da biblioteca virtual.

Materiais inspirados nas capturas 17-24-38 e 17-24-56 de referencia/ifrn.
O desenho não define colisões; apoios sólidos continuam no mapa de blocos.
"""
import pygame
from sistema import recursos
from interface import tema
from sistema.habilidades import Habilidade
from mundo.dados_biblioteca import DIALOGO_MODULO
from mundo.escola_sombria import EscolaSombria
from mundo.camera import Camera
from sistema.comandos import houve_interacao
from sistema.eventos_campanha import ObjetivoConcluido


class Biblioteca(EscolaSombria):
    def __init__(self, largura, altura, y_piso, eventos=None, progresso=None):
        super().__init__(largura, altura, y_piso)
        self.fundo_ifrn = recursos.load_image('cenarios/biblioteca_ifrn.png')
        self.largura = largura
        self.eventos = eventos
        self.paineis = [pygame.Rect(15*32, y_piso-40, 30, 40),
                        pygame.Rect(27*32, 9*32-40, 30, 40),
                        pygame.Rect(45*32, 9*32-40, 30, 40)]
        self.consultados = set()
        self.bilhete_lido = False
        self.bilhete = pygame.Rect(35*32, 7*32-26, 26, 26)
        self.modulo_obtido = False
        if progresso:
            salvos = progresso.objetivos_da_fase('biblioteca')
            self.consultados = {indice for indice in range(3) if f'arquivo_{indice}' in salvos}
            self.bilhete_lido = 'bilhete' in salvos
            self.modulo_obtido = 'modulo' in salvos
        self.modulo = pygame.Rect(18*32, y_piso-34, 30, 34)
        self.portao = pygame.Rect(59*32, 32, 32, y_piso-32)
        self.ajuda = ''
        self.camada = pygame.Surface((960, altura))
        self.camera_cenario = Camera(largura, altura)
        self.sombra_fundo = pygame.Surface((960, altura), pygame.SRCALPHA)
        self.sombra_fundo.fill((8, 17, 25, 45))

    def draw_background(self, superficie, camera):
        self.camera_cenario.deslocamento.update(camera.deslocamento.x, 0)
        self._desenhar_ambiente(self.camada, self.camera_cenario)
        superficie.blit(self.camada, (0, -round(camera.deslocamento.y)))

    def desenhar_objetivos(self, superficie):
        # Coluna central livre dos painéis de vida, habilidades e chefe.
        tema.panel(superficie, (240, 61, 330, 27), tema.AMBAR)
        rotulo = self.ajuda or f'ARQUIVOS {len(self.consultados)}/3  |  E consultar  |  siga os terminais'
        superficie.blit(self.fonte.render(tema.fit_text(self.fonte, rotulo, 310), True, (230, 221, 193)), (250, 69))

    def _desenhar_ambiente(self, superficie, camera):
        superficie.fill((35, 45, 53))
        for coluna in range(0, self.largura, self.fundo_ifrn.get_width()):
            x = round(coluna-camera.deslocamento.x)
            superficie.blit(self.fundo_ifrn, (x, self.y_piso-352))
        superficie.blit(self.sombra_fundo, (0, 0))

    def desenhar_interativos(self, superficie, camera):
        """Sinais no mesmo plano dos sólidos, após desenhar as plataformas."""
        for indice, painel in enumerate(self.paineis):
            destino = camera.apply(painel)
            pygame.draw.rect(superficie, (19, 30, 37), destino)
            cor = (119, 213, 176) if indice in self.consultados else (232, 194, 123)
            pygame.draw.rect(superficie, cor, destino.inflate(-8, -12), 2)
            superficie.blit(self.fonte.render(str(indice+1), True, cor), (destino.x+11, destino.y+12))
            rotulo = 'LIDO' if indice in self.consultados else f'ARQUIVO {indice+1}'
            self._rotular(superficie, destino, rotulo, cor)
            if indice in self.consultados:
                self._rotular(superficie, destino.move(0, 69), 'E · retorno à entrada' if indice == 0 else 'E · elevador ao piso', tema.CIANO)
        destino_bilhete = camera.apply(self.bilhete)
        pygame.draw.rect(superficie, (183, 193, 164) if self.bilhete_lido else (245, 220, 154), destino_bilhete)
        self._rotular(superficie, destino_bilhete, 'BILHETE · E', tema.AMBAR)
        if not self.modulo_obtido:
            destino = camera.apply(self.modulo)
            pygame.draw.rect(superficie, (85, 206, 211), destino, 2)
            pygame.draw.line(superficie, (226, 236, 220), destino.midbottom, destino.midtop, 3)
            self._rotular(superficie, destino, 'SALTO DUPLO', tema.CIANO)
        if len(self.consultados) < 3:
            destino = camera.apply(self.portao)
            pygame.draw.rect(superficie, (102, 83, 70), destino)
            for y in range(destino.top+8, destino.bottom-15, 24):
                pygame.draw.line(superficie, (228, 191, 122), (destino.x, y), (destino.right-1, y+15), 3)
            self._rotular(superficie, destino, f'ARQUIVOS {len(self.consultados)}/3', tema.AMBAR)

    def _rotular(self, superficie, destino, texto, cor):
        imagem = self.fonte.render(texto, True, cor)
        rotulo = imagem.get_rect(midbottom=(destino.centerx, destino.top-6))
        pygame.draw.rect(superficie, (14, 24, 30), rotulo.inflate(10, 6))
        superficie.blit(imagem, rotulo)

    def interagir(self, jogador, eventos, solidos):
        self.ajuda = ''
        alvos = [(self.modulo, 'Módulo: E para examinar')] if not self.modulo_obtido else []
        alvos += [(painel, 'E para consultar o arquivo') for painel in self.paineis]
        perto = [alvo for alvo, _ in alvos
                 if jogador.rect.colliderect(alvo.inflate(55, 30))
                 and jogador.rect.bottom <= alvo.bottom+16]
        for alvo, dica in alvos:
            if alvo in perto:
                self.ajuda = dica
        if not houve_interacao(eventos):
            return None
        if jogador.rect.colliderect(self.bilhete.inflate(50, 30)):
            self.bilhete_lido = True
            self.registrar('bilhete')
            return [('Aluno(a)', 'Bilhete de monitoria: entender uma dúvida com alguém vale mais que entregar uma resposta sem saber explicar.')]
        if not self.modulo_obtido and self.modulo in perto:
            self.modulo_obtido = True
            self.registrar('modulo')
            jogador.grant_ability(Habilidade.SALTO_DUPLO, aumentar_vida=False)
            return DIALOGO_MODULO
        for indice, painel in enumerate(self.paineis):
            if painel in perto and indice in self.consultados:
                jogador.cancelar_combate()
                jogador.rect.midbottom = (100 if indice == 0 else painel.centerx, self.y_piso)
                jogador.posicao.update(jogador.rect.topleft)
                jogador.velocidade.update(0, 0)
                self.ajuda = 'Elevador estabilizado · retorno ao piso seguro'
                return None
            if painel in perto and indice not in self.consultados:
                self.consultados.add(indice)
                self.registrar(f'arquivo_{indice}')
                textos = ('Registro: a mesma assinatura aparece em várias máquinas. Vencer Romerito não desligou a IA.',
                          'Mapa recuperado: existe uma passagem pelo pátio. Os colegas precisam dessa rota.',
                          'Inventário: o servidor usa nobreak. Cortar só a tomada não basta.')
                if len(self.consultados) == 3:
                    solidos.remove(self.portao)
                return [('Aluno(a)', textos[indice])]
        return None

    def registrar(self, identificador):
        if self.eventos:
            self.eventos.emitir(ObjetivoConcluido('biblioteca', identificador))
