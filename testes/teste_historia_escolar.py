"""Aceite do prólogo: caminhada real, interações e passagem ao mundo virtual."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')

from collections import defaultdict
import unittest
import pygame
import configuracoes
from entidades.professor import Professor
from jogo import (Jogo, ESTADO_JOGANDO, ESTADO_DIALOGO, ESTADO_CARTAO_FASE,
                  ESTADO_ABDUCAO, ESTADO_PAUSA)
from mundo.escola import FaseEscolar
from mundo.dados_escola import DESCOBERTA_MOUSE


class TestesHistoriaEscolar(unittest.TestCase):
    def setUp(self):
        self.jogo = Jogo()
        self.teclas = defaultdict(bool)

    def tearDown(self):
        pygame.quit()

    def key(self, tecla):
        eventos = [pygame.event.Event(pygame.KEYDOWN, key=tecla)]
        if tecla == pygame.K_x:
            eventos.append(pygame.event.Event(pygame.KEYUP, key=tecla))
        return self.jogo._process_events(eventos)

    def finish_dialogue(self):
        for _ in range(80):
            if not self.jogo.caixa_dialogo.ativo:
                return
            self.key(pygame.K_e)
            self.jogo._update(self.teclas, [])
        self.fail('Diálogo não terminou')

    def start_corridor(self, personagem='boy'):
        self.jogo.personagem_escolhido = personagem
        self.jogo._start_story()
        self.finish_dialogue()
        self.assertEqual(self.jogo.estado, ESTADO_CARTAO_FASE)
        self.key(pygame.K_RETURN)

    def walk_to(self, x):
        teclas = defaultdict(bool, {pygame.K_d: True})
        for _ in range(600):
            if self.jogo.jogador.rect.x >= x:
                break
            self.jogo._update(teclas, [])
        self.assertGreaterEqual(self.jogo.jogador.rect.x, x)

    def enter_lab(self):
        self.walk_to(self.jogo.fase.porta_a28.x - 40)
        eventos = self.key(pygame.K_e)
        self.jogo._update(self.teclas, eventos)
        self.assertEqual(self.jogo.fase.ambiente, 'lab')

    def begin_encounter(self):
        self.walk_to(630)
        eventos = self.key(pygame.K_e)
        self.jogo._update(self.teclas, eventos)
        self.assertEqual(self.jogo.estado, ESTADO_DIALOGO)

    def test_both_protagonists_walk_entire_route_and_get_mouse_only_after_discovery(self):
        for personagem in ('boy', 'menina'):
            with self.subTest(character=personagem):
                self.start_corridor(personagem)
                jogador = self.jogo.jogador
                self.assertFalse(jogador.chicote_desbloqueado)
                self.assertIsNone(self.jogo.fase.chefe)
                self.enter_lab()
                self.assertIs(self.jogo.jogador, jogador)
                self.assertGreater(self.jogo.fase.mapa_blocos.largura, 0)
                self.begin_encounter()
                self.finish_dialogue()
                self.assertEqual(self.jogo.estado, ESTADO_ABDUCAO)
                for _ in range(self.jogo.duracao_abducao):
                    self.jogo._update(self.teclas, [])
                self.assertEqual(self.jogo.estado, ESTADO_DIALOGO)
                self.assertEqual(self.jogo.caixa_dialogo.linhas, self.jogo.caixa_dialogo.resolve_lines(DESCOBERTA_MOUSE))
                self.assertEqual(self.jogo.jogador.personagem, personagem)
                self.assertIs(self.jogo.jogador, jogador)
                self.assertFalse(jogador.chicote_desbloqueado)
                jogador._try_melee()
                self.assertEqual(jogador.temporizador_golpe, 0)
                chefe = self.jogo.fase.chefe
                inicial = (chefe.vida, chefe.temporizador_ataque, jogador.vida, jogador.rect.copy())
                for _ in range(200):
                    self.jogo._update(self.teclas, [])
                self.assertEqual((chefe.vida, chefe.temporizador_ataque, jogador.vida, jogador.rect), inicial)
                self.assertFalse(chefe.ativo)
                self.finish_dialogue()
                self.assertTrue(jogador.chicote_desbloqueado)
                self.assertFalse(jogador.habilidades)
                self.assertEqual(self.jogo.estado, ESTADO_CARTAO_FASE)
                self.key(pygame.K_RETURN)
                eventos = self.key(pygame.K_x)
                self.jogo._update(self.teclas, eventos)
                self.assertGreater(jogador.temporizador_golpe, 0)
                self.assertEqual(jogador.personagem, personagem)

    def test_intro_shows_max_and_corrupts_monitors_when_ai_revolts(self):
        self.jogo._start_story()
        ambiente = self.jogo.fase
        self.assertEqual(ambiente.ambiente, 'classroom')
        self.assertEqual(next(iter(ambiente.professores)).nome, 'Professor Max')
        self.assertFalse(ambiente.corrompido)
        from mundo.dados_fases import INDICE_CORRUPCAO_HISTORIA
        self.jogo.caixa_dialogo.indice = INDICE_CORRUPCAO_HISTORIA
        self.jogo._update(self.teclas, [])
        self.assertTrue(ambiente.corrompido)
        self.assertEqual(ambiente.instantes, 0)
        self.assertFalse(self.jogo.jogador.chicote_desbloqueado)

    def test_interaction_requires_proximity_and_e_and_fires_once(self):
        self.start_corridor()
        corredor = self.jogo.fase
        self.assertIsNone(corredor.update(self.jogo.jogador,
                                         [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)])[0])
        self.walk_to(corredor.porta_a28.x-40)
        self.assertIsNone(corredor.update(self.jogo.jogador, [])[0])
        evento = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)
        self.assertEqual(corredor.update(self.jogo.jogador, [evento])[0], 'enter_lab')
        self.assertIsNone(corredor.update(self.jogo.jogador, [evento])[0])
        laboratorio = FaseEscolar('lab')
        jogador = self.jogo.jogador
        jogador.rect.x = 630
        self.assertIsNone(laboratorio.update(jogador, [])[0])
        self.assertEqual(laboratorio.update(jogador, [evento])[0], 'school_encounter')
        self.assertIsNone(laboratorio.update(jogador, [evento])[0])

    def test_pause_and_dialogue_freeze_school_and_abduction(self):
        self.start_corridor()
        self.enter_lab()
        self.begin_encounter()
        ambiente = self.jogo.fase
        professor = next(iter(ambiente.professores))
        retrato_estado = (ambiente.instantes, professor.instante_animacao, self.jogo.jogador.rect.copy())
        for _ in range(100):
            self.jogo._update(self.teclas, [])
        self.assertEqual((ambiente.instantes, professor.instante_animacao, self.jogo.jogador.rect), retrato_estado)
        self.finish_dialogue()
        self.jogo._update(self.teclas, [])
        temporizador = self.jogo.temporizador_abducao
        self.key(pygame.K_ESCAPE)
        self.assertEqual(self.jogo.estado, ESTADO_PAUSA)
        for _ in range(120):
            self.jogo._update(self.teclas, [])
        self.assertEqual(self.jogo.temporizador_abducao, temporizador)
        self.key(pygame.K_ESCAPE)
        self.assertEqual(self.jogo.estado, ESTADO_ABDUCAO)
        self.jogo._update(self.teclas, [])
        self.assertEqual(self.jogo.temporizador_abducao, temporizador+1)

    def test_weapon_stays_locked_after_school_respawn(self):
        self.start_corridor()
        jogador = self.jogo.jogador
        jogador.respawn(*self.jogo.fase.surgimento_jogador)
        jogador._try_melee()
        self.assertFalse(jogador.chicote_desbloqueado)
        self.assertEqual(jogador.temporizador_golpe, 0)

    def test_romerito_approaches_and_player_recoils_before_transport_without_losing_life(self):
        self.start_corridor()
        self.enter_lab()
        self.begin_encounter()
        self.finish_dialogue()
        professor = next(iter(self.jogo.fase.professores))
        professor_inicial = professor.rect.x
        jogador_inicial = self.jogo.jogador.rect.x
        for _ in range(18):
            self.jogo._update(self.teclas, [])
        self.assertLess(professor.rect.x, professor_inicial)
        self.assertLess(self.jogo.jogador.rect.x, jogador_inicial)
        self.assertEqual(self.jogo.jogador.vida, self.jogo.jogador.vida_maxima)
        self.assertFalse(self.jogo.jogador.chicote_desbloqueado)

    def test_school_geometry_supports_characters_and_camera_stays_in_bounds(self):
        self.jogo._start_story()
        jogador = self.jogo.jogador
        for nome_ambiente in ('classroom', 'corridor', 'lab'):
            ambiente = FaseEscolar(nome_ambiente)
            jogador.respawn(*ambiente.surgimento_jogador)
            for corpo in [jogador, *ambiente.professores]:
                self.assertEqual(corpo.rect.size, configuracoes.TAMANHO_PERSONAGEM)
                self.assertFalse(any(corpo.rect.colliderect(s) for s in ambiente.mapa_blocos.solidos))
                self.assertTrue(any(corpo.rect.move(0, 1).colliderect(s) for s in ambiente.mapa_blocos.solidos))
            for x in (-500, 0, 1000, 3000):
                jogador.rect.x = x
                ambiente.camera.update(jogador.rect)
                self.assertGreaterEqual(ambiente.camera.deslocamento.x, 0)
                self.assertLessEqual(ambiente.camera.deslocamento.x,
                                     max(0, ambiente.mapa_blocos.largura-configuracoes.LARGURA_TELA))

    def test_teachers_have_transparent_complete_frames_and_same_body_contract(self):
        for identidade in Professor.NOMES:
            professor = Professor(0, 0, identidade)
            self.assertEqual(professor.rect.size, configuracoes.TAMANHO_PERSONAGEM)
            for imagem in professor.quadros:
                self.assertEqual(imagem.get_size(), configuracoes.TAMANHO_PERSONAGEM)
                self.assertEqual(imagem.get_bounding_rect().bottom, configuracoes.TAMANHO_PERSONAGEM[1])
                self.assertEqual(imagem.get_at((0, 0)).a, 0)

    def test_every_school_dialogue_fits_in_panel_and_window_can_close_during_abduction(self):
        from mundo.dados_fases import INTRODUCAO_HISTORIA
        from mundo.dados_escola import DIALOGO_ENCONTRO
        for _, texto in INTRODUCAO_HISTORIA + DIALOGO_ENCONTRO + DESCOBERTA_MOUSE:
            self.assertLessEqual(len(self.jogo.caixa_dialogo._wrap(texto, 810)), 3)
        self.jogo.estado = ESTADO_ABDUCAO
        self.jogo._process_events([pygame.event.Event(pygame.QUIT)])
        self.assertFalse(self.jogo.executando)


if __name__ == '__main__':
    unittest.main()
