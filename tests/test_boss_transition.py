"""Transição cinematográfica e legibilidade da interface em condições reais."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')

from collections import defaultdict
import unittest
import pygame
import settings
from game import Game, STATE_PLAYING, STATE_BOSS_TRANSFORMATION, STATE_PAUSE
from powerups import Ability
from entities.projectile import Projectile
from ui import theme


class BossTransitionTests(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game._load_level(0, fresh_player=True)
        self.game.state = STATE_PLAYING
        self.level = self.game.level
        self.level.dialogue_played = True
        self.level.infected = True
        self.boss = self.level.boss
        self.boss.activate()
        self.player = self.game.player
        self.player.pos.update(self.boss.rect.x-90, self.level.player_spawn[1])
        self.player.rect.topleft = self.player.pos
        self.level.camera.update(self.player.rect)
        self.keys = defaultdict(bool)

    def tearDown(self):
        pygame.quit()

    def key(self, key):
        self.game._process_events([pygame.event.Event(pygame.KEYDOWN, key=key)])

    def begin(self, damage=8):
        self.boss.take_damage(damage)
        self.game._update(self.keys, [])
        self.assertEqual(self.game.state, STATE_BOSS_TRANSFORMATION)
        return self.game.boss_transition

    def until_speech(self):
        for _ in range(120):
            self.game._update(self.keys, [])
            if self.game.dialogue_box.active:
                return
        self.fail('A entidade não falou')

    def finish(self):
        for _ in range(400):
            if self.game.state == STATE_PLAYING:
                return
            if self.game.dialogue_box.active:
                self.key(pygame.K_e)
            self.game._update(self.keys, [])
        self.fail('A transição não terminou')

    def test_threshold_starts_kneeling_once_and_freezes_combat_and_health(self):
        self.boss.take_damage(7)
        self.assertFalse(self.boss.cinematic_pending)
        self.boss._shoot(self.player)
        self.player.projectiles.add(Projectile(100, 100, (1, 0)))
        self.player._try_melee()
        body = self.boss.rect.copy()
        transition = self.begin(1)
        self.assertEqual(transition.stage, 'kneel')
        self.assertEqual(self.boss.name, 'RomerBug')
        self.assertEqual(self.boss.health, 8)
        self.assertFalse(self.player.projectiles)
        self.assertFalse(self.boss.projectiles)
        self.assertEqual(self.player.attacking_timer, 0)
        snapshot = ([enemy.rect.copy() for enemy in self.level.enemies], self.player.rect.copy(), self.player.health)
        self.boss.take_damage(7)
        for _ in range(40):
            self.game._update(self.keys, [])
            self.assertEqual(self.boss.get_all_hit_rects(), [])
        self.assertEqual(self.boss.health, 8)
        self.assertEqual(self.boss.rect, body)
        self.assertEqual(([enemy.rect for enemy in self.level.enemies], self.player.rect, self.player.health), snapshot)

    def test_entity_says_requested_line_and_waits_for_player_before_morph(self):
        transition = self.begin()
        self.until_speech()
        self.assertEqual(self.game.dialogue_box.lines, [('Entidade', 'Ainda não terminou.')])
        self.assertEqual(transition.stage, 'speech')
        for _ in range(200): self.game._update(self.keys, [])
        self.assertEqual(transition.stage, 'speech')
        self.assertEqual(self.boss.name, 'RomerBug')
        self.key(pygame.K_e)
        self.assertEqual(transition.stage, 'morph')
        self.assertFalse(self.game.dialogue_box.active)

    def test_pause_freezes_motion_and_speech_and_resumes_same_stage(self):
        transition = self.begin()
        self.game._update(self.keys, [])
        tick = transition.tick
        self.key(pygame.K_ESCAPE)
        self.assertEqual(self.game.state, STATE_PAUSE)
        for _ in range(60): self.game._update(self.keys, [])
        self.assertEqual(transition.tick, tick)
        self.game._draw()
        self.key(pygame.K_ESCAPE)
        self.until_speech()
        self.key(pygame.K_ESCAPE)
        shown = self.game.dialogue_box._char_shown
        for _ in range(60): self.game._update(self.keys, [])
        self.assertEqual(self.game.dialogue_box._char_shown, shown)
        self.key(pygame.K_ESCAPE)
        self.assertEqual(self.game.state, STATE_BOSS_TRANSFORMATION)
        self.assertEqual(transition.stage, 'speech')

    def test_finishes_in_second_form_preserving_health_body_and_no_second_transition(self):
        before = self.boss.rect.copy()
        self.player.vel.update(2, -4)
        self.begin(damage=10)
        self.finish()
        self.assertEqual(self.boss.name, 'SpeedBug')
        self.assertEqual(self.boss.health, 6)
        self.assertEqual(self.boss.rect, before)
        self.assertFalse(self.boss.cinematic_pending)
        self.assertEqual(self.boss.transform_timer, 0)
        self.assertGreaterEqual(self.player.invuln_timer, 60)
        self.assertEqual(self.player.vel, pygame.Vector2(2, -4))
        self.boss.take_damage(1)
        self.assertEqual(self.boss.health, 5)
        self.assertFalse(self.boss.cinematic_pending)
        self.assertEqual(self.game.state, STATE_PLAYING)

    def test_visual_zoom_and_six_poses_do_not_change_physics_and_kneel_is_lower(self):
        transition = self.begin()
        before = (self.boss.rect.copy(), self.player.rect.copy(), self.level.camera.offset.copy())
        stages = set()
        for _ in range(320):
            stages.add(transition.stage)
            if self.game.dialogue_box.active: self.key(pygame.K_e)
            self.game._draw()
            self.assertEqual((self.boss.rect, self.player.rect, self.level.camera.offset), before)
            if self.game.state == STATE_PLAYING: break
            self.game._update(self.keys, [])
        self.assertTrue({'kneel', 'arrival', 'speech', 'morph', 'rise', 'release'}.issubset(stages))
        for frame in transition.frames:
            self.assertEqual(frame.get_size(), settings.CHARACTER_SIZE)
            self.assertEqual(frame.get_at((0, 0)).a, 0)
            self.assertEqual(frame.get_bounding_rect().bottom, settings.CHARACTER_SIZE[1])
        self.assertLess(transition.frames[1].get_bounding_rect().height,
                        transition.frames[5].get_bounding_rect().height)

    def test_all_power_hints_fit_rows_and_survive_low_health_and_boss_change(self):
        self.player.abilities = set(Ability)
        self.player.max_health = 10
        for health in (10, 2, 0):
            self.player.health = health
            self.game.hud.draw(self.game.screen, self.player, 'Laboratório A28 — escola corrompida', self.boss)
            self.game.hud.draw_controls_hint(self.game.screen, self.player)
            for row in self.game.hud.last_hint_rows:
                self.assertLessEqual(self.game.hud.font_small.size(row)[0], settings.SCREEN_WIDTH-64)
        self.assertGreater(len(self.game.hud.last_hint_rows), 1)
        self.assertLessEqual(self.game.hud.font.size(theme.fit_text(self.game.hud.font, 'Nome '*100, 100))[0], 100)

    def test_window_closes_while_entity_speaks(self):
        self.begin()
        self.until_speech()
        self.game._process_events([pygame.event.Event(pygame.QUIT)])
        self.assertFalse(self.game.running)


if __name__ == '__main__':
    unittest.main()
