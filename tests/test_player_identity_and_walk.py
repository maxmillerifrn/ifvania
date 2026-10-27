"""Entrada de nome, falas personalizadas e caminhada sincronizada ao movimento."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')

from collections import defaultdict
import unittest
import pygame
from entities.player import Player
from game import (Game, STATE_MENU, STATE_CHARACTER_SELECT, STATE_NAME_ENTRY,
                  STATE_DIALOGUE, STATE_GAME_OVER)
from world.levels_data import STORY_INTRO, REUNION_DIALOGUE, AFTER_BOSS_DIALOGUE
from world.school_data import ENCOUNTER_DIALOGUE, MOUSE_DISCOVERY


class PlayerIdentityAndWalkTests(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.keys = defaultdict(bool)
        self.floor = [pygame.Rect(0, 352, 3000, 100)]

    def tearDown(self):
        pygame.quit()

    def key(self, key):
        return self.game._process_events([pygame.event.Event(pygame.KEYDOWN, key=key)])

    def type(self, value):
        self.game._process_events([pygame.event.Event(pygame.TEXTINPUT, text=value)])

    def name_screen(self, girl=False):
        self.key(pygame.K_RETURN)
        if girl: self.key(pygame.K_RIGHT)
        self.key(pygame.K_RETURN)
        self.assertEqual(self.game.state, STATE_NAME_ENTRY)

    def test_name_with_accents_opens_student_teacher_dialogue_without_consuming_confirmation(self):
        self.name_screen(girl=True)
        self.type('Joa\u0303o')
        self.key(pygame.K_BACKSPACE)
        self.type('o')
        self.key(pygame.K_RETURN)
        self.assertEqual(self.game.state, STATE_DIALOGUE)
        self.assertEqual(self.game.player_name, 'João')
        self.assertEqual(self.game.player.name, 'João')
        self.assertEqual(self.game.player.character, 'girl')
        self.assertEqual(self.game.dialogue_box.lines[0][0], 'João')
        self.assertEqual(self.game.dialogue_box.index, 0)
        self.assertEqual(self.game.dialogue_box._char_shown, 0)
        self.assertEqual({speaker for speaker, _ in self.game.dialogue_box.lines}, {'João', 'Professor Max'})
        self.assertTrue(any('João' in text for speaker, text in self.game.dialogue_box.lines if speaker == 'Professor Max'))

    def test_blank_name_does_not_start_and_input_is_limited_and_can_return(self):
        self.name_screen()
        self.key(pygame.K_RETURN)
        self.assertEqual(self.game.state, STATE_NAME_ENTRY)
        self.assertIsNone(self.game.player)
        self.assertTrue(self.game.name_error)
        self.type(' \n\t ')
        self.key(pygame.K_RETURN)
        self.assertEqual(self.game.state, STATE_NAME_ENTRY)
        self.game.name_buffer = ''
        self.type('Á'*30)
        self.assertEqual(self.game.name_buffer, 'Á'*20)
        self.key(pygame.K_BACKSPACE)
        self.assertEqual(len(self.game.name_buffer), 19)
        self.key(pygame.K_ESCAPE)
        self.assertEqual(self.game.state, STATE_CHARACTER_SELECT)
        self.assertIsNone(self.game.player)
        self.key(pygame.K_RETURN)
        self.assertEqual(self.game.name_buffer, 'Á'*19)
        self.game._draw()

    def test_name_stays_through_scenes_and_new_campaign_resets_only_progress(self):
        self.name_screen()
        self.type('  Ana   Luiza  ')
        self.key(pygame.K_RETURN)
        self.assertEqual(self.game.player_name, 'Ana Luiza')
        player = self.game.player
        self.game._load_school('corridor')
        self.game._load_level(0)
        self.assertIs(self.game.player, player)
        self.assertEqual(player.name, 'Ana Luiza')
        self.game.dialogue_box.start(REUNION_DIALOGUE)
        self.assertTrue(any('Ana Luiza' in text for speaker, text in self.game.dialogue_box.lines if speaker == 'Professor Romerito'))
        self.game.state = STATE_GAME_OVER
        self.key(pygame.K_RETURN)
        self.assertEqual(self.game.state, STATE_MENU)
        self.name_screen()
        self.assertEqual(self.game.name_buffer, 'Ana Luiza')
        self.key(pygame.K_RETURN)
        self.assertIsNot(self.game.player, player)
        self.assertEqual(self.game.player.name, 'Ana Luiza')
        self.assertEqual(self.game.player.abilities, set())
        self.assertFalse(self.game.player.whip_unlocked)

    def test_personalization_does_not_mutate_shared_dialogue_or_keep_other_player_name(self):
        source = list(STORY_INTRO)
        box = self.game.dialogue_box
        for name in ('Lívia', 'Miguel'):
            box.player_name = name
            for lines in (STORY_INTRO, REUNION_DIALOGUE, ENCOUNTER_DIALOGUE, MOUSE_DISCOVERY, AFTER_BOSS_DIALOGUE):
                box.start(lines)
                self.assertIn(name, {speaker for speaker, _ in box.lines})
                self.assertNotIn('Narrador', {speaker for speaker, _ in box.lines})
                self.assertFalse(any('{player}' in text for _, text in box.lines))
                self.assertTrue(all(len(box._wrap(text, 810)) <= 3 for _, text in box.lines))
        self.assertEqual(STORY_INTRO, source)
        self.assertIn('Aluno(a)', {speaker for speaker, _ in STORY_INTRO})

    def test_walk_cycles_all_eight_frames_and_stops_against_wall(self):
        for character in ('boy', 'girl'):
            player = Player(120, 312, character)
            player.on_ground = True
            keys = defaultdict(bool, {pygame.K_d: True})
            frames = set()
            for _ in range(96):
                player.handle_input(keys, [])
                player.update(self.floor, [])
                self.assertEqual(player.anim_state, 'walk')
                frames.add(player.anim_frame)
            self.assertEqual(frames, set(range(8)))
            wall = pygame.Rect(player.rect.right, 0, 32, 352)
            x = player.rect.x
            for _ in range(60):
                player.handle_input(keys, [])
                player.update(self.floor+[wall], [])
            self.assertEqual(player.rect.x, x)
            self.assertEqual(player.anim_state, 'idle')
            self.assertEqual(player.walk_distance, 0)

    def test_same_distance_at_different_speeds_has_same_walk_phase(self):
        players = []
        for speed in (2, 4):
            player = Player(120, 312)
            player.on_ground = True
            for _ in range(60//speed):
                player.vel.x = speed
                player.update(self.floor, [])
            players.append(player)
        self.assertEqual(players[0].rect.x, players[1].rect.x)
        self.assertEqual(players[0].anim_frame, players[1].anim_frame)
        self.assertEqual(players[0].walk_distance, players[1].walk_distance)

    def test_start_and_respawn_use_standing_pose_and_jump_does_not_cycle_walk(self):
        player = Player(120, 312)
        self.assertEqual(player.anim_state, 'idle')
        self.assertIs(player.image, player.sprites['idle_r'][0])
        player.on_ground = True
        keys = defaultdict(bool, {pygame.K_d: True})
        player.handle_input(keys, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)])
        for _ in range(12):
            player.update(self.floor, [])
            self.assertEqual(player.anim_state, 'jump')
            self.assertEqual(player.walk_distance, 0)
        player.respawn(120, 312)
        self.assertEqual(player.anim_state, 'idle')
        self.assertEqual(player.anim_frame, 0)
        self.assertIs(player.image, player.sprites['idle_r'][0])


if __name__ == '__main__':
    unittest.main()
