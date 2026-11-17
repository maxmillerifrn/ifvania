"""Classe Fase: liga tilemap, inimigos, chefe, powerup e câmera numa fase jogável."""
import pygame
from sistema import configuracoes
from sistema import recursos
from mundo.mapa_blocos import MapaBlocos
from mundo.camera import Camera
from entidades.fabrica_entidades import criar_inimigo, criar_chefe
from entidades.chefes_professores import CLASSES_CHEFES
from entidades.romer_bug import RomerBug
from entidades.professor import Professor
from sistema.habilidades import ItemHabilidade
from sistema.habilidades import Habilidade
from mundo.escola_sombria import EscolaSombria
from mundo.biblioteca import Biblioteca
from sistema.eventos_campanha import ChefeDerrotado, ObjetivoConcluido
from mundo.efeitos_combate import EfeitosCombate
from mundo.cenario_guardioes import CenarioGuardioes
from sistema.comandos import houve_interacao
from entidades.bug_combate import BugGuarda, BugRetransmissor
from mundo.desafios_campus import DesafiosCampus

TB = configuracoes.TAMANHO_BLOCO


class Fase:
    def __init__(self, dados_fase, eventos=None, progresso=None):
        self.dados = dados_fase
        self.eventos = eventos
        self.progresso = progresso
        self.efeitos_combate = EfeitosCombate()
        self.identificador = dados_fase.get('identificador', f'antiga_{dados_fase["index"]}')
        self.nome = dados_fase["name"]
        self.mapa_blocos = MapaBlocos(dados_fase["ascii_map"])
        self.camera = Camera(self.mapa_blocos.largura, self.mapa_blocos.altura)

        self.inimigos = pygame.sprite.Group()
        for indice, (ex, ey) in enumerate(self.mapa_blocos.surgimentos_inimigos):
            tipo = ('lancador' if indice % 3 == 2 else 'combate') if dados_fase.get('identificador') else 'bug'
            if dados_fase.get('identificador') in ('copias', 'rede', 'continuidade') and indice % 2:
                tipo = 'guarda'
            if dados_fase.get('identificador') in ('rede', 'continuidade') and indice == 2:
                tipo = 'retransmissor'
            if dados_fase.get('library'):
                tipo = 'arquivo'
            if dados_fase.get('identificador') == 'copias' and tipo == 'combate':
                tipo = 'repetidor'
            self.inimigos.add(criar_inimigo(tipo, *self._grounded_spawn(ex, ey)))

        definicao_chefe = dados_fase["boss"]
        bx, by = self.mapa_blocos.surgimento_chefe
        classe_chefe = CLASSES_CHEFES.get(definicao_chefe['boss_type'])
        if classe_chefe is None:
            raise ValueError(f'Tipo de chefe desconhecido: {definicao_chefe["boss_type"]}')
        bx, by = self._grounded_spawn(bx, by)
        opcoes = {}
        if classe_chefe is RomerBug:
            opcoes['transformacao_cinematica'] = dados_fase.get('cinematic_transform', False)
            esquerda = dados_fase.get('arena_left', TB)
            opcoes["arena"] = pygame.Rect(esquerda, TB, self.mapa_blocos.largura - esquerda - TB,
                                            self.mapa_blocos.altura - 2 * TB)
        if dados_fase.get('library'):
            esquerda = dados_fase['arena_left']
            opcoes['arena'] = pygame.Rect(esquerda, TB, self.mapa_blocos.largura-esquerda-TB, 14*TB-TB)
        if dados_fase.get('campus_battle'):
            opcoes['arena'] = pygame.Rect(dados_fase['arena_left'], TB, self.mapa_blocos.largura-dados_fase['arena_left']-TB, 14*TB-TB)
        self.chefe = criar_chefe(definicao_chefe['boss_type'], bx, by, definicao_chefe["name"], definicao_chefe["subject"],
                          definicao_chefe["color"], vida=definicao_chefe["health"],
                          arquivo_figura=definicao_chefe.get("sprite_file"), **opcoes)

        self.itens_habilidades = pygame.sprite.Group()
        self.item_criado = False

        self.dialogo_exibido = False
        self.dialogo_derrota_exibido = False
        self.concluido = False
        self.surgimento_jogador = self._grounded_spawn(*self.mapa_blocos.surgimento_jogador)
        self.exige_infeccao = dados_fase.get('requires_infection', False)
        self.professor_liberto = False
        self.infectado = not self.exige_infeccao
        self.encontro_pendente = False
        self.professor_humano = Professor(bx, by, 'romerito') if self.exige_infeccao else None
        self.bug_infeccao = recursos.load_character_frames(['inimigos/bug_0.png'])[0] if self.exige_infeccao else None
        self.fonte_encontro = pygame.font.Font(None, 20)
        self.fonte_infeccao = pygame.font.Font(None, 24)
        self.objetivos = [pygame.Rect(x, y, 32, 40) for x, y in dados_fase.get('objetivos', ())]
        self.desafios = DesafiosCampus(self.identificador) if self.objetivos else None
        self.conectores = [pygame.Vector2(820, 310), pygame.Vector2(1190, 260), pygame.Vector2(1660, 310), pygame.Vector2(2200, 330), pygame.Vector2(2720, 320)] if dados_fase.get('identificador') in ('rede', 'continuidade') else [pygame.Vector2(2800, 330)] if dados_fase.get('identificador') == 'copias' else []
        self.consultados = set(progresso.objetivos_da_fase(self.identificador)) if progresso else set()
        self.portao_objetivos = pygame.Rect(56*TB, 0, TB, 14*TB) if self.objetivos else None
        if self.portao_objetivos and len(self.consultados) < len(self.objetivos):
            self.mapa_blocos.solidos.append(self.portao_objetivos)
        self.cenario_escolar = (EscolaSombria(self.mapa_blocos.largura, self.mapa_blocos.altura,
                                       self.surgimento_jogador[1]+configuracoes.TAMANHO_PERSONAGEM[1])
                             if dados_fase.get('school_battle') else None)

        self.biblioteca = None
        if dados_fase.get('campus_battle'):
            self.cenario_escolar = CenarioGuardioes(self.mapa_blocos.largura, self.mapa_blocos.altura,
                                                  14*TB, self.identificador)
            self.cenario_escolar.estabilizados = len(self.consultados)
        if dados_fase.get('library'):
            self.biblioteca = Biblioteca(self.mapa_blocos.largura, self.mapa_blocos.altura, 14*TB, eventos, progresso)
            self.cenario_escolar = self.biblioteca
            if len(self.biblioteca.consultados) < 3:
                self.mapa_blocos.solidos.append(self.biblioteca.portao)

        # sprites do cenário (carregados/cacheados uma vez em recursos.py)
        self.imagem_chao = recursos.load_image("blocos/chao.png", (TB, TB), configuracoes.COR_CHAO)
        self.imagem_espinho = recursos.load_image("blocos/espinho.png", (TB, TB), configuracoes.COR_ESPINHO)
        self.imagem_painel_fundo = recursos.load_image("cenarios/painel.png", (90, 220), configuracoes.COR_FUNDO_2)
        if progresso and self.identificador in progresso.fases_concluidas:
            self.chefe.vida = 0
            self.chefe.vivo = False
            self.chefe.derrotado = True
            self.dialogo_exibido = self.dialogo_derrota_exibido = True
            self.inimigos.empty()
            if self.objetivos:
                self.consultados = {f'terminal_{indice}' for indice in range(len(self.objetivos))}
                if self.portao_objetivos in self.mapa_blocos.solidos:
                    self.mapa_blocos.solidos.remove(self.portao_objetivos)
                self.cenario_escolar.estabilizados = len(self.consultados)
            if self.biblioteca:
                self.biblioteca.consultados = {0, 1, 2}
                self.biblioteca.modulo_obtido = True
                if self.biblioteca.portao in self.mapa_blocos.solidos:
                    self.mapa_blocos.solidos.remove(self.biblioteca.portao)
        if self.objetivos:
            self.cenario_escolar.consultados = self.consultados
        objetivos_prontos = bool(self.objetivos) and len(self.consultados) == len(self.objetivos)
        biblioteca_pronta = self.biblioteca is not None and len(self.biblioteca.consultados) == 3
        if objetivos_prontos or biblioteca_pronta:
            self.surgimento_jogador = self._grounded_spawn(dados_fase['arena_left']+64, self.surgimento_jogador[1])

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
        self.efeitos_combate.update()
        if self.concluido or self.encontro_pendente:
            return None, None
        if self.biblioteca:
            dialogo = self.biblioteca.interagir(jogador, eventos_quadro, self.mapa_blocos.solidos)
            if dialogo:
                return 'dialogue', dialogo
        if self.objetivos:
            for indice, terminal in enumerate(self.objetivos):
                if jogador.rect.colliderect(terminal.inflate(80, 30)) and houve_interacao(eventos_quadro):
                    identificador = f'terminal_{indice}'
                    if identificador not in self.consultados:
                        self.consultados.add(identificador)
                        self.desafios.registrar_resgate(terminal.midbottom, indice)
                        self.cenario_escolar.estabilizados = len(self.consultados)
                        if self.eventos:
                            self.eventos.emitir(ObjetivoConcluido(self.identificador, identificador))
                        if len(self.consultados) == len(self.objetivos) and self.portao_objetivos in self.mapa_blocos.solidos:
                            self.mapa_blocos.solidos.remove(self.portao_objetivos)
                        falas = self.dados.get('falas_objetivos', ())
                        texto = falas[indice] if falas else 'Conexão estabilizada.'
                        dialogo = [('Aluno(a)', f'{texto} ({len(self.consultados)}/{len(self.objetivos)})')]
                        if indice == 2 and self.identificador == 'recreio':
                            dialogo += [('IFVania', 'Posso entregar tudo por você. Nenhuma pendência.'),
                                        ('Aluno(a)', 'E ninguém vai poder sair?'),
                                        ('IFVania', 'Sair interrompe a aprendizagem.'),
                                        ('Aluno(a)', 'Então você ainda não entendeu o intervalo.')]
                        elif indice == 2 and self.identificador == 'rede':
                            dialogo += [('IFVania', 'Sua sessão pode terminar. As outras permanecem comigo.'),
                                        ('Aluno(a)', 'Eu não vim buscar só a minha saída.')]
                        return 'dialogue', dialogo
                    if self.identificador == 'copias':
                        jogador.cancelar_combate()
                        jogador.rect.topleft = self._grounded_spawn(terminal.x+96, 14*TB-40)
                        jogador.posicao.update(jogador.rect.topleft)
                        jogador.velocidade.update(0, 0)
                    return None, None
            if houve_interacao(eventos_quadro):
                jogador.tentar_ancoragem(self.conectores, self.mapa_blocos.solidos)
            self.desafios.update()
            for zona in self.desafios.areas_ativas(self.consultados):
                if jogador.rect.colliderect(zona):
                    jogador.take_damage(1, recuo=(-jogador.direcao_olhar*4, -5), bloqueavel=False)
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

        for inimigo in self.inimigos:
            if isinstance(inimigo, BugGuarda):
                inimigo.reforcado = any(isinstance(outro, BugRetransmissor) and abs(outro.rect.centerx-inimigo.rect.centerx) < 400 for outro in self.inimigos)
            if hasattr(inimigo, 'atualizar_combate'):
                inimigo.atualizar_combate(jogador, self.mapa_blocos.solidos)
            else:
                inimigo.update(self.mapa_blocos.solidos)
            if inimigo.rect.top > self.mapa_blocos.altura+100:
                inimigo.vida = 0
                inimigo.vivo = False
                inimigo.kill()
        if hasattr(self.chefe, 'quantidade_aliados'):
            self.chefe.quantidade_aliados = sum(inimigo.rect.right > self.chefe.arena.left for inimigo in self.inimigos)
        self.chefe.update(jogador, self.mapa_blocos.solidos)
        if hasattr(self.chefe, 'reforcos'):
            self.inimigos.add(*self.chefe.reforcos)
            self.chefe.reforcos.empty()
        self.itens_habilidades.update()
        self.camera.update(jogador.rect)

        # ataque corpo-a-corpo do jogador contra inimigos e chefe
        retangulo_golpe = jogador.get_melee_rect()
        if retangulo_golpe:
            for inimigo in list(self.inimigos):
                if retangulo_golpe.colliderect(jogador.chicote.area_alvo(inimigo)):
                    if jogador.try_melee_hit(inimigo, self.mapa_blocos.solidos):
                        self.efeitos_combate.adicionar(inimigo.rect.center, not inimigo.vivo)
            if self.chefe.ativo and self.chefe.vivo and retangulo_golpe.colliderect(jogador.chicote.area_alvo(self.chefe)):
                if jogador.try_melee_hit(self.chefe, self.mapa_blocos.solidos):
                    self.efeitos_combate.adicionar(self.chefe.rect.center, not self.chefe.vivo)

        # projéteis do jogador contra inimigos/chefe
        for projetil in list(jogador.projeteis):
            for inimigo in list(self.inimigos):
                if projetil.rect.colliderect(inimigo.rect):
                    inimigo.take_damage(1)
                    self.efeitos_combate.adicionar(inimigo.rect.center, not inimigo.vivo)
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
            areas = inimigo.areas_dano() if hasattr(inimigo, 'areas_dano') else [(inimigo.rect, inimigo.dano_contato)]
            for area, dano in areas:
                if area.colliderect(jogador.rect):
                    impulso = -1 if jogador.rect.centerx < area.centerx else 1
                    resposta = jogador.take_damage(dano, recuo=(impulso * 6, -6), origem=area.center)
                    if resposta == 'bloqueado':
                        inimigo.reagir_bloqueio(area)
                        for projetil in list(getattr(inimigo, 'projeteis', ())):
                            if projetil.rect is area:
                                projetil.kill()

        # ataques do chefe contra o jogador
        if self.chefe.ativo and self.chefe.vivo:
            for retangulo, dano in self.chefe.get_all_hit_rects():
                if retangulo.colliderect(jogador.rect):
                    impulso = -1 if jogador.rect.centerx < retangulo.centerx else 1
                    resposta = jogador.take_damage(dano, recuo=(impulso * 6, -7), origem=retangulo.center)
                    if resposta == 'bloqueado':
                        self.chefe.reagir_bloqueio(retangulo)
                        for projetil in list(self.chefe.projeteis):
                            if projetil.rect is retangulo:
                                projetil.kill()

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
            if self.eventos is not None:
                self.eventos.emitir(ChefeDerrotado(self.identificador))
            if self.identificador == 'copias':
                jogador.grant_ability(Habilidade.ANCORAGEM, aumentar_vida=False)
            self.chefe.projeteis.empty()
            if self.professor_humano:
                self.professor_liberto = True
                self.professor_humano.rect.topleft = self.chefe.rect.topleft
                self.professor_humano.posicao.update(self.chefe.rect.topleft)
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

        if self.biblioteca:
            self.biblioteca.desenhar_interativos(superficie, self.camera)
        if self.objetivos:
            self.desafios.draw(superficie, self.camera, self.consultados)
            for indice, terminal in enumerate(self.objetivos):
                destino = self.camera.apply(terminal)
                cor = (103, 211, 149) if f'terminal_{indice}' in self.consultados else (231, 183, 95)
                pygame.draw.rect(superficie, (19, 35, 48), destino, border_radius=4)
                pygame.draw.rect(superficie, cor, destino.inflate(-8, -10), 2)
                rotulo = self.fonte_encontro.render(f'E · {indice+1}', True, cor)
                superficie.blit(rotulo, rotulo.get_rect(midbottom=(destino.centerx, destino.top-7)))
                if self.identificador == 'copias' and f'terminal_{indice}' in self.consultados:
                    etiqueta = self.fonte_encontro.render('E · retorno estabilizado', True, (130, 214, 193))
                    superficie.blit(etiqueta, etiqueta.get_rect(midtop=(destino.centerx, destino.bottom+4)))
            if not self.chefe.ativo:
                texto = self.fonte_encontro.render(f'{self.dados["objetivo"]}  {len(self.consultados)}/3', True, (240, 225, 195))
                pygame.draw.rect(superficie, (16, 28, 36), (18, 145, 924, 34), border_radius=4)
                superficie.blit(texto, (30, 153))
            for ponto in self.conectores:
                centro = ponto-self.camera.deslocamento
                pygame.draw.circle(superficie, (130, 223, 218), centro, 10, 3)
                pygame.draw.line(superficie, (214, 245, 232), (centro.x-5, centro.y), (centro.x+5, centro.y), 2)

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
            if isinstance(inimigo, BugGuarda) and inimigo.reforcado:
                for outro in self.inimigos:
                    if isinstance(outro, BugRetransmissor) and abs(outro.rect.centerx-inimigo.rect.centerx) < 400:
                        pygame.draw.line(superficie, (107, 83, 143), self.camera.apply(inimigo.rect).center, self.camera.apply(outro.rect).center, 1)
            inimigo.draw(superficie, self.camera)
        self.efeitos_combate.draw(superficie, self.camera)

        for item_habilidade in self.itens_habilidades:
            item_habilidade.draw(superficie, self.camera)

        if self.infectado and not self.professor_liberto:
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
