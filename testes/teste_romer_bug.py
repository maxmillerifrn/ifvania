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
from habilidades import Habilidade
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

    def test_aviao_tem_aviso_mira_fixa_e_intervalo_maior(self):
        self.chefe.activate()
        for _ in range(70):self.chefe.update(self.jogador,self.piso)
        self.assertEqual(self.chefe.estado_ataque,'preparar_disparo')
        mira=self.chefe.mira_disparo.copy()
        self.jogador.rect.x=800
        for _ in range(29):
            self.assertFalse(self.chefe.projeteis)
            self.chefe.update(self.jogador,self.piso)
        self.assertEqual(self.chefe.mira_disparo,mira)
        self.chefe.update(self.jogador,self.piso)
        projetil=next(iter(self.chefe.projeteis))
        self.assertEqual(projetil.tipo,'plane')
        self.assertLess(projetil.velocidade.x,0)
        self.assertEqual(self.chefe.temporizador_ataque,108)
        for _ in range(137):self.chefe.update(self.jogador,self.piso)
        self.assertEqual(self.chefe.disparos_no_ciclo,1)
        self.chefe.update(self.jogador,self.piso)
        self.assertEqual(self.chefe.disparos_no_ciclo,2)
        self.assertEqual(self.chefe.estado_ataque,'pausa')

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

    def test_transformacao_limpa_projeteis_e_interrompe_ataque(self):
        self.chefe.activate()
        self.chefe.preparar_disparo(self.jogador)
        self.chefe.lancar_projetil()
        self.assertTrue(self.chefe.projeteis)
        self.chefe.take_damage(8)
        inicial=self.chefe.rect.copy()
        self.chefe.update(self.jogador,self.piso)
        self.assertFalse(self.chefe.projeteis)
        self.assertEqual(self.chefe.disparos_no_ciclo,0)
        self.assertEqual(self.chefe.get_all_hit_rects(),[])
        self.assertEqual(self.chefe.rect,inicial)

    def test_investida_nao_corrige_direcao_e_oferece_recuperacao(self):
        self.transform()
        self.chefe.preparar_ataque(self.jogador, self.piso)
        direcao = self.chefe.direcao_investida
        self.jogador.rect.x = 800
        for _ in range(36):
            self.assertEqual(self.chefe.get_all_hit_rects(), [])
            self.chefe.update(self.jogador, self.piso)
        inicial = self.chefe.rect.x
        for _ in range(27):
            self.assertEqual(self.chefe.direcao_investida, direcao)
            self.chefe.update(self.jogador, self.piso)
        self.assertEqual(self.chefe.rect.x-inicial, direcao*160)
        self.assertEqual(self.chefe.estado_ataque, 'recuperar')
        self.assertEqual(self.chefe.get_all_hit_rects(), [])
        self.assertEqual(self.chefe.temporizador_ataque, 78)
        self.assertFalse(self.chefe.projeteis)

    def test_investida_para_na_parede_sem_salto_reativo(self):
        self.transform()
        self.chefe.preparar_ataque(self.jogador, self.piso)
        parede = pygame.Rect(self.chefe.rect.left-32, 384, 32, 64)
        for _ in range(40):
            self.chefe.update(self.jogador, self.piso+[parede])
        self.assertGreaterEqual(self.chefe.rect.left, parede.right)
        self.assertEqual(self.chefe.velocidade.y, 0)
        self.assertEqual(self.chefe.estado_ataque, 'recuperar')

    def test_mira_lida_com_sobreposicao_e_alvo_a_direita(self):
        for centro in (self.chefe.rect.center,(800,420)):
            self.jogador.rect.center=centro
            self.chefe.preparar_disparo(self.jogador)
            self.assertEqual(self.chefe.direcao_olhar,1)
            self.chefe.lancar_projetil()
            self.assertGreater(len(self.chefe.projeteis),0)
            self.assertEqual(self.chefe.mira_disparo,pygame.Vector2(centro))

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

    def test_ciclo_completo_tem_dois_projeteis_pausa_e_investida_em_ambas_formas(self):
        for transformado in (False,True):
            chefe=RomerBug(500,408,arena=pygame.Rect(32,32,896,480))
            chefe.activate()
            if transformado:
                chefe.take_damage(8);chefe.temporizador_transformacao=0
            vistos=[];maximo_disparos=0
            for _ in range(650):
                chefe.update(self.jogador,self.piso)
                if not vistos or vistos[-1]!=chefe.estado_ataque:vistos.append(chefe.estado_ataque)
                maximo_disparos=max(maximo_disparos,chefe.disparos_no_ciclo)
                if chefe.estado_ataque in ('preparar','executar'):
                    self.assertFalse(chefe.projeteis)
                    self.assertEqual(chefe.disparos_no_ciclo,2)
                if chefe.estado_ataque=='recuperar':break
            self.assertEqual(maximo_disparos,2)
            self.assertEqual(vistos.count('preparar_disparo'),2)
            self.assertIn('pausa',vistos)
            self.assertEqual(vistos[-3:],['preparar','executar','recuperar'])
            self.assertEqual(chefe.get_all_hit_rects(),[])

    def test_medalha_tem_velocidade_moderada_e_nao_persegue_alvo(self):
        self.transform();self.chefe.preparar_disparo(self.jogador)
        self.chefe.lancar_projetil()
        projetil=next(iter(self.chefe.projeteis))
        velocidade=projetil.velocidade.copy()
        self.assertEqual(projetil.tipo,'medal')
        self.assertAlmostEqual(velocidade.length(),5)
        self.jogador.rect.x=850
        for _ in range(10):self.chefe.update(self.jogador,self.piso)
        self.assertEqual(projetil.velocidade,velocidade)
        self.assertIn((projetil.rect,projetil.dano),self.chefe.get_all_hit_rects())

    def test_pausa_antes_da_investida_aguarda_projeteis_restantes(self):
        self.chefe.activate();self.chefe.preparar_disparo(self.jogador)
        self.chefe.disparos_no_ciclo=1;self.chefe.lancar_projetil()
        projetil=next(iter(self.chefe.projeteis));projetil.velocidade.update(0,0)
        self.chefe.temporizador_ataque=1
        self.chefe.update(self.jogador,self.piso)
        self.assertEqual(self.chefe.estado_ataque,'pausa')
        self.assertTrue(self.chefe.projeteis)
        for _ in range(90):self.chefe.update(self.jogador,self.piso)
        self.assertFalse(self.chefe.projeteis)
        self.assertEqual(self.chefe.estado_ataque,'preparar')


if __name__ == '__main__':
    unittest.main()
