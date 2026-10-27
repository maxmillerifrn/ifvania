"""Sequência escolar com geometria editável e interações únicas.

A sala, o corredor e o A28 compartilham a interface usada por Game (tilemap,
câmera, spawn, update e draw), sem criar inimigos ou um boss antecipadamente.
"""
from types import SimpleNamespace
import pygame
import settings
from entities.npc import Teacher
from world.camera import Camera
from world.school_art import SchoolArt
from ui import theme


class SchoolLevel:
    FLOOR_Y = 352
    NAMES = {'classroom': 'Aula de programação orientada a serviço',
             'corridor': 'Corredores da escola — procure o laboratório A28',
             'lab': 'Laboratório A28 — encontre o professor Romerito'}

    def __init__(self, room):
        self.room = room
        self.name = self.NAMES[room]
        width = 1920 if room == 'corridor' else settings.SCREEN_WIDTH
        self.tilemap = SimpleNamespace(
            width=width, height=settings.SCREEN_HEIGHT, hazards=[],
            solids=[pygame.Rect(0, self.FLOOR_Y, width, settings.SCREEN_HEIGHT-self.FLOOR_Y),
                    pygame.Rect(-32, 0, 32, settings.SCREEN_HEIGHT),
                    pygame.Rect(width, 0, 32, settings.SCREEN_HEIGHT),
                    pygame.Rect(0, -32, width, 32)])
        self.camera = Camera(width, self.tilemap.height)
        self.player_spawn = (120, self.FLOOR_Y-settings.CHARACTER_SIZE[1])
        self.boss = None
        self.npcs = pygame.sprite.Group()
        if room != 'corridor':
            self.npcs.add(Teacher(700, self.player_spawn[1],
                                  'max' if room == 'classroom' else 'romerito'))
        self.a28_door = pygame.Rect(1664, 218, 80, self.FLOOR_Y-218)
        self.interaction_fired = False
        self.corrupted = room != 'classroom'
        self.ticks = 0
        self.visual_ticks = 0
        self.art = SchoolArt(room, width)
        self.font = pygame.font.Font(None, 22)
        self.small_font = pygame.font.Font(None, 18)
        self.prompt = None

    def interaction_zone(self):
        if self.room == 'corridor':
            return self.a28_door.inflate(112, 0)
        if self.room == 'lab':
            return next(iter(self.npcs)).rect.inflate(160, 100)
        return None

    def update(self, player, events):
        self.ticks += 1
        self.npcs.update()
        self.camera.update(player.rect)
        self.prompt = None
        zone = self.interaction_zone()
        if self.interaction_fired or zone is None:
            return None, None
        if player.rect.colliderect(zone):
            self.prompt = 'E — entrar no A28' if self.room == 'corridor' else 'E — falar com Romerito'
            if any(event.type == pygame.KEYDOWN and event.key == pygame.K_e for event in events):
                self.interaction_fired = True
                self.prompt = None
                return ('enter_lab' if self.room == 'corridor' else 'school_encounter'), None
        return None, None

    def begin_abduction(self, player):
        self.prompt = None
        self.attack_start = next(iter(self.npcs)).rect.x
        self.player_start = player.rect.x

    def update_abduction(self, player, timer):
        # Investida breve de Romerito e recuo do aluno antes da captura.
        # É uma ação narrativa, sem retirar vida ou habilitar combate escolar.
        fraction = min(1, timer/18)
        npc = next(iter(self.npcs))
        target = self.player_start + player.width - 8
        npc.rect.x = round(self.attack_start + (target-self.attack_start)*fraction)
        npc.pos.x = npc.rect.x
        player.pos.x = self.player_start - 12*fraction
        player.rect.x = round(player.pos.x)

    def _rect(self, surface, color, rect, width=0):
        pygame.draw.rect(surface, color, self.camera.apply(pygame.Rect(rect)), width)

    def _text(self, surface, text, x, y, color=(235, 242, 222), small=False):
        image = (self.small_font if small else self.font).render(text, True, color)
        rect = self.camera.apply(image.get_rect(topleft=(x, y)))
        surface.blit(image, rect)

    def update_visuals(self):
        self.visual_ticks += 1

    def _door(self, surface, x, label, active=False):
        # Porta metálica: caixilho, visor, dobradiças, puxador e chapa inferior.
        self._rect(surface, (21, 29, 34), (x-7, 210, 94, 142))
        self._rect(surface, (89, 100, 101), (x-4, 213, 88, 139), 2)
        self._rect(surface, (43, 57, 63), (x, 218, 80, 134))
        self._rect(surface, (71, 85, 89), (x+3, 221, 74, 128), 1)
        self._rect(surface, (14, 28, 35), (x+12, 230, 56, 42))
        self._rect(surface, (96, 123, 128), (x+12, 230, 56, 42), 2)
        self._rect(surface, (26, 47, 56), (x+16, 234, 48, 34))
        self._rect(surface, (65, 91, 99), (x+20, 237, 2, 27))
        self._rect(surface, (101, 113, 110), (x+61, 290, 10, 21))
        self._rect(surface, (164, 173, 163), (x+58, 295, 11, 3))
        self._rect(surface, (56, 69, 73), (x+8, 328, 64, 19))
        for hy in (239, 289, 327):
            self._rect(surface, (100, 107, 103), (x+2, hy, 4, 9))
        for sy in (334, 339, 344):
            self._rect(surface, (83, 93, 91), (x+15, sy, 46, 1))
        self._rect(surface, (13, 27, 33), (x-5, 180, 90, 25))
        self._rect(surface, (95, 117, 118), (x-5, 180, 90, 25), 1)
        self._text(surface, label, x+20, 185)
        if active:
            self._rect(surface, (110, 182, 179), (x+91, 288, 7, 4))

    def draw(self, surface):
        self.art.draw(surface, self.camera, self.visual_ticks, self.corrupted)
        if self.room == 'corridor':
            for x, label in ((160, 'A25'), (640, 'A26'), (1120, 'A27')):
                self._door(surface, x, label)
            self._door(surface, self.a28_door.x, 'A28', True)
            self._rect(surface, (17, 34, 40), (1280, 95, 250, 30))
            self._text(surface, 'LABORATÓRIO A28  >', 1295, 102)
        else:
            title = 'IFVania — inteligência artificial' if self.room == 'classroom' else 'LABORATÓRIO A28'
            self._text(surface, title, 454, 170)
            self._text(surface, 'Programação orientada a serviço' if self.room == 'classroom'
                       else 'Sistema sob controle da IFVania.', 454, 200, small=True)
        for npc in self.npcs:
            npc.draw(surface, self.camera)
            image = npc.get_draw_image()
            visual = image.get_rect(midbottom=npc.rect.midbottom)
            label = self.small_font.render(npc.name, True, theme.PAPER)
            rect = label.get_rect(midbottom=(npc.rect.centerx, visual.top-8))
            pygame.draw.rect(surface, theme.PANEL, self.camera.apply(rect.inflate(12, 6)))
            surface.blit(label, self.camera.apply(rect))
        if self.prompt:
            panel = pygame.Surface((340, 32), pygame.SRCALPHA)
            panel.fill((15, 31, 38, 230))
            surface.blit(panel, (310, 365))
            text = self.font.render(self.prompt.replace('—', ':'), True, (223, 238, 206))
            surface.blit(text, text.get_rect(center=(480, 381)))

    def draw_abduction(self, surface, player, progress):
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((16, 8, 59, int(180*progress)))
        surface.blit(overlay, (0, 0))
        if progress < 0.25:
            visual = player.get_draw_image().get_rect(
                midbottom=self.camera.apply(player.rect).midbottom)
            pygame.draw.rect(surface, (244, 201, 118),
                             visual.inflate(8, 8), 2)
        # Fios e anéis visuais representam a captura; não causam dano físico.
        for actor in [player, *self.npcs]:
            rect = actor.get_draw_image().get_rect(
                midbottom=self.camera.apply(actor.rect).midbottom)
            radius = rect.width//2+6 + int(progress*60)
            pygame.draw.ellipse(surface, (127, 227, 216),
                                (rect.centerx-radius, rect.centery-12, radius*2, 24), 2)
            pygame.draw.line(surface, (127, 227, 216), (rect.centerx, 90), rect.midtop, 2)
        self._text(surface, 'IFVania: transportando para o mundo virtual...', 220, 235)
