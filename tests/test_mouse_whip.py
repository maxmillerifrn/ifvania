import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import unittest
import pygame
from entities.player import Player
from entities.enemy import Enemy
from entities.romer_bug import RomerBug


class MouseWhipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((960, 540))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.player = Player(200, 200)
        self.player.facing = 1

    def swing(self, targets, solids=()):
        self.player.attack_cooldown = 0
        self.player._try_melee()
        for age in range(self.player.whip.DURATION):
            self.player.attacking_timer = self.player.whip.DURATION - age
            for target in targets:
                self.player.try_melee_hit(target, solids)

    def test_windup_and_recovery_do_not_damage(self):
        target = Enemy(228, 210, health=10)
        self.player._try_melee()
        for age in (0, 3, 5, 16, 20, 25):
            self.player.attacking_timer = self.player.whip.DURATION - age
            self.assertIsNone(self.player.get_melee_rect())
            self.assertFalse(self.player.try_melee_hit(target, []))
        self.assertEqual(target.health, 10)

    def test_one_hit_per_enemy_per_swing_and_next_swing_can_hit_again(self):
        near = Enemy(243, 210, health=10)
        far = Enemy(280, 210, health=10)
        self.swing([near, far])
        self.assertEqual(near.health, 9)
        self.assertEqual(far.health, 9)
        self.swing([near, far])
        self.assertEqual(near.health, 8)
        self.assertEqual(far.health, 8)

    def test_targets_behind_or_outside_reach_are_not_hit(self):
        behind = Enemy(150, 215, health=10)
        distant = Enemy(340, 210, health=10)
        self.swing([behind, distant])
        self.assertEqual(behind.health, 10)
        self.assertEqual(distant.health, 10)

    def test_whip_stops_at_wall(self):
        target = Enemy(280, 210, health=10)
        wall = pygame.Rect(260, 100, 15, 200)
        self.swing([target], [wall])
        self.assertEqual(target.health, 10)
        self.player.attacking_timer = self.player.whip.DURATION - 15
        self.assertLessEqual(max(p.x for p in self.player.whip.points(self.player, [wall])), wall.left)

    def test_left_attack_and_turning_during_swing(self):
        self.player.facing = -1
        self.player._try_melee()
        self.player.facing = 1
        target = Enemy(140, 210, health=10)
        for age in range(26):
            self.player.attacking_timer = 26 - age
            self.player.try_melee_hit(target, [])
        self.assertEqual(target.health, 9)
        self.assertEqual(self.player.whip.facing, -1)

    def test_respawn_cancels_swing(self):
        self.player._try_melee()
        self.player.respawn(100, 100)
        self.assertEqual(self.player.attacking_timer, 0)
        self.assertIsNone(self.player.get_melee_rect())

    def test_whip_can_defeat_boss_through_both_forms(self):
        boss = RomerBug(265, 176)
        boss.activate()
        for _ in range(8):
            self.swing([boss])
        self.assertEqual(boss.health, 8)
        self.assertTrue(boss.transformed)
        for _ in range(boss.TRANSFORM_DURATION):
            boss.update(self.player, [])
        for _ in range(8):
            self.swing([boss])
        self.assertTrue(boss.defeated)


class BossMotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((960, 540))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_running_accelerates_preserves_fractions_and_uses_full_cycle(self):
        boss = RomerBug(600, 384, arena=pygame.Rect(0, 0, 2000, 600))
        player = Player(100, 408)
        boss.activate()
        boss.take_damage(8)
        for _ in range(45):
            boss.update(player, [])
        floor = [pygame.Rect(0, 448, 2000, 100)]
        frames = set()
        fractions = []
        previous_speed = 0
        for i in range(90):
            boss.update(player, floor)
            if i < 12:
                self.assertLessEqual(abs(boss.vel.x - previous_speed), boss.BRAKING + 1e-6)
            previous_speed = boss.vel.x
            frames.add(boss.motion_frame)
            fractions.append(abs(boss.pos.x - round(boss.pos.x)))
        self.assertEqual(frames, set(range(6)))
        self.assertGreater(max(fractions), 0.1)
        self.assertEqual(boss.rect.bottom, 448)

    def test_blocked_runner_does_not_cycle_feet_without_displacement(self):
        boss = RomerBug(400, 384)
        player = Player(100, 408)
        boss.activate()
        boss.take_damage(8)
        boss.transform_timer = 0
        boss.jump_cooldown = 200
        floor = pygame.Rect(0, 448, 1000, 100)
        wall = pygame.Rect(368, 0, 32, 448)
        for _ in range(40):
            boss.update(player, [floor, wall])
        self.assertEqual(boss.rect.left, wall.right)
        self.assertLess(boss.stride_distance, 1)


if __name__ == '__main__':
    unittest.main()
