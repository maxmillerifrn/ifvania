"""Fluxo real de eventos entre menu, seleção, introdução e campanha."""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import unittest
from pathlib import Path

import pygame
import settings
from entities.player import Player
from entities.enemy import Enemy
from game import (Game, STATE_MENU, STATE_CHARACTER_SELECT, STATE_DIALOGUE,
                  STATE_LEVEL_CARD, STATE_PLAYING, STATE_PAUSE, STATE_GAME_OVER,
                  STATE_CONTENT_END)


class FrontendTests(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def tearDown(self):
        pygame.quit()

    def key(self, key):
        return self.game._process_events([pygame.event.Event(pygame.KEYDOWN, key=key)])

    def click(self, rect):
        return self.game._process_events([
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=rect.center)])

    def test_keyboard_requires_character_confirmation_before_intro(self):
        self.assertEqual(self.game.state, STATE_MENU)
        self.assertEqual(self.key(pygame.K_RETURN), [])
        self.assertEqual(self.game.state, STATE_CHARACTER_SELECT)
        self.assertIsNone(self.game.player)
        self.key(pygame.K_RIGHT)
        self.key(pygame.K_RETURN)
        self.assertEqual(self.game.state, STATE_DIALOGUE)
        self.assertEqual(self.game.player.character, 'girl')
        self.assertEqual(self.game.dialogue_box.index, 0)
        self.assertEqual(self.game.dialogue_box._char_shown, 0)
        self.assertEqual(self.game.player.abilities, set())

    def test_mouse_can_choose_either_character_and_confirm(self):
        for i, character in enumerate(('boy', 'girl')):
            with self.subTest(character=character):
                self.game.state = STATE_MENU
                self.click(self.game.frontend.menu_rects[0])
                self.click(self.game.frontend.character_rects[i])
                self.assertEqual(self.game.state, STATE_CHARACTER_SELECT)
                self.click(self.game.frontend.confirm_rect)
                self.assertEqual(self.game.player.character, character)
                self.assertEqual(self.game.dialogue_box.index, 0)

    def test_back_returns_to_menu_without_starting_campaign(self):
        self.key(pygame.K_RETURN)
        self.key(pygame.K_RIGHT)
        self.key(pygame.K_ESCAPE)
        self.assertEqual(self.game.state, STATE_MENU)
        self.assertIsNone(self.game.player)
        self.click(self.game.frontend.menu_rects[0])
        self.click(self.game.frontend.back_rect)
        self.assertEqual(self.game.state, STATE_MENU)

    def test_exit_button_and_keyboard_exit_stop_application(self):
        self.click(self.game.frontend.menu_rects[1])
        self.assertFalse(self.game.running)
        self.game.running = True
        self.game.menu_index = 0
        self.key(pygame.K_DOWN)
        self.key(pygame.K_RETURN)
        self.assertFalse(self.game.running)

    def test_menu_hover_updates_focus_without_starting_campaign(self):
        self.game._process_events([pygame.event.Event(
            pygame.MOUSEMOTION, pos=self.game.frontend.menu_rects[1].center)])
        self.assertEqual(self.game.menu_index, 1)
        self.assertEqual(self.game.state, STATE_MENU)
        self.assertIsNone(self.game.player)

    def test_character_survives_respawn_and_level_change_but_new_campaign_resets_progress(self):
        self.game.selected_character = 'girl'
        self.game._start_story()
        player = self.game.player
        from powerups import Ability
        player.grant_ability(Ability.DOUBLE_JUMP)
        player.respawn(*self.game.level.player_spawn)
        from world.legacy_levels import build_legacy_levels
        self.game.level_defs = build_legacy_levels()
        self.game._load_level(1)
        self.assertIs(self.game.player, player)
        self.assertEqual(player.character, 'girl')
        self.assertTrue(player.has(Ability.DOUBLE_JUMP))
        self.game.state = STATE_GAME_OVER
        self.key(pygame.K_RETURN)
        self.key(pygame.K_RETURN)
        self.key(pygame.K_RETURN)
        self.assertIsNot(self.game.player, player)
        self.assertEqual(self.game.player.character, 'girl')
        self.assertEqual(self.game.player.abilities, set())
        self.assertEqual(self.game.player.health, 6)

    def test_final_dialogue_key_does_not_skip_level_card_or_trigger_jump(self):
        self.game._start_story()
        self.game.dialogue_box.index = len(self.game.dialogue_box.lines) - 1
        self.game.dialogue_box._char_shown = 1000
        self.assertEqual(self.key(pygame.K_SPACE), [])
        self.assertEqual(self.game.state, STATE_LEVEL_CARD)
        self.assertEqual(self.game.player.vel.y, 0)

    def test_dialogue_input_does_not_leak_into_resumed_combat(self):
        self.game._load_level(0, fresh_player=True)
        self.game.state = STATE_DIALOGUE
        self.game.dialogue_box.start([('Aluno(a)', 'Continuar')],
                                     on_finish=self.game._resume_from_dialogue)
        self.game.dialogue_box._char_shown = 1000
        self.assertEqual(self.key(pygame.K_SPACE), [])
        self.assertEqual(self.game.state, STATE_PLAYING)
        self.assertEqual(self.game.player.vel.y, 0)

    def test_menu_selection_and_intro_do_not_advance_simulation(self):
        self.game._start_story()
        school = self.game.level
        initial = (school.ticks, self.game.player.rect.copy())
        for state in (STATE_MENU, STATE_CHARACTER_SELECT, STATE_DIALOGUE):
            self.game.state = state
            for _ in range(100):
                self.game._update(pygame.key.get_pressed(), [])
            self.assertEqual((school.ticks, self.game.player.rect), initial)

    def test_window_closes_from_each_screen(self):
        self.game._start_story()
        for state in (STATE_MENU, STATE_CHARACTER_SELECT, STATE_DIALOGUE,
                      STATE_LEVEL_CARD, STATE_PLAYING, STATE_PAUSE,
                      STATE_GAME_OVER, STATE_CONTENT_END):
            self.game.state = state
            self.game.running = True
            self.game._process_events([pygame.event.Event(pygame.QUIT)])
            self.assertFalse(self.game.running)

    def test_each_character_has_complete_distinct_frames_and_functional_whip(self):
        root = Path(__file__).resolve().parents[1] / 'assets' / 'images'
        boy = Player(200, 200, character='boy')
        girl = Player(200, 200, character='girl')
        self.assertIsNot(boy.sprites, girl.sprites)
        for key in boy.sprites:
            male = boy.sprites[key]
            female = girl.sprites[key]
            if not isinstance(male, list):
                male, female = [male], [female]
            self.assertEqual(len(male), len(female))
            for m, f in zip(male, female):
                self.assertEqual(f.get_size(), settings.CHARACTER_SIZE)
                self.assertGreater(f.get_bounding_rect().height, 0)
                self.assertEqual(f.get_at((0, 0)).a, 0)
                self.assertNotEqual(pygame.image.tostring(m, 'RGBA'),
                                    pygame.image.tostring(f, 'RGBA'))
        self.assertEqual(len(list((root / 'player' / 'girl').glob('*.png'))), 11)
        for player in (boy, girl):
            target = Enemy(260, 210, health=2)
            player._try_melee()
            for age in range(player.whip.DURATION):
                player.attacking_timer = player.whip.DURATION - age
                player.try_melee_hit(target, [])
            self.assertEqual(target.health, 1)
            self.assertEqual(player.rect.size, settings.CHARACTER_SIZE)


if __name__ == '__main__':
    unittest.main()
