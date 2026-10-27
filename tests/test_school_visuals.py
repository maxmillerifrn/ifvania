"""Escala legível, terminais recortados e animação visual independente da física."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')

from collections import defaultdict
import unittest
import pygame
from game import Game, STATE_DIALOGUE, STATE_PAUSE, STATE_PLAYING
from entities.npc import Teacher
from entities.enemy import Enemy
from entities.player import Player
from world.terminal import TerminalScreen
from world.camera import Camera
from world.school_art import SchoolArt


class SchoolVisualTests(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.keys = defaultdict(bool)

    def tearDown(self):
        pygame.quit()

    def test_larger_cast_preserves_body_size_feet_and_distinction_from_bugs(self):
        self.game._load_level(0, fresh_player=True)
        cast = [Player(120, 312, 'boy'), Player(120, 312, 'girl'),
                Teacher(700, 312, 'max'), Teacher(700, 312, 'romerito'), self.game.level.boss]
        for actor in cast:
            self.assertEqual(actor.get_draw_image().get_size(), (80, 80))
            self.assertEqual(actor.rect.size, (40, 40))
            visual = actor.get_draw_image().get_rect(midbottom=actor.rect.midbottom)
            self.assertEqual(visual.bottom, actor.rect.bottom)
        self.assertEqual(Enemy(0, 0).get_draw_image().get_size(), (40, 40))

    def test_terminal_changes_information_only_inside_monitor_and_restores_clipping(self):
        terminal = TerminalScreen()
        rect = pygame.Rect(40, 35, 72, 46)
        initial = pygame.Surface((160, 120))
        initial.fill((190, 100, 20))
        images = []
        for tick in (0, 35, 160, 315):
            surface = initial.copy()
            clip = surface.get_clip()
            terminal.draw(surface, rect, tick)
            self.assertEqual(surface.get_clip(), clip)
            for x in range(surface.get_width()):
                for y in range(surface.get_height()):
                    if not rect.collidepoint(x, y):
                        self.assertEqual(surface.get_at((x, y)), initial.get_at((x, y)))
            images.append(pygame.image.tostring(surface, 'RGB'))
        self.assertGreater(len(set(images)), 2)

    def test_scenery_information_tracks_camera_and_does_not_paint_bezels(self):
        art = SchoolArt('lab', 1920)
        camera = Camera(1920, 540)
        camera.offset.x = 960
        first = pygame.Surface((960, 540))
        second = first.copy()
        art.draw(first, camera, 0, False)
        art.draw(second, camera, 70, False)
        before = pygame.image.tostring(first, 'RGB')
        after = pygame.image.tostring(second, 'RGB')
        rects = [camera.apply(rect) for rect in art.monitor_screens]
        changes = 0
        for i in range(0, len(before), 3):
            if before[i:i+3] != after[i:i+3]:
                pixel = i//3
                self.assertTrue(any(r.collidepoint(pixel % 960, pixel//960) for r in rects))
                changes += 1
        self.assertGreater(changes, 50)

    def test_monitors_animate_during_intro_without_advancing_world_and_pause_freezes_them(self):
        self.game._start_story()
        room = self.game.level
        body = self.game.player.rect.copy()
        for _ in range(60): self.game._update(self.keys, [])
        self.assertEqual(self.game.state, STATE_DIALOGUE)
        self.assertEqual(room.ticks, 0)
        self.assertEqual(room.visual_ticks, 60)
        self.assertEqual(self.game.player.rect, body)
        self.game._process_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)])
        self.assertEqual(self.game.state, STATE_PAUSE)
        for _ in range(60): self.game._update(self.keys, [])
        self.assertEqual(room.visual_ticks, 60)

    def test_battle_monitors_change_during_dialogue_and_pause_holds_frame(self):
        self.game._load_level(0, fresh_player=True)
        level = self.game.level
        self.game.state = STATE_DIALOGUE
        self.game.dialogue_box.start([('Sistema', 'Acesso ao laboratório.')])
        initial = (level.boss.rect.copy(), level.boss.attack_timer)
        for _ in range(70): self.game._update(self.keys, [])
        self.assertEqual(level.school_scene.visual_ticks, 70)
        self.assertEqual((level.boss.rect, level.boss.attack_timer), initial)
        self.game._process_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)])
        for _ in range(70): self.game._update(self.keys, [])
        self.assertEqual(level.school_scene.visual_ticks, 70)

    def test_whip_follows_scaled_hand_without_extending_tip_trajectory(self):
        player = Player(200, 312)
        player._try_melee()
        player.attacking_timer = player.whip.DURATION-10
        player.VISUAL_SCALE = 1.0
        normal = player.whip.points(player)
        player.VISUAL_SCALE = 2.0
        larger = player.whip.points(player)
        self.assertNotEqual(normal[0], larger[0])
        self.assertEqual(normal[-1], larger[-1])
        self.assertEqual(player.rect.size, (40, 40))
        wall = pygame.Rect(player.rect.right, 250, 32, 150)
        self.assertTrue(all(p.x <= wall.left for p in player.whip.points(player, [wall])))


if __name__ == '__main__':
    unittest.main()
