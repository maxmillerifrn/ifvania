"""HUD com integridade segmentada, identificação da área e estado do boss."""
import pygame
import settings
from powerups import Ability, ABILITY_NAMES
from ui import theme


class HUD:
    def __init__(self):
        self.font = pygame.font.Font(None, 22)
        self.font_small = pygame.font.Font(None, 20)
        self.font_big = pygame.font.Font(None, 34)
        self.last_hint_rows = []

    def draw(self, surface, player, level_name, boss=None):
        theme.panel(surface, (18, 16, 204, 66), theme.CYAN)
        color = theme.DANGER if player.health <= 2 else theme.CYAN
        theme.text(surface, self.font_small, 'INTEGRIDADE', (31, 24), theme.MUTED)
        value = f'{player.health:02d} / {player.max_health:02d}'
        theme.text(surface, self.font_small, value, (160, 24), color)
        gap = 4
        width = (176-gap*(player.max_health-1)) / player.max_health
        for i in range(player.max_health):
            r = pygame.Rect(round(31+i*(width+gap)), 48, max(1, int(width)), 12)
            pygame.draw.rect(surface, color if i < player.health else (35, 47, 54), r)
        theme.text(surface, self.font_small, player_label(player), (31, 65), theme.MUTED)
        area_width = min(498, max(224, self.font.size(level_name)[0]+30))
        area_rect = pygame.Rect(settings.SCREEN_WIDTH-area_width-18, 16, area_width, 43)
        theme.panel(surface, area_rect)
        theme.text(surface, self.font_small, 'LOCALIZAÇÃO', (area_rect.x+12, 21), theme.AMBER)
        theme.text(surface, self.font, theme.fit_text(self.font, level_name, area_width-24),
                   (area_rect.x+12, 36))
        if player.abilities:
            labels = ' / '.join(ABILITY_NAMES[a] for a in sorted(player.abilities, key=lambda a: a.value))
            label = theme.fit_text(self.font_small, labels, area_width-24)
            theme.panel(surface, (area_rect.x, 64, area_width, 26))
            theme.text(surface, self.font_small, label, (area_rect.x+12, 70), theme.MUTED)
        if boss is not None and boss.active and boss.alive:
            self.draw_boss(surface, boss)

    def draw_boss(self, surface, boss):
        rect = pygame.Rect(248, 91, settings.SCREEN_WIDTH-496, 57)
        theme.panel(surface, rect, theme.DANGER)
        theme.text(surface, self.font, boss.name.upper(), (rect.x+14, rect.y+10))
        phase = 'FASE II' if boss.phase >= 2 else 'FASE I'
        theme.text(surface, self.font_small, phase, (rect.right-66, rect.y+12), theme.DANGER)
        bar = pygame.Rect(rect.x+14, rect.y+36, rect.width-28, 7)
        pygame.draw.rect(surface, (40, 30, 38), bar)
        ratio = max(0, min(1, boss.health/boss.max_health))
        pygame.draw.rect(surface, theme.DANGER, (bar.x, bar.y, round(bar.width*ratio), bar.height))
        pygame.draw.line(surface, theme.AMBER, (bar.centerx, bar.top-2), (bar.centerx, bar.bottom+2))

    def draw_controls_hint(self, surface, player):
        hints = ['A/D ou SETAS  mover', 'ESPAÇO  saltar',
                 'X  chicote' if player.whip_unlocked else 'E  interagir']
        for ability, hint in ((Ability.DOUBLE_JUMP, 'ESPAÇO 2x  salto duplo'),
                              (Ability.DASH, 'SHIFT  dash'), (Ability.WALL_CLIMB, 'PAREDE + SALTO'),
                              (Ability.RANGED_SHOT, 'F  tiro'), (Ability.SHIELD, 'Q  escudo')):
            if player.has(ability):
                hints.append(hint)
        hints.append('ESC  pausa')
        rows, line = [], ''
        for hint in hints:
            trial = line+'     |     '+hint if line else hint
            if self.font_small.size(trial)[0] > settings.SCREEN_WIDTH-64 and line:
                rows.append(line)
                line = hint
            else:
                line = trial
        rows.append(line)
        self.last_hint_rows = rows
        height = len(rows)*20+16
        rect = pygame.Rect(18, settings.SCREEN_HEIGHT-height-10, settings.SCREEN_WIDTH-36, height)
        theme.panel(surface, rect)
        for i, row in enumerate(rows):
            theme.text(surface, self.font_small, row, (rect.x+13, rect.y+9+i*20), theme.MUTED)

    def draw_center_text(self, surface, text, sub=None, y_offset=0):
        rect = pygame.Rect(150, settings.SCREEN_HEIGHT//2-67+y_offset, settings.SCREEN_WIDTH-300, 138)
        theme.panel(surface, rect, theme.AMBER)
        title = self.font_big.render(theme.fit_text(self.font_big, text, rect.width-40), True, theme.PAPER)
        surface.blit(title, title.get_rect(center=(rect.centerx, rect.y+46)))
        if sub:
            line = self.font.render(theme.fit_text(self.font, sub, rect.width-40), True, theme.MUTED)
            surface.blit(line, line.get_rect(center=(rect.centerx, rect.y+89)))


def player_label(player):
    return 'ESTUDANTE / '+('MENINA' if player.character == 'girl' else 'MENINO')
