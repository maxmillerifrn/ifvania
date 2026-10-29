"""Transição cinematográfica e legibilidade da interface em condições reais."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')

from collections import defaultdict
import unittest
import pygame
import configuracoes
from jogo import Jogo, ESTADO_JOGANDO, ESTADO_TRANSFORMACAO_CHEFE, ESTADO_PAUSA
from habilidades import Habilidade
from entidades.projetil import Projetil
from interface import tema


class TestesTransicaoChefe(unittest.TestCase):
    def setUp(self):
        self.jogo = Jogo()
        self.jogo._load_level(0, novo_jogador=True)
        self.jogo.estado = ESTADO_JOGANDO
        self.fase = self.jogo.fase
        self.fase.dialogo_exibido = True
        self.fase.infectado = True
        self.chefe = self.fase.chefe
        self.chefe.activate()
        self.jogador = self.jogo.jogador
        self.jogador.posicao.update(self.chefe.rect.x-90, self.fase.surgimento_jogador[1])
        self.jogador.rect.topleft = self.jogador.posicao
        self.fase.camera.update(self.jogador.rect)
        self.teclas = defaultdict(bool)

    def tearDown(self):
        pygame.quit()

    def key(self, tecla):
        self.jogo._process_events([pygame.event.Event(pygame.KEYDOWN, key=tecla)])

    def begin(self, dano=8):
        self.chefe.take_damage(dano)
        self.jogo._update(self.teclas, [])
        self.assertEqual(self.jogo.estado, ESTADO_TRANSFORMACAO_CHEFE)
        return self.jogo.transicao_chefe

    def until_speech(self):
        for _ in range(120):
            self.jogo._update(self.teclas, [])
            if self.jogo.caixa_dialogo.ativo:
                return
        self.fail('A entidade não falou')

    def finish(self):
        for _ in range(400):
            if self.jogo.estado == ESTADO_JOGANDO:
                return
            if self.jogo.caixa_dialogo.ativo:
                self.key(pygame.K_e)
            self.jogo._update(self.teclas, [])
        self.fail('A transição não terminou')

    def test_threshold_starts_kneeling_once_and_freezes_combat_and_health(self):
        self.chefe.take_damage(7)
        self.assertFalse(self.chefe.cinematica_pendente)
        self.chefe.preparar_ataque(self.jogador, self.fase.mapa_blocos.solidos)
        self.jogador.projeteis.add(Projetil(100, 100, (1, 0)))
        self.jogador._try_melee()
        corpo = self.chefe.rect.copy()
        transicao = self.begin(1)
        self.assertEqual(transicao.etapa, 'kneel')
        self.assertEqual(self.chefe.nome, 'RomerBug')
        self.assertEqual(self.chefe.vida, 8)
        self.assertFalse(self.jogador.projeteis)
        self.assertFalse(self.chefe.projeteis)
        self.assertEqual(self.jogador.temporizador_golpe, 0)
        retrato_estado = ([inimigo.rect.copy() for inimigo in self.fase.inimigos], self.jogador.rect.copy(), self.jogador.vida)
        self.chefe.take_damage(7)
        for _ in range(40):
            self.jogo._update(self.teclas, [])
            self.assertEqual(self.chefe.get_all_hit_rects(), [])
        self.assertEqual(self.chefe.vida, 8)
        self.assertEqual(self.chefe.rect, corpo)
        self.assertEqual(([inimigo.rect for inimigo in self.fase.inimigos], self.jogador.rect, self.jogador.vida), retrato_estado)

    def test_entity_says_requested_line_and_waits_for_player_before_morph(self):
        transicao = self.begin()
        self.until_speech()
        self.assertEqual(self.jogo.caixa_dialogo.linhas, [('Entidade', 'Ainda não terminou.')])
        self.assertEqual(transicao.etapa, 'speech')
        for _ in range(200): self.jogo._update(self.teclas, [])
        self.assertEqual(transicao.etapa, 'speech')
        self.assertEqual(self.chefe.nome, 'RomerBug')
        self.key(pygame.K_e)
        self.assertEqual(transicao.etapa, 'morph')
        self.assertFalse(self.jogo.caixa_dialogo.ativo)

    def test_pause_freezes_motion_and_speech_and_resumes_same_stage(self):
        transicao = self.begin()
        self.jogo._update(self.teclas, [])
        instante = transicao.instante
        self.key(pygame.K_ESCAPE)
        self.assertEqual(self.jogo.estado, ESTADO_PAUSA)
        for _ in range(60): self.jogo._update(self.teclas, [])
        self.assertEqual(transicao.instante, instante)
        self.jogo._draw()
        self.key(pygame.K_ESCAPE)
        self.until_speech()
        self.key(pygame.K_ESCAPE)
        exibido = self.jogo.caixa_dialogo._caracteres_exibidos
        for _ in range(60): self.jogo._update(self.teclas, [])
        self.assertEqual(self.jogo.caixa_dialogo._caracteres_exibidos, exibido)
        self.key(pygame.K_ESCAPE)
        self.assertEqual(self.jogo.estado, ESTADO_TRANSFORMACAO_CHEFE)
        self.assertEqual(transicao.etapa, 'speech')

    def test_finishes_in_second_form_preserving_health_body_and_no_second_transition(self):
        antes = self.chefe.rect.copy()
        self.jogador.velocidade.update(2, -4)
        self.begin(dano=10)
        self.finish()
        self.assertEqual(self.chefe.nome, 'SpeedBug')
        self.assertEqual(self.chefe.vida, 6)
        self.assertEqual(self.chefe.rect, antes)
        self.assertFalse(self.chefe.cinematica_pendente)
        self.assertEqual(self.chefe.temporizador_transformacao, 0)
        self.assertGreaterEqual(self.jogador.temporizador_invulnerabilidade, 60)
        self.assertEqual(self.jogador.velocidade, pygame.Vector2(2, -4))
        self.chefe.take_damage(1)
        self.assertEqual(self.chefe.vida, 5)
        self.assertFalse(self.chefe.cinematica_pendente)
        self.assertEqual(self.jogo.estado, ESTADO_JOGANDO)

    def test_visual_zoom_and_six_poses_do_not_change_physics_and_kneel_is_lower(self):
        transicao = self.begin()
        antes = (self.chefe.rect.copy(), self.jogador.rect.copy(), self.fase.camera.deslocamento.copy())
        etapas = set()
        for _ in range(320):
            etapas.add(transicao.etapa)
            if self.jogo.caixa_dialogo.ativo: self.key(pygame.K_e)
            self.jogo._draw()
            self.assertEqual((self.chefe.rect, self.jogador.rect, self.fase.camera.deslocamento), antes)
            if self.jogo.estado == ESTADO_JOGANDO: break
            self.jogo._update(self.teclas, [])
        self.assertTrue({'kneel', 'arrival', 'speech', 'morph', 'rise', 'release'}.issubset(etapas))
        for quadro in transicao.quadros:
            self.assertEqual(quadro.get_size(), configuracoes.TAMANHO_PERSONAGEM)
            self.assertEqual(quadro.get_at((0, 0)).a, 0)
            self.assertEqual(quadro.get_bounding_rect().bottom, configuracoes.TAMANHO_PERSONAGEM[1])
        self.assertLess(transicao.quadros[1].get_bounding_rect().height,
                        transicao.quadros[5].get_bounding_rect().height)

    def test_all_power_hints_fit_rows_and_survive_low_health_and_boss_change(self):
        self.jogador.habilidades = set(Habilidade)
        self.jogador.vida_maxima = 10
        for vida in (10, 2, 0):
            self.jogador.vida = vida
            self.jogo.painel_informacoes.draw(self.jogo.tela, self.jogador, 'Laboratório A28 — escola corrompida', self.chefe)
            self.jogo.painel_informacoes.draw_controls_hint(self.jogo.tela, self.jogador)
            for fileira in self.jogo.painel_informacoes.ultimas_linhas_dicas:
                self.assertLessEqual(self.jogo.painel_informacoes.fonte_pequena.size(fileira)[0], configuracoes.LARGURA_TELA-64)
        self.assertGreater(len(self.jogo.painel_informacoes.ultimas_linhas_dicas), 1)
        self.assertLessEqual(self.jogo.painel_informacoes.fonte.size(tema.fit_text(self.jogo.painel_informacoes.fonte, 'Nome '*100, 100))[0], 100)

    def test_window_closes_while_entity_speaks(self):
        self.begin()
        self.until_speech()
        self.jogo._process_events([pygame.event.Event(pygame.QUIT)])
        self.assertFalse(self.jogo.executando)


if __name__ == '__main__':
    unittest.main()
