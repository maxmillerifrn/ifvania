"""Cena dos 50%: joelho no chão, entidade, fala, metamorfose e retomada."""
import math
import pygame
import assets
import settings
from ui import theme


class BossTransition:
    DURATIONS = {'kneel': 42, 'arrival': 48, 'morph': 72, 'rise': 42, 'release': 24}
    ORDER = ('kneel', 'arrival', 'speech', 'morph', 'rise', 'release', 'complete')

    def __init__(self, level, player):
        self.level = level
        self.boss = level.boss
        self.player = player
        self.stage = 'kneel'
        self.tick = 0
        self.frames = assets.load_character_frames([f'bosses/transition/pose_{i}.png' for i in range(6)])
        self.entity = assets.load_character_frames(['bosses/transition/entity.png'])[0]
        self.facing = self.boss.facing
        self.start_rect = self.boss.rect.copy()
        self.player_velocity = player.vel.copy()
        self.font = pygame.font.Font(None, 19)
        self.layer = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        player.vel.update(0, 0)
        player.attacking_timer = 0
        player.attack_cooldown = 0
        player.whip.hit_targets.clear()
        player.projectiles.empty()
        self.boss.projectiles.empty()
        self.boss.hit_flash = 0
        self._pose(0)

    def _pose(self, index):
        frame = self.frames[index]
        self.boss.image = pygame.transform.flip(frame, self.facing < 0, False)

    def resume(self):
        if self.stage == 'speech':
            self.stage, self.tick = 'morph', 0

    def update(self):
        if self.stage in ('speech', 'complete'):
            return None
        self.tick += 1
        fraction = min(1, self.tick/self.DURATIONS[self.stage])
        if self.stage == 'kneel':
            self._pose(0 if fraction < 0.35 else 1)
        elif self.stage in ('arrival',):
            self._pose(2 if fraction > 0.5 else 1)
        elif self.stage == 'morph':
            old = self.frames[2].copy()
            new = self.frames[3].copy()
            new.set_alpha(round(255*fraction))
            old.set_alpha(round(255*(1-fraction)))
            combined = pygame.Surface(settings.CHARACTER_SIZE, pygame.SRCALPHA)
            combined.blit(old, (0, 0))
            combined.blit(new, (0, 0))
            self.boss.image = pygame.transform.flip(combined, self.facing < 0, False)
            if fraction >= 0.5:
                self.boss.name = 'SpeedBug'
        elif self.stage == 'rise':
            self._pose(3 if fraction < 0.25 else 4 if fraction < 0.7 else 5)
        else:
            self._pose(5)
        if self.tick >= self.DURATIONS[self.stage]:
            self.stage = self.ORDER[self.ORDER.index(self.stage)+1]
            self.tick = 0
            if self.stage == 'speech':
                return 'speech'
            if self.stage == 'complete':
                self.boss.finish_cinematic()
                self.player.vel.update(self.player_velocity)
                self.player.invuln_timer = max(60, self.player.invuln_timer)
                return 'complete'
        return None

    def draw(self, surface):
        # Zoom somente visual: posições, câmera e caixas de colisão não mudam.
        self.level.draw(self.layer)
        self.player.draw(self.layer, self.level.camera)
        body = self.level.camera.apply(self.boss.rect)
        entity_visible = self.stage != 'kneel'
        if entity_visible:
            size = tuple(round(side*settings.CHARACTER_VISUAL_SCALE) for side in self.entity.get_size())
            image = pygame.transform.flip(pygame.transform.scale(self.entity, size), self.facing < 0, False)
            alpha = 255
            if self.stage == 'arrival':
                alpha = round(255*self.tick/self.DURATIONS['arrival'])
            elif self.stage == 'release':
                alpha = round(255*(1-self.tick/self.DURATIONS['release']))
            image.set_alpha(alpha)
            x = body.centerx + (62 if self.facing > 0 else -62)
            y = body.bottom-92-round(2*math.sin(self.tick*0.09))
            self.layer.blit(image, image.get_rect(midbottom=(x, y+40)))
            if self.stage == 'morph':
                glow = pygame.Surface(self.layer.get_size(), pygame.SRCALPHA)
                pygame.draw.line(glow, (*theme.CYAN, 100), (x, y+28), body.center, 2)
                pygame.draw.ellipse(glow, (*theme.CYAN, 110), body.inflate(22, 12), 2)
                self.layer.blit(glow, (0, 0))
        amount = 1.0
        if self.stage == 'kneel':
            amount = self.tick/self.DURATIONS['kneel']
        elif self.stage == 'release':
            amount = 1-self.tick/self.DURATIONS['release']
        amount = amount*amount*(3-2*amount)
        width = round(settings.SCREEN_WIDTH*(1-0.5*amount))
        height = round(settings.SCREEN_HEIGHT*(1-0.5*amount))
        crop = pygame.Rect(0, 0, width, height)
        crop.center = (round(settings.SCREEN_WIDTH/2+(body.centerx-settings.SCREEN_WIDTH/2)*amount),
                       round(settings.SCREEN_HEIGHT/2+(body.centery-24-settings.SCREEN_HEIGHT/2)*amount))
        crop.clamp_ip(self.layer.get_rect())
        surface.blit(pygame.transform.scale(self.layer.subsurface(crop), surface.get_size()), (0, 0))
        # Barras de cinema e legenda de estado fora da área das personagens.
        bar_height = round(46*amount)
        pygame.draw.rect(surface, theme.INK, (0, 0, settings.SCREEN_WIDTH, bar_height))
        pygame.draw.rect(surface, theme.INK, (0, settings.SCREEN_HEIGHT-round(30*amount), settings.SCREEN_WIDTH, round(30*amount)))
        title = 'ROMERBUG / LIMIAR DE RUPTURA' if self.stage in ('kneel', 'arrival', 'speech') else 'SPEEDBUG / RECONSTITUIÇÃO'
        if bar_height >= 28:
            theme.text(surface, self.font, title, (28, 16), theme.AMBER)
            theme.text(surface, self.font, 'ESC  pausar', (settings.SCREEN_WIDTH-112, 16), theme.MUTED)
