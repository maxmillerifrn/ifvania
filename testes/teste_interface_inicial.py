"""Fluxo real de eventos entre menu, seleção, introdução e campanha."""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import unittest
from pathlib import Path

import pygame
import configuracoes
from entidades.jogador import Jogador
from entidades.inimigo import Inimigo
from jogo import (Jogo, ESTADO_MENU, ESTADO_SELECAO_PERSONAGEM, ESTADO_DIALOGO,
                  ESTADO_CARTAO_FASE, ESTADO_JOGANDO, ESTADO_PAUSA, ESTADO_DERROTA,
                  ESTADO_FIM_CONTEUDO, ESTADO_ENTRADA_NOME)


class TestesInterfaceInicial(unittest.TestCase):
    def setUp(self):
        self.jogo = Jogo()

    def tearDown(self):
        pygame.quit()

    def key(self, tecla):
        return self.jogo._process_events([pygame.event.Event(pygame.KEYDOWN, key=tecla)])

    def click(self, retangulo):
        return self.jogo._process_events([
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=retangulo.center)])

    def test_keyboard_requires_character_confirmation_before_intro(self):
        self.assertEqual(self.jogo.estado, ESTADO_MENU)
        self.assertEqual(self.key(pygame.K_RETURN), [])
        self.assertEqual(self.jogo.estado, ESTADO_SELECAO_PERSONAGEM)
        self.assertIsNone(self.jogo.jogador)
        self.key(pygame.K_RIGHT)
        self.key(pygame.K_RETURN)
        self.assertEqual(self.jogo.estado, ESTADO_ENTRADA_NOME)
        self.assertIsNone(self.jogo.jogador)
        self.jogo._process_events([pygame.event.Event(pygame.TEXTINPUT, text='Mara')])
        self.key(pygame.K_RETURN)
        self.assertEqual(self.jogo.estado, ESTADO_DIALOGO)
        self.assertEqual(self.jogo.jogador.personagem, 'menina')
        self.assertEqual(self.jogo.caixa_dialogo.indice, 0)
        self.assertEqual(self.jogo.caixa_dialogo._caracteres_exibidos, 0)
        self.assertEqual(self.jogo.jogador.habilidades, set())

    def test_mouse_can_choose_either_character_and_confirm(self):
        for i, personagem in enumerate(('boy', 'menina')):
            with self.subTest(character=personagem):
                self.jogo.estado = ESTADO_MENU
                self.click(self.jogo.interface_inicial.retangulos_menu[0])
                self.click(self.jogo.interface_inicial.retangulos_personagens[i])
                self.assertEqual(self.jogo.estado, ESTADO_SELECAO_PERSONAGEM)
                self.click(self.jogo.interface_inicial.retangulo_confirmar)
                self.assertEqual(self.jogo.estado, ESTADO_ENTRADA_NOME)
                self.jogo.nome_digitado = ''
                self.jogo._process_events([pygame.event.Event(pygame.TEXTINPUT, text='Alex')])
                self.click(self.jogo.interface_inicial.retangulo_confirmar_nome)
                self.assertEqual(self.jogo.jogador.personagem, personagem)
                self.assertEqual(self.jogo.caixa_dialogo.indice, 0)

    def test_back_returns_to_menu_without_starting_campaign(self):
        self.key(pygame.K_RETURN)
        self.key(pygame.K_RIGHT)
        self.key(pygame.K_ESCAPE)
        self.assertEqual(self.jogo.estado, ESTADO_MENU)
        self.assertIsNone(self.jogo.jogador)
        self.click(self.jogo.interface_inicial.retangulos_menu[0])
        self.click(self.jogo.interface_inicial.retangulo_voltar)
        self.assertEqual(self.jogo.estado, ESTADO_MENU)

    def test_exit_button_and_keyboard_exit_stop_application(self):
        self.click(self.jogo.interface_inicial.retangulos_menu[1])
        self.assertFalse(self.jogo.executando)
        self.jogo.executando = True
        self.jogo.indice_menu = 0
        self.key(pygame.K_DOWN)
        self.key(pygame.K_RETURN)
        self.assertFalse(self.jogo.executando)

    def test_menu_hover_updates_focus_without_starting_campaign(self):
        self.jogo._process_events([pygame.event.Event(
            pygame.MOUSEMOTION, pos=self.jogo.interface_inicial.retangulos_menu[1].center)])
        self.assertEqual(self.jogo.indice_menu, 1)
        self.assertEqual(self.jogo.estado, ESTADO_MENU)
        self.assertIsNone(self.jogo.jogador)

    def test_character_survives_respawn_and_level_change_but_new_campaign_resets_progress(self):
        self.jogo.personagem_escolhido = 'menina'
        self.jogo._start_story()
        jogador = self.jogo.jogador
        from habilidades import Habilidade
        jogador.grant_ability(Habilidade.SALTO_DUPLO)
        jogador.respawn(*self.jogo.fase.surgimento_jogador)
        from mundo.fases_antigas import build_legacy_levels
        self.jogo.definicoes_fases = build_legacy_levels()
        self.jogo._load_level(1)
        self.assertIs(self.jogo.jogador, jogador)
        self.assertEqual(jogador.personagem, 'menina')
        self.assertTrue(jogador.has(Habilidade.SALTO_DUPLO))
        self.jogo.estado = ESTADO_DERROTA
        self.key(pygame.K_RETURN)
        self.key(pygame.K_RETURN)
        self.key(pygame.K_RETURN)
        self.assertEqual(self.jogo.estado, ESTADO_ENTRADA_NOME)
        self.jogo._process_events([pygame.event.Event(pygame.TEXTINPUT, text='Lia')])
        self.key(pygame.K_RETURN)
        self.assertIsNot(self.jogo.jogador, jogador)
        self.assertEqual(self.jogo.jogador.personagem, 'menina')
        self.assertEqual(self.jogo.jogador.habilidades, set())
        self.assertEqual(self.jogo.jogador.vida, 6)

    def test_final_dialogue_key_does_not_skip_level_card_or_trigger_jump(self):
        self.jogo._start_story()
        self.jogo.caixa_dialogo.indice = len(self.jogo.caixa_dialogo.linhas) - 1
        self.jogo.caixa_dialogo._caracteres_exibidos = 1000
        self.assertEqual(self.key(pygame.K_SPACE), [])
        self.assertEqual(self.jogo.estado, ESTADO_CARTAO_FASE)
        self.assertEqual(self.jogo.jogador.velocidade.y, 0)

    def test_dialogue_input_does_not_leak_into_resumed_combat(self):
        self.jogo._load_level(0, novo_jogador=True)
        self.jogo.estado = ESTADO_DIALOGO
        self.jogo.caixa_dialogo.start([('Aluno(a)', 'Continuar')],
                                     ao_concluir=self.jogo._resume_from_dialogue)
        self.jogo.caixa_dialogo._caracteres_exibidos = 1000
        self.assertEqual(self.key(pygame.K_SPACE), [])
        self.assertEqual(self.jogo.estado, ESTADO_JOGANDO)
        self.assertEqual(self.jogo.jogador.velocidade.y, 0)

    def test_menu_selection_and_intro_do_not_advance_simulation(self):
        self.jogo._start_story()
        escola = self.jogo.fase
        inicial = (escola.instantes, self.jogo.jogador.rect.copy())
        for estado in (ESTADO_MENU, ESTADO_SELECAO_PERSONAGEM, ESTADO_DIALOGO):
            self.jogo.estado = estado
            for _ in range(100):
                self.jogo._update(pygame.key.get_pressed(), [])
            self.assertEqual((escola.instantes, self.jogo.jogador.rect), inicial)

    def test_window_closes_from_each_screen(self):
        self.jogo._start_story()
        for estado in (ESTADO_MENU, ESTADO_SELECAO_PERSONAGEM, ESTADO_ENTRADA_NOME, ESTADO_DIALOGO,
                      ESTADO_CARTAO_FASE, ESTADO_JOGANDO, ESTADO_PAUSA,
                      ESTADO_DERROTA, ESTADO_FIM_CONTEUDO, ESTADO_ENTRADA_NOME):
            self.jogo.estado = estado
            self.jogo.executando = True
            self.jogo._process_events([pygame.event.Event(pygame.QUIT)])
            self.assertFalse(self.jogo.executando)

    def test_each_character_has_complete_distinct_frames_and_functional_whip(self):
        raiz = Path(__file__).resolve().parents[1] / 'recursos' / 'imagens'
        menino = Jogador(200, 200, personagem='boy')
        menina = Jogador(200, 200, personagem='menina')
        self.assertIsNot(menino.figuras, menina.figuras)
        for tecla in menino.figuras:
            masculino = menino.figuras[tecla]
            feminino = menina.figuras[tecla]
            if not isinstance(masculino, list):
                masculino, feminino = [masculino], [feminino]
            self.assertEqual(len(masculino), len(feminino))
            for m, f in zip(masculino, feminino):
                self.assertEqual(f.get_size(), configuracoes.TAMANHO_PERSONAGEM)
                self.assertGreater(f.get_bounding_rect().height, 0)
                self.assertEqual(f.get_at((0, 0)).a, 0)
                self.assertNotEqual(pygame.image.tostring(m, 'RGBA'),
                                    pygame.image.tostring(f, 'RGBA'))
        self.assertEqual(len(list((raiz / 'jogador' / 'menina').glob('*.png'))), 11)
        for jogador in (menino, menina):
            alvo = Inimigo(260, 210, vida=2)
            jogador._try_melee()
            for idade in range(jogador.chicote.DURACAO):
                jogador.temporizador_golpe = jogador.chicote.DURACAO - idade
                jogador.try_melee_hit(alvo, [])
            self.assertEqual(alvo.vida, 1)
            self.assertEqual(jogador.rect.size, configuracoes.TAMANHO_PERSONAGEM)


if __name__ == '__main__':
    unittest.main()
