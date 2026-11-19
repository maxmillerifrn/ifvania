"""Continuidade de mochila/luva e congelamento da cena de equipamento."""
import os
os.environ.setdefault('SDL_VIDEODRIVER','dummy')
os.environ.setdefault('SDL_AUDIODRIVER','dummy')
import unittest
from collections import defaultdict
import pygame
from sistema.jogo import Jogo, ESTADO_PAUSA, ESTADO_DIALOGO, ESTADO_CARTAO_FASE
from sistema import recursos
from entidades.visual_equipamento import pose_equipamento


class TestesEquipamentoVisual(unittest.TestCase):
    def setUp(self):
        self.jogo = Jogo()
        self.teclas = defaultdict(bool)
        self.addCleanup(pygame.quit)

    def test_mochila_sai_em_casa_e_retorna_somente_ao_recolher(self):
        for personagem in ('boy','menina'):
            self.jogo.personagem_escolhido = personagem
            self.jogo._start_story()
            cena = self.jogo.introducao
            for indice, tempo, esperado in ((0,8,True),(0,8.2,False),(1,3,False),(2,12,False),
                                             (4,10,False),(5,1,False),(5,2.5,True)):
                cena.indice,cena.quadro = indice, round(tempo*60)
                self.assertEqual(cena.com_mochila, esperado)
                cena.desenhar(self.jogo.tela)

    def iniciar_equipamento(self):
        self.jogo._enter_virtual()
        self.jogo.caixa_dialogo.ativo = False
        self.jogo._grant_mouse()
        return self.jogo.descoberta_mouse

    def test_avanco_rapido_nao_pula_animacao_nem_habilita_ataque(self):
        cena = self.iniciar_equipamento()
        jogador = self.jogo.jogador
        origem = jogador.rect.copy()
        inimigos = [inimigo.rect.copy() for inimigo in self.jogo.fase.inimigos]
        poses = set()
        for _ in range(cena.DURACAO-1):
            eventos = self.jogo._process_events([pygame.event.Event(pygame.KEYDOWN,key=pygame.K_x)])
            self.jogo._update(self.teclas,eventos)
            poses.add(cena.indice_pose)
        self.assertEqual(poses, set(range(6,12)))
        self.assertEqual(self.jogo.estado,ESTADO_DIALOGO)
        self.assertFalse(jogador.chicote_desbloqueado)
        self.assertEqual(jogador.rect,origem)
        self.assertEqual([inimigo.rect for inimigo in self.jogo.fase.inimigos],inimigos)
        self.jogo._update(self.teclas,[])
        self.assertTrue(jogador.chicote_desbloqueado)
        self.assertEqual(self.jogo.estado,ESTADO_CARTAO_FASE)
        self.assertIsNone(self.jogo.descoberta_mouse)
        self.assertEqual(jogador.temporizador_golpe,0)

    def test_pausa_e_perda_de_foco_congelam_equipamento(self):
        cena = self.iniciar_equipamento()
        for _ in range(65): self.jogo._update(self.teclas,[])
        for evento in (pygame.event.Event(pygame.KEYDOWN,key=pygame.K_ESCAPE),
                       pygame.event.Event(pygame.WINDOWFOCUSLOST)):
            self.jogo._process_events([evento])
            self.assertEqual(self.jogo.estado,ESTADO_PAUSA)
            instante = cena.instante
            for _ in range(30):
                self.jogo._update(self.teclas,[])
                self.jogo._draw()
            self.assertEqual(cena.instante,instante)
            self.jogo._process_events([pygame.event.Event(pygame.KEYDOWN,key=pygame.K_ESCAPE)])
            self.jogo._update(self.teclas,[])
            self.assertEqual(cena.instante,instante+1)

    def test_poses_transparentes_e_luva_integrada_sem_mudar_corpo(self):
        for personagem in ('boy','menina'):
            for indice in range(24):
                imagem = pose_equipamento(personagem,indice)
                self.assertEqual(imagem.get_size(),(80,80))
                self.assertEqual(imagem.get_at((0,0)).a,0)
                self.assertGreater(imagem.get_bounding_rect().height,40)
            self.jogo.personagem_escolhido = personagem
            self.jogo._load_level(0,novo_jogador=True)
            jogador = self.jogo.jogador
            corpo = jogador.rect.copy()
            jogador.estado_animacao = 'idle'
            self.assertIs(jogador.get_draw_image(),pose_equipamento(personagem,12))
            jogador._try_melee()
            jogador.temporizador_golpe = jogador.chicote.DURACAO-8
            jogador._animate()
            self.assertIs(jogador.get_draw_image(),pose_equipamento(personagem,14))
            self.assertEqual(jogador.rect,corpo)

    def test_acesso_a28_reutiliza_panorama_sem_mudar_porta_e_colisoes(self):
        self.jogo._load_school('corridor',novo_jogador=True)
        fase = self.jogo.fase
        origem = recursos.load_image('cenarios/corredor_biblioteca.png')
        self.assertEqual(fase.corredor_a28.get_size(),origem.get_size())
        self.assertEqual(fase.corredor_a28.get_at((100,200)),origem.get_at((1819,200)))
        self.assertEqual(fase.porta_a28,pygame.Rect(1728,306,80,134))
        self.assertEqual(fase.Y_PISO,440)
        fase.draw(self.jogo.tela)
