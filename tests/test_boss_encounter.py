"""Regressões do acesso à arena e do combate pelo fluxo real do jogo."""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import unittest
import pygame
from entities.player import Player
from game import Game, STATE_PLAYING, STATE_DIALOGUE
from world.level import Level
from world.legacy_levels import build_legacy_levels


class BossEncounterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((960, 540))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_entering_in_air_or_beyond_old_trigger_activates_all_bosses(self):
        for data in build_legacy_levels():
            for height in (80, 300, 408):
                for beyond in (0, 100):
                    with self.subTest(level=data['index'], height=height, beyond=beyond):
                        level = Level(data)
                        player = Player(level.tilemap.dialogue_trigger.x + beyond, height)
                        event, _ = level.update(player, [])
                        self.assertEqual(event, 'dialogue')
                        self.assertTrue(level.boss.active)
                        self.assertNotEqual(level.update(player, [])[0], 'dialogue')

    def test_exploration_before_arena_does_not_activate_boss(self):
        for data in build_legacy_levels():
            level = Level(data)
            player = Player(0, 300)
            player.rect.right = level.tilemap.dialogue_trigger.left
            player.pos.update(player.rect.topleft)
            self.assertIsNone(level.update(player, [])[0])
            self.assertFalse(level.boss.active)

    def test_all_bosses_have_clear_space_and_supporting_floor(self):
        for data in build_legacy_levels():
            level = Level(data)
            boss = level.boss
            self.assertFalse(any(boss.rect.colliderect(s) for s in level.tilemap.solids))
            floor_probe = pygame.Rect(boss.rect.left, boss.rect.bottom, boss.width, 1)
            self.assertTrue(any(floor_probe.colliderect(s) for s in level.tilemap.solids))
            arena_air = pygame.Rect(level.tilemap.dialogue_trigger.left, 32,
                                    level.tilemap.width - 32 - level.tilemap.dialogue_trigger.left,
                                    boss.rect.bottom - 32)
            self.assertFalse(any(arena_air.colliderect(s) for s in level.tilemap.solids))

    def test_entry_dialogue_precedes_damage_even_next_to_boss(self):
        level = Level(build_legacy_levels()[0])
        player = Player(level.boss.rect.left - 28, 408)
        player.facing = 1
        player._try_melee()
        health = level.boss.health
        self.assertEqual(level.update(player, [])[0], 'dialogue')
        self.assertEqual(level.boss.health, health)
        self.assertEqual(player.health, player.max_health)
        self.assertFalse(level.boss.projectiles)

    def test_game_dialogue_then_keyboard_melee_and_plane_deal_damage(self):
        game = Game()
        game.level_defs = build_legacy_levels()
        game._load_level(0, fresh_player=True)
        game.state = STATE_PLAYING
        boss = game.level.boss
        player = game.player
        player.pos.update(boss.rect.left - 75, 408)
        player.rect.topleft = player.pos
        player.facing = 1
        keys = pygame.key.get_pressed()
        game._update(keys, [])
        self.assertEqual(game.state, STATE_DIALOGUE)
        initial_timer = boss.attack_timer
        for _ in range(10):
            game._update(keys, [])
        self.assertEqual(boss.attack_timer, initial_timer)
        for _ in range(len(game.dialogue_box.lines) * 2):
            game.dialogue_box.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e))
        self.assertEqual(game.state, STATE_PLAYING)
        game._update(keys, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_x)])
        self.assertEqual(boss.health, boss.max_health)  # preparação do chicote
        for _ in range(15):
            game._update(keys, [])
        self.assertLess(boss.health, boss.max_health)
        self.assertEqual(boss.health, boss.max_health - 1)
        # Afasta o aluno para verificar o avião sem dano de contato.
        player.pos.x -= 80
        player.rect.x = round(player.pos.x)
        for _ in range(120):
            game._update(keys, [])
            if player.health < player.max_health:
                break
        self.assertEqual(boss.name, 'RomerBug')
        self.assertLess(player.health, player.max_health)


if __name__ == '__main__':
    unittest.main()
