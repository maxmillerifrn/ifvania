"""Aceite da etapa 4: percurso básico, infecção, combate e fim do conteúdo."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')

from collections import defaultdict
import unittest
import pygame
import settings
from entities.player import Player
from entities.projectile import Projectile
from game import (Game, STATE_PLAYING, STATE_DIALOGUE, STATE_INFECTION,
                  STATE_PAUSE, STATE_CONTENT_END, STATE_MENU, STATE_BOSS_TRANSFORMATION)
from world.level import Level
from world.levels_data import build_levels, REUNION_DIALOGUE, AFTER_BOSS_DIALOGUE
from world.legacy_levels import build_legacy_levels


class VirtualCampaignTests(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.keys = defaultdict(bool)
        self.game._load_level(0, fresh_player=True)
        self.game.state = STATE_PLAYING

    def tearDown(self):
        pygame.quit()

    def key(self, key):
        return self.game._process_events([pygame.event.Event(pygame.KEYDOWN, key=key)])

    def finish_dialogue(self):
        for _ in range(40):
            if not self.game.dialogue_box.active:
                return
            self.key(pygame.K_e)
        self.fail('Diálogo não terminou')

    def start_meeting(self):
        level = self.game.level
        player = self.game.player
        player.pos.update(level.tilemap.dialogue_trigger.left+10, level.player_spawn[1])
        player.rect.topleft = player.pos
        self.game._update(self.keys, [])
        self.assertEqual(self.game.state, STATE_DIALOGUE)
        return level, player, level.boss

    def start_fight(self):
        level, player, boss = self.start_meeting()
        self.finish_dialogue()
        self.assertEqual(self.game.state, STATE_INFECTION)
        for _ in range(self.game.infection_duration):
            self.game._update(self.keys, [])
        self.assertEqual(self.game.state, STATE_PLAYING)
        self.assertTrue(boss.active)
        return level, player, boss

    def defeat(self, boss, player, solids):
        boss.take_damage(boss.max_health//2)
        self.finish_transformation()
        boss.take_damage(boss.health)
        self.assertTrue(boss.defeated)

    def finish_transformation(self):
        for _ in range(400):
            if not self.game.level.boss.cinematic_pending:
                return
            if self.game.dialogue_box.active:
                self.key(pygame.K_e)
            self.game._update(self.keys, [])
        self.fail('Transição do boss não terminou')

    def test_main_campaign_has_only_defined_content_and_legacy_remains_separate(self):
        self.assertEqual(len(self.game.level_defs), 1)
        self.assertEqual(self.game.level_defs[0]['name'], 'Fase 1: Mundo virtual')
        self.assertIsNone(self.game.level_defs[0]['ability_reward'])
        self.assertEqual(len(build_legacy_levels()), 6)
        self.assertEqual(build_levels(), build_levels())

    def test_basic_movement_and_jump_reach_arena_and_exit_without_powers(self):
        for character in ('boy', 'girl'):
            with self.subTest(character=character):
                level = Level(build_levels()[0])
                player = Player(*level.player_spawn, character=character)
                keys = defaultdict(bool, {pygame.K_d: True})
                jumps = 0
                for _ in range(1000):
                    events = []
                    if player.on_ground:
                        events = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)]
                        jumps += 1
                    player.handle_input(keys, events)
                    player.update(level.tilemap.solids, level.tilemap.hazards)
                    self.assertFalse(any(player.rect.colliderect(s) for s in level.tilemap.solids))
                    if player.rect.colliderect(level.tilemap.exit_trigger):
                        break
                self.assertTrue(player.rect.colliderect(level.tilemap.exit_trigger))
                self.assertGreater(jumps, 0)
                self.assertEqual(player.abilities, set())
                self.assertEqual(player.max_health, 6)
                self.assertEqual(player.health, 6)

    def test_human_romerito_speaks_before_infection_and_cannot_take_damage(self):
        level, player, boss = self.start_meeting()
        self.assertFalse(level.infected)
        self.assertEqual(level.human_teacher.name, 'Professor Romerito')
        self.assertEqual(self.game.dialogue_box.lines, REUNION_DIALOGUE)
        text = ' '.join(line for _, line in REUNION_DIALOGUE)
        self.assertIn('Brasília', text)
        self.assertIn('corridas', text)
        self.assertIn('nunca mais', text)
        boss.take_damage(100)
        self.assertEqual(boss.health, boss.max_health)
        old_timer = boss.attack_timer
        for _ in range(120):
            self.game._update(self.keys, [])
            self.assertEqual(level.update(player, []), (None, None))
        self.assertEqual(boss.attack_timer, old_timer)
        self.assertFalse(boss.projectiles)
        self.assertFalse(boss.active)
        self.assertEqual(level.human_teacher.rect, boss.rect)

    def test_infection_swaps_visual_without_changing_body_or_health_and_then_starts_fight(self):
        level, player, boss = self.start_meeting()
        before = (boss.rect.copy(), boss.health, player.health, player.rect.copy())
        self.finish_dialogue()
        self.assertEqual(self.game.state, STATE_INFECTION)
        for _ in range(self.game.infection_duration//2):
            self.game._update(self.keys, [])
        self.assertTrue(level.infected)
        self.assertFalse(boss.active)
        self.assertEqual((boss.rect, boss.health, player.health, player.rect), before)
        for _ in range(self.game.infection_duration//2):
            self.game._update(self.keys, [])
        self.assertTrue(boss.active)
        self.assertFalse(level.encounter_pending)
        self.assertEqual(self.game.state, STATE_PLAYING)

    def test_infection_pauses_resumes_and_window_closes(self):
        self.start_meeting()
        self.finish_dialogue()
        self.game._update(self.keys, [])
        timer = self.game.infection_timer
        self.key(pygame.K_ESCAPE)
        self.assertEqual(self.game.state, STATE_PAUSE)
        for _ in range(100):
            self.game._update(self.keys, [])
        self.assertEqual(self.game.infection_timer, timer)
        self.key(pygame.K_ESCAPE)
        self.assertEqual(self.game.state, STATE_INFECTION)
        self.game._update(self.keys, [])
        self.assertEqual(self.game.infection_timer, timer+1)
        self.game._process_events([pygame.event.Event(pygame.QUIT)])
        self.assertFalse(self.game.running)

    def test_planes_then_medals_and_single_transform_keep_body_and_remaining_health(self):
        level, player, boss = self.start_fight()
        before = boss.rect.copy()
        boss._shoot(player)
        self.assertTrue(all(p.kind == 'plane' for p in boss.projectiles))
        boss.take_damage(7)
        self.assertFalse(boss.transformed)
        boss.take_damage(1)
        self.assertTrue(boss.transformed)
        self.assertEqual(boss.rect, before)
        self.assertEqual(boss.health, 8)
        self.assertEqual(boss.rect.size, settings.CHARACTER_SIZE)
        self.finish_transformation()
        boss._shoot(player)
        self.assertTrue(all(p.kind == 'medal' for p in boss.projectiles))
        boss.take_damage(1)
        self.assertEqual(boss.health, 7)
        self.assertEqual(boss.transform_timer, 0)
        self.assertEqual(boss.name, 'SpeedBug')

    def test_defeat_clears_threats_and_never_gives_an_old_reward(self):
        level, player, boss = self.start_fight()
        self.defeat(boss, player, level.tilemap.solids)
        player.projectiles.add(Projectile(200, 300, (1, 0)))
        self.assertTrue(level.enemies)
        self.game._update(self.keys, [])
        self.assertEqual(self.game.state, STATE_DIALOGUE)
        self.assertEqual(self.game.dialogue_box.lines, AFTER_BOSS_DIALOGUE)
        self.assertFalse(level.enemies)
        self.assertFalse(boss.projectiles)
        self.assertFalse(player.projectiles)
        self.assertFalse(level.powerups)
        self.finish_dialogue()
        for _ in range(150):
            self.game._update(self.keys, [])
        self.assertEqual(self.game.state, STATE_PLAYING)
        self.assertFalse(level.powerups)
        self.assertEqual(player.abilities, set())
        self.assertEqual(player.max_health, 6)
        self.assertEqual(player.health, 6)

    def test_exit_requires_defeat_and_ends_only_available_content_then_can_restart(self):
        level, player, boss = self.start_fight()
        player.rect.right = level.tilemap.exit_trigger.right
        player.rect.bottom = level.player_spawn[1]+settings.CHARACTER_SIZE[1]
        player.pos.update(player.rect.topleft)
        self.game._update(self.keys, [])
        self.assertEqual(self.game.state, STATE_PLAYING)
        self.assertFalse(level.completed)
        self.defeat(boss, player, level.tilemap.solids)
        self.game._update(self.keys, [])
        self.assertEqual(self.game.state, STATE_DIALOGUE)
        self.finish_dialogue()
        self.assertEqual(self.game.state, STATE_PLAYING)
        self.game._update(self.keys, [])
        self.assertEqual(self.game.state, STATE_CONTENT_END)
        self.assertTrue(level.completed)
        self.assertEqual(level.update(player, []), (None, None))
        self.game._draw()
        self.key(pygame.K_RETURN)
        self.assertEqual(self.game.state, STATE_MENU)
        self.key(pygame.K_RETURN)
        self.key(pygame.K_RETURN)
        self.assertEqual(self.game.level.room, 'classroom')
        self.assertIsNot(self.game.player, player)
        self.assertFalse(self.game.player.whip_unlocked)
        self.assertEqual(self.game.player.abilities, set())

    def test_every_new_dialogue_fits_in_three_lines(self):
        for _, text in REUNION_DIALOGUE+AFTER_BOSS_DIALOGUE:
            self.assertLessEqual(len(self.game.dialogue_box._wrap(text, 810)), 3)

    def test_both_characters_defeat_both_forms_using_keyboard_whip_without_powers(self):
        for character in ('boy', 'girl'):
            with self.subTest(character=character):
                self.game.selected_character = character
                self.game._load_level(0, fresh_player=True)
                self.game.state = STATE_PLAYING
                level, player, boss = self.start_fight()
                # Isola o funcionamento da arma do balanceamento de sobrevivência.
                player.invuln_timer = 10000
                saw_speedbug = False
                for _ in range(24):
                    player.pos.update(boss.rect.left-75, level.player_spawn[1])
                    player.rect.topleft = player.pos
                    player.vel.update(0, 0)
                    player.facing = 1
                    events = self.key(pygame.K_x)
                    self.game._update(self.keys, events)
                    for _ in range(settings.ATTACK_COOLDOWN+1):
                        self.game._update(self.keys, [])
                        saw_speedbug |= boss.transformed
                        if self.game.state == STATE_BOSS_TRANSFORMATION:
                            self.finish_transformation()
                        if self.game.state == STATE_DIALOGUE:
                            break
                    if boss.defeated:
                        break
                self.assertTrue(saw_speedbug)
                self.assertTrue(boss.defeated)
                self.assertEqual(self.game.state, STATE_DIALOGUE)
                self.assertEqual(player.character, character)
                self.assertFalse(player.abilities)
                self.assertEqual(player.max_health, 6)
                self.assertFalse(level.powerups)
                self.assertFalse(boss.projectiles)


if __name__ == '__main__':
    unittest.main()
