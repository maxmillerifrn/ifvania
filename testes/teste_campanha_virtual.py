"""Aceite da etapa 4: percurso básico, infecção, combate e fim do conteúdo."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')

from collections import defaultdict
import unittest
import pygame
import configuracoes
from entidades.jogador import Jogador
from entidades.projetil import Projetil
from jogo import (Jogo, ESTADO_JOGANDO, ESTADO_DIALOGO, ESTADO_INFECCAO,
                  ESTADO_PAUSA, ESTADO_FIM_CONTEUDO, ESTADO_MENU, ESTADO_TRANSFORMACAO_CHEFE)
from mundo.fase import Fase
from mundo.dados_fases import build_levels, DIALOGO_REENCONTRO, DIALOGO_APOS_CHEFE
from mundo.fases_antigas import build_legacy_levels


class TestesCampanhaVirtual(unittest.TestCase):
    def setUp(self):
        self.jogo = Jogo()
        self.teclas = defaultdict(bool)
        self.jogo._load_level(0, novo_jogador=True)
        self.jogo.estado = ESTADO_JOGANDO

    def tearDown(self):
        pygame.quit()

    def key(self, tecla):
        eventos = [pygame.event.Event(pygame.KEYDOWN, key=tecla)]
        if tecla == pygame.K_x:
            eventos.append(pygame.event.Event(pygame.KEYUP, key=tecla))
        return self.jogo._process_events(eventos)

    def finish_dialogue(self):
        for _ in range(40):
            if not self.jogo.caixa_dialogo.ativo:
                return
            self.key(pygame.K_e)
        self.fail('Diálogo não terminou')

    def start_meeting(self):
        fase = self.jogo.fase
        jogador = self.jogo.jogador
        jogador.posicao.update(fase.mapa_blocos.gatilho_dialogo.left+10, fase.surgimento_jogador[1])
        jogador.rect.topleft = jogador.posicao
        self.jogo._update(self.teclas, [])
        self.assertEqual(self.jogo.estado, ESTADO_DIALOGO)
        return fase, jogador, fase.chefe

    def start_fight(self):
        fase, jogador, chefe = self.start_meeting()
        self.finish_dialogue()
        self.assertEqual(self.jogo.estado, ESTADO_INFECCAO)
        for _ in range(self.jogo.duracao_infeccao):
            self.jogo._update(self.teclas, [])
        self.assertEqual(self.jogo.estado, ESTADO_JOGANDO)
        self.assertTrue(chefe.ativo)
        return fase, jogador, chefe

    def defeat(self, chefe, jogador, solidos):
        chefe.take_damage(chefe.vida_maxima//2)
        self.finish_transformation()
        chefe.take_damage(chefe.vida)
        self.assertTrue(chefe.derrotado)

    def finish_transformation(self):
        for _ in range(400):
            if not self.jogo.fase.chefe.cinematica_pendente:
                return
            if self.jogo.caixa_dialogo.ativo:
                self.key(pygame.K_e)
            self.jogo._update(self.teclas, [])
        self.fail('Transição do boss não terminou')

    def test_main_campaign_has_only_defined_content_and_legacy_remains_separate(self):
        self.assertEqual(len(self.jogo.definicoes_fases), 1)
        self.assertEqual(self.jogo.definicoes_fases[0]['name'], 'Fase 1: Mundo virtual')
        self.assertIsNone(self.jogo.definicoes_fases[0]['ability_reward'])
        self.assertEqual(len(build_legacy_levels()), 6)
        self.assertEqual(build_levels(), build_levels())

    def test_basic_movement_and_jump_reach_arena_and_exit_without_powers(self):
        for personagem in ('boy', 'menina'):
            with self.subTest(character=personagem):
                fase = Fase(build_levels()[0])
                jogador = Jogador(*fase.surgimento_jogador, personagem=personagem)
                teclas = defaultdict(bool, {pygame.K_d: True})
                saltos = 0
                for _ in range(1000):
                    eventos = []
                    if jogador.no_chao:
                        eventos = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)]
                        saltos += 1
                    jogador.handle_input(teclas, eventos)
                    jogador.update(fase.mapa_blocos.solidos, fase.mapa_blocos.perigos)
                    self.assertFalse(any(jogador.rect.colliderect(s) for s in fase.mapa_blocos.solidos))
                    if jogador.rect.colliderect(fase.mapa_blocos.gatilho_saida):
                        break
                self.assertTrue(jogador.rect.colliderect(fase.mapa_blocos.gatilho_saida))
                self.assertGreater(saltos, 0)
                self.assertEqual(jogador.habilidades, set())
                self.assertEqual(jogador.vida_maxima, 6)
                self.assertEqual(jogador.vida, 6)

    def test_human_romerito_speaks_before_infection_and_cannot_take_damage(self):
        fase, jogador, chefe = self.start_meeting()
        self.assertFalse(fase.infectado)
        self.assertEqual(fase.professor_humano.nome, 'Professor Romerito')
        self.assertEqual(self.jogo.caixa_dialogo.linhas, self.jogo.caixa_dialogo.resolve_lines(DIALOGO_REENCONTRO))
        texto = ' '.join(linha for _, linha in DIALOGO_REENCONTRO)
        self.assertIn('Brasília', texto)
        self.assertIn('corridas', texto)
        self.assertIn('nunca mais', texto)
        chefe.take_damage(100)
        self.assertEqual(chefe.vida, chefe.vida_maxima)
        temporizador_anterior = chefe.temporizador_ataque
        for _ in range(120):
            self.jogo._update(self.teclas, [])
            self.assertEqual(fase.update(jogador, []), (None, None))
        self.assertEqual(chefe.temporizador_ataque, temporizador_anterior)
        self.assertFalse(chefe.projeteis)
        self.assertFalse(chefe.ativo)
        self.assertEqual(fase.professor_humano.rect, chefe.rect)

    def test_infection_swaps_visual_without_changing_body_or_health_and_then_starts_fight(self):
        fase, jogador, chefe = self.start_meeting()
        antes = (chefe.rect.copy(), chefe.vida, jogador.vida, jogador.rect.copy())
        self.finish_dialogue()
        self.assertEqual(self.jogo.estado, ESTADO_INFECCAO)
        for _ in range(self.jogo.duracao_infeccao//2):
            self.jogo._update(self.teclas, [])
        self.assertTrue(fase.infectado)
        self.assertFalse(chefe.ativo)
        self.assertEqual((chefe.rect, chefe.vida, jogador.vida, jogador.rect), antes)
        for _ in range(self.jogo.duracao_infeccao//2):
            self.jogo._update(self.teclas, [])
        self.assertTrue(chefe.ativo)
        self.assertFalse(fase.encontro_pendente)
        self.assertEqual(self.jogo.estado, ESTADO_JOGANDO)

    def test_infection_pauses_resumes_and_window_closes(self):
        self.start_meeting()
        self.finish_dialogue()
        self.jogo._update(self.teclas, [])
        temporizador = self.jogo.temporizador_infeccao
        self.key(pygame.K_ESCAPE)
        self.assertEqual(self.jogo.estado, ESTADO_PAUSA)
        for _ in range(100):
            self.jogo._update(self.teclas, [])
        self.assertEqual(self.jogo.temporizador_infeccao, temporizador)
        self.key(pygame.K_ESCAPE)
        self.assertEqual(self.jogo.estado, ESTADO_INFECCAO)
        self.jogo._update(self.teclas, [])
        self.assertEqual(self.jogo.temporizador_infeccao, temporizador+1)
        self.jogo._process_events([pygame.event.Event(pygame.QUIT)])
        self.assertFalse(self.jogo.executando)

    def test_sobrecarga_investida_e_transformacao_preservam_vida_e_corpo(self):
        fase, jogador, chefe = self.start_fight()
        antes = chefe.rect.copy()
        chefe.preparar_ataque(jogador, fase.mapa_blocos.solidos)
        self.assertEqual(chefe.choose_attack(jogador), 'sobrecarga')
        self.assertIsNotNone(chefe.zona_descarga)
        chefe.take_damage(7)
        self.assertFalse(chefe.transformado)
        chefe.take_damage(1)
        self.assertTrue(chefe.transformado)
        self.assertEqual(chefe.rect, antes)
        self.assertEqual(chefe.vida, 8)
        self.assertEqual(chefe.rect.size, configuracoes.TAMANHO_PERSONAGEM)
        self.finish_transformation()
        chefe.preparar_ataque(jogador, fase.mapa_blocos.solidos)
        self.assertEqual(chefe.choose_attack(jogador), 'investida')
        self.assertIsNone(chefe.zona_descarga)
        chefe.take_damage(1)
        self.assertEqual(chefe.vida, 7)
        self.assertEqual(chefe.temporizador_transformacao, 0)
        self.assertEqual(chefe.nome, 'SpeedBug')

    def test_defeat_clears_threats_and_never_gives_an_old_reward(self):
        fase, jogador, chefe = self.start_fight()
        self.defeat(chefe, jogador, fase.mapa_blocos.solidos)
        jogador.projeteis.add(Projetil(200, 300, (1, 0)))
        self.assertTrue(fase.inimigos)
        self.jogo._update(self.teclas, [])
        self.assertEqual(self.jogo.estado, ESTADO_DIALOGO)
        self.assertEqual(self.jogo.caixa_dialogo.linhas, self.jogo.caixa_dialogo.resolve_lines(DIALOGO_APOS_CHEFE))
        self.assertFalse(fase.inimigos)
        self.assertFalse(chefe.projeteis)
        self.assertFalse(jogador.projeteis)
        self.assertFalse(fase.itens_habilidades)
        self.finish_dialogue()
        for _ in range(150):
            self.jogo._update(self.teclas, [])
        self.assertEqual(self.jogo.estado, ESTADO_JOGANDO)
        self.assertFalse(fase.itens_habilidades)
        self.assertEqual(jogador.habilidades, set())
        self.assertEqual(jogador.vida_maxima, 6)
        self.assertEqual(jogador.vida, 6)

    def test_exit_requires_defeat_and_ends_only_available_content_then_can_restart(self):
        fase, jogador, chefe = self.start_fight()
        jogador.rect.right = fase.mapa_blocos.gatilho_saida.right
        jogador.rect.bottom = fase.surgimento_jogador[1]+configuracoes.TAMANHO_PERSONAGEM[1]
        jogador.posicao.update(jogador.rect.topleft)
        self.jogo._update(self.teclas, [])
        self.assertEqual(self.jogo.estado, ESTADO_JOGANDO)
        self.assertFalse(fase.concluido)
        self.defeat(chefe, jogador, fase.mapa_blocos.solidos)
        self.jogo._update(self.teclas, [])
        self.assertEqual(self.jogo.estado, ESTADO_DIALOGO)
        self.finish_dialogue()
        self.assertEqual(self.jogo.estado, ESTADO_JOGANDO)
        self.jogo._update(self.teclas, [])
        self.assertEqual(self.jogo.estado, ESTADO_FIM_CONTEUDO)
        self.assertTrue(fase.concluido)
        self.assertEqual(fase.update(jogador, []), (None, None))
        self.jogo._draw()
        self.key(pygame.K_RETURN)
        self.assertEqual(self.jogo.estado, ESTADO_MENU)
        self.key(pygame.K_RETURN)
        self.key(pygame.K_RETURN)
        self.jogo._process_events([pygame.event.Event(pygame.TEXTINPUT, text='Alex')])
        self.key(pygame.K_RETURN)
        self.assertEqual(self.jogo.fase.ambiente, 'classroom')
        self.assertIsNot(self.jogo.jogador, jogador)
        self.assertFalse(self.jogo.jogador.chicote_desbloqueado)
        self.assertEqual(self.jogo.jogador.habilidades, set())

    def test_every_new_dialogue_fits_in_three_lines(self):
        for _, texto in DIALOGO_REENCONTRO+DIALOGO_APOS_CHEFE:
            self.assertLessEqual(len(self.jogo.caixa_dialogo._wrap(texto, 810)), 3)

    def test_both_characters_defeat_both_forms_using_keyboard_whip_without_powers(self):
        for personagem in ('boy', 'menina'):
            with self.subTest(character=personagem):
                self.jogo.personagem_escolhido = personagem
                self.jogo._load_level(0, novo_jogador=True)
                self.jogo.estado = ESTADO_JOGANDO
                fase, jogador, chefe = self.start_fight()
                # Isola o funcionamento da arma do balanceamento de sobrevivência.
                jogador.temporizador_invulnerabilidade = 10000
                viu_speedbug = False
                for _ in range(24):
                    jogador.posicao.update(chefe.rect.left-75, fase.surgimento_jogador[1])
                    jogador.rect.topleft = jogador.posicao
                    jogador.velocidade.update(0, 0)
                    jogador.direcao_olhar = 1
                    eventos = self.key(pygame.K_x)
                    self.jogo._update(self.teclas, eventos)
                    for _ in range(configuracoes.ESPERA_ATAQUE+1):
                        self.jogo._update(self.teclas, [])
                        viu_speedbug |= chefe.transformado
                        if self.jogo.estado == ESTADO_TRANSFORMACAO_CHEFE:
                            self.finish_transformation()
                        if self.jogo.estado == ESTADO_DIALOGO:
                            break
                    if chefe.derrotado:
                        break
                self.assertTrue(viu_speedbug)
                self.assertTrue(chefe.derrotado)
                self.assertEqual(self.jogo.estado, ESTADO_DIALOGO)
                self.assertEqual(jogador.personagem, personagem)
                self.assertFalse(jogador.habilidades)
                self.assertEqual(jogador.vida_maxima, 6)
                self.assertFalse(fase.itens_habilidades)
                self.assertFalse(chefe.projeteis)


if __name__ == '__main__':
    unittest.main()
