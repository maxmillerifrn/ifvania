"""Avatar ficcional de Ricardo Rodrigues: luta corporal e raios pela cabeça."""
import pygame
from entidades.chefe import Chefe
from entidades.romer_bug import RomerBug
from entidades.poderes_chefes import RaioBrilhante
from sistema import recursos


class MenteBrilhante(RomerBug):
    def __init__(self,*argumentos,**opcoes):
        super().__init__(*argumentos,**opcoes)
        poses = recursos.load_character_frames([f'chefes/mente_brilhante/pose_{i}.png' for i in range(6)])
        direcoes = {1:poses,-1:[recursos.espelhar_quadro(p) for p in poses]}
        for forma in ('romerbug','speedbug'):
            self.poses_corpo[forma] = direcoes
            self.figuras_formas[forma] = {direcao:[quadros[0],quadros[3]] for direcao,quadros in direcoes.items()}
            self.figuras_movimento[forma] = {direcao:[quadros[1],quadros[2]]*3 for direcao,quadros in direcoes.items()}
        self._animate_form()

    def choose_attack(self,jogador):
        distancia = abs(jogador.rect.centerx-self.rect.centerx)
        if distancia > 180:
            return 'raio' if self.ciclo_combate % 2 else 'barrigada'
        return ('cruzado','chute','barrigada','raio')[self.ciclo_combate % 4]

    def take_damage(self,quantidade,recuo=(0,0)):
        if not self.ativo or not self.vivo:
            return
        Chefe.take_damage(self,quantidade,recuo)
        self.etapa = min(2,self.etapa)
        if not self.vivo:
            self.image = self.poses_corpo['romerbug'][self.direcao_olhar][0]
        if self.vivo and self.estado_ataque not in ('executar','recuperar') and self.interrupcoes < 2:
            self.interrupcoes += 1
            self.estado_ataque = 'recuo'
            self.temporizador_ataque = 10
            self.velocidade.x = max(-4,min(4,recuo[0]))

    def origem_raio(self):
        # Cabeça da apresentação de 80 px, não o topo do corpo lógico de 40.
        return pygame.Vector2(self.rect.centerx+self.direcao_investida*6,self.rect.bottom-72)

    def lancar_especial(self,jogador):
        origem = self.origem_raio()
        direcao = pygame.Vector2(jogador.rect.center)-origem
        if not direcao.length_squared(): direcao.update(self.direcao_investida,0)
        self.projeteis.add(RaioBrilhante(origem,direcao))
