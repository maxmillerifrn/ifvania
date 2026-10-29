"""Classe do personagem principal: o aluno.

Implementa física de plataforma (movimento, pulo, gravidade), um sistema
de habilidades progressivas (metroidvania) e combate simples. Herda de
`Personagem` (posição, vida, gravidade e colisão com o cenário) e adiciona
tudo que é específico do aluno: habilidades, dash, tiro, escudo e ataque
corpo a corpo.
"""
import pygame
import configuracoes
import recursos
from entidades.personagem import Personagem
from habilidades import Habilidade
from entidades.projetil import Projetil
from entidades.chicote_mouse import ChicoteMouse


class Jogador(Personagem):
    ESCALA_VISUAL = configuracoes.ESCALA_VISUAL_PERSONAGEM
    # imagens carregadas uma única vez e compartilhadas por todas as instâncias
    _FIGURAS = {}
    PERSONAGENS = {"boy": "Menino", 'menina': "Menina"}

    # quantos quadros de jogo cada estado de animação segura antes de avançar
    # para o próximo quadro (menor = mais rápido)
    _VELOCIDADE_ANIMACAO = {"idle": 22, "jump": 1, "dash": 1}

    @classmethod
    def _load_sprites(cls, personagem="boy"):
        if personagem not in cls.PERSONAGENS:
            raise ValueError(f"Personagem desconhecido: {personagem}")
        chave_cache = (personagem, configuracoes.TAMANHO_PERSONAGEM)
        if chave_cache not in cls._FIGURAS:
            uniforme = (36, 112, 76)
            pasta = 'jogador' if personagem == "boy" else "jogador/menina"
            caminhos = [f"{pasta}/repouso_{i}.png" for i in range(2)]
            caminhos += [f"{pasta}/ciclo_caminhada/caminhada_{i}.png" for i in range(8)]
            caminhos += [f"{pasta}/salto.png", f"{pasta}/arrancada.png"]
            caminhos += [f"{pasta}/ataque_{i}.png" for i in range(3)]
            quadros = recursos.load_character_frames(caminhos, uniforme)
            espelhado = [pygame.transform.flip(quadro, True, False) for quadro in quadros]
            figuras = {
                "attack_r": quadros[12:],
                "attack_l": espelhado[12:],
            }
            for sufixo, sequencia in (("_r", quadros), ("_l", espelhado)):
                figuras.update({
                    "idle" + sufixo: sequencia[:2],
                    "walk" + sufixo: sequencia[2:10],
                    "jump" + sufixo: sequencia[10],
                    "dash" + sufixo: sequencia[11],
                })
            cls._FIGURAS[chave_cache] = figuras
        return cls._FIGURAS[chave_cache]

    def __init__(self, x, y, personagem="boy", nome=None):
        super().__init__(x, y, *configuracoes.TAMANHO_PERSONAGEM, vida=6)
        self.personagem = personagem
        self.nome = nome or ('Aluna' if personagem == 'menina' else 'Aluno')
        self.figuras = self._load_sprites(personagem)

        # Animação (estado atual: idle/walk/jump/dash + quadro dentro dele)
        self.estado_animacao = "idle"
        self.quadro_animacao = 0
        self.temporizador_animacao = 0
        self.distancia_caminhada = 0.0
        self.deslocamento_x = 0.0
        self.direcao_animacao = 1
        self.image = self.figuras["idle_r"][0]

        # Estado físico
        self.no_chao = False
        self.na_parede = 0          # -1 esquerda, 1 direita, 0 nenhuma
        self.direcao_olhar = 1
        self.saltos_usados = 0

        # Combate
        self.temporizador_invulnerabilidade = 0
        self.espera_ataque = 0
        self.temporizador_golpe = 0
        self.chicote = ChicoteMouse()
        self.chicote_desbloqueado = True  # Fases de combate antigas; o prólogo bloqueia a arma.
        self._solidos = ()
        self.pausa_impacto = 0
        self.carregando = False
        self.carga = 0
        self.aguardando_soltar = False
        self.ataque_pendente = 0
        self.memoria_ataque = 0
        self.memoria_salto = 0
        self.tolerancia_borda = 0
        self.temporizador_recuo = 0
        self.temporizador_esquiva = 0
        self.espera_esquiva = 0
        self.direcao_esquiva = 1
        self.carga_sinalizada = False

        # Timers de habilidades
        self.temporizador_arrancada = 0
        self.espera_arrancada = 0
        self.espera_disparo = 0
        self.escudo_ativo = False
        self.espera_escudo = 0

        # Habilidades adquiridas (metroidvania core)
        self.habilidades = set()

        # Progresso da história
        self.chefes_derrotados = set()

        self.projeteis = pygame.sprite.Group()

    # ------------------------------------------------------------------
    # Habilidades
    # ------------------------------------------------------------------
    def has(self, habilidade: Habilidade) -> bool:
        return habilidade in self.habilidades

    def grant_ability(self, habilidade: Habilidade):
        self.habilidades.add(habilidade)
        if habilidade != Habilidade.ESCUDO:
            self.vida_maxima += 1
        self.vida = self.vida_maxima

    # ------------------------------------------------------------------
    # Entrada / atualização
    # ------------------------------------------------------------------
    def handle_input(self, teclas, eventos):
        movimento = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            movimento -= 1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            movimento += 1

        if self.temporizador_esquiva > 0:
            self.velocidade.x = self.direcao_esquiva * configuracoes.VELOCIDADE_ESQUIVA
        elif self.temporizador_arrancada <= 0 and self.temporizador_recuo <= 0:
            limite = configuracoes.VELOCIDADE_JOGADOR * (0.75 if self.carregando else 1)
            alvo = movimento * limite
            aceleracao = (configuracoes.ACELERACAO_JOGADOR if self.no_chao
                          else configuracoes.ACELERACAO_AEREA)
            if movimento == 0 or alvo * self.velocidade.x < 0:
                aceleracao = configuracoes.FRENAGEM_JOGADOR
            self.velocidade.x += max(-aceleracao, min(aceleracao, alvo-self.velocidade.x))
            if movimento != 0:
                self.direcao_olhar = movimento

        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                    self.memoria_salto = configuracoes.TOLERANCIA_SALTO
                    self._try_jump()
                elif evento.key == pygame.K_LSHIFT:
                    if self.has(Habilidade.ARRANCADA):
                        self._try_dash()
                    elif self.chicote_desbloqueado:
                        self.tentar_esquiva()
                elif evento.key == pygame.K_f and self.has(Habilidade.DISPARO_DISTANCIA):
                    self._try_shoot()
                elif evento.key == pygame.K_q and self.has(Habilidade.ESCUDO):
                    self._toggle_shield()
                elif evento.key == pygame.K_x and not getattr(evento, 'repeat', False):
                    if (self.chicote_desbloqueado and not self.aguardando_soltar
                            and self.temporizador_esquiva == 0 and self.temporizador_golpe == 0
                            and self.espera_ataque <= 6):
                        self.carregando = True
                        self.aguardando_soltar = True
                        self.carga = 0
                        self.carga_sinalizada = False
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_x:
                if self.carregando:
                    self.ataque_pendente = 2 if self.carga >= configuracoes.TEMPO_CARGA else 1
                    self.memoria_ataque = 6
                    self.carregando = False
                    self._try_melee(self.ataque_pendente)
                self.aguardando_soltar = False

    def cancelar_entrada(self):
        self.carregando = False
        self.carga = 0
        self.ataque_pendente = self.memoria_ataque = 0
        self.memoria_salto = 0
        self.aguardando_soltar = False

    def cancelar_combate(self):
        self.cancelar_entrada()
        self.pausa_impacto = 0
        self.temporizador_golpe = 0
        self.temporizador_esquiva = 0
        self.chicote.alvos_atingidos.clear()
        self.chicote.limpar_trajetoria()
        # Um novo KEYDOWN físico é necessário após qualquer interrupção.
        self.aguardando_soltar = False

    def tentar_esquiva(self):
        if (not self.chicote_desbloqueado or self.espera_esquiva > 0
                or self.temporizador_recuo > 0
                or (self.temporizador_golpe > 0 and self.chicote.age(self) < self.chicote.FIM_GOLPE)):
            return
        self.cancelar_combate()
        self.direcao_esquiva = self.direcao_olhar
        self.temporizador_esquiva = configuracoes.DURACAO_ESQUIVA
        self.espera_esquiva = configuracoes.ESPERA_ESQUIVA
        self.velocidade.x = self.direcao_esquiva * configuracoes.VELOCIDADE_ESQUIVA

    def _try_jump(self):
        if self.no_chao or self.tolerancia_borda > 0:
            self.velocidade.y = configuracoes.FORCA_SALTO_JOGADOR
            self.no_chao = False
            self.saltos_usados = 1
            self.tolerancia_borda = self.memoria_salto = 0
        elif self.na_parede != 0 and self.has(Habilidade.ESCALADA_PAREDE):
            self.velocidade.y = configuracoes.SALTO_PAREDE_Y
            self.velocidade.x = -self.na_parede * configuracoes.SALTO_PAREDE_X
            self.na_parede = 0
            self.memoria_salto = 0
            self.saltos_usados = 1
        elif self.has(Habilidade.SALTO_DUPLO) and self.saltos_usados < 2:
            self.velocidade.y = configuracoes.FORCA_SALTO_DUPLO
            self.saltos_usados += 1
            self.memoria_salto = 0

    def _try_dash(self):
        if self.espera_arrancada <= 0:
            self.temporizador_arrancada = configuracoes.DURACAO_ARRANCADA
            self.espera_arrancada = configuracoes.ESPERA_ARRANCADA
            self.velocidade.x = configuracoes.VELOCIDADE_ARRANCADA * self.direcao_olhar
            self.velocidade.y = 0

    def _try_shoot(self):
        if self.espera_disparo <= 0:
            direcao = (self.direcao_olhar, 0)
            origem = (self.rect.centerx + self.direcao_olhar * 20, self.rect.centery - 4)
            self.projeteis.add(Projetil(*origem, direcao, dono='jogador'))
            self.espera_disparo = configuracoes.ESPERA_DISPARO

    def _toggle_shield(self):
        if self.espera_escudo <= 0:
            self.escudo_ativo = not self.escudo_ativo

    def _try_melee(self, dano=1):
        if self.chicote_desbloqueado and self.espera_ataque <= 0 and self.temporizador_esquiva == 0:
            self.espera_ataque = configuracoes.ESPERA_ATAQUE
            self.temporizador_golpe = self.chicote.DURACAO
            self.chicote.start(self.direcao_olhar, dano)
            self.ataque_pendente = self.memoria_ataque = 0
            self.carga = 0

    def get_melee_rect(self):
        return self.chicote.hit_bounds(self, self._solidos)

    def try_melee_hit(self, alvo, solidos):
        return self.chicote.try_hit(self, alvo, solidos)

    def update(self, solidos, perigos):
        self._solidos = solidos
        if self.carregando and self.espera_ataque <= 0:
            self.carga = min(configuracoes.TEMPO_CARGA, self.carga + 1)
            if self.carga == configuracoes.TEMPO_CARGA and not self.carga_sinalizada:
                from sons import tocar
                tocar('carga')
                self.carga_sinalizada = True
        self.temporizador_recuo = max(0, self.temporizador_recuo-1)
        self.temporizador_esquiva = max(0, self.temporizador_esquiva-1)
        self.espera_esquiva = max(0, self.espera_esquiva-1)
        if self.no_chao:
            self.tolerancia_borda = configuracoes.TOLERANCIA_SALTO
        else:
            self.tolerancia_borda = max(0, self.tolerancia_borda-1)
        if self.memoria_salto > 0:
            self._try_jump()
            self.memoria_salto = max(0, self.memoria_salto-1)
        # timers
        if self.temporizador_arrancada > 0:
            self.temporizador_arrancada -= 1
        if self.espera_arrancada > 0:
            self.espera_arrancada -= 1
        if self.espera_disparo > 0:
            self.espera_disparo -= 1
        if self.espera_ataque > 0:
            self.espera_ataque -= 1
        if self.temporizador_golpe > 0:
            self.temporizador_golpe -= 1
        if self.temporizador_invulnerabilidade > 0:
            self.temporizador_invulnerabilidade -= 1
        if self.ataque_pendente:
            self._try_melee(self.ataque_pendente)
            self.memoria_ataque = max(0, self.memoria_ataque-1)
            if self.memoria_ataque == 0:
                self.ataque_pendente = 0
        if self.escudo_ativo:
            self.espera_escudo = 10
        elif self.espera_escudo > 0:
            self.espera_escudo -= 1

        # gravidade / wall slide
        if self.temporizador_arrancada <= 0:
            if self.na_parede != 0 and self.has(Habilidade.ESCALADA_PAREDE) and self.velocidade.y > 0:
                self.velocidade.y = min(self.velocidade.y + configuracoes.GRAVIDADE * 0.3, configuracoes.VELOCIDADE_DESLIZAMENTO_PAREDE)
            else:
                self.apply_gravity()

        x_anterior = self.rect.x
        self._move_and_collide(solidos)
        self.deslocamento_x = abs(self.rect.x-x_anterior)

        # dano por espinhos
        for perigo in perigos:
            if self.rect.colliderect(perigo):
                self.take_damage(1, recuo=(-self.direcao_olhar * 6, -6))

        self.projeteis.update(solidos)
        self._animate()

    def _move_and_collide(self, solidos):
        self.na_parede = self.move_and_collide_x(solidos)
        if self.na_parede != 0 and self.temporizador_arrancada > 0:
            self.velocidade.x = 0

        self.no_chao = self.move_and_collide_y(solidos)
        if self.no_chao:
            self.saltos_usados = 0

    def take_damage(self, quantidade, recuo=(0, 0)):
        if (self.temporizador_invulnerabilidade > 0 or not self.vivo
                or 4 <= self.temporizador_esquiva <= 11):
            return
        if self.escudo_ativo:
            self.escudo_ativo = False
            self.espera_escudo = 60
            self.temporizador_invulnerabilidade = 30
            return
        self.cancelar_combate()
        super().take_damage(quantidade)
        self.temporizador_recuo = 8
        self.temporizador_invulnerabilidade = configuracoes.TEMPO_INVULNERABILIDADE
        self.velocidade.x, self.velocidade.y = recuo

    def respawn(self, x, y):
        self.cancelar_combate()
        self.temporizador_recuo = self.espera_esquiva = self.tolerancia_borda = 0
        self.posicao = pygame.Vector2(x, y)
        self.rect.topleft = (x, y)
        self.velocidade = pygame.Vector2(0, 0)
        self.vida = self.vida_maxima
        self.vivo = True
        self.temporizador_invulnerabilidade = 60
        self.temporizador_golpe = 0
        self.espera_ataque = 0
        self.chicote.alvos_atingidos.clear()
        self.distancia_caminhada = 0.0
        self.deslocamento_x = 0.0
        self.estado_animacao = 'idle'
        self.quadro_animacao = self.temporizador_animacao = 0
        self.na_parede = self.saltos_usados = 0
        self.no_chao = False
        self.image = self.figuras['idle_r' if self.direcao_olhar > 0 else 'idle_l'][0]

    # ------------------------------------------------------------------
    # Desenho (sprites carregados de recursos/imagens/jogador/)
    # ------------------------------------------------------------------
    def _animate(self):
        """Escolhe o estado de animação (ataque > dash > pulo > andar > parado) e
        sincroniza os passos ao deslocamento real; repouso usa temporizador."""
        if self.carregando:
            self.estado_animacao = 'charge'
            self.image = self.figuras['attack_r' if self.direcao_olhar > 0 else 'attack_l'][0]
            return
        if self.temporizador_esquiva > 0:
            self.estado_animacao = 'dodge'
            self.image = self.figuras['dash_r' if self.direcao_esquiva > 0 else 'dash_l']
            return
        if self.temporizador_golpe > 0:
            self.estado_animacao = "attack"
            self.quadro_animacao = self.chicote.pose(self)
            sufixo = "_r" if self.chicote.direcao_olhar > 0 else "_l"
            self.image = self.figuras["attack" + sufixo][self.quadro_animacao]
            return
        if self.temporizador_arrancada > 0:
            estado = "dash"
        elif not self.no_chao:
            estado = "jump"
        elif self.deslocamento_x > 0.01:
            estado = "walk"
        else:
            estado = "idle"

        if estado != self.estado_animacao:
            self.estado_animacao = estado
            self.quadro_animacao = 0
            self.temporizador_animacao = 0
            self.distancia_caminhada = 0.0

        if self.direcao_olhar != self.direcao_animacao:
            self.distancia_caminhada = 0.0
            self.direcao_animacao = self.direcao_olhar

        sufixo = "_r" if self.direcao_olhar > 0 else "_l"
        figura = self.figuras[estado + sufixo]
        if estado == 'walk':
            self.distancia_caminhada += self.deslocamento_x
            distancia_passo = 6*self.ESCALA_VISUAL
            self.quadro_animacao = int(self.distancia_caminhada/distancia_passo) % len(figura)
            self.image = figura[self.quadro_animacao]
            return
        if isinstance(figura, list):
            self.temporizador_animacao += 1
            if self.temporizador_animacao >= self._VELOCIDADE_ANIMACAO[estado]:
                self.temporizador_animacao = 0
                self.quadro_animacao = (self.quadro_animacao + 1) % len(figura)
            self.image = figura[self.quadro_animacao]
        else:
            self.image = figura

    def draw(self, superficie, camera):
        piscando = self.temporizador_invulnerabilidade > 0 and (self.temporizador_invulnerabilidade // 4) % 2 == 0
        destino = camera.apply(self.rect)
        if not piscando:
            imagem = self.get_draw_image()
            superficie.blit(imagem, imagem.get_rect(midbottom=destino.midbottom))
        if self.carregando:
            self.chicote.desenhar_carga(superficie, camera, self)
        if self.temporizador_esquiva > 0:
            pygame.draw.line(superficie, (136, 159, 163),
                             (destino.centerx-self.direcao_esquiva*34, destino.centery), destino.center, 2)
        if self.temporizador_golpe > 0:
            self.chicote.draw(superficie, camera, self, self._solidos)
        if self.escudo_ativo:
            pygame.draw.circle(superficie, (120, 220, 255), destino.center, self.largura, 2)
        for projetil in self.projeteis:
            projetil.draw(superficie, camera)
