"""Regressões do acesso à arena e do combate pelo fluxo real do jogo."""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import unittest
import pygame
from entidades.jogador import Jogador
from jogo import Jogo, ESTADO_JOGANDO, ESTADO_DIALOGO
from mundo.fase import Fase
from mundo.fases_antigas import build_legacy_levels


class TestesEncontroChefe(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((960, 540))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_entering_in_air_or_beyond_old_trigger_activates_all_bosses(self):
        for dados in build_legacy_levels():
            for altura in (80, 300, 408):
                for alem in (0, 100):
                    with self.subTest(level=dados['index'], height=altura, beyond=alem):
                        fase = Fase(dados)
                        jogador = Jogador(fase.mapa_blocos.gatilho_dialogo.x + alem, altura)
                        evento, _ = fase.update(jogador, [])
                        self.assertEqual(evento, 'dialogue')
                        self.assertTrue(fase.chefe.ativo)
                        self.assertNotEqual(fase.update(jogador, [])[0], 'dialogue')

    def test_exploration_before_arena_does_not_activate_boss(self):
        for dados in build_legacy_levels():
            fase = Fase(dados)
            jogador = Jogador(0, 300)
            jogador.rect.right = fase.mapa_blocos.gatilho_dialogo.left
            jogador.posicao.update(jogador.rect.topleft)
            self.assertIsNone(fase.update(jogador, [])[0])
            self.assertFalse(fase.chefe.ativo)

    def test_all_bosses_have_clear_space_and_supporting_floor(self):
        for dados in build_legacy_levels():
            fase = Fase(dados)
            chefe = fase.chefe
            self.assertFalse(any(chefe.rect.colliderect(s) for s in fase.mapa_blocos.solidos))
            sondagem_piso = pygame.Rect(chefe.rect.left, chefe.rect.bottom, chefe.largura, 1)
            self.assertTrue(any(sondagem_piso.colliderect(s) for s in fase.mapa_blocos.solidos))
            espaco_arena = pygame.Rect(fase.mapa_blocos.gatilho_dialogo.left, 32,
                                    fase.mapa_blocos.largura - 32 - fase.mapa_blocos.gatilho_dialogo.left,
                                    chefe.rect.bottom - 32)
            self.assertFalse(any(espaco_arena.colliderect(s) for s in fase.mapa_blocos.solidos))

    def test_entry_dialogue_precedes_damage_even_next_to_boss(self):
        fase = Fase(build_legacy_levels()[0])
        jogador = Jogador(fase.chefe.rect.left - 28, 408)
        jogador.direcao_olhar = 1
        jogador._try_melee()
        vida = fase.chefe.vida
        self.assertEqual(fase.update(jogador, [])[0], 'dialogue')
        self.assertEqual(fase.chefe.vida, vida)
        self.assertEqual(jogador.vida, jogador.vida_maxima)
        self.assertFalse(fase.chefe.projeteis)

    def test_dialogo_golpe_e_aviao_causam_dano(self):
        jogo = Jogo()
        jogo.definicoes_fases = build_legacy_levels()
        jogo._load_level(0, novo_jogador=True)
        jogo.estado = ESTADO_JOGANDO
        chefe = jogo.fase.chefe
        jogador = jogo.jogador
        jogador.posicao.update(chefe.rect.left - 75, 408)
        jogador.rect.topleft = jogador.posicao
        jogador.direcao_olhar = 1
        teclas = pygame.key.get_pressed()
        jogo._update(teclas, [])
        self.assertEqual(jogo.estado, ESTADO_DIALOGO)
        temporizador_inicial = chefe.temporizador_ataque
        for _ in range(10):
            jogo._update(teclas, [])
        self.assertEqual(chefe.temporizador_ataque, temporizador_inicial)
        for _ in range(len(jogo.caixa_dialogo.linhas) * 2):
            jogo.caixa_dialogo.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e))
        self.assertEqual(jogo.estado, ESTADO_JOGANDO)
        jogo._update(teclas, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_x), pygame.event.Event(pygame.KEYUP, key=pygame.K_x)])
        self.assertEqual(chefe.vida, chefe.vida_maxima)  # preparação do chicote
        for _ in range(15):
            jogo._update(teclas, [])
        self.assertLess(chefe.vida, chefe.vida_maxima)
        self.assertEqual(chefe.vida, chefe.vida_maxima - 1)
        # O avião usa a mira anunciada e pode atingir o aluno parado.
        jogador.posicao.x -= 80
        jogador.rect.x = round(jogador.posicao.x)
        for _ in range(120):
            jogo._update(teclas, [])
            if jogador.vida < jogador.vida_maxima:
                break
        self.assertEqual(chefe.nome, 'RomerBug')
        self.assertLess(jogador.vida, jogador.vida_maxima)


if __name__ == '__main__':
    unittest.main()
