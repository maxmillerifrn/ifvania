"""Aceite do prólogo: caminhada real, interações e passagem ao mundo virtual."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')

from collections import defaultdict
import unittest
import pygame
import settings
from entities.npc import Teacher
from game import (Game, STATE_PLAYING, STATE_DIALOGUE, STATE_LEVEL_CARD,
                  STATE_ABDUCTION, STATE_PAUSE)
from world.school import SchoolLevel
from world.school_data import MOUSE_DISCOVERY


class SchoolStoryTests(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.keys = defaultdict(bool)

    def tearDown(self):
        pygame.quit()

    def key(self, key):
        return self.game._process_events([pygame.event.Event(pygame.KEYDOWN, key=key)])

    def finish_dialogue(self):
        for _ in range(80):
            if not self.game.dialogue_box.active:
                return
            self.key(pygame.K_e)
            self.game._update(self.keys, [])
        self.fail('Diálogo não terminou')

    def start_corridor(self, character='boy'):
        self.game.selected_character = character
        self.game._start_story()
        self.finish_dialogue()
        self.assertEqual(self.game.state, STATE_LEVEL_CARD)
        self.key(pygame.K_RETURN)

    def walk_to(self, x):
        keys = defaultdict(bool, {pygame.K_d: True})
        for _ in range(600):
            if self.game.player.rect.x >= x:
                break
            self.game._update(keys, [])
        self.assertGreaterEqual(self.game.player.rect.x, x)

    def enter_lab(self):
        self.walk_to(self.game.level.a28_door.x - 40)
        events = self.key(pygame.K_e)
        self.game._update(self.keys, events)
        self.assertEqual(self.game.level.room, 'lab')

    def begin_encounter(self):
        self.walk_to(630)
        events = self.key(pygame.K_e)
        self.game._update(self.keys, events)
        self.assertEqual(self.game.state, STATE_DIALOGUE)

    def test_both_protagonists_walk_entire_route_and_get_mouse_only_after_discovery(self):
        for character in ('boy', 'girl'):
            with self.subTest(character=character):
                self.start_corridor(character)
                player = self.game.player
                self.assertFalse(player.whip_unlocked)
                self.assertIsNone(self.game.level.boss)
                self.enter_lab()
                self.assertIs(self.game.player, player)
                self.assertGreater(self.game.level.tilemap.width, 0)
                self.begin_encounter()
                self.finish_dialogue()
                self.assertEqual(self.game.state, STATE_ABDUCTION)
                for _ in range(self.game.abduction_duration):
                    self.game._update(self.keys, [])
                self.assertEqual(self.game.state, STATE_DIALOGUE)
                self.assertEqual(self.game.dialogue_box.lines, MOUSE_DISCOVERY)
                self.assertEqual(self.game.player.character, character)
                self.assertIs(self.game.player, player)
                self.assertFalse(player.whip_unlocked)
                player._try_melee()
                self.assertEqual(player.attacking_timer, 0)
                boss = self.game.level.boss
                initial = (boss.health, boss.attack_timer, player.health, player.rect.copy())
                for _ in range(200):
                    self.game._update(self.keys, [])
                self.assertEqual((boss.health, boss.attack_timer, player.health, player.rect), initial)
                self.assertFalse(boss.active)
                self.finish_dialogue()
                self.assertTrue(player.whip_unlocked)
                self.assertFalse(player.abilities)
                self.assertEqual(self.game.state, STATE_LEVEL_CARD)
                self.key(pygame.K_RETURN)
                events = self.key(pygame.K_x)
                self.game._update(self.keys, events)
                self.assertGreater(player.attacking_timer, 0)
                self.assertEqual(player.character, character)

    def test_intro_shows_max_and_corrupts_monitors_when_ai_revolts(self):
        self.game._start_story()
        room = self.game.level
        self.assertEqual(room.room, 'classroom')
        self.assertEqual(next(iter(room.npcs)).name, 'Professor Max')
        self.assertFalse(room.corrupted)
        self.game.dialogue_box.index = 4
        self.game._update(self.keys, [])
        self.assertTrue(room.corrupted)
        self.assertEqual(room.ticks, 0)
        self.assertFalse(self.game.player.whip_unlocked)

    def test_interaction_requires_proximity_and_e_and_fires_once(self):
        self.start_corridor()
        corridor = self.game.level
        self.assertIsNone(corridor.update(self.game.player,
                                         [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)])[0])
        self.walk_to(corridor.a28_door.x-40)
        self.assertIsNone(corridor.update(self.game.player, [])[0])
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)
        self.assertEqual(corridor.update(self.game.player, [event])[0], 'enter_lab')
        self.assertIsNone(corridor.update(self.game.player, [event])[0])
        lab = SchoolLevel('lab')
        player = self.game.player
        player.rect.x = 630
        self.assertIsNone(lab.update(player, [])[0])
        self.assertEqual(lab.update(player, [event])[0], 'school_encounter')
        self.assertIsNone(lab.update(player, [event])[0])

    def test_pause_and_dialogue_freeze_school_and_abduction(self):
        self.start_corridor()
        self.enter_lab()
        self.begin_encounter()
        room = self.game.level
        npc = next(iter(room.npcs))
        snapshot = (room.ticks, npc.animation_tick, self.game.player.rect.copy())
        for _ in range(100):
            self.game._update(self.keys, [])
        self.assertEqual((room.ticks, npc.animation_tick, self.game.player.rect), snapshot)
        self.finish_dialogue()
        self.game._update(self.keys, [])
        timer = self.game.abduction_timer
        self.key(pygame.K_ESCAPE)
        self.assertEqual(self.game.state, STATE_PAUSE)
        for _ in range(120):
            self.game._update(self.keys, [])
        self.assertEqual(self.game.abduction_timer, timer)
        self.key(pygame.K_ESCAPE)
        self.assertEqual(self.game.state, STATE_ABDUCTION)
        self.game._update(self.keys, [])
        self.assertEqual(self.game.abduction_timer, timer+1)

    def test_weapon_stays_locked_after_school_respawn(self):
        self.start_corridor()
        player = self.game.player
        player.respawn(*self.game.level.player_spawn)
        player._try_melee()
        self.assertFalse(player.whip_unlocked)
        self.assertEqual(player.attacking_timer, 0)

    def test_romerito_approaches_and_player_recoils_before_transport_without_losing_life(self):
        self.start_corridor()
        self.enter_lab()
        self.begin_encounter()
        self.finish_dialogue()
        npc = next(iter(self.game.level.npcs))
        initial_npc = npc.rect.x
        initial_player = self.game.player.rect.x
        for _ in range(18):
            self.game._update(self.keys, [])
        self.assertLess(npc.rect.x, initial_npc)
        self.assertLess(self.game.player.rect.x, initial_player)
        self.assertEqual(self.game.player.health, self.game.player.max_health)
        self.assertFalse(self.game.player.whip_unlocked)

    def test_school_geometry_supports_characters_and_camera_stays_in_bounds(self):
        self.game._start_story()
        player = self.game.player
        for room_name in ('classroom', 'corridor', 'lab'):
            room = SchoolLevel(room_name)
            player.respawn(*room.player_spawn)
            for body in [player, *room.npcs]:
                self.assertEqual(body.rect.size, settings.CHARACTER_SIZE)
                self.assertFalse(any(body.rect.colliderect(s) for s in room.tilemap.solids))
                self.assertTrue(any(body.rect.move(0, 1).colliderect(s) for s in room.tilemap.solids))
            for x in (-500, 0, 1000, 3000):
                player.rect.x = x
                room.camera.update(player.rect)
                self.assertGreaterEqual(room.camera.offset.x, 0)
                self.assertLessEqual(room.camera.offset.x,
                                     max(0, room.tilemap.width-settings.SCREEN_WIDTH))

    def test_teachers_have_transparent_complete_frames_and_same_body_contract(self):
        for identity in Teacher.NAMES:
            npc = Teacher(0, 0, identity)
            self.assertEqual(npc.rect.size, settings.CHARACTER_SIZE)
            for image in npc.frames:
                self.assertEqual(image.get_size(), settings.CHARACTER_SIZE)
                self.assertEqual(image.get_bounding_rect().bottom, settings.CHARACTER_SIZE[1])
                self.assertEqual(image.get_at((0, 0)).a, 0)

    def test_every_school_dialogue_fits_in_panel_and_window_can_close_during_abduction(self):
        from world.levels_data import STORY_INTRO
        from world.school_data import ENCOUNTER_DIALOGUE
        for _, text in STORY_INTRO + ENCOUNTER_DIALOGUE + MOUSE_DISCOVERY:
            self.assertLessEqual(len(self.game.dialogue_box._wrap(text, 810)), 3)
        self.game.state = STATE_ABDUCTION
        self.game._process_events([pygame.event.Event(pygame.QUIT)])
        self.assertFalse(self.game.running)


if __name__ == '__main__':
    unittest.main()
