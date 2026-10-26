"""Telas de acesso à escola, com navegação por mouse e teclado."""
import pygame
import assets
import settings
from entities.player import Player
from ui import theme


class Frontend:
    def __init__(self):
        facade = assets.load_image('menu/school_night.png')
        self.background = pygame.transform.scale(facade, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.font_title = pygame.font.Font(None, 94)
        self.font_heading = pygame.font.Font(None, 36)
        self.font = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 20)
        self.menu_rects = [pygame.Rect(56, 300, 304, 54), pygame.Rect(56, 370, 304, 54)]
        self.character_rects = [pygame.Rect(244, 132, 220, 272), pygame.Rect(496, 132, 220, 272)]
        self.confirm_rect = pygame.Rect(320, 428, 320, 48)
        self.back_rect = pygame.Rect(28, 28, 120, 40)
        self.characters = tuple(Player.CHARACTERS)
        self.previews = {}
        for character in self.characters:
            self.previews[character] = [pygame.transform.scale(frame, (136, 136))
                                        for frame in Player._load_sprites(character)['idle_r']]
        self.animation_tick = 0
        self.veil = pygame.Surface(self.background.get_size(), pygame.SRCALPHA)
        for x in range(settings.SCREEN_WIDTH):
            alpha = max(0, int(225*(1-x/760)))
            pygame.draw.line(self.veil, (*theme.INK, alpha), (x, 0), (x, settings.SCREEN_HEIGHT))

    def update(self):
        self.animation_tick += 1

    def _center(self, surface, value, center, font=None, color=theme.PAPER):
        rendered = (font or self.font).render(value, True, color)
        surface.blit(rendered, rendered.get_rect(center=center))

    def _button(self, surface, rect, label, focused=False, number=None):
        theme.panel(surface, rect, theme.AMBER if focused else None,
                    theme.RAISED if focused else theme.PANEL)
        if focused:
            pygame.draw.line(surface, theme.AMBER, rect.topleft, (rect.right-1, rect.top))
        if number:
            theme.text(surface, self.font_small, number, (rect.x+17, rect.y+19), theme.AMBER if focused else theme.MUTED)
            theme.text(surface, self.font, label, (rect.x+54, rect.y+15), theme.PAPER)
            if focused:
                theme.text(surface, self.font, '>', (rect.right-30, rect.y+14), theme.AMBER)
        else:
            self._center(surface, label, rect.center, color=theme.AMBER if focused else theme.PAPER)

    def draw_menu(self, surface, menu_index):
        surface.blit(self.background, (0, 0))
        surface.blit(self.veil, (0, 0))
        theme.text(surface, self.font_small, 'IFRN  /  CAMPUS CAICÓ', (58, 66), theme.AMBER)
        theme.text(surface, self.font_title, 'IFVania', (51, 106))
        pygame.draw.line(surface, theme.AMBER, (58, 193), (104, 193), 3)
        theme.text(surface, self.font, 'A escola não é mais a mesma.', (58, 218), theme.PAPER)
        for i, (rect, label) in enumerate(zip(self.menu_rects, ('Jogar', 'Sair'))):
            self._button(surface, rect, label, i == menu_index, f'0{i+1}')
        theme.text(surface, self.font_small, 'Uma presença tomou os corredores.', (58, 454), theme.MUTED)
        pygame.draw.rect(surface, theme.INK, (0, 498, settings.SCREEN_WIDTH, 42))
        pygame.draw.line(surface, theme.BORDER, (28, 498), (932, 498))
        theme.text(surface, self.font_small, 'SETAS  escolher     ENTER  confirmar     MOUSE  selecionar', (56, 513), theme.MUTED)
        theme.text(surface, self.font_small, 'IFVANIA / ACESSO', (790, 513), theme.AMBER)

    def draw_selection(self, surface, character_index):
        surface.blit(self.background, (0, 0))
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((*theme.INK, 215))
        surface.blit(overlay, (0, 0))
        self._button(surface, self.back_rect, 'Voltar')
        self._center(surface, 'ESCOLHA SEU PERSONAGEM', (480, 59), self.font_heading)
        self._center(surface, 'A mesma escola. O mesmo perigo.', (480, 95), self.font_small, theme.MUTED)
        for i, rect in enumerate(self.character_rects):
            selected = i == character_index
            theme.panel(surface, rect, theme.AMBER if selected else None,
                        theme.RAISED if selected else theme.PANEL)
            theme.text(surface, self.font_small, f'0{i+1} / ESTUDANTE', (rect.x+18, rect.y+16), theme.AMBER if selected else theme.MUTED)
            pygame.draw.line(surface, theme.BORDER, (rect.x+18, rect.y+44), (rect.right-18, rect.y+44))
            character = self.characters[i]
            frame = self.previews[character][(self.animation_tick//24) % 2]
            pygame.draw.ellipse(surface, (7, 13, 18), (rect.centerx-58, 304, 116, 12))
            surface.blit(frame, frame.get_rect(midbottom=(rect.centerx, 316)))
            self._center(surface, Player.CHARACTERS[character], (rect.centerx, 342), self.font_heading)
            self._center(surface, 'SELECIONADO' if selected else 'Clique para escolher',
                         (rect.centerx, 382), self.font_small, theme.AMBER if selected else theme.MUTED)
        self._button(surface, self.confirm_rect,
                     f'Jogar com {Player.CHARACTERS[self.characters[character_index]]}', True)
        self._center(surface, 'Mesmos controles e habilidades para os dois personagens.', (480, 501), self.font_small, theme.MUTED)
        self._center(surface, 'SETAS escolher    ENTER começar    ESC voltar', (480, 526), self.font_small, theme.MUTED)
