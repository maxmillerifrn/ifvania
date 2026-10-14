"""Testes de comportamento do primeiro chefe, sem abrir janela."""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import unittest
from types import SimpleNamespace

import pygame
from entities.boss import Boss
from entities.romer_bug import RomerBug, ProfessorProjectile
from entities.player import Player
from powerups import Ability
from world.level import Level
from world.levels_data import build_levels


class RomerBugTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((960, 540))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.boss = RomerBug(400, 384, arena=pygame.Rect(32, 32, 896, 480))
        self.player = SimpleNamespace(rect=pygame.Rect(180, 408, 26, 40))
        self.floor = [pygame.Rect(0, 448, 960, 64)]

    def transform(self):
        self.boss.activate()
        self.boss.take_damage(8)
        for _ in range(self.boss.TRANSFORM_DURATION):
            self.boss.update(self.player, self.floor)

    def test_only_first_of_six_bosses_is_specialized(self):
        levels = [Level(data) for data in build_levels()]
        self.assertEqual(len(levels), 6)
        self.assertIsInstance(levels[0].boss, RomerBug)
        self.assertIsInstance(levels[0].boss, Boss)
        self.assertTrue(all(type(level.boss) is Boss for level in levels[1:]))
        self.assertEqual(levels[0].data['ability_reward'], Ability.DOUBLE_JUMP)

    def test_inactive_boss_neither_attacks_moves_nor_takes_damage(self):
        initial = self.boss.rect.copy()
        self.boss.take_damage(8)
        for _ in range(150):
            self.boss.update(self.player, self.floor)
        self.assertEqual(self.boss.health, 16)
        self.assertEqual(self.boss.rect, initial)
        self.assertFalse(self.boss.projectiles)

    def test_formal_boss_walks_and_throws_aimed_planes(self):
        self.boss.activate()
        initial = self.boss.rect.copy()
        for _ in range(70):
            self.boss.update(self.player, self.floor)
        projectile = next(iter(self.boss.projectiles))
        self.assertEqual(projectile.kind, 'plane')
        self.assertEqual(projectile.owner, 'boss')
        self.assertLess(projectile.vel.x, 0)
        self.assertLess(self.boss.rect.x, initial.x)
        self.assertEqual(self.boss.rect.bottom, initial.bottom)
        self.assertLess(abs(self.boss.vel.x), self.boss.WALK_SPEED)

    def test_transforms_at_exactly_half_health_once(self):
        self.boss.activate()
        self.boss.take_damage(7)
        self.assertEqual(self.boss.name, 'RomerBug')
        self.assertFalse(self.boss.transformed)
        old_image = self.boss.image
        self.boss.take_damage(1)
        self.assertEqual(self.boss.health, 8)
        self.assertEqual(self.boss.name, 'SpeedBug')
        self.assertIsNot(self.boss.image, old_image)
        self.assertEqual(self.boss.phase, 2)
        self.assertEqual(self.boss.get_all_hit_rects(), [])
        self.boss.take_damage(1)
        self.assertEqual(self.boss.health, 8)
        for _ in range(45):
            self.boss.update(self.player, self.floor)
        self.boss.take_damage(5)
        self.assertEqual(self.boss.phase, 2)
        self.assertEqual(self.boss.transform_timer, 0)
        self.assertEqual(self.boss.health, 3)

    def test_crossing_threshold_also_transforms_without_healing(self):
        self.boss.activate()
        self.boss.take_damage(10)
        self.assertTrue(self.boss.transformed)
        self.assertEqual(self.boss.health, 6)

    def test_transformation_clears_planes_and_pauses_motion(self):
        self.boss.activate()
        self.boss._shoot(self.player)
        self.assertTrue(self.boss.projectiles)
        self.boss.take_damage(8)
        initial = self.boss.rect.copy()
        self.boss.update(self.player, self.floor)
        self.assertFalse(self.boss.projectiles)
        self.assertEqual(self.boss.rect, initial)

    def test_runner_chases_both_directions_and_throws_medals(self):
        self.transform()
        old_x = self.boss.rect.x
        for _ in range(30):
            self.boss.update(self.player, self.floor)
        self.assertLess(self.boss.rect.x, old_x)
        self.assertEqual(self.boss.rect.bottom, 448)
        self.assertTrue(self.boss.projectiles)
        self.assertTrue(all(p.kind == 'medal' for p in self.boss.projectiles))
        self.player.rect.x = 800
        old_x = self.boss.rect.x
        old_speed = self.boss.vel.x
        self.boss.update(self.player, self.floor)
        self.assertGreater(self.boss.vel.x, old_speed)
        self.assertLess(self.boss.vel.x, 0)  # freia antes de inverter a direção
        for _ in range(35):
            self.boss.update(self.player, self.floor)
        self.assertGreater(self.boss.rect.x, old_x)
        self.assertEqual(self.boss.facing, 1)

    def test_runner_collides_with_wall_and_jumps(self):
        self.transform()
        self.boss.update(self.player, self.floor)
        wall = pygame.Rect(self.boss.rect.left - 32, 384, 32, 64)
        self.boss.update(self.player, self.floor + [wall])
        self.assertGreaterEqual(self.boss.rect.left, wall.right)
        self.assertLess(self.boss.vel.y, 0)

    def test_aim_handles_right_and_exact_overlap(self):
        for target in [(800, 400), (449, 411)]:
            self.player.rect.center = target
            self.boss.facing = 1
            self.boss._shoot(self.player)
            shot = list(self.boss.projectiles)[-1]
            self.assertGreater(shot.vel.x, 0)

    def test_projectiles_expire_and_collide_with_world(self):
        for kind in ('plane', 'medal'):
            shot = ProfessorProjectile((100, 100), (1, 0), kind)
            group = pygame.sprite.Group(shot)
            shot.update([pygame.Rect(100, 80, 50, 50)])
            self.assertFalse(group)
            shot = ProfessorProjectile((100, 100), (1, 0), kind)
            group.add(shot)
            for _ in range(90):
                shot.update([])
            self.assertFalse(group)

    def test_defeat_rewards_once_and_allows_exit(self):
        level = Level(build_levels()[0])
        player = Player(*level.player_spawn)
        player.rect.topleft = level.tilemap.dialogue_trigger.topleft
        player.pos.update(player.rect.topleft)
        self.assertEqual(level.update(player, [])[0], 'dialogue')
        boss = level.boss
        boss.take_damage(8)
        for _ in range(boss.TRANSFORM_DURATION):
            boss.update(player, level.tilemap.solids)
        boss.take_damage(8)
        self.assertTrue(boss.defeated)
        self.assertFalse(boss.projectiles)
        self.assertEqual(level.update(player, [])[0], 'dialogue')
        self.assertEqual(len(level.powerups), 1)
        reward = next(iter(level.powerups))
        player.rect.topleft = reward.rect.topleft
        level.update(player, [])
        self.assertTrue(player.has(Ability.DOUBLE_JUMP))
        self.assertEqual(len(level.powerups), 0)
        player.rect.topleft = level.tilemap.exit_trigger.topleft
        self.assertEqual(level.update(player, [])[0], 'level_complete')


if __name__ == '__main__':
    unittest.main()
