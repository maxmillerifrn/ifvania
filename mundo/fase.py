"""Classe Fase: liga tilemap, inimigos, chefe, powerup e câmera numa fase jogável."""
import pygame
import configuracoes
import recursos
from mundo.mapa_blocos import MapaBlocos
from mundo.camera import Camera
from entidades.inimigo import Inimigo
from entidades.chefes_professores import CLASSES_CHEFES
from entidades.romer_bug import RomerBug
from entidades.professor import Professor
from habilidades import ItemHabilidade
from mundo.escola_sombria import EscolaSombria

TB = configuracoes.TAMANHO_BLOCO


class Fase:
    def __init__(self, dados_fase):
        self.dados = dados_fase
        self.nome = dados_fase["name"]
        self.mapa_blocos = MapaBlocos(dados_fase["ascii_map"])
        self.camera = Camera(self.mapa_blocos.largura, self.mapa_blocos.altura)

        self.inimigos = pygame.sprite.Group()
        for (ex, ey) in self.mapa_blocos.surgimentos_inimigos:
            self.inimigos.add(Inimigo(*self._grounded_spawn(ex, ey)))

        definicao_chefe = dados_fase["boss"]
        bx, by = self.mapa_blocos.surgimento_chefe
        classe_chefe = CLASSES_CHEFES[definicao_chefe["boss_type"]]
        bx, by = self._grounded_spawn(bx, by)
        opcoes = {}
        if classe_chefe is RomerBug:
            opcoes['transformacao_cinematica'] = dados_fase.get('cinematic_transform', False)
            esquerda = dados_fase.get('arena_left', TB)
            opcoes["arena"] = pygame.Rect(esquerda, TB, self.mapa_blocos.largura - esquerda - TB,
                                            self.mapa_blocos.altura - 2 * TB)
        self.chefe = classe_chefe(bx, by, definicao_chefe["name"], definicao_chefe["subject"],
                          definicao_chefe["color"], vida=definicao_chefe["health"],
                          arquivo_figura=definicao_chefe.get("sprite_file"), **opcoes)

        self.itens_habilidades = pygame.sprite.Group()
        self.item_criado = False

        self.dialogo_exibido = False
        self.dialogo_derrota_exibido = False
        self.concluido = False
        self.surgimento_jogador = self._grounded_spawn(*self.mapa_blocos.surgimento_jogador)
        self.exige_infeccao = dados_fase.get('requires_infection', False)
        self.infectado = not self.exige_infeccao
        self.encontro_pendente = False
        self.professor_humano = Professor(bx, by, 'romerito') if self.exige_infeccao else None
        self.bug_infeccao = recursos.load_character_frames(['inimigos/bug_0.png'])[0] if self.exige_infeccao else None
        self.fonte_encontro = pygame.font.Font(None, 20)
        self.fonte_infeccao = pygame.font.Font(None, 24)
        self.cenario_escolar = (EscolaSombria(self.mapa_blocos.largura, self.mapa_blocos.altura,
                                       self.surgimento_jogador[1]+configuracoes.TAMANHO_PERSONAGEM[1])
                             if dados_fase.get('school_battle') else None)

        # sprites do cenário (carregados/cacheados uma vez em recursos.py)
        self.imagem_chao = recursos.load_image("blocos/chao.png", (TB, TB), configuracoes.COR_CHAO)
        self.imagem_espinho = recursos.load_image("blocos/espinho.png", (TB, TB), configuracoes.COR_ESPINHO)
        self.imagem_painel_fundo = recursos.load_image("cenarios/painel.png", (90, 220), configuracoes.COR_FUNDO_2)

    def _grounded_spawn(self, x, y):
        """Os marcadores do mapa indicam a coluna; os pés usam o piso abaixo."""
        largura, altura = configuracoes.TAMANHO_PERSONAGEM
        pisos = sorted({solido.top for solido in self.mapa_blocos.solidos
                         if solido.left < x + largura and solido.right > x
                         and solido.top >= y - altura},
                        key=lambda topo: abs(topo - (y + TB)))
        for piso in pisos:
            corpo = pygame.Rect(x, piso - altura, largura, altura)
            if not any(corpo.colliderect(solido) for solido in self.mapa_blocos.solidos):
                return corpo.topleft
        raise ValueError(f"Sem piso livre para personagem em {(x, y)}")

    # ------------------------------------------------------------------
    def update_visuals(self):
        if self.cenario_escolar:
            self.cenario_escolar.update()

    def update(self, jogador, eventos_quadro):
        if self.concluido or self.encontro_pendente:
            return None, None
        if getattr(self.chefe, 'cinematica_pendente', False):
            return 'boss_transform', None
        if self.chefe.derrotado:
            return self._after_defeat(jogador)
        # A entrada da arena abre a conversa antes de processar qualquer dano,
        # inclusive quando o jogador chega pulando ou além do primeiro bloco.
        if not self.dialogo_exibido and self.mapa_blocos.gatilho_dialogo:
            if jogador.rect.colliderect(self.mapa_blocos.gatilho_dialogo):
                self.dialogo_exibido = True
                if self.exige_infeccao:
                    self.encontro_pendente = True
                else:
                    self.chefe.activate()
                self.camera.update(jogador.rect)
                return ("dialogue", self.dados["boss_dialogue"])

        self.inimigos.update(self.mapa_blocos.solidos)
        self.chefe.update(jogador, self.mapa_blocos.solidos)
        self.itens_habilidades.update()
        self.camera.update(jogador.rect)

        # ataque corpo-a-corpo do jogador contra inimigos e chefe
        retangulo_golpe = jogador.get_melee_rect()
        if retangulo_golpe:
            for inimigo in list(self.inimigos):
                if retangulo_golpe.colliderect(jogador.chicote.area_alvo(inimigo)):
                    jogador.try_melee_hit(inimigo, self.mapa_blocos.solidos)
            if self.chefe.ativo and self.chefe.vivo and retangulo_golpe.colliderect(jogador.chicote.area_alvo(self.chefe)):
                jogador.try_melee_hit(self.chefe, self.mapa_blocos.solidos)

        # projéteis do jogador contra inimigos/chefe
        for projetil in list(jogador.projeteis):
            for inimigo in list(self.inimigos):
                if projetil.rect.colliderect(inimigo.rect):
                    inimigo.take_damage(1)
                    projetil.kill()
                    break
            else:
                if self.chefe.ativo and self.chefe.vivo and projetil.rect.colliderect(self.chefe.rect):
                    self.chefe.take_damage(1)
                    projetil.kill()

        if getattr(self.chefe, 'cinematica_pendente', False):
            return 'boss_transform', None
        if self.chefe.derrotado:
            return self._after_defeat(jogador)

        # contato de inimigos comuns com o jogador
        for inimigo in self.inimigos:
            if inimigo.rect.colliderect(jogador.rect):
                impulso = -1 if jogador.rect.centerx < inimigo.rect.centerx else 1
                jogador.take_damage(inimigo.dano_contato, recuo=(impulso * 6, -6))

        # ataques do chefe contra o jogador
        if self.chefe.ativo and self.chefe.vivo:
            for retangulo, dano in self.chefe.get_all_hit_rects():
                if retangulo.colliderect(jogador.rect):
                    impulso = -1 if jogador.rect.centerx < retangulo.centerx else 1
                    jogador.take_damage(dano, recuo=(impulso * 6, -7))

        # projéteis do chefe contra as plataformas já tratados em Chefe.update

        # coleta de power-up (somente mapas antigos possuem recompensas)
        self._collect_powerups(jogador)
        return self._check_transition(jogador)

    def finish_boss_dialogue(self):
        if self.encontro_pendente:
            self.infectado = True
            self.encontro_pendente = False
            self.chefe.activate()

    def _after_defeat(self, jogador):
        self.camera.update(jogador.rect)
        if self.chefe.derrotado and not self.dialogo_derrota_exibido:
            self.dialogo_derrota_exibido = True
            self.chefe.projeteis.empty()
            if self.dados.get('clear_encounter_on_defeat'):
                self.inimigos.empty()
                jogador.projeteis.empty()
            if self.dados["ability_reward"] is not None:
                item_habilidade = ItemHabilidade(self.chefe.rect.centerx, self.chefe.rect.centery, self.dados["ability_reward"])
                self.itens_habilidades.add(item_habilidade)
            return ("dialogue", self.dados["victory_dialogue"])
        self.itens_habilidades.update()
        self._collect_powerups(jogador)
        return self._check_transition(jogador)

    def _collect_powerups(self, jogador):
        for item_habilidade in list(self.itens_habilidades):
            if item_habilidade.rect.colliderect(jogador.rect):
                jogador.grant_ability(item_habilidade.habilidade)
                item_habilidade.kill()

    def _check_transition(self, jogador):
        # saída da fase (só habilitada após derrotar o chefe)
        if self.chefe.derrotado and self.mapa_blocos.gatilho_saida:
            if jogador.rect.colliderect(self.mapa_blocos.gatilho_saida):
                self.concluido = True
                return ("level_complete", None)

        # queda para fora do mapa -> respawn
        if jogador.rect.top > self.mapa_blocos.altura + 200:
            return ("fell", None)

        return (None, None)

    # ------------------------------------------------------------------
    def draw(self, superficie):
        superficie.fill(configuracoes.COR_FUNDO)
        if self.cenario_escolar:
            self.cenario_escolar.draw_background(superficie, self.camera)
        else:
            self._draw_parallax(superficie)

        ocupados = {(r.x, r.y) for r in self.mapa_blocos.solidos}
        for retangulo in self.mapa_blocos.solidos:
            r = self.camera.apply(retangulo)
            if r.colliderect(superficie.get_rect()):
                if self.cenario_escolar:
                    self.cenario_escolar.draw_block(superficie, retangulo, self.camera, self.mapa_blocos.largura,
                                                   (retangulo.x, retangulo.y-TB) not in ocupados)
                else:
                    superficie.blit(self.imagem_chao, r)

        for retangulo in self.mapa_blocos.perigos:
            # o retângulo de dano é só a metade inferior do bloco; a imagem
            # do espinho ocupa o bloco inteiro (ponta encostando no topo)
            retangulo_bloco = pygame.Rect(retangulo.x, retangulo.y - TB // 2, TB, TB)
            r = self.camera.apply(retangulo_bloco)
            superficie.blit(self.imagem_espinho, r)

        if self.mapa_blocos.gatilho_saida:
            if self.cenario_escolar:
                self.cenario_escolar.draw_exit(superficie, self.mapa_blocos.gatilho_saida, self.camera, self.chefe.derrotado)
            else:
                r = self.camera.apply(self.mapa_blocos.gatilho_saida)
                cor = configuracoes.COR_SAIDA if self.chefe.derrotado else configuracoes.COR_PORTAO
                pygame.draw.rect(superficie, cor, r, border_radius=6)
                pygame.draw.rect(superficie, configuracoes.BRANCO, r, 2, border_radius=6)

        for inimigo in self.inimigos:
            inimigo.draw(superficie, self.camera)

        for item_habilidade in self.itens_habilidades:
            item_habilidade.draw(superficie, self.camera)

        if self.infectado:
            self.chefe.draw(superficie, self.camera)
        else:
            self.professor_humano.draw(superficie, self.camera)
            nome = self.fonte_encontro.render('Professor Romerito', True, configuracoes.COR_TEXTO)
            retangulo = self.professor_humano.get_draw_image().get_rect(
                midbottom=self.camera.apply(self.professor_humano.rect).midbottom)
            superficie.blit(nome, nome.get_rect(midbottom=(retangulo.centerx, retangulo.top-6)))

    def draw_infection(self, superficie, progresso):
        retangulo = self.camera.apply(self.chefe.rect)
        bug = self.bug_infeccao
        x = retangulo.centerx-bug.get_width()//2 + 90*(1-min(1, progresso*2))
        if progresso < 0.5:
            superficie.blit(bug, (round(x), retangulo.top))
        raio = 20+int(30*progresso)
        pygame.draw.circle(superficie, (142, 230, 128), retangulo.center, raio, 2)
        texto = self.fonte_infeccao.render('Romerito está se transformando em RomerBug!', True, (206, 246, 164))
        superficie.blit(texto, texto.get_rect(center=(configuracoes.LARGURA_TELA//2, 180)))

    def _draw_parallax(self, superficie):
        for i in range(6):
            x = (i * 220 - int(self.camera.deslocamento.x * 0.3)) % (configuracoes.LARGURA_TELA + 220) - 110
            superficie.blit(self.imagem_painel_fundo, (x, 60))
