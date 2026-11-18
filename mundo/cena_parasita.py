"""Fuga do último bug, fusão e expulsão; relógio controlado pela aplicação."""
import math
import pygame
from sistema import recursos
from interface import tema


class CenaParasita:
    def __init__(self, fase, jogador, modo):
        self.fase, self.jogador, self.modo = fase, jogador, modo
        self.instante = 0
        self.quadros = recursos.load_character_frames([f'inimigos/bug_humanoide/pose_{i}.png' for i in range(4)])
        self.origem = pygame.Vector2(getattr(fase, 'origem_fusao', fase.chefe.rect.midbottom))
        self.destino = pygame.Vector2(fase.chefe.rect.midbottom)
        self.altura_visual = jogador.get_draw_image().get_height()
        self.torax = self.destino-pygame.Vector2(0,self.altura_visual*0.5)
        self.direcao_corrida = 1 if self.destino.x >= self.origem.x else -1
        self.corrida = max(45, min(240, round(self.origem.distance_to(self.destino)/5)))
        self.duracao = self.corrida+90 if modo == 'fusao' else 150
        jogador.cancelar_combate()
        jogador.velocidade.update(0,0)
        jogador.projeteis.empty()
        fase.chefe.projeteis.empty()

    def ponto_corrida(self):
        fracao = min(1,self.instante/self.corrida)
        ponto = self.origem.lerp(self.destino,fracao)
        if fracao < 1:
            x,y = self.fase._grounded_spawn(round(ponto.x)-20,round(ponto.y)-40)
            ponto.y = y+40
        return ponto

    def update(self):
        self.instante += 1
        if self.modo == 'fusao':
            ponto = self.ponto_corrida()
            foco = pygame.Rect(0,0,40,40)
            foco.midbottom = ponto
            self.fase.camera.update(foco)
        if self.modo == 'fusao' and self.instante >= self.corrida+45:
            self.fase.infectado = True
        if self.modo == 'libertacao' and self.instante >= 35:
            self.fase.professor_liberto = True
            self.fase.professor_humano.rect.topleft = self.fase.chefe.rect.topleft
            self.fase.professor_humano.posicao.update(self.fase.chefe.rect.topleft)
        return self.instante >= self.duracao

    def draw(self, superficie):
        self.fase.draw(superficie)
        self.jogador.draw(superficie,self.fase.camera,mostrar_sempre=True)
        if self.modo == 'fusao':
            fracao = min(1,self.instante/self.corrida)
            ponto = self.ponto_corrida()
            if fracao >= 1:
                progresso_fusao = min(1,(self.instante-self.corrida)/45)
                ponto = self.destino.lerp(self.torax,progresso_fusao)
            escala = 1 if fracao < 1 else max(0.05,1-(self.instante-self.corrida)/45)
            indice = 1+(self.instante//6)%2
            cor = (109,239,131)
            titulo = 'O ÚLTIMO BUG NÃO ESTÁ FUGINDO...'
            if fracao >= 1: titulo = 'ELE ESTÁ SE FUNDINDO A ROMERITO!'
            visivel = self.instante < self.corrida+45
        else:
            fracao = min(1,max(0,(self.instante-20)/65))
            ponto = self.destino+pygame.Vector2(100*fracao,-45*math.sin(fracao*math.pi/2))
            escala = 1
            indice = 3
            cor = (163,109,238)
            titulo = 'ROMERITO ESTÁ LIVRE — VÍNCULO ROMPIDO'
            visivel = 20 <= self.instante < 90
        quadro = recursos.imagem_apresentacao(self.quadros[indice],(self.altura_visual,self.altura_visual))
        imagem = pygame.transform.smoothscale(quadro,(max(1,round(self.altura_visual*escala)),max(1,round(self.altura_visual*escala))))
        if self.modo == 'fusao' and self.direcao_corrida < 0:
            imagem = pygame.transform.flip(imagem,True,False)
        centro = ponto-self.fase.camera.deslocamento
        if visivel:
            if self.modo == 'libertacao': imagem.set_alpha(max(0,255-round(fracao*100)))
            superficie.blit(imagem,imagem.get_rect(midbottom=centro))
        if self.modo == 'fusao' and self.instante >= self.corrida:
            mistura = min(1,(self.instante-self.corrida)/45)
            corpo = self.fase.camera.apply(self.fase.chefe.rect)
            imagem_chefe = self.fase.chefe.get_draw_image().copy()
            imagem_chefe.set_alpha(round(255*mistura))
            superficie.blit(imagem_chefe,imagem_chefe.get_rect(midbottom=corpo.midbottom))
            for indice in range(18):
                angulo = indice*math.tau/18+self.instante*0.15
                raio = 44*(1-mistura)
                foco = self.torax-self.fase.camera.deslocamento
                ponto = (round(foco.x+math.cos(angulo)*raio),round(foco.y+math.sin(angulo)*raio))
                pygame.draw.circle(superficie,cor,ponto,2)
        if self.modo == 'libertacao' and self.instante >= 85:
            dispersao = self.instante-85
            for indice in range(42):
                angulo = indice*2.399
                raio = dispersao*(0.7+indice%6/5)
                ponto = self.destino+pygame.Vector2(100,-45-self.altura_visual/2)+pygame.Vector2(math.cos(angulo)*raio,math.sin(angulo)*raio)
                ponto -= self.fase.camera.deslocamento
                tamanho = max(1,5-dispersao//15)
                if dispersao < 65: pygame.draw.rect(superficie,cor,(round(ponto.x),round(ponto.y),tamanho,tamanho))
        faixa = pygame.Rect(0,0,superficie.get_width(),48)
        pygame.draw.rect(superficie,tema.TINTA,faixa)
        fonte = self.fase.fonte_infeccao
        texto = fonte.render(titulo,True,cor)
        superficie.blit(texto,texto.get_rect(center=faixa.center))
