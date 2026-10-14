"""Máquina de estados principal do jogo."""
import sys
import pygame
import settings
from entities.player import Player
from world.level import Level
from world.levels_data import build_levels, STORY_INTRO
from ui.dialogue import DialogueBox
from ui.hud import HUD

STATE_MENU = "menu"
STATE_STORY = "story"
STATE_PLAYING = "playing"
STATE_DIALOGUE = "dialogue"
STATE_LEVEL_CARD = "level_card"
STATE_PAUSE = "pause"
STATE_GAME_OVER = "game_over"
STATE_VICTORY = "victory"


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.hud = HUD()
        self.dialogue_box = DialogueBox()
        self.font_title = pygame.font.SysFont(settings.FONT_NAME, 46, bold=True)
        self.font_menu = pygame.font.SysFont(settings.FONT_NAME, 22)

        self.level_defs = build_levels()
        self.level_index = 0
        self.level = None
        self.player = None

        self.state = STATE_MENU
        self.level_card_timer = 0

    # ------------------------------------------------------------------
    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                self.dialogue_box.handle_event(event)
                if event.type == pygame.KEYDOWN:
                    self._handle_keydown(event, events)

            keys = pygame.key.get_pressed()
            self._update(keys, events)
            self._draw()

            self.clock.tick(settings.FPS)

        pygame.quit()
        sys.exit()

    # ------------------------------------------------------------------
    def _handle_keydown(self, event, events):
        if event.key == pygame.K_ESCAPE:
            if self.state == STATE_PLAYING:
                self.state = STATE_PAUSE
            elif self.state == STATE_PAUSE:
                self.state = STATE_PLAYING
            else:
                self.running = False

        if self.state == STATE_MENU and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self._start_story()

        elif self.state in (STATE_GAME_OVER, STATE_VICTORY) and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.state = STATE_MENU
            self.level_index = 0

        elif self.state == STATE_LEVEL_CARD and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.state = STATE_PLAYING

    # ------------------------------------------------------------------
    def _start_story(self):
        self.level_index = 0
        self._load_level(0, fresh_player=True)
        self.state = STATE_DIALOGUE
        self.dialogue_box.start(STORY_INTRO, on_finish=self._show_level_card)

    def _load_level(self, index, fresh_player=False):
        self.level = Level(self.level_defs[index])
        spawn = self.level.player_spawn
        if fresh_player or self.player is None:
            self.player = Player(*spawn)
        else:
            saved_abilities = self.player.abilities
            saved_health_bonus = self.player.max_health
            self.player.respawn(*spawn)
            self.player.abilities = saved_abilities
            self.player.max_health = saved_health_bonus
            self.player.health = self.player.max_health

    def _show_level_card(self):
        self.state = STATE_LEVEL_CARD
        self.level_card_timer = 0

    # ------------------------------------------------------------------
    def _update(self, keys, events):
        if self.state == STATE_PLAYING:
            self.player.handle_input(keys, events)
            self.player.update(self.level.tilemap.solids, self.level.tilemap.hazards)

            event_type, payload = self.level.update(self.player, events)
            if event_type == "dialogue":
                self.state = STATE_DIALOGUE
                self.dialogue_box.start(payload, on_finish=self._resume_from_dialogue)
            elif event_type == "level_complete":
                self._advance_level()
            elif event_type == "fell":
                self.player.respawn(*self.level.player_spawn)

            if not self.player.alive:
                self.state = STATE_GAME_OVER

        elif self.state == STATE_DIALOGUE:
            self.dialogue_box.update()

        elif self.state == STATE_LEVEL_CARD:
            self.level_card_timer += 1
            if self.level_card_timer > 90:
                self.state = STATE_PLAYING

    def _resume_from_dialogue(self):
        if self.state == STATE_DIALOGUE:
            self.state = STATE_PLAYING

    def _advance_level(self):
        self.level_index += 1
        if self.level_index >= len(self.level_defs):
            self.state = STATE_VICTORY
        else:
            self._load_level(self.level_index)
            self._show_level_card()

    # ------------------------------------------------------------------
    def _draw(self):
        if self.state == STATE_MENU:
            self._draw_menu()
        elif self.state in (STATE_PLAYING, STATE_DIALOGUE, STATE_PAUSE):
            self.level.draw(self.screen)
            self.player.draw(self.screen, self.level.camera)
            self.hud.draw(self.screen, self.player, self.level.name, self.level.boss)
            self.hud.draw_controls_hint(self.screen, self.player)
            if self.state == STATE_DIALOGUE:
                self.dialogue_box.draw(self.screen)
            if self.state == STATE_PAUSE:
                self._draw_overlay("PAUSADO", "ESC para continuar")
        elif self.state == STATE_LEVEL_CARD:
            self.screen.fill(settings.BG_COLOR)
            self._draw_overlay(self.level.name, "Pressione ENTER para começar")
        elif self.state == STATE_GAME_OVER:
            self.screen.fill((25, 10, 15))
            self._draw_overlay("VOCÊ FOI REPROVADO(A)...", "ENTER para voltar ao menu")
        elif self.state == STATE_VICTORY:
            self.screen.fill((10, 25, 18))
            self._draw_overlay("PARABÉNS! ESCOLA SALVA!", "ENTER para voltar ao menu")

        pygame.display.flip()

    def _draw_overlay(self, title, sub):
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        self.hud.draw_center_text(self.screen, title, sub)

    def _draw_menu(self):
        self.screen.fill(settings.BG_COLOR)
        title = self.font_title.render(settings.TITLE, True, settings.NAME_COLOR)
        self.screen.blit(title, title.get_rect(center=(settings.SCREEN_WIDTH // 2, 160)))

        subtitle = self.font_menu.render(
            "Um metroidvania sobre enfrentar 6 professores de programação corrompidos",
            True, settings.TEXT_COLOR)
        self.screen.blit(subtitle, subtitle.get_rect(center=(settings.SCREEN_WIDTH // 2, 220)))

        prompt = self.font_menu.render("Pressione ENTER ou ESPAÇO para começar", True, settings.WHITE)
        self.screen.blit(prompt, prompt.get_rect(center=(settings.SCREEN_WIDTH // 2, 320)))

        controls = [
            "<- -> mover   ESPAÇO pular   X mouse-chicote   SHIFT dash   F tiro   Q escudo   ESC pausar",
        ]
        for i, line in enumerate(controls):
            c_surf = self.font_menu.render(line, True, (190, 190, 190))
            self.screen.blit(c_surf, c_surf.get_rect(center=(settings.SCREEN_WIDTH // 2, 380 + i * 26)))
