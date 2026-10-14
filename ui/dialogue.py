"""Sistema simples de caixas de diálogo estilo RPG/metroidvania."""
import pygame
import settings


class DialogueBox:
    def __init__(self):
        self.lines = []          # lista de tuplas (falante, texto)
        self.index = 0
        self.active = False
        self.on_finish = None
        self.font = pygame.font.SysFont(settings.FONT_NAME, 20)
        self.name_font = pygame.font.SysFont(settings.FONT_NAME, 22, bold=True)
        self._char_shown = 0
        self._typing_speed = 2  # caracteres por frame

    def start(self, lines, on_finish=None):
        if not lines:
            if on_finish:
                on_finish()
            return
        self.lines = lines
        self.index = 0
        self.active = True
        self.on_finish = on_finish
        self._char_shown = 0

    def handle_event(self, event):
        if not self.active:
            return
        if event.type == pygame.KEYDOWN and event.key in (
            pygame.K_e, pygame.K_RETURN, pygame.K_SPACE
        ):
            speaker, text = self.lines[self.index]
            if self._char_shown < len(text):
                self._char_shown = len(text)  # revela tudo de uma vez
                return
            self.index += 1
            self._char_shown = 0
            if self.index >= len(self.lines):
                self.active = False
                cb = self.on_finish
                self.on_finish = None
                if cb:
                    cb()

    def update(self):
        if not self.active:
            return
        speaker, text = self.lines[self.index]
        if self._char_shown < len(text):
            self._char_shown = min(len(text), self._char_shown + self._typing_speed)

    def _wrap(self, text, max_width):
        words = text.split(' ')
        lines, cur = [], ''
        for w in words:
            trial = (cur + ' ' + w).strip()
            if self.font.size(trial)[0] > max_width:
                lines.append(cur)
                cur = w
            else:
                cur = trial
        if cur:
            lines.append(cur)
        return lines

    def draw(self, surface):
        if not self.active:
            return
        speaker, text = self.lines[self.index]
        shown_text = text[: self._char_shown]

        box_h = 130
        box_rect = pygame.Rect(20, settings.SCREEN_HEIGHT - box_h - 20,
                                settings.SCREEN_WIDTH - 40, box_h)
        panel = pygame.Surface(box_rect.size, pygame.SRCALPHA)
        panel.fill(settings.UI_BG)
        pygame.draw.rect(panel, settings.UI_BORDER, panel.get_rect(), 3, border_radius=10)
        surface.blit(panel, box_rect.topleft)

        # retrato circular simples com inicial do falante
        portrait_rect = pygame.Rect(box_rect.x + 16, box_rect.y + 16, 60, 60)
        pygame.draw.circle(surface, settings.NAME_COLOR, portrait_rect.center, 30)
        pygame.draw.circle(surface, settings.WHITE, portrait_rect.center, 30, 2)
        initial = self.name_font.render(speaker[:1], True, settings.BLACK)
        surface.blit(initial, initial.get_rect(center=portrait_rect.center))

        name_surf = self.name_font.render(speaker, True, settings.NAME_COLOR)
        surface.blit(name_surf, (box_rect.x + 90, box_rect.y + 14))

        wrapped = self._wrap(shown_text, box_rect.width - 110)
        for i, line in enumerate(wrapped[:3]):
            line_surf = self.font.render(line, True, settings.TEXT_COLOR)
            surface.blit(line_surf, (box_rect.x + 90, box_rect.y + 46 + i * 24))

        if self._char_shown >= len(text):
            hint = self.font.render("[E / Enter] continuar", True, (180, 180, 180))
            surface.blit(hint, (box_rect.right - hint.get_width() - 16, box_rect.bottom - 26))
