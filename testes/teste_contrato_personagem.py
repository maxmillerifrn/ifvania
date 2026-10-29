"""Contrato corporal, alinhamento dos sprites e estratégias dos encontros."""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import unittest
from unittest.mock import patch
from types import SimpleNamespace

import pygame
import recursos
import configuracoes
from entidades.chefe import Chefe
from entidades.jogador import Jogador
from mundo.fase import Fase
from mundo.fases_antigas import build_legacy_levels


class TestesContratoPersonagem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((960, 540))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_all_available_characters_share_body_size_and_clear_spawns(self):
        for dados in build_legacy_levels():
            fase = Fase(dados)
            entidades = [Jogador(*fase.surgimento_jogador), fase.chefe, *fase.inimigos]
            for entidade in entidades:
                with self.subTest(level=dados['index'], entity=type(entidade).__name__):
                    self.assertEqual(entidade.rect.size, configuracoes.TAMANHO_PERSONAGEM)
                    self.assertEqual(entidade.image.get_size(), configuracoes.TAMANHO_PERSONAGEM)
                    self.assertFalse(any(entidade.rect.colliderect(s) for s in fase.mapa_blocos.solidos))
                    sondagem = entidade.rect.move(0, 1)
                    self.assertTrue(any(sondagem.colliderect(s) for s in fase.mapa_blocos.solidos))

    def test_all_romerbug_forms_keep_body_and_feet_alignment(self):
        chefe = Fase(build_legacy_levels()[0]).chefe
        antes = chefe.rect.copy()
        chefe.activate()
        chefe.take_damage(8)
        self.assertEqual(chefe.rect, antes)
        self.assertEqual(chefe.vida, 8)
        for figuras in (chefe.figuras_formas, chefe.figuras_movimento):
            for direcoes in figuras.values():
                for sequencia in direcoes.values():
                    for quadro in sequencia:
                        self.assertEqual(quadro.get_size(), configuracoes.TAMANHO_PERSONAGEM)
                        self.assertEqual(quadro.get_bounding_rect().bottom, configuracoes.TAMANHO_PERSONAGEM[1])

    def test_sprite_normalization_preserves_proportions_and_relative_pose_scale(self):
        largo = pygame.Surface((100, 100), pygame.SRCALPHA)
        largo.fill((0, 0, 0, 0))
        pygame.draw.rect(largo, 'white', (20, 20, 40, 60))
        ajoelhado = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.rect(ajoelhado, 'white', (20, 20, 40, 30))
        recursos.clear_cache()
        with patch.object(recursos, 'load_image', side_effect=[largo, ajoelhado]):
            quadros = recursos.load_character_frames(['test/tall', 'test/crouched'])
        limites_alto, limites_baixo = [f.get_bounding_rect() for f in quadros]
        self.assertEqual(limites_alto.width, limites_baixo.width)
        self.assertAlmostEqual(limites_alto.height / limites_baixo.height, 2, delta=0.1)
        self.assertAlmostEqual(limites_alto.width / limites_alto.height, 40 / 60, delta=0.05)
        self.assertEqual(limites_alto.bottom, configuracoes.TAMANHO_PERSONAGEM[1])
        self.assertEqual(limites_baixo.bottom, configuracoes.TAMANHO_PERSONAGEM[1])

    def test_generic_boss_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Chefe(0, 0, 'Generic', 'Subject', (0, 0, 0))

    def test_unknown_boss_type_is_rejected_instead_of_using_generic(self):
        dados = build_legacy_levels()[0]
        dados['boss'] = dict(dados['boss'], boss_type='unknown')
        with self.assertRaises(KeyError):
            Fase(dados)

    def test_legacy_strategies_respond_to_distance_phase_and_cycles(self):
        chefes = {dados['boss']['boss_type']: Fase(dados).chefe for dados in build_legacy_levels()}
        jogador = SimpleNamespace(rect=pygame.Rect(0, 0, *configuracoes.TAMANHO_PERSONAGEM))
        python = chefes['python']
        jogador.rect.center = python.rect.center
        self.assertEqual(python.choose_attack(jogador), 'lunge')
        jogador.rect.x -= 200
        self.assertEqual(python.choose_attack(jogador), 'spread')
        java = chefes['java']
        self.assertEqual([java.choose_attack(jogador) for _ in range(3)], ['slam', 'lunge', 'slam'])
        c = chefes['c']
        self.assertEqual(c.choose_attack(jogador), 'lunge')
        c.activate()
        c.take_damage(c.vida_maxima // 2)
        self.assertEqual(c.choose_attack(jogador), 'spread')
        sql = chefes['sql']
        jogador.rect.centery = sql.rect.centery + 50
        self.assertEqual(sql.choose_attack(jogador), 'slam')
        jogador.rect.centery -= 100
        self.assertEqual(sql.choose_attack(jogador), 'spread')
        assembly = chefes['assembly']
        self.assertEqual([assembly.choose_attack(jogador) for _ in range(4)],
                         ['spread', 'lunge', 'slam', 'spread'])


if __name__ == '__main__':
    unittest.main()
