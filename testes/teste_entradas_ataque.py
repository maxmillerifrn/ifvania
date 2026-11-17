"""Alternativas de ataque, combinação de entradas e locomoção durante a carga."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
from collections import defaultdict
import unittest
import pygame
from entidades.jogador import Jogador
from sistema import configuracoes
from sistema.jogo import Jogo, ESTADO_JOGANDO


class TestesEntradasAtaque(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((960, 540))
        self.teclas = defaultdict(bool)
        self.piso = [pygame.Rect(0, 352, 3000, 100)]

    def tearDown(self):
        pygame.quit()

    def eventos(self, comando):
        if comando == 'mouse':
            return (pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(400, 250)),
                    pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=(400, 250)))
        return (pygame.event.Event(pygame.KEYDOWN, key=comando),
                pygame.event.Event(pygame.KEYUP, key=comando))

    def novo_jogador(self, personagem='boy'):
        jogador = Jogador(200, 312, personagem=personagem)
        jogador.no_chao = True
        return jogador

    def test_todos_comandos_disparam_rapido_e_carregado_na_soltura(self):
        for comando in (pygame.K_x, pygame.K_k, 'mouse'):
            for duracao, dano in ((2, 1), (configuracoes.TEMPO_CARGA, 2)):
                with self.subTest(comando=comando, dano=dano):
                    jogador = self.novo_jogador()
                    pressionar, soltar = self.eventos(comando)
                    jogador.handle_input(self.teclas, [pressionar])
                    for _ in range(duracao):
                        jogador.update(self.piso, [])
                    self.assertEqual(jogador.temporizador_golpe, 0)
                    jogador.handle_input(self.teclas, [soltar])
                    self.assertGreater(jogador.temporizador_golpe, 0)
                    self.assertEqual(jogador.chicote.dano, dano)

    def test_outro_comando_nao_reinicia_nem_solta_carga_em_andamento(self):
        jogador = self.novo_jogador()
        inicio, fim = self.eventos(pygame.K_k)
        jogador.handle_input(self.teclas, [inicio])
        for _ in range(20): jogador.update(self.piso, [])
        for comando in ('mouse', pygame.K_x):
            jogador.handle_input(self.teclas, self.eventos(comando))
            self.assertTrue(jogador.carregando)
            self.assertEqual(jogador.carga, 20)
            self.assertEqual(jogador.temporizador_golpe, 0)
        jogador.handle_input(self.teclas, [fim])
        self.assertGreater(jogador.temporizador_golpe, 0)

    def test_carga_mantem_caminhada_e_salto_dos_dois_protagonistas(self):
        for personagem in ('boy', 'menina'):
            for comando in (pygame.K_k, 'mouse'):
                jogador = self.novo_jogador(personagem)
                jogador.handle_input(self.teclas, [self.eventos(comando)[0]])
                imagens = set()
                for _ in range(40):
                    jogador.handle_input(defaultdict(bool, {pygame.K_d: True}), [])
                    jogador.update(self.piso, [])
                    self.assertEqual(jogador.estado_animacao, 'walk')
                    imagens.add(pygame.image.tostring(jogador.image, 'RGBA'))
                self.assertGreater(jogador.rect.x, 240)
                self.assertGreater(len(imagens), 2)
                self.assertTrue(jogador.carregando)
                jogador.handle_input(self.teclas, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)])
                jogador.update(self.piso, [])
                self.assertEqual(jogador.estado_animacao, 'jump')
                self.assertTrue(jogador.carregando)

    def test_pausa_e_foco_cancelam_carga_das_novas_entradas(self):
        jogo = Jogo()
        jogo._load_level(0, novo_jogador=True)
        for comando in (pygame.K_k, 'mouse'):
            for interrupcao in (pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE),
                                pygame.event.Event(pygame.WINDOWFOCUSLOST)):
                jogo.maquina_estados.estado = ESTADO_JOGANDO
                inicio, fim = self.eventos(comando)
                eventos = jogo._process_events([inicio])
                jogo._update(self.teclas, eventos)
                self.assertTrue(jogo.jogador.carregando)
                jogo._process_events([interrupcao])
                self.assertFalse(jogo.jogador.carregando)
                jogo.maquina_estados.estado = ESTADO_JOGANDO
                jogo._update(self.teclas, jogo._process_events([fim]))
                self.assertEqual(jogo.jogador.temporizador_golpe, 0)

    def test_botao_direito_e_repeticao_nao_disparam(self):
        jogador = self.novo_jogador()
        jogador.handle_input(self.teclas, [pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=3),
                                         pygame.event.Event(pygame.KEYDOWN, key=pygame.K_k, repeat=True)])
        self.assertFalse(jogador.carregando)
        jogador.chicote_desbloqueado = False
        jogador.handle_input(self.teclas, [self.eventos('mouse')[0], self.eventos(pygame.K_k)[0]])
        self.assertFalse(jogador.carregando)
