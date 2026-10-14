"""Classe Level: liga tilemap, inimigos, chefe, powerup e câmera numa fase jogável."""
import pygame
import settings
import assets
from world.tilemap import TileMap
from world.camera import Camera
from entities.enemy import Enemy
from entities.boss import Boss
from entities.romer_bug import RomerBug
from powerups import PowerUp

TS = settings.TILE_SIZE


class Level:
    def __init__(self, level_data):
        self.data = level_data
        self.name = level_data["name"]
        self.tilemap = TileMap(level_data["ascii_map"])
        self.camera = Camera(self.tilemap.width, self.tilemap.height)

        self.enemies = pygame.sprite.Group()
        for (ex, ey) in self.tilemap.enemy_spawns:
            self.enemies.add(Enemy(ex, ey - 8))

        boss_def = level_data["boss"]
        bx, by = self.tilemap.boss_spawn
        boss_class = RomerBug if boss_def.get("boss_type") == "romerbug" else Boss
        options = {}
        if boss_class is RomerBug:
            options["arena"] = pygame.Rect(TS, TS, self.tilemap.width - 2 * TS,
                                            self.tilemap.height - 2 * TS)
        self.boss = boss_class(bx, by, boss_def["name"], boss_def["subject"],
                          boss_def["color"], health=boss_def["health"],
                          sprite_file=boss_def.get("sprite_file"), **options)

        self.powerups = pygame.sprite.Group()
        self.spawned_powerup = False

        self.dialogue_played = False
        self.boss_defeated_dialogue_played = False
        self.completed = False
        self.player_spawn = self.tilemap.player_spawn

        # sprites do cenário (carregados/cacheados uma vez em assets.py)
        self.ground_img = assets.load_image("tiles/ground.png", (TS, TS), settings.GROUND_COLOR)
        self.spike_img = assets.load_image("tiles/spike.png", (TS, TS), settings.SPIKE_COLOR)
        self.bg_panel_img = assets.load_image("background/panel.png", (90, 220), settings.BG_COLOR_2)

    # ------------------------------------------------------------------
    def update(self, player, dt_events):
        # Abre o encontro antes de processar ataques: entrar pulando ou já
        # além da entrada também ativa o chefe, sem dano antes do diálogo.
        if not self.dialogue_played and self.tilemap.dialogue_trigger:
            if player.rect.colliderect(self.tilemap.dialogue_trigger):
                self.dialogue_played = True
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

        # diálogo de vitória + drop de habilidade quando o chefe morre
        if self.boss.defeated and not self.boss_defeated_dialogue_played:
            self.boss_defeated_dialogue_played = True
            if self.data["ability_reward"] is not None:
                pu = PowerUp(self.boss.rect.centerx, self.boss.rect.centery, self.data["ability_reward"])
                self.powerups.add(pu)
            return ("dialogue", self.data["victory_dialogue"])

        # coleta de power-up
        for pu in list(self.powerups):
            if pu.rect.colliderect(player.rect):
                player.grant_ability(pu.ability)
                pu.kill()

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
        self._draw_parallax(surface)

        for rect in self.tilemap.solids:
            r = self.camera.apply(rect)
            if r.colliderect(surface.get_rect()):
                surface.blit(self.ground_img, r)

        for rect in self.tilemap.hazards:
            # o retângulo de dano é só a metade inferior do bloco; a imagem
            # do espinho ocupa o bloco inteiro (ponta encostando no topo)
            tile_rect = pygame.Rect(rect.x, rect.y - TS // 2, TS, TS)
            r = self.camera.apply(tile_rect)
            surface.blit(self.spike_img, r)

        if self.tilemap.exit_trigger:
            r = self.camera.apply(self.tilemap.exit_trigger)
            color = settings.EXIT_COLOR if self.boss.defeated else settings.GATE_COLOR
            pygame.draw.rect(surface, color, r, border_radius=6)
            pygame.draw.rect(surface, settings.WHITE, r, 2, border_radius=6)

        for enemy in self.enemies:
            enemy.draw(surface, self.camera)

        for pu in self.powerups:
            pu.draw(surface, self.camera)

        self.boss.draw(surface, self.camera)

    def _draw_parallax(self, surface):
        for i in range(6):
            x = (i * 220 - int(self.camera.offset.x * 0.3)) % (settings.SCREEN_WIDTH + 220) - 110
            surface.blit(self.bg_panel_img, (x, 60))
