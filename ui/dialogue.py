"""Sistema simples de caixas de diálogo estilo RPG/metroidvania."""
import pygame
import settings
from ui import theme


class DialogueBox:
    def __init__(self):
        self.lines = []          # lista de tuplas (falante, texto)
        self.index = 0
        self.active = False
        self.on_finish = None
        self.font = pygame.font.Font(None, 22)
        self.name_font = pygame.font.Font(None, 24)
        self._char_shown = 0
        self._typing_speed = 2  # caracteres por frame
        self.player_name = 'Aluno(a)'

    def resolve_lines(self, lines):
        return [(self.player_name if speaker in ('Aluno(a)', '{player}') else speaker,
                 text.replace('{player}', self.player_name)) for speaker, text in lines]

    def start(self, lines, on_finish=None):
        if not lines:
            if on_finish:
                on_finish()
            return
        self.lines = self.resolve_lines(lines)
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

        box_rect = pygame.Rect(24, settings.SCREEN_HEIGHT-156, settings.SCREEN_WIDTH-48, 142)
        theme.panel(surface, box_rect, theme.CYAN if speaker == 'Entidade' else theme.AMBER)
        pygame.draw.line(surface, theme.BORDER, (box_rect.x+20, box_rect.y+36),
                         (box_rect.right-20, box_rect.y+36))
        theme.text(surface, self.name_font, speaker.upper(), (box_rect.x+20, box_rect.y+12),
                   theme.CYAN if speaker == 'Entidade' else theme.AMBER)
        wrapped = self._wrap(shown_text, box_rect.width-40)
        for i, line in enumerate(wrapped[:3]):
            theme.text(surface, self.font, line, (box_rect.x+20, box_rect.y+48+i*20))
        if self._char_shown >= len(text):
            hint_font = pygame.font.Font(None, 18)
            hint = hint_font.render('E / ENTER  continuar', True, theme.MUTED)
            surface.blit(hint, hint.get_rect(bottomright=(box_rect.right-20, box_rect.bottom-10)))
