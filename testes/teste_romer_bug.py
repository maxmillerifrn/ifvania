"""Testes de comportamento do primeiro chefe, sem abrir janela."""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import unittest
from types import SimpleNamespace

import pygame
from entidades.chefe import Chefe
from entidades.chefes_professores import CLASSES_CHEFES
from entidades.romer_bug import RomerBug, ProjetilProfessor
from entidades.jogador import Jogador
from sistema.habilidades import Habilidade
from mundo.fase import Fase
from mundo.fases_antigas import build_legacy_levels


class TestesRomerBug(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((960, 540))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.chefe = RomerBug(400, 408, arena=pygame.Rect(32, 32, 896, 480))
        self.jogador = SimpleNamespace(rect=pygame.Rect(180, 408, 26, 40))
        self.piso = [pygame.Rect(0, 448, 960, 64)]

    def transform(self):
        self.chefe.activate()
        self.chefe.take_damage(8)
        for _ in range(self.chefe.DURACAO_TRANSFORMACAO):
            self.chefe.update(self.jogador, self.piso)

    def test_each_existing_boss_has_its_registered_concrete_class(self):
        fases = [Fase(dados) for dados in build_legacy_levels()]
        self.assertEqual(len(fases), 6)
        self.assertIsInstance(fases[0].chefe, RomerBug)
        self.assertIsInstance(fases[0].chefe, Chefe)
        self.assertEqual(len({type(fase.chefe) for fase in fases}), 6)
        for fase in fases:
            self.assertIs(type(fase.chefe), CLASSES_CHEFES[fase.dados['boss']['boss_type']])
            self.assertIsNot(type(fase.chefe), Chefe)
        self.assertEqual(fases[0].dados['ability_reward'], Habilidade.SALTO_DUPLO)

    def test_inactive_boss_neither_attacks_moves_nor_takes_damage(self):
        inicial = self.chefe.rect.copy()
        self.chefe.take_damage(8)
        for _ in range(150):
            self.chefe.update(self.jogador, self.piso)
        self.assertEqual(self.chefe.vida, 16)
        self.assertEqual(self.chefe.rect, inicial)
        self.assertFalse(self.chefe.projeteis)


    def test_transforms_at_exactly_half_health_once(self):
        self.chefe.activate()
        self.chefe.take_damage(7)
        self.assertEqual(self.chefe.nome, 'RomerBug')
        self.assertFalse(self.chefe.transformado)
        imagem_anterior = self.chefe.image
        self.chefe.take_damage(1)
        self.assertEqual(self.chefe.vida, 8)
        self.assertEqual(self.chefe.nome, 'SpeedBug')
        self.assertIsNot(self.chefe.image, imagem_anterior)
        self.assertEqual(self.chefe.etapa, 2)
        self.assertEqual(self.chefe.get_all_hit_rects(), [])
        self.chefe.take_damage(1)
        self.assertEqual(self.chefe.vida, 8)
        for _ in range(45):
            self.chefe.update(self.jogador, self.piso)
        self.chefe.take_damage(5)
        self.assertEqual(self.chefe.etapa, 2)
        self.assertEqual(self.chefe.temporizador_transformacao, 0)
        self.assertEqual(self.chefe.vida, 3)

    def test_crossing_threshold_also_transforms_without_healing(self):
        self.chefe.activate()
        self.chefe.take_damage(10)
        self.assertTrue(self.chefe.transformado)
        self.assertEqual(self.chefe.vida, 6)





    def test_projectiles_expire_and_collide_with_world(self):
        for tipo in ('plane', 'medal'):
            disparo = ProjetilProfessor((100, 100), (1, 0), tipo)
            grupo = pygame.sprite.Group(disparo)
            disparo.update([pygame.Rect(100, 80, 50, 50)])
            self.assertFalse(grupo)
            disparo = ProjetilProfessor((100, 100), (1, 0), tipo)
            grupo.add(disparo)
            for _ in range(90):
                disparo.update([])
            self.assertFalse(grupo)

    def test_defeat_rewards_once_and_allows_exit(self):
        fase = Fase(build_legacy_levels()[0])
        jogador = Jogador(*fase.surgimento_jogador)
        jogador.rect.topleft = fase.mapa_blocos.gatilho_dialogo.topleft
        jogador.posicao.update(jogador.rect.topleft)
        self.assertEqual(fase.update(jogador, [])[0], 'dialogue')
        chefe = fase.chefe
        chefe.take_damage(8)
        for _ in range(chefe.DURACAO_TRANSFORMACAO):
            chefe.update(jogador, fase.mapa_blocos.solidos)
        chefe.take_damage(8)
        self.assertTrue(chefe.derrotado)
        self.assertFalse(chefe.projeteis)
        self.assertEqual(fase.update(jogador, [])[0], 'dialogue')
        self.assertEqual(len(fase.itens_habilidades), 1)
        recompensa = next(iter(fase.itens_habilidades))
        jogador.rect.topleft = recompensa.rect.topleft
        fase.update(jogador, [])
        self.assertTrue(jogador.has(Habilidade.SALTO_DUPLO))
        self.assertEqual(len(fase.itens_habilidades), 0)
        jogador.rect.topleft = fase.mapa_blocos.gatilho_saida.topleft
        self.assertEqual(fase.update(jogador, [])[0], 'level_complete')




    def test_aproxima_sem_trilho_e_ataca_sem_projeteis_nas_duas_formas(self):
        for transformar in (False, True):
            self.setUp()
            self.chefe.activate()
            if transformar:
                self.transform()
            vistos = set()
            menor_distancia = 1000
            for _ in range(240):
                self.chefe.update(self.jogador, self.piso)
                vistos.add(self.chefe.estado_ataque)
                menor_distancia = min(menor_distancia, abs(self.chefe.rect.centerx-self.jogador.rect.centerx))
                self.assertFalse(self.chefe.projeteis)
            self.assertLess(menor_distancia, 110)
            self.assertTrue({'preparar', 'executar', 'recuperar'} <= vistos)

    def test_aviso_nao_causa_dano_e_direcao_nao_persegue_durante_golpe(self):
        self.chefe.activate()
        self.jogador.rect.x = 330
        self.chefe.preparar_ataque(self.jogador)
        direcao = self.chefe.direcao_investida
        self.jogador.rect.x = 600
        for _ in range(28):
            self.assertFalse(self.chefe.get_all_hit_rects())
            self.chefe.update(self.jogador, self.piso)
        self.assertEqual(self.chefe.estado_ataque, 'executar')
        self.assertEqual(self.chefe.direcao_investida, direcao)
        area, dano = self.chefe.get_all_hit_rects()[0]
        self.assertLess(area.centerx, self.chefe.rect.centerx)
        self.assertEqual(dano, 1)
        for _ in range(10):
            self.chefe.update(self.jogador, self.piso)
        self.assertEqual(self.chefe.estado_ataque, 'recuperar')
        self.assertFalse(self.chefe.get_all_hit_rects())

    def test_sequencia_tem_novo_aviso_entre_golpes_e_recuperacao(self):
        for transformar, quantidade in ((False, 2), (True, 3)):
            self.setUp()
            self.chefe.activate()
            if transformar:
                self.transform()
            self.jogador.rect.x = 340
            self.chefe.preparar_ataque(self.jogador)
            golpes = 0
            anterior = ''
            for _ in range(200):
                self.chefe.update(self.jogador, self.piso)
                if self.chefe.estado_ataque == 'executar' and anterior != 'executar':
                    golpes += 1
                    self.assertEqual(anterior, 'preparar')
                anterior = self.chefe.estado_ataque
                if anterior == 'recuperar':
                    break
            self.assertEqual(golpes, quantidade)
            self.assertGreaterEqual(self.chefe.temporizador_ataque, 32)

    def test_dano_interrompe_duas_vezes_sem_permitir_trava_infinita(self):
        self.chefe.activate()
        origem = self.chefe.posicao.x
        self.chefe.take_damage(1, recuo=(4, 0))
        self.assertEqual(self.chefe.estado_ataque, 'recuo')
        for _ in range(10): self.chefe.update(self.jogador, self.piso)
        self.assertGreater(self.chefe.posicao.x, origem)
        self.chefe.take_damage(1)
        for _ in range(10): self.chefe.update(self.jogador, self.piso)
        self.chefe.preparar_ataque(self.jogador)
        self.chefe.take_damage(1)
        self.assertEqual(self.chefe.estado_ataque, 'preparar')
        self.assertEqual(self.chefe.vida, 13)

    def test_bloquear_golpe_cancela_resto_da_sequencia(self):
        self.chefe.activate()
        self.jogador.rect.x = 340
        self.chefe.preparar_ataque(self.jogador)
        for _ in range(28): self.chefe.update(self.jogador, self.piso)
        self.chefe.reagir_bloqueio(self.chefe.get_all_hit_rects()[0][0])
        self.assertEqual(self.chefe.estado_ataque, 'recuperar')
        self.assertEqual(self.chefe.temporizador_ataque, 44)
        self.assertFalse(self.chefe.get_all_hit_rects())

    def test_varrida_pode_ser_saltada_e_nao_atinge_pelas_costas(self):
        self.chefe.golpe_atual = 'varrida'
        self.chefe.direcao_investida = 1
        area = self.chefe.area_golpe()
        self.assertEqual(area.height, 22)
        self.assertFalse(area.colliderect(pygame.Rect(380, 408, 15, 40)))
        self.assertFalse(area.colliderect(pygame.Rect(450, 350, 40, 40)))
        self.assertTrue(area.colliderect(pygame.Rect(450, 408, 40, 40)))

    def test_transformacao_limpa_ataques_e_protege_reserva_compartilhada(self):
        self.chefe.activate()
        self.chefe.projeteis.add(ProjetilProfessor(self.chefe.rect.center, (1, 0), 'plane'))
        self.chefe.take_damage(8)
        self.chefe.take_damage(2)
        self.assertEqual(self.chefe.vida, 8)
        self.assertFalse(self.chefe.projeteis)
        self.assertFalse(self.chefe.get_all_hit_rects())

    def test_deslocamento_e_hitboxes_respeitam_parede(self):
        self.chefe.activate()
        self.jogador.rect.x = 100
        parede = pygame.Rect(368, 0, 32, 448)
        for _ in range(100):
            self.chefe.update(self.jogador, self.piso+[parede])
            self.assertFalse(self.chefe.rect.colliderect(parede))
        self.assertEqual(self.chefe.rect.x, 400)
        self.assertEqual(self.chefe.deslocamento_real, 0)

    def test_golpe_nao_atravessa_parede_e_origem_e_do_atacante(self):
        self.chefe.solidos_combate = [pygame.Rect(445, 360, 32, 88)]
        self.chefe.direcao_investida = 1
        area = self.chefe.area_golpe()
        self.assertLessEqual(area.right, 445)
        self.assertEqual(self.chefe.origem_ataque(area), self.chefe.rect.center)

    def test_recuperacao_nao_encurta_quando_recebe_combo(self):
        self.chefe.activate()
        self.chefe._recuperar(bloqueado=True)
        self.chefe.take_damage(1, recuo=(5, 0))
        self.assertEqual(self.chefe.estado_ataque, 'recuperar')
        self.assertEqual(self.chefe.temporizador_ataque, 44)
        self.assertEqual(self.chefe.vida, 15)


if __name__ == '__main__':
    unittest.main()
