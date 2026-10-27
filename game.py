"""Máquina de estados principal do jogo."""
import sys
import unicodedata
import pygame
import settings
from entities.player import Player
from world.level import Level
from world.levels_data import build_levels, STORY_INTRO, STORY_CORRUPTION_INDEX
from world.school import SchoolLevel
from world.school_data import ENCOUNTER_DIALOGUE, MOUSE_DISCOVERY
from world.boss_transition import BossTransition
from ui.dialogue import DialogueBox
from ui.hud import HUD
from ui.frontend import Frontend

STATE_MENU = "menu"
STATE_CHARACTER_SELECT = "character_select"
STATE_NAME_ENTRY = 'name_entry'
STATE_PLAYING = "playing"
STATE_DIALOGUE = "dialogue"
STATE_LEVEL_CARD = "level_card"
STATE_PAUSE = "pause"
STATE_GAME_OVER = "game_over"
STATE_CONTENT_END = "content_end"
STATE_ABDUCTION = "abduction"
STATE_INFECTION = "infection"
STATE_BOSS_TRANSFORMATION = 'boss_transformation'


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.hud = HUD()
        self.dialogue_box = DialogueBox()
        self.frontend = Frontend()
        self.menu_index = 0
        self.character_index = 0
        self.selected_character = "boy"
        self.player_name = ''
        self.name_buffer = ''
        self.name_error = ''

        self.level_defs = build_levels()
        self.level_index = 0
        self.level = None
        self.player = None
        self.in_story_intro = False

        self.state = STATE_MENU
        self.level_card_timer = 0
        self.abduction_timer = 0
        self.abduction_duration = 90
        self.pause_return_state = STATE_PLAYING
        self.infection_timer = 0
        self.infection_duration = 60
        self.boss_transition = None

    # ------------------------------------------------------------------
    def run(self):
        while self.running:
            events = pygame.event.get()
            gameplay_events = self._process_events(events)
            if not self.running:
                break

            keys = pygame.key.get_pressed()
            self._update(keys, gameplay_events)
            self._draw()

            self.clock.tick(settings.FPS)

        pygame.quit()
        sys.exit()

    # ------------------------------------------------------------------
    def _process_events(self, events):
        gameplay_events = []
        for event in events:
            previous_state = self.state
            self._handle_event(event)
            if previous_state == STATE_PLAYING and self.state == STATE_PLAYING:
                gameplay_events.append(event)
            if not self.running:
                break
        return gameplay_events

    def _handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.key.stop_text_input()
            self.running = False
            return
        if self.state == STATE_NAME_ENTRY:
            if event.type == pygame.TEXTINPUT:
                value = ''.join(c for c in event.text if c.isprintable())
                self.name_buffer = unicodedata.normalize('NFC', self.name_buffer+value)[:20]
                self.name_error = ''
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.name_buffer = self.name_buffer[:-1]
                    self.name_error = ''
                elif event.key == pygame.K_RETURN:
                    self._confirm_name()
                elif event.key == pygame.K_ESCAPE:
                    pygame.key.stop_text_input()
                    self.state = STATE_CHARACTER_SELECT
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.frontend.name_confirm_rect.collidepoint(event.pos):
                    self._confirm_name()
                elif self.frontend.back_rect.collidepoint(event.pos):
                    pygame.key.stop_text_input()
                    self.state = STATE_CHARACTER_SELECT
            return
        # Um evento pertence a uma única tela, mesmo se o callback trocar estado.
        if self.state == STATE_DIALOGUE or (self.state == STATE_BOSS_TRANSFORMATION and self.dialogue_box.active):
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.pause_return_state = self.state
                self.state = STATE_PAUSE
                return
            self.dialogue_box.handle_event(event)
            return
        if event.type == pygame.KEYDOWN:
            self._handle_keydown(event, [event])
        elif event.type == pygame.MOUSEMOTION and self.state == STATE_MENU:
            for i, rect in enumerate(self.frontend.menu_rects):
                if rect.collidepoint(event.pos):
                    self.menu_index = i
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.state == STATE_MENU:
                for i, rect in enumerate(self.frontend.menu_rects):
                    if rect.collidepoint(event.pos):
                        self.menu_index = i
                        self._activate_menu()
                        return
            elif self.state == STATE_CHARACTER_SELECT:
                if self.frontend.back_rect.collidepoint(event.pos):
                    self.state = STATE_MENU
                elif self.frontend.confirm_rect.collidepoint(event.pos):
                    self._confirm_character()
                else:
                    for i, rect in enumerate(self.frontend.character_rects):
                        if rect.collidepoint(event.pos):
                            self.character_index = i

    def _activate_menu(self):
        if self.menu_index == 0:
            self.state = STATE_CHARACTER_SELECT
            self.character_index = self.frontend.characters.index(self.selected_character)
        else:
            self.running = False

    def _confirm_character(self):
        self.selected_character = self.frontend.characters[self.character_index]
        self.state = STATE_NAME_ENTRY
        self.name_error = ''
        pygame.key.start_text_input()
        pygame.key.set_text_input_rect(self.frontend.name_rect)

    def _confirm_name(self):
        name = ' '.join(self.name_buffer.split())
        if not name:
            self.name_error = 'Digite seu nome para continuar.'
            return
        self.player_name = self.name_buffer = name
        pygame.key.stop_text_input()
        self._start_story()

    def _handle_keydown(self, event, events):
        if self.state == STATE_MENU:
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_w, pygame.K_s, pygame.K_TAB):
                self.menu_index = 1 - self.menu_index
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._activate_menu()
            elif event.key == pygame.K_ESCAPE:
                self.running = False
            return
        if self.state == STATE_CHARACTER_SELECT:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d, pygame.K_TAB):
                self.character_index = 1 - self.character_index
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._confirm_character()
            elif event.key == pygame.K_ESCAPE:
                self.state = STATE_MENU
            return
        if event.key == pygame.K_ESCAPE:
            if self.state in (STATE_PLAYING, STATE_ABDUCTION, STATE_INFECTION, STATE_BOSS_TRANSFORMATION):
                self.pause_return_state = self.state
                self.state = STATE_PAUSE
            elif self.state == STATE_PAUSE:
                self.state = self.pause_return_state
            else:
                self.running = False

        if self.state in (STATE_GAME_OVER, STATE_CONTENT_END) and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.state = STATE_MENU
            self.menu_index = 0
            self.level_index = 0

        elif self.state == STATE_LEVEL_CARD and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.state = STATE_PLAYING

    # ------------------------------------------------------------------
    def _start_story(self):
        self.dialogue_box.player_name = self.player_name or ('Aluna' if self.selected_character == 'girl' else 'Aluno')
        self.boss_transition = None
        self.level_index = 0
        self._load_school('classroom', fresh_player=True)
        self.in_story_intro = True
        self.state = STATE_DIALOGUE
        self.dialogue_box.start(STORY_INTRO, on_finish=self._begin_corridor)

    def _load_school(self, room, fresh_player=False):
        self.level = SchoolLevel(room)
        if fresh_player:
            self.player = Player(*self.level.player_spawn, character=self.selected_character,
                                 name=self.player_name or None)
        else:
            self.player.respawn(*self.level.player_spawn)
        self.player.whip_unlocked = False
        self.player.on_ground = True
        self.level.camera.update(self.player.rect)

    def _begin_corridor(self):
        self._load_school('corridor')
        self._show_level_card()

    def _start_abduction(self):
        self.state = STATE_ABDUCTION
        self.abduction_timer = 0
        self.player.vel.update(0, 0)
        self.level.begin_abduction(self.player)

    def _enter_virtual(self):
        self._load_level(0)
        self.player.whip_unlocked = False
        self.state = STATE_DIALOGUE
        self.dialogue_box.start(MOUSE_DISCOVERY, on_finish=self._grant_mouse)

    def _grant_mouse(self):
        self.player.whip_unlocked = True
        self._show_level_card()

    def _start_boss_transformation(self):
        self.boss_transition = BossTransition(self.level, self.player)
        self.state = STATE_BOSS_TRANSFORMATION

    def _load_level(self, index, fresh_player=False):
        self.level = Level(self.level_defs[index])
        spawn = self.level.player_spawn
        if fresh_player or self.player is None:
            self.player = Player(*spawn, character=self.selected_character, name=self.player_name or None)
        else:
            saved_abilities = self.player.abilities
            saved_health_bonus = self.player.max_health
            self.player.respawn(*spawn)
            self.player.abilities = saved_abilities
            self.player.max_health = saved_health_bonus
            self.player.health = self.player.max_health
        self.player.whip_unlocked = True
        self.player.on_ground = True
        self.dialogue_box.player_name = self.player.name
        self.level.camera.update(self.player.rect)

    def _show_level_card(self):
        self.in_story_intro = False
        self.state = STATE_LEVEL_CARD
        self.level_card_timer = 0

    # ------------------------------------------------------------------
    def _update(self, keys, events):
        if self.level and self.state in (STATE_PLAYING, STATE_DIALOGUE, STATE_ABDUCTION,
                                        STATE_INFECTION, STATE_BOSS_TRANSFORMATION):
            self.level.update_visuals()
        if self.state in (STATE_MENU, STATE_CHARACTER_SELECT, STATE_NAME_ENTRY):
            self.frontend.update()
        elif self.state == STATE_PLAYING:
            if getattr(self.level.boss, 'cinematic_pending', False):
                self._start_boss_transformation()
                return
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
            elif event_type == 'enter_lab':
                self._load_school('lab')
            elif event_type == 'school_encounter':
                self.state = STATE_DIALOGUE
                self.player.vel.update(0, 0)
                self.dialogue_box.start(ENCOUNTER_DIALOGUE, on_finish=self._start_abduction)
            elif event_type == 'boss_transform':
                self._start_boss_transformation()

            if not self.player.alive:
                self.state = STATE_GAME_OVER

        elif self.state == STATE_DIALOGUE:
            self.dialogue_box.update()
            if self.in_story_intro and self.dialogue_box.index >= STORY_CORRUPTION_INDEX:
                self.level.corrupted = True

        elif self.state == STATE_ABDUCTION:
            self.abduction_timer += 1
            self.level.update_abduction(self.player, self.abduction_timer)
            if self.abduction_timer >= self.abduction_duration:
                self._enter_virtual()

        elif self.state == STATE_INFECTION:
            self.infection_timer += 1
            if self.infection_timer >= self.infection_duration//2:
                self.level.infected = True
            if self.infection_timer >= self.infection_duration:
                self.level.finish_boss_dialogue()
                self.state = STATE_PLAYING

        elif self.state == STATE_BOSS_TRANSFORMATION:
            if self.dialogue_box.active:
                self.dialogue_box.update()
            else:
                event = self.boss_transition.update()
                if event == 'speech':
                    self.dialogue_box.start([('Entidade', 'Ainda não terminou.')],
                                             on_finish=self.boss_transition.resume)
                elif event == 'complete':
                    self.state = STATE_PLAYING

        elif self.state == STATE_LEVEL_CARD:
            self.level_card_timer += 1
            if self.level_card_timer > 90:
                self.state = STATE_PLAYING

    def _resume_from_dialogue(self):
        if self.state == STATE_DIALOGUE:
            if getattr(self.level, 'encounter_pending', False):
                self.infection_timer = 0
                self.state = STATE_INFECTION
            else:
                self.state = STATE_PLAYING

    def _advance_level(self):
        self.level_index += 1
        if self.level_index >= len(self.level_defs):
            self.state = STATE_CONTENT_END
        else:
            self._load_level(self.level_index)
            self._show_level_card()

    # ------------------------------------------------------------------
    def _draw(self):
        if self.state == STATE_MENU:
            self._draw_menu()
        elif self.state == STATE_CHARACTER_SELECT:
            self.frontend.draw_selection(self.screen, self.character_index)
        elif self.state == STATE_NAME_ENTRY:
            self.frontend.draw_name_entry(self.screen, self.name_buffer,
                                          self.selected_character, self.name_error)
        elif self.state == STATE_BOSS_TRANSFORMATION or (self.state == STATE_PAUSE
                                                        and self.pause_return_state == STATE_BOSS_TRANSFORMATION):
            self.boss_transition.draw(self.screen)
            if self.dialogue_box.active:
                self.dialogue_box.draw(self.screen)
            if self.state == STATE_PAUSE:
                self._draw_overlay('PAUSADO', 'ESC para continuar')
        elif self.state in (STATE_PLAYING, STATE_DIALOGUE, STATE_PAUSE, STATE_ABDUCTION, STATE_INFECTION):
            self.level.draw(self.screen)
            self.player.draw(self.screen, self.level.camera)
            if not self.in_story_intro:
                self.hud.draw(self.screen, self.player, self.level.name, self.level.boss)
                if self.state not in (STATE_ABDUCTION, STATE_INFECTION) and not (
                        self.state == STATE_PAUSE and self.pause_return_state in (STATE_ABDUCTION, STATE_INFECTION)):
                    self.hud.draw_controls_hint(self.screen, self.player)
            if self.state == STATE_ABDUCTION or (self.state == STATE_PAUSE
                                                  and self.pause_return_state == STATE_ABDUCTION):
                self.level.draw_abduction(self.screen, self.player,
                                           self.abduction_timer/self.abduction_duration)
            if self.state == STATE_INFECTION or (self.state == STATE_PAUSE
                                                 and self.pause_return_state == STATE_INFECTION):
                self.level.draw_infection(self.screen, self.infection_timer/self.infection_duration)
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
        elif self.state == STATE_CONTENT_END:
            self.screen.fill((10, 25, 18))
            self._draw_overlay("A JORNADA CONTINUA", "Fim do conteúdo disponível. ENTER para voltar ao menu")
            text = self.hud.font_small.render(
                'A IFVania segue ativa. A energia da escola ainda precisa ser desligada.',
                True, settings.TEXT_COLOR)
            self.screen.blit(text, text.get_rect(center=(settings.SCREEN_WIDTH//2, 340)))

        pygame.display.flip()

    def _draw_overlay(self, title, sub):
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        self.hud.draw_center_text(self.screen, title, sub)

    def _draw_menu(self):
        self.frontend.draw_menu(self.screen, self.menu_index)
