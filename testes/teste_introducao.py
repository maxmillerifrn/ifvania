"""Passagens entre a abertura doméstica, a primeira fase e o checkpoint."""
import os
from collections import defaultdict
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')

import pygame

from sistema.configuracoes import QUADROS_POR_SEGUNDO
from sistema.jogo import Jogo, ESTADO_DIALOGO, ESTADO_INTRODUCAO, ESTADO_JOGANDO, ESTADO_PAUSA


class TestesIntroducao(unittest.TestCase):
    def setUp(self):
        self.pasta = TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)
        self.addCleanup(pygame.quit)
        self.arquivo = Path(self.pasta.name)/'partida.json'
        self.jogo = Jogo(caminho_salvamento=self.arquivo)
        self.jogo.nome_jogador = 'Lia'
        self.jogo.personagem_escolhido = 'menina'
        self.jogo._start_story()
        self.teclas = defaultdict(bool)

    def tecla(self, codigo):
        return self.jogo._process_events([pygame.event.Event(pygame.KEYDOWN, key=codigo)])

    def test_cenas_entregam_personagem_e_controles_ao_a28(self):
        self.assertEqual(self.jogo.estado, ESTADO_INTRODUCAO)
        cenas_exibidas = set()
        duracao = sum(cena.duracao for cena in self.jogo.introducao.CENAS)
        for _ in range(round(duracao*QUADROS_POR_SEGUNDO)):
            cenas_exibidas.add(self.jogo.introducao.indice)
            self.jogo._update(self.teclas, [])
        self.assertEqual(cenas_exibidas, set(range(6)))
        self.assertEqual(self.jogo.estado, ESTADO_DIALOGO)
        self.assertFalse(self.jogo.jogador.chicote_desbloqueado)
        self.jogo._draw()
        self.assertEqual(self.jogo.fase.ambiente, 'classroom')
        self.assertEqual(self.jogo.caixa_dialogo.linhas[0][0], 'Lia')
        self.assertIn('Depois da apresentação', self.jogo.caixa_dialogo.linhas[0][1])
        identidade = self.jogo.jogador
        def concluir_dialogo():
            for _ in range(80):
                if not self.jogo.caixa_dialogo.ativo:
                    if self.jogo.descoberta_mouse and self.jogo.descoberta_mouse.aguardando_conclusao:
                        for _ in range(self.jogo.descoberta_mouse.DURACAO):
                            self.jogo._update(self.teclas, [])
                    return
                self.tecla(pygame.K_e)
                self.jogo._update(self.teclas, [])
            self.fail('Diálogo não concluiu')
        def andar(destino):
            for _ in range(600):
                if self.jogo.jogador.rect.x >= destino:
                    return
                self.jogo._update(defaultdict(bool, {pygame.K_d: True}), [])
            self.fail('Não chegou ao destino')
        concluir_dialogo()
        self.tecla(pygame.K_RETURN)
        self.assertEqual(self.jogo.fase.ambiente, 'corridor')
        andar(self.jogo.fase.porta_a28.x-40)
        self.jogo._update(self.teclas, self.tecla(pygame.K_e))
        self.assertEqual(self.jogo.fase.ambiente, 'lab')
        andar(630)
        self.jogo._update(self.teclas, self.tecla(pygame.K_e))
        concluir_dialogo()
        for _ in range(self.jogo.duracao_abducao):
            self.jogo._update(self.teclas, [])
        self.assertEqual(self.jogo.fase.identificador, 'a28')
        self.assertIs(self.jogo.jogador, identidade)
        self.assertFalse(self.jogo.jogador.chicote_desbloqueado)
        concluir_dialogo()
        self.tecla(pygame.K_RETURN)
        self.assertEqual(self.jogo.estado, ESTADO_JOGANDO)
        self.assertTrue(self.jogo.jogador.chicote_desbloqueado)
        origem = self.jogo.jogador.rect.copy()
        self.teclas[pygame.K_RIGHT] = True
        for _ in range(20):
            self.jogo._update(self.teclas, [])
        self.assertGreater(self.jogo.jogador.rect.x, origem.x)
        self.jogo._update(self.teclas, self.tecla(pygame.K_SPACE))
        self.assertLess(self.jogo.jogador.rect.y, origem.y)

    def test_pausa_pulo_e_continuacao_persistida(self):
        self.jogo._update(self.teclas, [])
        abertura = self.jogo.introducao
        quadro = abertura.quadro
        self.tecla(pygame.K_ESCAPE)
        self.assertEqual(self.jogo.estado, ESTADO_PAUSA)
        self.jogo._update(self.teclas, [])
        self.assertEqual(abertura.quadro, quadro)
        self.assertEqual(self.tecla(pygame.K_f), [])
        self.assertEqual(self.jogo.estado, ESTADO_JOGANDO)
        self.assertIsNone(self.jogo.introducao)
        self.assertFalse(self.jogo.caixa_dialogo.ativo)
        self.assertTrue(self.jogo.jogador.chicote_desbloqueado)
        self.assertFalse(self.jogo.progresso_campanha.fases_concluidas)
        outro = Jogo(caminho_salvamento=self.arquivo)
        self.assertTrue(outro.checkpoints.continuar())
        self.assertEqual(outro.estado, ESTADO_JOGANDO)
        self.assertIsNone(outro.introducao)
        self.assertEqual(outro.jogador.nome, 'Lia')
        self.assertEqual(outro.jogador.personagem, 'menina')
        self.assertEqual(outro.fase.identificador, 'a28')
