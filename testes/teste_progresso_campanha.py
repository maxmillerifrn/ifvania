"""Regressões do primeiro incremento de arquitetura da campanha."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')

import unittest
import pygame
from mundo.fabrica_cenas import FabricaCenas
from sistema.eventos_campanha import EventosCampanha, ChefeDerrotado, FaseConcluida
from sistema.progresso_campanha import ProgressoCampanha
from sistema.jogo import Jogo, ESTADO_FIM_CONTEUDO


class TestesEventosCampanha(unittest.TestCase):
    def test_observadores_seguem_ordem_sem_duplicacao_e_podem_ser_removidos(self):
        eventos = EventosCampanha()
        recebidos = []

        def registrar(evento):
            recebidos.append(('primeiro', evento.identificador_fase))

        remover = eventos.inscrever(FaseConcluida, registrar)
        eventos.inscrever(FaseConcluida, registrar)
        eventos.inscrever(FaseConcluida, lambda evento: recebidos.append(('segundo', evento.identificador_fase)))
        eventos.emitir(ChefeDerrotado('a28'))
        self.assertEqual(recebidos, [])
        eventos.emitir(FaseConcluida('a28'))
        remover()
        remover()
        eventos.emitir(FaseConcluida('biblioteca'))
        self.assertEqual(recebidos, [('primeiro', 'a28'), ('segundo', 'a28'), ('segundo', 'biblioteca')])

    def test_remocao_durante_entrega_nao_pula_observador_seguinte(self):
        eventos = EventosCampanha()
        recebidos = []

        def primeiro(evento):
            recebidos.append('primeiro')
            remover()

        remover = eventos.inscrever(FaseConcluida, primeiro)
        eventos.inscrever(FaseConcluida, lambda evento: recebidos.append('segundo'))
        eventos.emitir(FaseConcluida('a28'))
        eventos.emitir(FaseConcluida('a28'))
        self.assertEqual(recebidos, ['primeiro', 'segundo', 'segundo'])

    def test_progresso_idempotente_e_sessao_encerrada_nao_recebe_eventos(self):
        eventos = EventosCampanha()
        progresso = ProgressoCampanha(eventos)
        for _ in range(2):
            eventos.emitir(ChefeDerrotado('a28'))
            eventos.emitir(FaseConcluida('a28'))
        self.assertEqual(progresso.chefes_derrotados, {'a28'})
        self.assertEqual(progresso.fases_concluidas, {'a28'})
        progresso.encerrar()
        progresso.encerrar()
        eventos.emitir(FaseConcluida('biblioteca'))
        self.assertEqual(progresso.fases_concluidas, {'a28'})
        self.assertEqual(ProgressoCampanha(eventos).fases_concluidas, set())


class TestesFabricaCenas(unittest.TestCase):
    def test_tipo_ambiente_e_registro_invalidos_falham_sem_substituto(self):
        fabrica = FabricaCenas(EventosCampanha())
        with self.assertRaisesRegex(ValueError, 'Tipo de cena desconhecido'):
            fabrica.criar('ausente')
        with self.assertRaisesRegex(ValueError, 'Ambiente escolar desconhecido'):
            fabrica.criar('escola', ambiente='ausente')
        with self.assertRaisesRegex(ValueError, 'já registrado'):
            fabrica.registrar('fase', dict)
        with self.assertRaises(ValueError):
            fabrica.registrar('nova', None)
        fabrica.registrar('nova', lambda destino: ('cena', destino))
        self.assertEqual(fabrica.criar('nova', destino='jardim'), ('cena', 'jardim'))


class TestesIntegracaoProgresso(unittest.TestCase):
    def setUp(self):
        self.jogo = Jogo()

    def tearDown(self):
        pygame.quit()

    def test_vitoria_real_registra_chefe_uma_vez_antes_da_saida(self):
        self.jogo._load_level(1, novo_jogador=True)
        fase = self.jogo.fase
        recebidos = []
        self.jogo.eventos_campanha.inscrever(ChefeDerrotado, recebidos.append)
        fase.chefe.activate()
        fase.chefe.take_damage(fase.chefe.vida)
        fase.update(self.jogo.jogador, [])
        fase.update(self.jogo.jogador, [])
        self.assertEqual(recebidos, [ChefeDerrotado('biblioteca')])
        self.assertEqual(self.jogo.progresso_campanha.chefes_derrotados, {'biblioteca'})
        self.assertEqual(self.jogo.progresso_campanha.fases_concluidas, set())

    def test_progresso_e_atualizado_antes_da_navegacao_e_final_nao_duplica(self):
        self.jogo._load_level(0, novo_jogador=True)
        observados = []
        self.jogo.eventos_campanha.inscrever(FaseConcluida, lambda evento: observados.append(
            (self.jogo.indice_fase, self.jogo.progresso_campanha.fases_concluidas)))
        self.jogo._advance_level()
        self.assertEqual(observados, [(0, frozenset({'a28'}))])
        self.assertEqual(self.jogo.fase.setor, 'convivencia')
        self.jogo._load_level(1)
        self.jogo._advance_level()
        self.jogo._advance_level()
        self.assertEqual(self.jogo.fase.setor, 'convivencia')
        self.assertEqual(self.jogo.indice_fase, 1)
        self.assertEqual(len(observados), 2)
        self.assertEqual(self.jogo.progresso_campanha.fases_concluidas, {'a28', 'biblioteca'})

    def test_nova_campanha_limpa_progresso_e_desliga_observador_antigo(self):
        eventos_antigos = self.jogo.eventos_campanha
        progresso_antigo = self.jogo.progresso_campanha
        eventos_antigos.emitir(FaseConcluida('a28'))
        self.jogo._start_story()
        self.assertEqual(self.jogo.progresso_campanha.fases_concluidas, set())
        eventos_antigos.emitir(FaseConcluida('biblioteca'))
        self.assertEqual(progresso_antigo.fases_concluidas, {'a28'})
        self.assertEqual(self.jogo.progresso_campanha.fases_concluidas, set())

    def test_recarregar_fase_concluida_nao_bloqueia_a_saida_da_nova_instancia(self):
        self.jogo._load_level(1, novo_jogador=True)
        self.jogo._advance_level()
        self.jogo._load_level(1, novo_jogador=True)
        self.jogo._advance_level()
        self.assertEqual(self.jogo.fase.setor, 'convivencia')
        self.assertEqual(self.jogo.indice_fase, 1)
        self.assertEqual(self.jogo.progresso_campanha.fases_concluidas, {'biblioteca'})


if __name__ == '__main__':
    unittest.main()
