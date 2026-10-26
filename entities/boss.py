"""Os professores-chefe (bosses) de cada fase.

Cada Boss tem padrões de ataque próprios, fases baseadas em vida restante,
e concede uma habilidade ao ser derrotado. Herda de `Character` (vida,
dano, desenho básico) mas NÃO usa a gravidade/colisão da base: o chefe
flutua dentro de uma arena fixa, então cuida do próprio movimento.
"""
import pygame
from abc import abstractmethod
import settings
import assets
from entities.character import Character
from entities.projectile import Projectile


class Boss(Character):
    VISUAL_SCALE = settings.CHARACTER_VISUAL_SCALE

    def __init__(self, x, y, name, subject, color, health=20, arena=None, sprite_file=None):
        super().__init__(x, y, *settings.CHARACTER_SIZE, health=health)
        self.name = name
        self.subject = subject
        self.color = color
        sprite_file = sprite_file or "bosses/prof_scratch.png"
        self.sprite_r = assets.load_character_frames([sprite_file], color)[0]
        self.sprite_l = pygame.transform.flip(self.sprite_r, True, False)
        self.image = self.sprite_l
        self.start_x = x
        self.arena = arena or pygame.Rect(x - 220, y - 200, 440, 260)

        self.phase = 1
        self.defeated = False
        self.active = False  # só luta depois do diálogo de introdução

        self.attack_timer = 90
        self.attack_state = None
        self.attack_clock = 0
        self.facing = -1
        self.hit_flash = 0
        self.projectiles = pygame.sprite.Group()
        self._t = 0  # relógio interno só para animar o balanço (bob) do sprite

        self._draw_sprite()

    def activate(self):
        self.active = True

    def take_damage(self, amount, knockback=(0, 0)):
        if not self.active or not self.alive:
            return
        super().take_damage(amount)
        self.hit_flash = 8
        if self.health <= self.max_health * 0.5 and self.phase == 1:
            self.phase = 2
        if self.health <= self.max_health * 0.2 and self.phase == 2:
            self.phase = 3
        if not self.alive:
            self.defeated = True
            self.projectiles.empty()

    @abstractmethod
    def choose_attack(self, player):
        """As classes concretas definem a estratégia do encontro."""
        raise NotImplementedError("Cada boss deve implementar sua estratégia de ataques")

    def update(self, player, solids):
        self._t += 1
        if not self.active or not self.alive:
            self._draw_sprite()
            return

        if self.hit_flash > 0:
            self.hit_flash -= 1

        self.facing = 1 if player.rect.centerx > self.rect.centerx else -1
        self.attack_timer -= 1
        speed_mult = 1 + (self.phase - 1) * 0.35

        if self.attack_timer <= 0 and self.attack_state is None:
            self.attack_state = self.choose_attack(player)
            self.attack_clock = 0

        if self.attack_state == "lunge":
            self.attack_clock += 1
            self.vel.x = self.facing * 3.2 * speed_mult
            if self.attack_clock > 26:
                self._end_attack(speed_mult)
        elif self.attack_state == "spread":
            self.vel.x = 0
            self.attack_clock += 1
            if self.attack_clock == 15:
                for ang in (-0.3, 0, 0.3):
                    dx = (1 if self.facing > 0 else -1) + ang
                    self.projectiles.add(Projectile(self.rect.centerx, self.rect.centery,
                                                      (dx, ang), owner="boss", speed=6))
            if self.attack_clock > 40:
                self._end_attack(speed_mult)
        elif self.attack_state == "slam":
            self.vel.x = 0
            self.attack_clock += 1
            if self.attack_clock == 20:
                for dx in (-1, 1):
                    self.projectiles.add(Projectile(self.rect.centerx, self.rect.bottom - 10,
                                                      (dx, -0.15), owner="boss", speed=5))
            if self.attack_clock > 45:
                self._end_attack(speed_mult)
        else:
            # perseguição leve dentro da arena
            direction = 1 if player.rect.centerx > self.rect.centerx else -1
            self.vel.x = direction * 0.8 * speed_mult

        self.pos.x += self.vel.x
        self.rect.x = round(self.pos.x)
        self.rect.clamp_ip(self.arena)
        self.pos.x = self.rect.x

        self.projectiles.update(solids)
        self._draw_sprite()

    def _end_attack(self, speed_mult):
        self.attack_state = None
        self.attack_timer = max(35, int(70 / speed_mult))

    def get_all_hit_rects(self):
        rects = [(self.rect, self.contact_damage)]
        for p in self.projectiles:
            rects.append((p.rect, p.damage))
        return rects

    def _draw_sprite(self):
        # escolhe o sprite (imagem carregada de assets/images/bosses/) conforme direção
        self.image = self.sprite_r if self.facing > 0 else self.sprite_l

    def draw(self, surface, camera):
        image = self.get_draw_image()
        dest = image.get_rect(midbottom=camera.apply(self.rect).midbottom)
        surface.blit(image, dest)
        if self.hit_flash > 0:
            # flash branco ao levar dano, sem alterar a imagem original em cache
            flash = image.copy()
            flash.fill((255, 255, 255, 140), special_flags=pygame.BLEND_RGBA_MULT)
            surface.blit(flash, dest, special_flags=pygame.BLEND_RGBA_ADD)
        # indicadores de fase de raiva (não fazem parte da arte base)
        if self.active and self.alive:
            if self.phase >= 2:
                pygame.draw.circle(surface, (255, 60, 60), (dest.right - 8, dest.top + 8), 4)
            if self.phase >= 3:
                pygame.draw.circle(surface, (255, 60, 60), (dest.left + 8, dest.top + 8), 4)
        for p in self.projectiles:
            p.draw(surface, camera)


# ----------------------------------------------------------------------
# Definições narrativas dos 6 professores-chefe
# ----------------------------------------------------------------------
BOSS_DEFS = [
    dict(name="RomerBug", subject="Lógica de Blocos", color=(50, 65, 105), health=16,
         sprite_file="bosses/romerbug_0.png", boss_type="romerbug"),
    dict(name="Prof. Python", subject="Laboratório de Lógica", color=(60, 140, 220), health=20,
         sprite_file="bosses/prof_python.png", boss_type="python"),
    dict(name="Prof. Java", subject="Sala de POO", color=(200, 60, 60), health=24,
         sprite_file="bosses/prof_java.png", boss_type="java"),
    dict(name="Prof. C", subject="Sala de Memória", color=(120, 120, 130), health=28,
         sprite_file="bosses/prof_c.png", boss_type="c"),
    dict(name="Prof. SQL", subject="Biblioteca de Dados", color=(60, 180, 140), health=32,
         sprite_file="bosses/prof_sql.png", boss_type="sql"),
    dict(name="Prof. Assembly", subject="Núcleo do Sistema", color=(30, 30, 40), health=40,
         sprite_file="bosses/prof_assembly.png", boss_type="assembly"),
]
