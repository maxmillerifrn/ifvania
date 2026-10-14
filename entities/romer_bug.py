"""Primeiro professor-chefe: RomerBug se transforma em SpeedBug a 50% de vida."""
import pygame

import assets
from entities.boss import Boss
from entities.projectile import Projectile


class ProfessorProjectile(Projectile):
    """Avião de papel ou medalha, com colisão e expiração de Projectile."""

    def __init__(self, origin, direction, kind):
        self.kind = kind
        size = (26, 14) if kind == "plane" else (18, 22)
        speed = 5 if kind == "plane" else 6.5
        super().__init__(*origin, direction, owner="boss", speed=speed)
        filename = "paper_plane.png" if kind == "plane" else "medal.png"
        self.image = assets.load_image(f"projectiles/{filename}", size)
        if kind == "plane":
            self.image = pygame.transform.rotate(self.image, -self.vel.as_polar()[1])
        self.rect = self.image.get_rect(center=origin)
        self.pos.update(self.rect.center)


class RomerBug(Boss):
    """Professor formal que, ferido, veste roupa de corrida e persegue o aluno.

    SpeedBug é a segunda forma da mesma instância: vida, recompensa e estado
    de derrota continuam pertencendo ao mesmo chefe.
    """

    RUN_SPEED = 3.4
    WALK_SPEED = 1.15
    ACCELERATION = 0.20
    BRAKING = 0.32
    PLANE_INTERVAL = 90
    MEDAL_INTERVAL = 55
    TRANSFORM_DURATION = 45

    def __init__(self, x, y, name="RomerBug", subject="Lógica de Blocos",
                 color=(50, 65, 105), health=16, arena=None,
                 sprite_file="bosses/romerbug_0.png"):
        super().__init__(x, y, name, subject, color, health, arena, sprite_file)
        self.transformed = False
        self.transform_timer = 0
        self.throw_timer = 0
        self.jump_cooldown = 0
        self.on_ground = False
        self.stride_distance = 0.0
        self.motion_frame = 0
        self.patrol_target = x - 80
        self.attack_timer = 70
        self.form_sprites = {}
        for form in ("romerbug", "speedbug"):
            self.form_sprites[form] = {
                1: [assets.load_image(f"bosses/{form}_{i}.png", (54, 64)) for i in range(2)],
                -1: [assets.load_flipped(f"bosses/{form}_{i}.png", (54, 64)) for i in range(2)],
            }
        self.motion_sprites = {}
        for form, action in (("romerbug", "walk"), ("speedbug", "run")):
            self.motion_sprites[form] = {
                1: [assets.load_image(f"bosses/{form}_{action}_{i}.png", (54, 64)) for i in range(6)],
                -1: [assets.load_flipped(f"bosses/{form}_{action}_{i}.png", (54, 64)) for i in range(6)],
            }
        self.transform_font = pygame.font.Font(None, 22)
        self._animate_form()

    def take_damage(self, amount, knockback=(0, 0)):
        if not self.active or not self.alive or self.transform_timer > 0:
            return
        super().take_damage(amount, knockback)
        if not self.alive:
            self.projectiles.empty()
            return
        if not self.transformed and self.health <= self.max_health * 0.5:
            self.transformed = True
            self.name = "SpeedBug"
            self.phase = 2
            self.transform_timer = self.TRANSFORM_DURATION
            self.attack_timer = 30
            self.throw_timer = 0
            self.vel.update(0, 0)
            self.stride_distance = 0
            self.projectiles.empty()
            self._animate_form()
        if self.transformed:
            # Este chefe possui duas formas, sem uma terceira fase a 20%.
            self.phase = 2

    def _shoot(self, player):
        origin = pygame.Vector2(self.rect.centerx + self.facing * 22,
                                self.rect.centery - 5)
        direction = pygame.Vector2(player.rect.center) - origin
        if direction.length_squared() == 0:
            direction.update(self.facing, 0)
        kind = "medal" if self.transformed else "plane"
        self.projectiles.add(ProfessorProjectile(origin, direction, kind))
        self.throw_timer = 12
        self.attack_timer = self.MEDAL_INTERVAL if self.transformed else self.PLANE_INTERVAL

    def update(self, player, solids):
        if not self.active or not self.alive:
            return
        self._t += 1
        self.hit_flash = max(0, self.hit_flash - 1)
        if self.transform_timer > 0:
            self.transform_timer -= 1
            self._animate_form()
            return

        dx = player.rect.centerx - self.rect.centerx
        self.jump_cooldown = max(0, self.jump_cooldown - 1)
        self.throw_timer = max(0, self.throw_timer - 1)
        if self.transformed:
            target_speed = max(-self.RUN_SPEED, min(self.RUN_SPEED, dx * 0.15)) if abs(dx) > 12 else 0
        else:
            if abs(self.patrol_target - self.pos.x) < 10:
                self.patrol_target = self.start_x + 65 if self.patrol_target < self.start_x else self.start_x - 80
            target_speed = max(-self.WALK_SPEED, min(self.WALK_SPEED,
                               (self.patrol_target - self.pos.x) * 0.10))
            if self.attack_timer <= 14 or self.throw_timer > 0:
                target_speed = 0

        acceleration = self.BRAKING if target_speed * self.vel.x <= 0 else self.ACCELERATION
        self.vel.x += max(-acceleration, min(acceleration, target_speed - self.vel.x))
        if abs(self.vel.x) > 0.15:
            self.facing = 1 if self.vel.x > 0 else -1
        if not self.transformed and (self.attack_timer <= 14 or self.throw_timer > 0) and dx:
            self.facing = 1 if dx > 0 else -1

        previous_x = self.rect.x
        wall = self.move_and_collide_x(solids)
        if wall:
            self.vel.x = 0
            if not self.transformed:
                self.patrol_target = self.pos.x - wall * 80
        above = player.rect.bottom < self.rect.top + 16 and abs(dx) < 180
        if self.transformed and self.on_ground and self.jump_cooldown == 0 and (wall or above):
            self.vel.y = -11
            self.jump_cooldown = 35
        bounded_x = max(self.arena.left, min(self.rect.x, self.arena.right - self.width))
        if bounded_x != self.rect.x:
            self.rect.x = bounded_x
            self.pos.x = self.rect.x
            self.vel.x = 0
        # Conserva a parte fracionária da posição entre atualizações.
        distance = abs(self.rect.x - previous_x)
        self.apply_gravity()
        self.on_ground = self.move_and_collide_y(solids)
        if self.on_ground:
            self.stride_distance += distance

        self.attack_timer -= 1
        if self.attack_timer <= 0:
            self._shoot(player)
        self.projectiles.update(solids)
        self._animate_form()

    def _animate_form(self):
        form = "speedbug" if self.transformed else "romerbug"
        if self.transform_timer > 0:
            self.image = self.form_sprites[form][self.facing][0]
        elif not self.transformed and (self.throw_timer > 0 or self.attack_timer <= 14):
            self.image = self.form_sprites[form][self.facing][int(self.throw_timer > 0)]
        elif self.transformed and not self.on_ground:
            self.image = self.motion_sprites[form][self.facing][2]
        elif abs(self.vel.x) > 0.15:
            step_length = 11 if self.transformed else 7
            self.motion_frame = int(self.stride_distance / step_length) % 6
            self.image = self.motion_sprites[form][self.facing][self.motion_frame]
        else:
            self.image = self.motion_sprites[form][self.facing][1]

    def get_all_hit_rects(self):
        if self.transform_timer > 0:
            return []
        return super().get_all_hit_rects()

    def draw(self, surface, camera):
        # Os próprios quadros contêm a oscilação do corpo. Não aplicar o bob
        # flutuante de Boss, que fazia os pés deslizarem acima do chão.
        rect = camera.apply(self.rect)
        surface.blit(self.image, rect)
        if self.hit_flash > 0:
            flash = self.image.copy()
            flash.fill((255, 255, 255, 100), special_flags=pygame.BLEND_RGBA_MULT)
            surface.blit(flash, rect, special_flags=pygame.BLEND_RGBA_ADD)
        for projectile in self.projectiles:
            projectile.draw(surface, camera)
        if self.transform_timer > 0:
            rect = camera.apply(self.rect)
            radius = 36 + (self.TRANSFORM_DURATION - self.transform_timer) // 3
            pygame.draw.circle(surface, (255, 200, 65), rect.center, radius, 3)
            text = self.transform_font.render("SpeedBug!", True, (255, 215, 80))
            surface.blit(text, text.get_rect(midbottom=(rect.centerx, rect.top - 12)))
