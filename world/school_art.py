"""Ambientes escolares detalhados com mobiliário e terminais em camadas."""
import pygame
import assets
import settings
from world.terminal import TerminalScreen


class SchoolArt:
    def __init__(self, room, width):
        name = 'corridor_detailed.png' if room == 'corridor' else 'lab_detailed.png'
        self.background = assets.load_image('background/'+name)
        self.room = room
        self.width = width
        self.terminals = TerminalScreen()
        self.monitor_screens = []
        self.static = pygame.Surface((width, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        if room != 'corridor':
            for base in range(0, width, 960):
                for x in (112, 272, 432, 592):
                    if base+x+138 < width:
                        self._workstation(base+x, 240)

    def _workstation(self, x, y):
        s = self.static
        # Mesa: tampo com espessura, gaveta, pés, gabinete e teclado.
        pygame.draw.rect(s, (11, 18, 24), (x-8, y+78, 142, 34))
        for panel_x in (x-4, x+66):
            pygame.draw.rect(s, (29, 40, 46), (panel_x, y+83, 62, 25))
            pygame.draw.rect(s, (51, 64, 68), (panel_x, y+83, 62, 25), 1)
            pygame.draw.line(s, (106, 116, 112), (panel_x+45, y+89), (panel_x+55, y+89), 2)
            for vent in range(3):
                pygame.draw.line(s, (15, 26, 32), (panel_x+6, y+93+vent*4), (panel_x+24, y+93+vent*4))
        pygame.draw.rect(s, (91, 91, 77), (x-12, y+74, 150, 6))
        pygame.draw.line(s, (152, 142, 111), (x-12, y+74), (x+137, y+74))
        for leg in (x-6, x+125):
            pygame.draw.rect(s, (42, 55, 60), (leg, y+80, 5, 32))
        pygame.draw.rect(s, (19, 28, 34), (x+104, y+43, 24, 31))
        pygame.draw.rect(s, (53, 67, 71), (x+106, y+45, 20, 2))
        for row in range(4):
            pygame.draw.line(s, (48, 64, 68), (x+108, y+51+row*4), (x+122, y+51+row*4))
        pygame.draw.circle(s, (88, 164, 166), (x+119, y+69), 1)
        pygame.draw.rect(s, (24, 37, 44), (x+10, y+65, 76, 8))
        for kx in range(x+14, x+80, 6):
            for ky in (y+67, y+70):
                pygame.draw.rect(s, (74, 90, 91), (kx, ky, 4, 1))
        # Moldura e reflexos do monitor; nada animado é pintado na moldura.
        pygame.draw.rect(s, (5, 11, 17), (x+10, y, 84, 58))
        pygame.draw.rect(s, (66, 81, 87), (x+10, y, 84, 58), 2)
        pygame.draw.line(s, (112, 128, 127), (x+12, y+1), (x+91, y+1))
        pygame.draw.rect(s, (47, 61, 67), (x+46, y+58, 10, 6))
        pygame.draw.rect(s, (58, 70, 73), (x+34, y+62, 34, 3))
        pygame.draw.circle(s, (89, 176, 171), (x+87, y+54), 1)
        self.monitor_screens.append(pygame.Rect(x+16, y+5, 72, 46))
        # Cabos e pequenos acessórios dão profundidade sem novas colisões.
        pygame.draw.lines(s, (24, 35, 40), False,
                          [(x+100, y+68), (x+100, y+88), (x+117, y+88), (x+117, y+110)], 2)
        pygame.draw.ellipse(s, (88, 104, 107), (x+91, y+66, 8, 5))

    def draw(self, surface, camera, tick, corrupted):
        offset = round(camera.offset.x)
        # Módulos em resolução nativa: sem esticar uma sala para cobrir todo o corredor.
        for x in range(0, self.width, self.background.get_width()):
            surface.blit(self.background, (x-offset, -round(camera.offset.y)))
        surface.blit(self.static, (-offset, -round(camera.offset.y)))
        for seed, rect in enumerate(self.monitor_screens):
            self.terminals.draw(surface, camera.apply(rect), tick, seed, corrupted)
