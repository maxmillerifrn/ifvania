"""Classe do personagem principal: o aluno.

Implementa física de plataforma (movimento, pulo, gravidade), um sistema
de habilidades progressivas (metroidvania) e combate simples. Herda de
`Character` (posição, vida, gravidade e colisão com o cenário) e adiciona
tudo que é específico do aluno: habilidades, dash, tiro, escudo e ataque
corpo a corpo.
"""
import pygame
import settings
import assets
from entities.character import Character
from powerups import Ability
from entities.projectile import Projectile
from entities.mouse_whip import MouseWhip


class Player(Character):
    VISUAL_SCALE = settings.CHARACTER_VISUAL_SCALE
    # imagens carregadas uma única vez e compartilhadas por todas as instâncias
    _SPRITES = {}
    CHARACTERS = {"boy": "Menino", "girl": "Menina"}

    # quantos quadros de jogo cada estado de animação segura antes de avançar
    # para o próximo quadro (menor = mais rápido)
    _ANIM_SPEED = {"idle": 22, "jump": 1, "dash": 1}

    @classmethod
    def _load_sprites(cls, character="boy"):
        if character not in cls.CHARACTERS:
            raise ValueError(f"Personagem desconhecido: {character}")
        cache_key = (character, settings.CHARACTER_SIZE)
        if cache_key not in cls._SPRITES:
            uniform = (36, 112, 76)
            folder = "player" if character == "boy" else "player/girl"
            paths = [f"{folder}/idle_{i}.png" for i in range(2)]
            paths += [f"{folder}/walk_cycle/walk_{i}.png" for i in range(8)]
            paths += [f"{folder}/jump.png", f"{folder}/dash.png"]
            paths += [f"{folder}/attack_{i}.png" for i in range(3)]
            frames = assets.load_character_frames(paths, uniform)
            flipped = [pygame.transform.flip(frame, True, False) for frame in frames]
            sprites = {
                "attack_r": frames[12:],
                "attack_l": flipped[12:],
            }
            for suffix, sequence in (("_r", frames), ("_l", flipped)):
                sprites.update({
                    "idle" + suffix: sequence[:2],
                    "walk" + suffix: sequence[2:10],
                    "jump" + suffix: sequence[10],
                    "dash" + suffix: sequence[11],
                })
            cls._SPRITES[cache_key] = sprites
        return cls._SPRITES[cache_key]

    def __init__(self, x, y, character="boy", name=None):
        super().__init__(x, y, *settings.CHARACTER_SIZE, health=6)
        self.character = character
        self.name = name or ('Aluna' if character == 'girl' else 'Aluno')
        self.sprites = self._load_sprites(character)

        # Animação (estado atual: idle/walk/jump/dash + quadro dentro dele)
        self.anim_state = "idle"
        self.anim_frame = 0
        self.anim_timer = 0
        self.walk_distance = 0.0
        self.moved_x = 0.0
        self.animation_facing = 1
        self.image = self.sprites["idle_r"][0]

        # Estado físico
        self.on_ground = False
        self.on_wall = 0          # -1 esquerda, 1 direita, 0 nenhuma
        self.facing = 1
        self.jumps_used = 0

        # Combate
        self.invuln_timer = 0
        self.attack_cooldown = 0
        self.attacking_timer = 0
        self.whip = MouseWhip()
        self.whip_unlocked = True  # Fases de combate antigas; o prólogo bloqueia a arma.
        self._solids = ()

        # Timers de habilidades
        self.dash_timer = 0
        self.dash_cooldown_timer = 0
        self.shot_cooldown = 0
        self.shield_active = False
        self.shield_cooldown = 0

        # Habilidades adquiridas (metroidvania core)
        self.abilities = set()

        # Progresso da história
        self.defeated_bosses = set()

        self.projectiles = pygame.sprite.Group()

    # ------------------------------------------------------------------
    # Habilidades
    # ------------------------------------------------------------------
    def has(self, ability: Ability) -> bool:
        return ability in self.abilities

    def grant_ability(self, ability: Ability):
        self.abilities.add(ability)
        if ability != Ability.SHIELD:
            self.max_health += 1
        self.health = self.max_health

    # ------------------------------------------------------------------
    # Entrada / atualização
    # ------------------------------------------------------------------
    def handle_input(self, keys, events):
        move = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move += 1

        if self.dash_timer <= 0:
            self.vel.x = move * settings.PLAYER_SPEED
            if move != 0:
                self.facing = move

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                    self._try_jump()
                elif event.key == pygame.K_LSHIFT and self.has(Ability.DASH):
                    self._try_dash()
                elif event.key == pygame.K_f and self.has(Ability.RANGED_SHOT):
                    self._try_shoot()
                elif event.key == pygame.K_q and self.has(Ability.SHIELD):
                    self._toggle_shield()
                elif event.key == pygame.K_x:
                    self._try_melee()

    def _try_jump(self):
        if self.on_ground:
            self.vel.y = settings.PLAYER_JUMP_STRENGTH
            self.on_ground = False
            self.jumps_used = 1
        elif self.on_wall != 0 and self.has(Ability.WALL_CLIMB):
            self.vel.y = settings.WALL_JUMP_Y
            self.vel.x = -self.on_wall * settings.WALL_JUMP_X
            self.on_wall = 0
            self.jumps_used = 1
        elif self.has(Ability.DOUBLE_JUMP) and self.jumps_used < 2:
            self.vel.y = settings.DOUBLE_JUMP_STRENGTH
            self.jumps_used += 1

    def _try_dash(self):
        if self.dash_cooldown_timer <= 0:
            self.dash_timer = settings.DASH_DURATION
            self.dash_cooldown_timer = settings.DASH_COOLDOWN
            self.vel.x = settings.DASH_SPEED * self.facing
            self.vel.y = 0

    def _try_shoot(self):
        if self.shot_cooldown <= 0:
            direction = (self.facing, 0)
            origin = (self.rect.centerx + self.facing * 20, self.rect.centery - 4)
            self.projectiles.add(Projectile(*origin, direction, owner="player"))
            self.shot_cooldown = settings.SHOT_COOLDOWN

    def _toggle_shield(self):
        if self.shield_cooldown <= 0:
            self.shield_active = not self.shield_active

    def _try_melee(self):
        if self.whip_unlocked and self.attack_cooldown <= 0:
            self.attack_cooldown = settings.ATTACK_COOLDOWN
            self.attacking_timer = self.whip.DURATION
            self.whip.start(self.facing)

    def get_melee_rect(self):
        return self.whip.hit_bounds(self, self._solids)

    def try_melee_hit(self, target, solids):
        return self.whip.try_hit(self, target, solids)

    def update(self, solids, hazards):
        self._solids = solids
        # timers
        if self.dash_timer > 0:
            self.dash_timer -= 1
        if self.dash_cooldown_timer > 0:
            self.dash_cooldown_timer -= 1
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.attacking_timer > 0:
            self.attacking_timer -= 1
        if self.invuln_timer > 0:
            self.invuln_timer -= 1
        if self.shield_active:
            self.shield_cooldown = 10
        elif self.shield_cooldown > 0:
            self.shield_cooldown -= 1

        # gravidade / wall slide
        if self.dash_timer <= 0:
            if self.on_wall != 0 and self.has(Ability.WALL_CLIMB) and self.vel.y > 0:
                self.vel.y = min(self.vel.y + settings.GRAVITY * 0.3, settings.WALL_SLIDE_SPEED)
            else:
                self.apply_gravity()

        previous_x = self.rect.x
        self._move_and_collide(solids)
        self.moved_x = abs(self.rect.x-previous_x)

        # dano por espinhos
        for hz in hazards:
            if self.rect.colliderect(hz):
                self.take_damage(1, knockback=(-self.facing * 6, -6))

        self.projectiles.update(solids)
        self._animate()

    def _move_and_collide(self, solids):
        self.on_wall = self.move_and_collide_x(solids)
        if self.on_wall != 0 and self.dash_timer > 0:
            self.vel.x = 0

        self.on_ground = self.move_and_collide_y(solids)
        if self.on_ground:
            self.jumps_used = 0

    def take_damage(self, amount, knockback=(0, 0)):
        if self.invuln_timer > 0 or not self.alive:
            return
        if self.shield_active:
            self.shield_active = False
            self.shield_cooldown = 60
            self.invuln_timer = 30
            return
        super().take_damage(amount)
        self.invuln_timer = settings.INVULN_TIME
        self.vel.x, self.vel.y = knockback

    def respawn(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.rect.topleft = (x, y)
        self.vel = pygame.Vector2(0, 0)
        self.health = self.max_health
        self.alive = True
        self.invuln_timer = 60
        self.attacking_timer = 0
        self.attack_cooldown = 0
        self.whip.hit_targets.clear()
        self.walk_distance = 0.0
        self.moved_x = 0.0
        self.anim_state = 'idle'
        self.anim_frame = self.anim_timer = 0
        self.on_wall = self.jumps_used = 0
        self.on_ground = False
        self.image = self.sprites['idle_r' if self.facing > 0 else 'idle_l'][0]

    # ------------------------------------------------------------------
    # Desenho (sprites carregados de assets/images/player/)
    # ------------------------------------------------------------------
    def _animate(self):
        """Escolhe o estado de animação (ataque > dash > pulo > andar > parado) e
        sincroniza os passos ao deslocamento real; repouso usa temporizador."""
        if self.attacking_timer > 0:
            self.anim_state = "attack"
            self.anim_frame = self.whip.pose(self)
            suffix = "_r" if self.whip.facing > 0 else "_l"
            self.image = self.sprites["attack" + suffix][self.anim_frame]
            return
        if self.dash_timer > 0:
            state = "dash"
        elif not self.on_ground:
            state = "jump"
        elif self.moved_x > 0.01:
            state = "walk"
        else:
            state = "idle"

        if state != self.anim_state:
            self.anim_state = state
            self.anim_frame = 0
            self.anim_timer = 0
            self.walk_distance = 0.0

        if self.facing != self.animation_facing:
            self.walk_distance = 0.0
            self.animation_facing = self.facing

        suffix = "_r" if self.facing > 0 else "_l"
        sprite = self.sprites[state + suffix]
        if state == 'walk':
            self.walk_distance += self.moved_x
            step_distance = 6*self.VISUAL_SCALE
            self.anim_frame = int(self.walk_distance/step_distance) % len(sprite)
            self.image = sprite[self.anim_frame]
            return
        if isinstance(sprite, list):
            self.anim_timer += 1
            if self.anim_timer >= self._ANIM_SPEED[state]:
                self.anim_timer = 0
                self.anim_frame = (self.anim_frame + 1) % len(sprite)
            self.image = sprite[self.anim_frame]
        else:
            self.image = sprite

    def draw(self, surface, camera):
        blink = self.invuln_timer > 0 and (self.invuln_timer // 4) % 2 == 0
        dest = camera.apply(self.rect)
        if not blink:
            image = self.get_draw_image()
            surface.blit(image, image.get_rect(midbottom=dest.midbottom))
        if self.attacking_timer > 0:
            self.whip.draw(surface, camera, self, self._solids)
        if self.shield_active:
            pygame.draw.circle(surface, (120, 220, 255), dest.center, self.width, 2)
        for proj in self.projectiles:
            proj.draw(surface, camera)
