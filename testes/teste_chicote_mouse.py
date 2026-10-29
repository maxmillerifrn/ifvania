import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import unittest
import pygame
from entidades.jogador import Jogador
from entidades.inimigo import Inimigo
from entidades.romer_bug import RomerBug


class TestesChicoteMouse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((960, 540))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.jogador = Jogador(200, 200)
        self.jogador.direcao_olhar = 1

    def swing(self, alvos, solidos=()):
        self.jogador.espera_ataque = 0
        self.jogador._try_melee()
        for idade in range(self.jogador.chicote.DURACAO):
            self.jogador.temporizador_golpe = self.jogador.chicote.DURACAO - idade
            for alvo in alvos:
                self.jogador.try_melee_hit(alvo, solidos)

    def test_windup_and_recovery_do_not_damage(self):
        alvo = Inimigo(228, 210, vida=10)
        self.jogador._try_melee()
        for idade in (0, 3, 4, 19, 25, 29):
            self.jogador.temporizador_golpe = self.jogador.chicote.DURACAO - idade
            self.assertIsNone(self.jogador.get_melee_rect())
            self.assertFalse(self.jogador.try_melee_hit(alvo, []))
        self.assertEqual(alvo.vida, 10)

    def test_one_hit_per_enemy_per_swing_and_next_swing_can_hit_again(self):
        proximo = Inimigo(243, 210, vida=10)
        afastado = Inimigo(280, 210, vida=10)
        self.swing([proximo, afastado])
        self.assertEqual(proximo.vida, 9)
        self.assertEqual(afastado.vida, 9)
        self.swing([proximo, afastado])
        self.assertEqual(proximo.vida, 8)
        self.assertEqual(afastado.vida, 8)

    def test_targets_behind_or_outside_reach_are_not_hit(self):
        atras = Inimigo(150, 215, vida=10)
        distante = Inimigo(380, 210, vida=10)
        self.swing([atras, distante])
        self.assertEqual(atras.vida, 10)
        self.assertEqual(distante.vida, 10)

    def test_whip_stops_at_wall(self):
        alvo = Inimigo(280, 210, vida=10)
        parede = pygame.Rect(260, 100, 15, 200)
        self.swing([alvo], [parede])
        self.assertEqual(alvo.vida, 10)
        self.jogador.temporizador_golpe = self.jogador.chicote.DURACAO - 15
        self.assertLessEqual(max(p.x for p in self.jogador.chicote.points(self.jogador, [parede])), parede.left)

    def test_left_attack_and_turning_during_swing(self):
        self.jogador.direcao_olhar = -1
        self.jogador._try_melee()
        self.jogador.direcao_olhar = 1
        alvo = Inimigo(140, 210, vida=10)
        for idade in range(26):
            self.jogador.temporizador_golpe = 26 - idade
            self.jogador.try_melee_hit(alvo, [])
        self.assertEqual(alvo.vida, 9)
        self.assertEqual(self.jogador.chicote.direcao_olhar, -1)

    def test_respawn_cancels_swing(self):
        self.jogador._try_melee()
        self.jogador.respawn(100, 100)
        self.assertEqual(self.jogador.temporizador_golpe, 0)
        self.assertIsNone(self.jogador.get_melee_rect())

    def test_whip_can_defeat_boss_through_both_forms(self):
        chefe = RomerBug(265, 176)
        chefe.activate()
        for _ in range(8):
            self.swing([chefe])
        self.assertEqual(chefe.vida, 8)
        self.assertTrue(chefe.transformado)
        for _ in range(chefe.DURACAO_TRANSFORMACAO):
            chefe.update(self.jogador, [])
        for _ in range(8):
            self.swing([chefe])
        self.assertTrue(chefe.derrotado)


class TestesMovimentoChefe(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((960, 540))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_deslocamento_curto_preserva_fracoes_e_investida_usa_ciclo_completo(self):
        chefe=RomerBug(600,408,arena=pygame.Rect(0,0,2000,600))
        jogador=Jogador(100,408);chefe.activate();chefe.take_damage(8)
        chefe.temporizador_transformacao=0
        piso=[pygame.Rect(0,448,2000,100)]
        origem=chefe.rect.x
        fracoes=[]
        for _ in range(100):
            chefe.update(jogador,piso)
            fracoes.append(abs(chefe.posicao.x-round(chefe.posicao.x)))
        self.assertLessEqual(abs(chefe.rect.x-origem),24)
        self.assertGreater(max(fracoes),0.1)
        chefe.projeteis.empty();chefe.preparar_ataque(jogador,piso)
        quadros=set()
        for _ in range(63):
            chefe.update(jogador,piso);quadros.add(chefe.quadro_movimento)
        self.assertEqual(quadros,set(range(6)))
        self.assertEqual(chefe.rect.bottom,448)

    def test_blocked_runner_does_not_cycle_feet_without_displacement(self):
        chefe = RomerBug(400, 384)
        jogador = Jogador(100, 408)
        chefe.activate()
        chefe.take_damage(8)
        chefe.temporizador_transformacao = 0
        chefe.espera_salto = 200
        piso = pygame.Rect(0, 448, 1000, 100)
        parede = pygame.Rect(368, 0, 32, 448)
        for _ in range(40):
            chefe.update(jogador, [piso, parede])
        self.assertEqual(chefe.rect.left, parede.right)
        self.assertLess(chefe.distancia_passada, 1)


if __name__ == '__main__':
    unittest.main()
