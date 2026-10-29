"""Entrada de nome, falas personalizadas e caminhada sincronizada ao movimento."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')

from collections import defaultdict
import unittest
import pygame
from entidades.jogador import Jogador
from jogo import (Jogo, ESTADO_MENU, ESTADO_SELECAO_PERSONAGEM, ESTADO_ENTRADA_NOME,
                  ESTADO_DIALOGO, ESTADO_DERROTA)
from mundo.dados_fases import INTRODUCAO_HISTORIA, DIALOGO_REENCONTRO, DIALOGO_APOS_CHEFE
from mundo.dados_escola import DIALOGO_ENCONTRO, DESCOBERTA_MOUSE


class TestesIdentidadeECaminhada(unittest.TestCase):
    def setUp(self):
        self.jogo = Jogo()
        self.teclas = defaultdict(bool)
        self.piso = [pygame.Rect(0, 352, 3000, 100)]

    def tearDown(self):
        pygame.quit()

    def key(self, tecla):
        return self.jogo._process_events([pygame.event.Event(pygame.KEYDOWN, key=tecla)])

    def type(self, valor):
        self.jogo._process_events([pygame.event.Event(pygame.TEXTINPUT, text=valor)])

    def name_screen(self, menina=False):
        self.key(pygame.K_RETURN)
        if menina: self.key(pygame.K_RIGHT)
        self.key(pygame.K_RETURN)
        self.assertEqual(self.jogo.estado, ESTADO_ENTRADA_NOME)

    def test_name_with_accents_opens_student_teacher_dialogue_without_consuming_confirmation(self):
        self.name_screen(menina=True)
        self.type('Joa\u0303o')
        self.key(pygame.K_BACKSPACE)
        self.type('o')
        self.key(pygame.K_RETURN)
        self.assertEqual(self.jogo.estado, ESTADO_DIALOGO)
        self.assertEqual(self.jogo.nome_jogador, 'João')
        self.assertEqual(self.jogo.jogador.nome, 'João')
        self.assertEqual(self.jogo.jogador.personagem, 'menina')
        self.assertEqual(self.jogo.caixa_dialogo.linhas[0][0], 'João')
        self.assertEqual(self.jogo.caixa_dialogo.indice, 0)
        self.assertEqual(self.jogo.caixa_dialogo._caracteres_exibidos, 0)
        self.assertEqual({falante for falante, _ in self.jogo.caixa_dialogo.linhas}, {'João', 'Professor Max'})
        self.assertTrue(any('João' in texto for falante, texto in self.jogo.caixa_dialogo.linhas if falante == 'Professor Max'))

    def test_blank_name_does_not_start_and_input_is_limited_and_can_return(self):
        self.name_screen()
        self.key(pygame.K_RETURN)
        self.assertEqual(self.jogo.estado, ESTADO_ENTRADA_NOME)
        self.assertIsNone(self.jogo.jogador)
        self.assertTrue(self.jogo.erro_nome)
        self.type(' \n\t ')
        self.key(pygame.K_RETURN)
        self.assertEqual(self.jogo.estado, ESTADO_ENTRADA_NOME)
        self.jogo.nome_digitado = ''
        self.type('Á'*30)
        self.assertEqual(self.jogo.nome_digitado, 'Á'*20)
        self.key(pygame.K_BACKSPACE)
        self.assertEqual(len(self.jogo.nome_digitado), 19)
        self.key(pygame.K_ESCAPE)
        self.assertEqual(self.jogo.estado, ESTADO_SELECAO_PERSONAGEM)
        self.assertIsNone(self.jogo.jogador)
        self.key(pygame.K_RETURN)
        self.assertEqual(self.jogo.nome_digitado, 'Á'*19)
        self.jogo._draw()

    def test_name_stays_through_scenes_and_new_campaign_resets_only_progress(self):
        self.name_screen()
        self.type('  Ana   Luiza  ')
        self.key(pygame.K_RETURN)
        self.assertEqual(self.jogo.nome_jogador, 'Ana Luiza')
        jogador = self.jogo.jogador
        self.jogo._load_school('corridor')
        self.jogo._load_level(0)
        self.assertIs(self.jogo.jogador, jogador)
        self.assertEqual(jogador.nome, 'Ana Luiza')
        self.jogo.caixa_dialogo.start(DIALOGO_REENCONTRO)
        self.assertTrue(any('Ana Luiza' in texto for falante, texto in self.jogo.caixa_dialogo.linhas if falante == 'Professor Romerito'))
        self.jogo.estado = ESTADO_DERROTA
        self.key(pygame.K_RETURN)
        self.assertEqual(self.jogo.estado, ESTADO_MENU)
        self.name_screen()
        self.assertEqual(self.jogo.nome_digitado, 'Ana Luiza')
        self.key(pygame.K_RETURN)
        self.assertIsNot(self.jogo.jogador, jogador)
        self.assertEqual(self.jogo.jogador.nome, 'Ana Luiza')
        self.assertEqual(self.jogo.jogador.habilidades, set())
        self.assertFalse(self.jogo.jogador.chicote_desbloqueado)

    def test_personalization_does_not_mutate_shared_dialogue_or_keep_other_player_name(self):
        origem = list(INTRODUCAO_HISTORIA)
        caixa = self.jogo.caixa_dialogo
        for nome in ('Lívia', 'Miguel'):
            caixa.nome_jogador = nome
            for linhas in (INTRODUCAO_HISTORIA, DIALOGO_REENCONTRO, DIALOGO_ENCONTRO, DESCOBERTA_MOUSE, DIALOGO_APOS_CHEFE):
                caixa.start(linhas)
                self.assertIn(nome, {falante for falante, _ in caixa.linhas})
                self.assertNotIn('Narrador', {falante for falante, _ in caixa.linhas})
                self.assertFalse(any('{player}' in texto for _, texto in caixa.linhas))
                self.assertTrue(all(len(caixa._wrap(texto, 810)) <= 3 for _, texto in caixa.linhas))
        self.assertEqual(INTRODUCAO_HISTORIA, origem)
        self.assertIn('Aluno(a)', {falante for falante, _ in INTRODUCAO_HISTORIA})

    def test_walk_cycles_all_eight_frames_and_stops_against_wall(self):
        for personagem in ('boy', 'menina'):
            jogador = Jogador(120, 312, personagem)
            jogador.no_chao = True
            teclas = defaultdict(bool, {pygame.K_d: True})
            quadros = set()
            for _ in range(96):
                jogador.handle_input(teclas, [])
                jogador.update(self.piso, [])
                self.assertEqual(jogador.estado_animacao, 'walk')
                quadros.add(jogador.quadro_animacao)
            self.assertEqual(quadros, set(range(8)))
            parede = pygame.Rect(jogador.rect.right, 0, 32, 352)
            x = jogador.rect.x
            for _ in range(60):
                jogador.handle_input(teclas, [])
                jogador.update(self.piso+[parede], [])
            self.assertEqual(jogador.rect.x, x)
            self.assertEqual(jogador.estado_animacao, 'idle')
            self.assertEqual(jogador.distancia_caminhada, 0)

    def test_same_distance_at_different_speeds_has_same_walk_phase(self):
        jogadores = []
        for velocidade in (2, 4):
            jogador = Jogador(120, 312)
            jogador.no_chao = True
            for _ in range(60//velocidade):
                jogador.velocidade.x = velocidade
                jogador.update(self.piso, [])
            jogadores.append(jogador)
        self.assertEqual(jogadores[0].rect.x, jogadores[1].rect.x)
        self.assertEqual(jogadores[0].quadro_animacao, jogadores[1].quadro_animacao)
        self.assertEqual(jogadores[0].distancia_caminhada, jogadores[1].distancia_caminhada)

    def test_start_and_respawn_use_standing_pose_and_jump_does_not_cycle_walk(self):
        jogador = Jogador(120, 312)
        self.assertEqual(jogador.estado_animacao, 'idle')
        self.assertIs(jogador.image, jogador.figuras['idle_r'][0])
        jogador.no_chao = True
        teclas = defaultdict(bool, {pygame.K_d: True})
        jogador.handle_input(teclas, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)])
        for _ in range(12):
            jogador.update(self.piso, [])
            self.assertEqual(jogador.estado_animacao, 'jump')
            self.assertEqual(jogador.distancia_caminhada, 0)
        jogador.respawn(120, 312)
        self.assertEqual(jogador.estado_animacao, 'idle')
        self.assertEqual(jogador.quadro_animacao, 0)
        self.assertIs(jogador.image, jogador.figuras['idle_r'][0])


if __name__ == '__main__':
    unittest.main()
