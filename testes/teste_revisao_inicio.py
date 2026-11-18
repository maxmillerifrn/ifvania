"""Regressões da encenação inicial, sucção e investida junto à borda."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
from collections import defaultdict
import unittest
import pygame
from sistema.jogo import Jogo, ESTADO_DIALOGO, ESTADO_PAUSA, ESTADO_ABDUCAO, ESTADO_JOGANDO
from mundo.dados_fases import (INTRODUCAO_HISTORIA, INDICE_CORRUPCAO_HISTORIA,
                               INDICE_EXECUCAO_HISTORIA, INDICE_MEMORIA_HISTORIA)
from mundo.succao_computador import SuccaoComputador


class TestesRevisaoInicio(unittest.TestCase):
    def setUp(self):
        self.jogo = Jogo()
        self.teclas = defaultdict(bool)

    def tearDown(self):
        pygame.quit()

    def test_abertura_encadeia_memoria_pendrive_execucao_e_corrupcao(self):
        self.jogo._start_story()
        fase = self.jogo.fase
        self.assertIsNotNone(fase.arte.turma)
        self.assertEqual(len(fase.arte.turma.postos), 2)
        self.assertLess(INDICE_MEMORIA_HISTORIA, INDICE_EXECUCAO_HISTORIA)
        self.assertLess(INDICE_EXECUCAO_HISTORIA, INDICE_CORRUPCAO_HISTORIA)
        for indice, etapa in [(0, 'codigo'), (INDICE_EXECUCAO_HISTORIA, 'execucao'),
                              (INDICE_CORRUPCAO_HISTORIA, 'revolta')]:
            self.jogo.caixa_dialogo.indice = indice
            self.jogo._update(self.teclas, [])
            self.assertEqual(fase.arte.etapa_aula, etapa)
            self.jogo._draw()
        self.assertTrue(fase.corrompido)
        self.assertEqual(fase.instantes, 0)
        self.assertFalse(self.jogo.jogador.chicote_desbloqueado)
        for _, fala in INTRODUCAO_HISTORIA:
            self.assertLessEqual(len(self.jogo.caixa_dialogo._wrap(fala, 810)), 3)

    def test_hipnose_visivel_em_dialogo_e_congelada_na_pausa(self):
        self.jogo._start_story()
        self.jogo.caixa_dialogo.indice = INDICE_CORRUPCAO_HISTORIA
        self.jogo._update(self.teclas, [])
        for _ in range(50):
            self.jogo._update(self.teclas, [])
        fase = self.jogo.fase
        self.assertGreater(fase.hipnose, 0.4)
        antes = fase.hipnose
        self.jogo._process_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)])
        self.assertEqual(self.jogo.estado, ESTADO_PAUSA)
        for _ in range(50):
            self.jogo._update(self.teclas, [])
        self.assertEqual(fase.hipnose, antes)
        self.assertEqual(fase.instantes, 0)

    def test_succao_encolhe_ambos_ate_monitor_sem_alterar_corpos_no_desenho(self):
        for personagem in ('boy', 'menina'):
            self.jogo.personagem_escolhido = personagem
            self.jogo._load_school('lab', novo_jogador=True)
            jogador = self.jogo.jogador
            jogador.rect.x = 630
            jogador.posicao.x = 630
            from sistema.jogo import ESTADO_DIALOGO
            self.jogo.maquina_estados.estado = ESTADO_DIALOGO
            self.jogo._start_abduction()
            succao = self.jogo.fase.succao
            self.assertEqual(self.jogo.duracao_abducao, SuccaoComputador.DURACAO)
            corpos = [ator.rect.copy() for ator in succao.atores]
            alvo = pygame.Vector2(self.jogo.fase.camera.apply(succao.monitor).center)
            for indice in (0, 1):
                inicio, escala_inicial, _ = succao.amostra(indice, 0.2)
                fim, escala_final, _ = succao.amostra(indice, 0.96)
                self.assertLess(fim.distance_to(alvo), inicio.distance_to(alvo))
                self.assertLess(escala_final, escala_inicial/4)
            self.jogo.temporizador_abducao = 95
            self.jogo._draw()
            self.assertEqual([ator.rect for ator in succao.atores], corpos)
            self.jogo._process_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)])
            for _ in range(60):
                self.jogo._update(self.teclas, [])
            self.assertEqual(self.jogo.temporizador_abducao, 95)

    def test_speedbug_ataca_nas_bordas_sem_recuo_artificial(self):
        for direita in (False, True):
            self.jogo._load_level(0, novo_jogador=True)
            fase, jogador = self.jogo.fase, self.jogo.jogador
            chefe = fase.chefe
            chefe.activate()
            chefe.take_damage(8)
            chefe.finish_cinematic()
            chefe.rect.x = chefe.arena.right-chefe.largura if direita else chefe.arena.left
            chefe.posicao.update(chefe.rect.topleft)
            jogador.rect.x = chefe.rect.x+(-70 if direita else 70)
            chefe.preparar_ataque(jogador)
            self.assertEqual(chefe.estado_ataque, 'preparar')
            for _ in range(20): chefe.update(jogador, fase.mapa_blocos.solidos)
            self.assertEqual(chefe.estado_ataque, 'executar')
            self.assertTrue(chefe.get_all_hit_rects())
            self.assertGreaterEqual(chefe.rect.left, chefe.arena.left)
            self.assertLessEqual(chefe.rect.right, chefe.arena.right)

    def test_romerito_recupera_forma_humana_na_derrota(self):
        self.jogo._load_level(0, novo_jogador=True)
        fase = self.jogo.fase
        fase.chefe.activate()
        fase.chefe.take_damage(8)
        fase.chefe.finish_cinematic()
        fase.chefe.take_damage(8)
        self.jogo.maquina_estados.estado = ESTADO_JOGANDO
        self.jogo._update(self.teclas,[])
        for _ in range(150): self.jogo._update(self.teclas,[])
        self.assertTrue(fase.professor_liberto)
        self.assertEqual(fase.professor_humano.rect, fase.chefe.rect)
        self.assertFalse(fase.inimigos)
        fase.draw(self.jogo.tela)

    def test_fundos_preservam_colisoes_e_sao_exportados_em_resolucao_nativa(self):
        from mundo.escola import FaseEscolar
        fase = FaseEscolar('corridor')
        corpos = [bloco.copy() for bloco in fase.mapa_blocos.solidos]
        self.assertEqual(fase.arte.fundo.get_size(), (960, 540))
        fase.draw(self.jogo.tela)
        self.assertEqual(fase.mapa_blocos.solidos, corpos)
        self.jogo._load_level(1, novo_jogador=True)
        fase = self.jogo.fase
        corpos = [bloco.copy() for bloco in fase.mapa_blocos.solidos]
        fase.draw(self.jogo.tela)
        self.assertEqual(fase.biblioteca.fundo_ifrn.get_size(), (960, 540))
        self.assertEqual(fase.mapa_blocos.solidos, corpos)
