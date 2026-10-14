"""HUD: vida do jogador, habilidades adquiridas e barra de vida do chefe."""
import pygame
import settings
from powerups import ABILITY_NAMES, ABILITY_HOTKEYS


class HUD:
    def __init__(self):
        self.font = pygame.font.SysFont(settings.FONT_NAME, 18)
        self.font_small = pygame.font.SysFont(settings.FONT_NAME, 14)
        self.font_big = pygame.font.SysFont(settings.FONT_NAME, 26, bold=True)

    def draw(self, surface, player, level_name, boss=None):
        # coração/vida
        for i in range(player.max_health):
            x = 16 + i * 22
            y = 16
            color = settings.HP_COLOR if i < player.health else settings.HP_BG
            pygame.draw.circle(surface, color, (x, y), 8)
            pygame.draw.circle(surface, settings.WHITE, (x, y), 8, 1)

        name_surf = self.font.render(level_name, True, settings.TEXT_COLOR)
        surface.blit(name_surf, (16, 34))

        # ícones de habilidades adquiridas
        for i, ab in enumerate(player.abilities):
            x = settings.SCREEN_WIDTH - 36 - i * 34
            y = 16
            pygame.draw.rect(surface, (40, 40, 60), (x - 14, y - 14, 28, 28), border_radius=6)
            pygame.draw.rect(surface, settings.POWERUP_COLOR, (x - 14, y - 14, 28, 28), 2, border_radius=6)
            label = self.font_small.render(ABILITY_NAMES[ab].split(' ')[0][:3], True, settings.WHITE)
            surface.blit(label, label.get_rect(center=(x, y)))

        if boss is not None and boss.active and boss.alive:
            bar_w = 400
            bar_rect = pygame.Rect((settings.SCREEN_WIDTH - bar_w) // 2, 16, bar_w, 18)
            pygame.draw.rect(surface, settings.HP_BG, bar_rect, border_radius=6)
            pct = max(0, boss.health / boss.max_health)
            fill_rect = pygame.Rect(bar_rect.x, bar_rect.y, int(bar_w * pct), bar_rect.height)
            pygame.draw.rect(surface, settings.BOSS_HP_COLOR, fill_rect, border_radius=6)
            pygame.draw.rect(surface, settings.UI_BORDER, bar_rect, 2, border_radius=6)
            name_surf = self.font.render(f"{boss.name} - {boss.subject}", True, settings.TEXT_COLOR)
            surface.blit(name_surf, name_surf.get_rect(centerx=settings.SCREEN_WIDTH // 2, y=36))

    def draw_controls_hint(self, surface, player):
        hints = ["<- ->: mover", "ESPAÇO: pular", "X: mouse"]
        from powerups import Ability
        if player.has(Ability.DOUBLE_JUMP):
            hints.append("ESPAÇO (2x): pulo duplo")
        if player.has(Ability.DASH):
            hints.append("SHIFT: dash")
        if player.has(Ability.WALL_CLIMB):
            hints.append("segure na parede: escalar")
        if player.has(Ability.RANGED_SHOT):
            hints.append("F: tiro")
        if player.has(Ability.SHIELD):
            hints.append("Q: escudo")
        text = "  |  ".join(hints)
        surf = self.font_small.render(text, True, (200, 200, 200))
        surface.blit(surf, (16, settings.SCREEN_HEIGHT - 22))

    def draw_center_text(self, surface, text, sub=None, y_offset=0):
        surf = self.font_big.render(text, True, settings.WHITE)
        rect = surf.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + y_offset))
        surface.blit(surf, rect)
        if sub:
            sub_surf = self.font.render(sub, True, (210, 210, 210))
            sub_rect = sub_surf.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + y_offset + 34))
            surface.blit(sub_surf, sub_rect)
