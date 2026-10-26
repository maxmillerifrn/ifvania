"""Classe Level: liga tilemap, inimigos, chefe, powerup e câmera numa fase jogável."""
import pygame
import settings
import assets
from world.tilemap import TileMap
from world.camera import Camera
from entities.enemy import Enemy
from entities.teacher_bosses import BOSS_CLASSES
from entities.romer_bug import RomerBug
from entities.npc import Teacher
from powerups import PowerUp
from world.dark_school import DarkSchool

TS = settings.TILE_SIZE


class Level:
    def __init__(self, level_data):
        self.data = level_data
        self.name = level_data["name"]
        self.tilemap = TileMap(level_data["ascii_map"])
        self.camera = Camera(self.tilemap.width, self.tilemap.height)

        self.enemies = pygame.sprite.Group()
        for (ex, ey) in self.tilemap.enemy_spawns:
            self.enemies.add(Enemy(*self._grounded_spawn(ex, ey)))

        boss_def = level_data["boss"]
        bx, by = self.tilemap.boss_spawn
        boss_class = BOSS_CLASSES[boss_def["boss_type"]]
        bx, by = self._grounded_spawn(bx, by)
        options = {}
        if boss_class is RomerBug:
            options['cinematic_transform'] = level_data.get('cinematic_transform', False)
            left = level_data.get('arena_left', TS)
            options["arena"] = pygame.Rect(left, TS, self.tilemap.width - left - TS,
                                            self.tilemap.height - 2 * TS)
        self.boss = boss_class(bx, by, boss_def["name"], boss_def["subject"],
                          boss_def["color"], health=boss_def["health"],
                          sprite_file=boss_def.get("sprite_file"), **options)

        self.powerups = pygame.sprite.Group()
        self.spawned_powerup = False

        self.dialogue_played = False
        self.boss_defeated_dialogue_played = False
        self.completed = False
        self.player_spawn = self._grounded_spawn(*self.tilemap.player_spawn)
        self.requires_infection = level_data.get('requires_infection', False)
        self.infected = not self.requires_infection
        self.encounter_pending = False
        self.human_teacher = Teacher(bx, by, 'romerito') if self.requires_infection else None
        self.infection_bug = assets.load_character_frames(['enemies/bug_0.png'])[0] if self.requires_infection else None
        self.encounter_font = pygame.font.Font(None, 20)
        self.infection_font = pygame.font.Font(None, 24)
        self.school_scene = (DarkSchool(self.tilemap.width, self.tilemap.height,
                                       self.player_spawn[1]+settings.CHARACTER_SIZE[1])
                             if level_data.get('school_battle') else None)

        # sprites do cenário (carregados/cacheados uma vez em assets.py)
        self.ground_img = assets.load_image("tiles/ground.png", (TS, TS), settings.GROUND_COLOR)
        self.spike_img = assets.load_image("tiles/spike.png", (TS, TS), settings.SPIKE_COLOR)
        self.bg_panel_img = assets.load_image("background/panel.png", (90, 220), settings.BG_COLOR_2)

    def _grounded_spawn(self, x, y):
        """Os marcadores do mapa indicam a coluna; os pés usam o piso abaixo."""
        width, height = settings.CHARACTER_SIZE
        floors = sorted({solid.top for solid in self.tilemap.solids
                         if solid.left < x + width and solid.right > x
                         and solid.top >= y - height},
                        key=lambda top: abs(top - (y + TS)))
        for floor in floors:
            body = pygame.Rect(x, floor - height, width, height)
            if not any(body.colliderect(solid) for solid in self.tilemap.solids):
                return body.topleft
        raise ValueError(f"Sem piso livre para personagem em {(x, y)}")

    # ------------------------------------------------------------------
    def update(self, player, dt_events):
        if self.completed or self.encounter_pending:
            return None, None
        if getattr(self.boss, 'cinematic_pending', False):
            return 'boss_transform', None
        if self.boss.defeated:
            return self._after_defeat(player)
        # A entrada da arena abre a conversa antes de processar qualquer dano,
        # inclusive quando o jogador chega pulando ou além do primeiro bloco.
        if not self.dialogue_played and self.tilemap.dialogue_trigger:
            if player.rect.colliderect(self.tilemap.dialogue_trigger):
                self.dialogue_played = True
                if self.requires_infection:
                    self.encounter_pending = True
                else:
                    self.boss.activate()
                self.camera.update(player.rect)
                return ("dialogue", self.data["boss_dialogue"])

        self.enemies.update(self.tilemap.solids)
        self.boss.update(player, self.tilemap.solids)
        self.powerups.update()
        self.camera.update(player.rect)

        # ataque corpo-a-corpo do jogador contra inimigos e chefe
        melee_rect = player.get_melee_rect()
        if melee_rect:
            for enemy in list(self.enemies):
                if melee_rect.colliderect(enemy.rect):
                    player.try_melee_hit(enemy, self.tilemap.solids)
            if self.boss.active and self.boss.alive and melee_rect.colliderect(self.boss.rect):
                player.try_melee_hit(self.boss, self.tilemap.solids)

        # projéteis do jogador contra inimigos/chefe
        for proj in list(player.projectiles):
            for enemy in list(self.enemies):
                if proj.rect.colliderect(enemy.rect):
                    enemy.take_damage(1)
                    proj.kill()
                    break
            else:
                if self.boss.active and self.boss.alive and proj.rect.colliderect(self.boss.rect):
                    self.boss.take_damage(1)
                    proj.kill()

        if getattr(self.boss, 'cinematic_pending', False):
            return 'boss_transform', None
        if self.boss.defeated:
            return self._after_defeat(player)

        # contato de inimigos comuns com o jogador
        for enemy in self.enemies:
            if enemy.rect.colliderect(player.rect):
                push = -1 if player.rect.centerx < enemy.rect.centerx else 1
                player.take_damage(enemy.contact_damage, knockback=(push * -6, -6))

        # ataques do chefe contra o jogador
        if self.boss.active and self.boss.alive:
            for rect, dmg in self.boss.get_all_hit_rects():
                if rect.colliderect(player.rect):
                    push = -1 if player.rect.centerx < self.boss.rect.centerx else 1
                    player.take_damage(dmg, knockback=(push * -6, -7))

        # projéteis do chefe contra as plataformas já tratados em Boss.update

        # coleta de power-up (somente mapas antigos possuem recompensas)
        self._collect_powerups(player)
        return self._check_transition(player)

    def finish_boss_dialogue(self):
        if self.encounter_pending:
            self.infected = True
            self.encounter_pending = False
            self.boss.activate()

    def _after_defeat(self, player):
        self.camera.update(player.rect)
        if self.boss.defeated and not self.boss_defeated_dialogue_played:
            self.boss_defeated_dialogue_played = True
            self.boss.projectiles.empty()
            if self.data.get('clear_encounter_on_defeat'):
                self.enemies.empty()
                player.projectiles.empty()
            if self.data["ability_reward"] is not None:
                pu = PowerUp(self.boss.rect.centerx, self.boss.rect.centery, self.data["ability_reward"])
                self.powerups.add(pu)
            return ("dialogue", self.data["victory_dialogue"])
        self.powerups.update()
        self._collect_powerups(player)
        return self._check_transition(player)

    def _collect_powerups(self, player):
        for pu in list(self.powerups):
            if pu.rect.colliderect(player.rect):
                player.grant_ability(pu.ability)
                pu.kill()

    def _check_transition(self, player):
        # saída da fase (só habilitada após derrotar o chefe)
        if self.boss.defeated and self.tilemap.exit_trigger:
            if player.rect.colliderect(self.tilemap.exit_trigger):
                self.completed = True
                return ("level_complete", None)

        # queda para fora do mapa -> respawn
        if player.rect.top > self.tilemap.height + 200:
            return ("fell", None)

        return (None, None)

    # ------------------------------------------------------------------
    def draw(self, surface):
        surface.fill(settings.BG_COLOR)
        if self.school_scene:
            self.school_scene.draw_background(surface, self.camera)
        else:
            self._draw_parallax(surface)

        for rect in self.tilemap.solids:
            r = self.camera.apply(rect)
            if r.colliderect(surface.get_rect()):
                if self.school_scene:
                    self.school_scene.draw_block(surface, rect, self.camera, self.tilemap.width)
                else:
                    surface.blit(self.ground_img, r)

        for rect in self.tilemap.hazards:
            # o retângulo de dano é só a metade inferior do bloco; a imagem
            # do espinho ocupa o bloco inteiro (ponta encostando no topo)
            tile_rect = pygame.Rect(rect.x, rect.y - TS // 2, TS, TS)
            r = self.camera.apply(tile_rect)
            surface.blit(self.spike_img, r)

        if self.tilemap.exit_trigger:
            if self.school_scene:
                self.school_scene.draw_exit(surface, self.tilemap.exit_trigger, self.camera, self.boss.defeated)
            else:
                r = self.camera.apply(self.tilemap.exit_trigger)
                color = settings.EXIT_COLOR if self.boss.defeated else settings.GATE_COLOR
                pygame.draw.rect(surface, color, r, border_radius=6)
                pygame.draw.rect(surface, settings.WHITE, r, 2, border_radius=6)

        for enemy in self.enemies:
            enemy.draw(surface, self.camera)

        for pu in self.powerups:
            pu.draw(surface, self.camera)

        if self.infected:
            self.boss.draw(surface, self.camera)
        else:
            self.human_teacher.draw(surface, self.camera)
            name = self.encounter_font.render('Professor Romerito', True, settings.TEXT_COLOR)
            rect = self.camera.apply(self.human_teacher.rect)
            surface.blit(name, name.get_rect(midbottom=(rect.centerx, rect.top-6)))

    def draw_infection(self, surface, progress):
        rect = self.camera.apply(self.boss.rect)
        bug = self.infection_bug
        x = rect.centerx-bug.get_width()//2 + 90*(1-min(1, progress*2))
        if progress < 0.5:
            surface.blit(bug, (round(x), rect.top))
        radius = 20+int(30*progress)
        pygame.draw.circle(surface, (142, 230, 128), rect.center, radius, 2)
        text = self.infection_font.render('Romerito está se transformando em RomerBug!', True, (206, 246, 164))
        surface.blit(text, text.get_rect(center=(settings.SCREEN_WIDTH//2, 180)))

    def _draw_parallax(self, surface):
        for i in range(6):
            x = (i * 220 - int(self.camera.offset.x * 0.3)) % (settings.SCREEN_WIDTH + 220) - 110
            surface.blit(self.bg_panel_img, (x, 60))
