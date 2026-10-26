"""Contrato corporal, alinhamento dos sprites e estratégias dos encontros."""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import unittest
from unittest.mock import patch
from types import SimpleNamespace

import pygame
import assets
import settings
from entities.boss import Boss
from entities.player import Player
from world.level import Level
from world.legacy_levels import build_legacy_levels


class CharacterContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((960, 540))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_all_available_characters_share_body_size_and_clear_spawns(self):
        for data in build_legacy_levels():
            level = Level(data)
            entities = [Player(*level.player_spawn), level.boss, *level.enemies]
            for entity in entities:
                with self.subTest(level=data['index'], entity=type(entity).__name__):
                    self.assertEqual(entity.rect.size, settings.CHARACTER_SIZE)
                    self.assertEqual(entity.image.get_size(), settings.CHARACTER_SIZE)
                    self.assertFalse(any(entity.rect.colliderect(s) for s in level.tilemap.solids))
                    probe = entity.rect.move(0, 1)
                    self.assertTrue(any(probe.colliderect(s) for s in level.tilemap.solids))

    def test_all_romerbug_forms_keep_body_and_feet_alignment(self):
        boss = Level(build_legacy_levels()[0]).boss
        before = boss.rect.copy()
        boss.activate()
        boss.take_damage(8)
        self.assertEqual(boss.rect, before)
        self.assertEqual(boss.health, 8)
        for sprites in (boss.form_sprites, boss.motion_sprites):
            for directions in sprites.values():
                for sequence in directions.values():
                    for frame in sequence:
                        self.assertEqual(frame.get_size(), settings.CHARACTER_SIZE)
                        self.assertEqual(frame.get_bounding_rect().bottom, settings.CHARACTER_SIZE[1])

    def test_sprite_normalization_preserves_proportions_and_relative_pose_scale(self):
        wide = pygame.Surface((100, 100), pygame.SRCALPHA)
        wide.fill((0, 0, 0, 0))
        pygame.draw.rect(wide, 'white', (20, 20, 40, 60))
        crouched = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.rect(crouched, 'white', (20, 20, 40, 30))
        assets.clear_cache()
        with patch.object(assets, 'load_image', side_effect=[wide, crouched]):
            frames = assets.load_character_frames(['test/tall', 'test/crouched'])
        tall_bounds, short_bounds = [f.get_bounding_rect() for f in frames]
        self.assertEqual(tall_bounds.width, short_bounds.width)
        self.assertAlmostEqual(tall_bounds.height / short_bounds.height, 2, delta=0.1)
        self.assertAlmostEqual(tall_bounds.width / tall_bounds.height, 40 / 60, delta=0.05)
        self.assertEqual(tall_bounds.bottom, settings.CHARACTER_SIZE[1])
        self.assertEqual(short_bounds.bottom, settings.CHARACTER_SIZE[1])

    def test_generic_boss_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Boss(0, 0, 'Generic', 'Subject', (0, 0, 0))

    def test_unknown_boss_type_is_rejected_instead_of_using_generic(self):
        data = build_legacy_levels()[0]
        data['boss'] = dict(data['boss'], boss_type='unknown')
        with self.assertRaises(KeyError):
            Level(data)

    def test_legacy_strategies_respond_to_distance_phase_and_cycles(self):
        bosses = {data['boss']['boss_type']: Level(data).boss for data in build_legacy_levels()}
        player = SimpleNamespace(rect=pygame.Rect(0, 0, *settings.CHARACTER_SIZE))
        python = bosses['python']
        player.rect.center = python.rect.center
        self.assertEqual(python.choose_attack(player), 'lunge')
        player.rect.x -= 200
        self.assertEqual(python.choose_attack(player), 'spread')
        java = bosses['java']
        self.assertEqual([java.choose_attack(player) for _ in range(3)], ['slam', 'lunge', 'slam'])
        c = bosses['c']
        self.assertEqual(c.choose_attack(player), 'lunge')
        c.activate()
        c.take_damage(c.max_health // 2)
        self.assertEqual(c.choose_attack(player), 'spread')
        sql = bosses['sql']
        player.rect.centery = sql.rect.centery + 50
        self.assertEqual(sql.choose_attack(player), 'slam')
        player.rect.centery -= 100
        self.assertEqual(sql.choose_attack(player), 'spread')
        assembly = bosses['assembly']
        self.assertEqual([assembly.choose_attack(player) for _ in range(4)],
                         ['spread', 'lunge', 'slam', 'spread'])


if __name__ == '__main__':
    unittest.main()
