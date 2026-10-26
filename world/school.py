"""Sequência escolar com geometria editável e interações únicas.

A sala, o corredor e o A28 compartilham a interface usada por Game (tilemap,
câmera, spawn, update e draw), sem criar inimigos ou um boss antecipadamente.
"""
from types import SimpleNamespace
import pygame
import settings
from entities.npc import Teacher
from world.camera import Camera


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

    def _monitor(self, surface, x, y):
        self._rect(surface, (27, 44, 52), (x, y, 54, 40))
        color = (166, 55, 99) if self.corrupted else (49, 148, 126)
        self._rect(surface, color, (x+4, y+4, 46, 30))
        for line in range(3):
            self._rect(surface, (216, 225, 191), (x+10, y+10+line*7, 24-line*5, 2))
        self._rect(surface, (47, 57, 60), (x+23, y+40, 8, 9))
        self._rect(surface, (47, 57, 60), (x+12, y+48, 30, 3))

    def _door(self, surface, x, label, active=False):
        self._rect(surface, (104, 91, 71), (x-6, 212, 92, 140))
        self._rect(surface, (57, 94, 93) if active else (98, 119, 108), (x, 218, 80, 134))
        self._rect(surface, (45, 63, 68), (x+10, 229, 60, 45))
        self._rect(surface, (224, 202, 121), (x+64, 296, 5, 5))
        self._rect(surface, (24, 60, 60), (x-6, 180, 92, 24))
        self._text(surface, label, x+15, 184)

    def draw(self, surface):
        surface.fill((222, 216, 182))
        width = self.tilemap.width
        self._rect(surface, (236, 228, 196), (0, 0, width, 210))
        self._rect(surface, (190, 171, 112), (0, 210, width, 142))
        for x in range(0, width, 32):
            self._rect(surface, (180, 161, 105), (x, 210, 1, 142))
        for y in range(210, 352, 32):
            self._rect(surface, (180, 161, 105), (0, y, width, 1))
        self._rect(surface, (90, 100, 88), (0, 346, width, 6))
        self._rect(surface, (160, 165, 146), (0, 352, width, 188))
        for y in range(352, 540, 32):
            self._rect(surface, (142, 148, 134), (0, y, width, 1))
        for x in range(0, width, 64):
            self._rect(surface, (142, 148, 134), (x, 352, 1, 188))
        for x in range(90, width, 360):
            self._rect(surface, (150, 159, 140), (x, 72, 150, 10))
            self._rect(surface, (250, 246, 211), (x+4, 74, 142, 4))
        if self.room == 'corridor':
            for x, label in ((160, 'A25'), (640, 'A26'), (1120, 'A27')):
                self._door(surface, x, label)
            self._door(surface, self.a28_door.x, 'A28', True)
            for x in (340, 820, 1300):
                self._rect(surface, (57, 94, 93), (x, 120, 200, 95))
                self._rect(surface, (118, 170, 181), (x+6, 126, 188, 83))
                self._rect(surface, (106, 138, 91), (x+6, 174, 188, 35))
                self._rect(surface, (57, 94, 93), (x+96, 120, 8, 95))
                # Corrimão vermelho, retomando a referência da fachada.
                self._rect(surface, (151, 59, 58), (x-10, 260, 220, 5))
                for rx in range(x, x+210, 50):
                    self._rect(surface, (151, 59, 58), (rx, 260, 4, 82))
            self._rect(surface, (24, 60, 60), (1280, 95, 250, 30))
            self._text(surface, 'LABORATÓRIO A28  >', 1295, 102)
        else:
            self._rect(surface, (112, 103, 77), (370, 105, 470, 100))
            self._rect(surface, (27, 69, 64), (376, 111, 458, 88))
            title = 'IFVania — inteligência artificial' if self.room == 'classroom' else 'LABORATÓRIO A28'
            self._text(surface, title, 398, 130)
            self._text(surface, 'Programação orientada a serviço' if self.room == 'classroom'
                       else 'O sistema está sob controle da IFVania.', 398, 167, small=True)
            for x in (120, 280, 440, 600):
                self._rect(surface, (102, 80, 63), (x-12, 323, 100, 9))
                self._rect(surface, (73, 78, 73), (x-8, 332, 5, 20))
                self._rect(surface, (73, 78, 73), (x+73, 332, 5, 20))
                self._monitor(surface, x+8, 270)
        for npc in self.npcs:
            npc.draw(surface, self.camera)
            self._text(surface, npc.name, npc.rect.x-32, npc.rect.y-24, (31, 55, 48), small=True)
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
            pygame.draw.rect(surface, (244, 201, 118),
                             self.camera.apply(player.rect).inflate(8, 8), 2)
        # Fios e anéis visuais representam a captura; não causam dano físico.
        for body in [player.rect, *[npc.rect for npc in self.npcs]]:
            rect = self.camera.apply(body)
            radius = 26 + int(progress*60)
            pygame.draw.ellipse(surface, (127, 227, 216),
                                (rect.centerx-radius, rect.centery-12, radius*2, 24), 2)
            pygame.draw.line(surface, (127, 227, 216), (rect.centerx, 90), rect.midtop, 2)
        self._text(surface, 'IFVania: transportando para o mundo virtual...', 220, 235)
