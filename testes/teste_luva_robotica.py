"""Regressões de progressão, defesa, alcance corporal e tutorial integrado."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
import unittest
from collections import defaultdict
from pathlib import Path
from tempfile import TemporaryDirectory
import pygame
from entidades.jogador import Jogador
from entidades.inimigo import Inimigo
from sistema.habilidades import Habilidade
from sistema.jogo import Jogo, ESTADO_JOGANDO
from mundo.tutorial_luva import TutorialLuva


class TestesLuvaRobotica(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((960, 540))
        self.addCleanup(pygame.quit)
        self.jogador = Jogador(200, 312)
        self.jogador.no_chao = True
        self.piso = [pygame.Rect(0, 352, 1000, 100)]

    def test_soco_curto_nao_alcanca_distancia_do_chicote(self):
        perto, longe = Inimigo(250, 312, vida=5), Inimigo(310, 312, vida=5)
        self.jogador._try_melee()
        for _ in range(24):
            self.jogador.update(self.piso, [])
            self.jogador.try_melee_hit(perto, self.piso)
            self.jogador.try_melee_hit(longe, self.piso)
        self.assertEqual(perto.vida, 4)
        self.assertEqual(longe.vida, 5)

    def test_contra_ataque_consumido_uma_vez(self):
        jogador = self.jogador
        jogador.tentar_bloqueio()
        self.assertEqual(jogador.take_damage(1, origem=(270, 320)), 'bloqueado')
        jogador.handle_input(defaultdict(bool), [pygame.event.Event(pygame.KEYUP, key=pygame.K_q)])
        jogador._try_melee()
        self.assertEqual(jogador.chicote.dano, 2)
        self.assertEqual(jogador.janela_contra_ataque, 0)
        for _ in range(25): jogador.update(self.piso, [])
        jogador._try_melee()
        self.assertEqual(jogador.chicote.dano, 1)

    def test_protecao_automatica_nao_bloqueia_costas_e_so_ocorre_uma_vez(self):
        jogador = self.jogador
        jogador.protecao_inicial = True
        self.assertEqual(jogador.take_damage(1, origem=(270, 320)), 'bloqueado')
        self.assertFalse(jogador.protecao_inicial)
        jogador.defesa.cancelar()
        jogador.take_damage(1, origem=(270, 320))
        self.assertEqual(jogador.vida, 5)

    def test_sobrecarga_exige_modulo_e_respeita_recarga(self):
        jogador = self.jogador
        evento = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)
        jogador.handle_input(defaultdict(bool), [evento])
        self.assertEqual(jogador.tempo_sobrecarga, 0)
        jogador.grant_ability(Habilidade.SOBRECARGA, aumentar_vida=False)
        jogador.handle_input(defaultdict(bool), [evento])
        self.assertEqual(jogador.tempo_sobrecarga, 300)
        for _ in range(301): jogador.update(self.piso, [])
        jogador.handle_input(defaultdict(bool), [evento])
        self.assertEqual(jogador.tempo_sobrecarga, 0)
        self.assertGreater(jogador.recarga_sobrecarga, 0)

    def test_defesa_reforcada_reduz_custo_sem_proteger_costas(self):
        jogador = self.jogador
        jogador.grant_ability(Habilidade.DEFESA_REFORCADA, aumentar_vida=False)
        jogador.update(self.piso, [])
        jogador.tentar_bloqueio()
        jogador.take_damage(1, origem=(270, 320))
        self.assertEqual(jogador.defesa.resistencia, 83)
        jogador.take_damage(1, origem=(150, 320))
        self.assertEqual(jogador.vida, 5)

    def test_onda_respeita_parede_e_exige_modulo(self):
        jogador = self.jogador
        jogador.tipo_golpe = 'descendente'
        jogador._try_melee()
        jogador.temporizador_golpe = 15
        alcance_inicial = jogador.chicote.points(jogador)[-1].x
        jogador.grant_ability(Habilidade.ONDA_CHOQUE, aumentar_vida=False)
        self.assertGreater(jogador.chicote.points(jogador)[-1].x, alcance_inicial)
        parede = pygame.Rect(275, 280, 20, 72)
        self.assertLessEqual(jogador.chicote.points(jogador, [parede])[-1].x, 275)

    def test_modulos_persistem_e_nao_sao_concedidos_ao_pular(self):
        with TemporaryDirectory() as pasta:
            jogo = Jogo(caminho_salvamento=Path(pasta)/'save.json')
            jogo._start_story()
            jogo._concluir_introducao(pular=True)
            self.assertEqual(jogo.jogador.habilidades, set())
            jogo.jogador.grant_ability(Habilidade.PUNHO_IMPACTO, aumentar_vida=False)
            jogo.jogador.grant_ability(Habilidade.SOBRECARGA, aumentar_vida=False)
            jogo.checkpoints.registrar()
            self.assertTrue(jogo.checkpoints.continuar())
            self.assertIn(Habilidade.PUNHO_IMPACTO, jogo.jogador.habilidades)
            self.assertIn(Habilidade.SOBRECARGA, jogo.jogador.habilidades)
            self.assertEqual(jogo.estado, ESTADO_JOGANDO)
            self.assertIsNone(jogo.tutorial_luva)

    def test_tutorial_exige_acoes_e_derrota_real(self):
        jogo = Jogo()
        jogo._load_level(0, novo_jogador=True)
        tutorial = TutorialLuva(jogo.jogador, jogo.fase)
        tutorial.atualizar(jogo.jogador)
        self.assertIn('A/D', tutorial.texto)
        jogo.jogador.acoes_luva.update(('movimento', 'guarda', 'esquiva', 'ataque', 'combo'))
        tutorial.atualizar(jogo.jogador)
        self.assertIn('Derrote', tutorial.texto)
        tutorial.alvo.take_damage(100)
        for _ in range(240): tutorial.atualizar(jogo.jogador)
        self.assertTrue(tutorial.concluido)
        self.assertFalse(jogo.jogador.protecao_inicial)

    def test_recompensas_de_cada_chefe_seguem_ordem_e_nao_duplicam_vida(self):
        jogo = Jogo()
        for indice, habilidade in enumerate((Habilidade.PUNHO_IMPACTO, Habilidade.SOBRECARGA,
                                             Habilidade.ONDA_CHOQUE, Habilidade.DEFESA_REFORCADA,
                                             Habilidade.COMBO_TECNOLOGICO)):
            jogo._load_level(indice, novo_jogador=True)
            self.assertNotIn(habilidade, jogo.jogador.habilidades)
            jogo.fase.chefe.derrotado = True
            jogo.fase.libertacao_concluida = True
            jogo.fase._after_defeat(jogo.jogador)
            self.assertIn(habilidade, jogo.jogador.habilidades)
            self.assertEqual(jogo.jogador.vida_maxima, 6)
            jogo.fase._after_defeat(jogo.jogador)
            self.assertEqual(jogo.jogador.vida_maxima, 6)
