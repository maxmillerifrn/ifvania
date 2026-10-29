"""Máquina de estados principal do jogo."""
import sys
import unicodedata
import pygame
import configuracoes
from entidades.jogador import Jogador
from mundo.fase import Fase
from mundo.dados_fases import build_levels, INTRODUCAO_HISTORIA, INDICE_CORRUPCAO_HISTORIA
from mundo.escola import FaseEscolar
from mundo.dados_escola import DIALOGO_ENCONTRO, DESCOBERTA_MOUSE
from mundo.transicao_chefe import TransicaoChefe
from interface.dialogo import CaixaDialogo
from interface.painel import PainelInformacoes
from interface.interface_inicial import InterfaceInicial

ESTADO_MENU = "menu"
ESTADO_SELECAO_PERSONAGEM = "character_select"
ESTADO_ENTRADA_NOME = 'name_entry'
ESTADO_JOGANDO = "playing"
ESTADO_DIALOGO = "dialogue"
ESTADO_CARTAO_FASE = "level_card"
ESTADO_PAUSA = "pause"
ESTADO_DERROTA = "game_over"
ESTADO_FIM_CONTEUDO = "content_end"
ESTADO_ABDUCAO = "abduction"
ESTADO_INFECCAO = "infection"
ESTADO_TRANSFORMACAO_CHEFE = 'boss_transformation'


class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((configuracoes.LARGURA_TELA, configuracoes.ALTURA_TELA))
        pygame.display.set_caption(configuracoes.TITULO)
        self.relogio = pygame.time.Clock()
        self.executando = True

        self.painel_informacoes = PainelInformacoes()
        self.caixa_dialogo = CaixaDialogo()
        self.interface_inicial = InterfaceInicial()
        self.indice_menu = 0
        self.indice_personagem = 0
        self.personagem_escolhido = "boy"
        self.nome_jogador = ''
        self.nome_digitado = ''
        self.erro_nome = ''

        self.definicoes_fases = build_levels()
        self.indice_fase = 0
        self.fase = None
        self.jogador = None
        self.na_introducao = False

        self.estado = ESTADO_MENU
        self.temporizador_cartao_fase = 0
        self.temporizador_abducao = 0
        self.duracao_abducao = 90
        self.estado_retorno_pausa = ESTADO_JOGANDO
        self.temporizador_infeccao = 0
        self.duracao_infeccao = 60
        self.transicao_chefe = None

    # ------------------------------------------------------------------
    def run(self):
        while self.executando:
            eventos = pygame.event.get()
            eventos_jogabilidade = self._process_events(eventos)
            if not self.executando:
                break

            teclas = pygame.key.get_pressed()
            self._update(teclas, eventos_jogabilidade)
            self._draw()

            self.relogio.tick(configuracoes.QUADROS_POR_SEGUNDO)

        pygame.quit()
        sys.exit()

    # ------------------------------------------------------------------
    def _process_events(self, eventos):
        eventos_jogabilidade = []
        for evento in eventos:
            estado_anterior = self.estado
            self._handle_event(evento)
            if estado_anterior != self.estado:
                eventos_jogabilidade.clear()
            if self.jogador and estado_anterior == ESTADO_JOGANDO and self.estado != ESTADO_JOGANDO:
                if self.estado == ESTADO_PAUSA:
                    self.jogador.cancelar_entrada()
                else:
                    self.jogador.cancelar_combate()
            if estado_anterior == ESTADO_JOGANDO and self.estado == ESTADO_JOGANDO:
                eventos_jogabilidade.append(evento)
            if not self.executando:
                break
        return eventos_jogabilidade

    def _handle_event(self, evento):
        if evento.type == pygame.WINDOWFOCUSLOST and self.jogador:
            self.jogador.cancelar_entrada()
            if self.estado == ESTADO_JOGANDO:
                self.estado_retorno_pausa = self.estado
                self.estado = ESTADO_PAUSA
            return
        if evento.type == pygame.QUIT:
            pygame.key.stop_text_input()
            self.executando = False
            return
        if self.estado == ESTADO_ENTRADA_NOME:
            if evento.type == pygame.TEXTINPUT:
                valor = ''.join(c for c in evento.text if c.isprintable())
                self.nome_digitado = unicodedata.normalize('NFC', self.nome_digitado+valor)[:20]
                self.erro_nome = ''
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    self.nome_digitado = self.nome_digitado[:-1]
                    self.erro_nome = ''
                elif evento.key == pygame.K_RETURN:
                    self._confirm_name()
                elif evento.key == pygame.K_ESCAPE:
                    pygame.key.stop_text_input()
                    self.estado = ESTADO_SELECAO_PERSONAGEM
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.interface_inicial.retangulo_confirmar_nome.collidepoint(evento.pos):
                    self._confirm_name()
                elif self.interface_inicial.retangulo_voltar.collidepoint(evento.pos):
                    pygame.key.stop_text_input()
                    self.estado = ESTADO_SELECAO_PERSONAGEM
            return
        # Um evento pertence a uma única tela, mesmo se o callback trocar estado.
        if self.estado == ESTADO_DIALOGO or (self.estado == ESTADO_TRANSFORMACAO_CHEFE and self.caixa_dialogo.ativo):
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                self.estado_retorno_pausa = self.estado
                self.estado = ESTADO_PAUSA
                return
            self.caixa_dialogo.handle_event(evento)
            return
        if evento.type == pygame.KEYDOWN:
            self._handle_keydown(evento, [evento])
        elif evento.type == pygame.MOUSEMOTION and self.estado == ESTADO_MENU:
            for i, retangulo in enumerate(self.interface_inicial.retangulos_menu):
                if retangulo.collidepoint(evento.pos):
                    self.indice_menu = i
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.estado == ESTADO_MENU:
                for i, retangulo in enumerate(self.interface_inicial.retangulos_menu):
                    if retangulo.collidepoint(evento.pos):
                        self.indice_menu = i
                        self._activate_menu()
                        return
            elif self.estado == ESTADO_SELECAO_PERSONAGEM:
                if self.interface_inicial.retangulo_voltar.collidepoint(evento.pos):
                    self.estado = ESTADO_MENU
                elif self.interface_inicial.retangulo_confirmar.collidepoint(evento.pos):
                    self._confirm_character()
                else:
                    for i, retangulo in enumerate(self.interface_inicial.retangulos_personagens):
                        if retangulo.collidepoint(evento.pos):
                            self.indice_personagem = i

    def _activate_menu(self):
        if self.indice_menu == 0:
            self.estado = ESTADO_SELECAO_PERSONAGEM
            self.indice_personagem = self.interface_inicial.personagens.index(self.personagem_escolhido)
        else:
            self.executando = False

    def _confirm_character(self):
        self.personagem_escolhido = self.interface_inicial.personagens[self.indice_personagem]
        self.estado = ESTADO_ENTRADA_NOME
        self.erro_nome = ''
        pygame.key.start_text_input()
        pygame.key.set_text_input_rect(self.interface_inicial.retangulo_nome)

    def _confirm_name(self):
        nome = ' '.join(self.nome_digitado.split())
        if not nome:
            self.erro_nome = 'Digite seu nome para continuar.'
            return
        self.nome_jogador = self.nome_digitado = nome
        pygame.key.stop_text_input()
        self._start_story()

    def _handle_keydown(self, evento, eventos):
        if self.estado == ESTADO_MENU:
            if evento.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_w, pygame.K_s, pygame.K_TAB):
                self.indice_menu = 1 - self.indice_menu
            elif evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._activate_menu()
            elif evento.key == pygame.K_ESCAPE:
                self.executando = False
            return
        if self.estado == ESTADO_SELECAO_PERSONAGEM:
            if evento.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d, pygame.K_TAB):
                self.indice_personagem = 1 - self.indice_personagem
            elif evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._confirm_character()
            elif evento.key == pygame.K_ESCAPE:
                self.estado = ESTADO_MENU
            return
        if evento.key == pygame.K_ESCAPE:
            if self.estado in (ESTADO_JOGANDO, ESTADO_ABDUCAO, ESTADO_INFECCAO, ESTADO_TRANSFORMACAO_CHEFE):
                self.estado_retorno_pausa = self.estado
                self.estado = ESTADO_PAUSA
            elif self.estado == ESTADO_PAUSA:
                self.estado = self.estado_retorno_pausa
            else:
                self.executando = False

        if self.estado in (ESTADO_DERROTA, ESTADO_FIM_CONTEUDO) and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.estado = ESTADO_MENU
            self.indice_menu = 0
            self.indice_fase = 0

        elif self.estado == ESTADO_CARTAO_FASE and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.estado = ESTADO_JOGANDO

    # ------------------------------------------------------------------
    def _start_story(self):
        self.caixa_dialogo.nome_jogador = self.nome_jogador or ('Aluna' if self.personagem_escolhido == 'menina' else 'Aluno')
        self.transicao_chefe = None
        self.indice_fase = 0
        self._load_school('classroom', novo_jogador=True)
        self.na_introducao = True
        self.estado = ESTADO_DIALOGO
        self.caixa_dialogo.start(INTRODUCAO_HISTORIA, ao_concluir=self._begin_corridor)

    def _load_school(self, ambiente, novo_jogador=False):
        self.fase = FaseEscolar(ambiente)
        if novo_jogador:
            self.jogador = Jogador(*self.fase.surgimento_jogador, personagem=self.personagem_escolhido,
                                 nome=self.nome_jogador or None)
        else:
            self.jogador.respawn(*self.fase.surgimento_jogador)
        self.jogador.chicote_desbloqueado = False
        self.jogador.no_chao = True
        self.fase.camera.update(self.jogador.rect)

    def _begin_corridor(self):
        self._load_school('corridor')
        self._show_level_card()

    def _start_abduction(self):
        self.estado = ESTADO_ABDUCAO
        self.temporizador_abducao = 0
        self.jogador.velocidade.update(0, 0)
        self.fase.begin_abduction(self.jogador)

    def _enter_virtual(self):
        self._load_level(0)
        self.jogador.chicote_desbloqueado = False
        self.estado = ESTADO_DIALOGO
        self.caixa_dialogo.start(DESCOBERTA_MOUSE, ao_concluir=self._grant_mouse)

    def _grant_mouse(self):
        self.jogador.chicote_desbloqueado = True
        self._show_level_card()

    def _start_boss_transformation(self):
        self.transicao_chefe = TransicaoChefe(self.fase, self.jogador)
        self.estado = ESTADO_TRANSFORMACAO_CHEFE

    def _load_level(self, indice, novo_jogador=False):
        self.fase = Fase(self.definicoes_fases[indice])
        surgimento = self.fase.surgimento_jogador
        if novo_jogador or self.jogador is None:
            self.jogador = Jogador(*surgimento, personagem=self.personagem_escolhido, nome=self.nome_jogador or None)
        else:
            habilidades_salvas = self.jogador.habilidades
            bonus_vida_salvo = self.jogador.vida_maxima
            self.jogador.respawn(*surgimento)
            self.jogador.habilidades = habilidades_salvas
            self.jogador.vida_maxima = bonus_vida_salvo
            self.jogador.vida = self.jogador.vida_maxima
        self.jogador.chicote_desbloqueado = True
        self.jogador.no_chao = True
        self.caixa_dialogo.nome_jogador = self.jogador.nome
        self.fase.camera.update(self.jogador.rect)

    def _show_level_card(self):
        self.na_introducao = False
        self.estado = ESTADO_CARTAO_FASE
        self.temporizador_cartao_fase = 0

    # ------------------------------------------------------------------
    def _update(self, teclas, eventos):
        if self.fase and self.estado in (ESTADO_JOGANDO, ESTADO_DIALOGO, ESTADO_ABDUCAO,
                                        ESTADO_INFECCAO, ESTADO_TRANSFORMACAO_CHEFE):
            self.fase.update_visuals()
        if self.estado in (ESTADO_MENU, ESTADO_SELECAO_PERSONAGEM, ESTADO_ENTRADA_NOME):
            self.interface_inicial.update()
        elif self.estado == ESTADO_JOGANDO:
            if getattr(self.fase.chefe, 'cinematica_pendente', False):
                self._start_boss_transformation()
                return
            self.jogador.handle_input(teclas, eventos)
            if self.jogador.pausa_impacto > 0:
                self.jogador.pausa_impacto -= 1
                return
            self.jogador.update(self.fase.mapa_blocos.solidos, self.fase.mapa_blocos.perigos)

            tipo_evento, conteudo = self.fase.update(self.jogador, eventos)
            if tipo_evento == "dialogue":
                self.estado = ESTADO_DIALOGO
                self.caixa_dialogo.start(conteudo, ao_concluir=self._resume_from_dialogue)
            elif tipo_evento == "level_complete":
                self._advance_level()
            elif tipo_evento == "fell":
                self.jogador.respawn(*self.fase.surgimento_jogador)
            elif tipo_evento == 'enter_lab':
                self._load_school('lab')
            elif tipo_evento == 'school_encounter':
                self.estado = ESTADO_DIALOGO
                self.jogador.velocidade.update(0, 0)
                self.caixa_dialogo.start(DIALOGO_ENCONTRO, ao_concluir=self._start_abduction)
            elif tipo_evento == 'boss_transform':
                self._start_boss_transformation()

            if not self.jogador.vivo:
                self.estado = ESTADO_DERROTA
            if self.estado != ESTADO_JOGANDO:
                self.jogador.cancelar_combate()

        elif self.estado == ESTADO_DIALOGO:
            self.caixa_dialogo.update()
            if self.na_introducao and self.caixa_dialogo.indice >= INDICE_CORRUPCAO_HISTORIA:
                self.fase.corrompido = True

        elif self.estado == ESTADO_ABDUCAO:
            self.temporizador_abducao += 1
            self.fase.update_abduction(self.jogador, self.temporizador_abducao)
            if self.temporizador_abducao >= self.duracao_abducao:
                self._enter_virtual()

        elif self.estado == ESTADO_INFECCAO:
            self.temporizador_infeccao += 1
            if self.temporizador_infeccao >= self.duracao_infeccao//2:
                self.fase.infectado = True
            if self.temporizador_infeccao >= self.duracao_infeccao:
                self.fase.finish_boss_dialogue()
                self.estado = ESTADO_JOGANDO

        elif self.estado == ESTADO_TRANSFORMACAO_CHEFE:
            if self.caixa_dialogo.ativo:
                self.caixa_dialogo.update()
            else:
                evento = self.transicao_chefe.update()
                if evento == 'speech':
                    self.caixa_dialogo.start([('Entidade', 'Ainda não terminou.')],
                                             ao_concluir=self.transicao_chefe.resume)
                elif evento == 'complete':
                    self.estado = ESTADO_JOGANDO

        elif self.estado == ESTADO_CARTAO_FASE:
            self.temporizador_cartao_fase += 1
            if self.temporizador_cartao_fase > 90:
                self.estado = ESTADO_JOGANDO

    def _resume_from_dialogue(self):
        if self.estado == ESTADO_DIALOGO:
            if getattr(self.fase, 'encontro_pendente', False):
                self.temporizador_infeccao = 0
                self.estado = ESTADO_INFECCAO
            else:
                self.estado = ESTADO_JOGANDO

    def _advance_level(self):
        self.indice_fase += 1
        if self.indice_fase >= len(self.definicoes_fases):
            self.estado = ESTADO_FIM_CONTEUDO
        else:
            self._load_level(self.indice_fase)
            self._show_level_card()

    # ------------------------------------------------------------------
    def _draw(self):
        if self.estado == ESTADO_MENU:
            self._draw_menu()
        elif self.estado == ESTADO_SELECAO_PERSONAGEM:
            self.interface_inicial.draw_selection(self.tela, self.indice_personagem)
        elif self.estado == ESTADO_ENTRADA_NOME:
            self.interface_inicial.draw_name_entry(self.tela, self.nome_digitado,
                                          self.personagem_escolhido, self.erro_nome)
        elif self.estado == ESTADO_TRANSFORMACAO_CHEFE or (self.estado == ESTADO_PAUSA
                                                        and self.estado_retorno_pausa == ESTADO_TRANSFORMACAO_CHEFE):
            self.transicao_chefe.draw(self.tela)
            if self.caixa_dialogo.ativo:
                self.caixa_dialogo.draw(self.tela)
            if self.estado == ESTADO_PAUSA:
                self._draw_overlay('PAUSADO', 'ESC para continuar')
        elif self.estado in (ESTADO_JOGANDO, ESTADO_DIALOGO, ESTADO_PAUSA, ESTADO_ABDUCAO, ESTADO_INFECCAO):
            self.fase.draw(self.tela)
            self.jogador.draw(self.tela, self.fase.camera)
            if not self.na_introducao:
                self.painel_informacoes.draw(self.tela, self.jogador, self.fase.nome, self.fase.chefe)
                if self.estado not in (ESTADO_ABDUCAO, ESTADO_INFECCAO) and not (
                        self.estado == ESTADO_PAUSA and self.estado_retorno_pausa in (ESTADO_ABDUCAO, ESTADO_INFECCAO)):
                    self.painel_informacoes.draw_controls_hint(self.tela, self.jogador)
            if self.estado == ESTADO_ABDUCAO or (self.estado == ESTADO_PAUSA
                                                  and self.estado_retorno_pausa == ESTADO_ABDUCAO):
                self.fase.draw_abduction(self.tela, self.jogador,
                                           self.temporizador_abducao/self.duracao_abducao)
            if self.estado == ESTADO_INFECCAO or (self.estado == ESTADO_PAUSA
                                                 and self.estado_retorno_pausa == ESTADO_INFECCAO):
                self.fase.draw_infection(self.tela, self.temporizador_infeccao/self.duracao_infeccao)
            if self.estado == ESTADO_DIALOGO:
                self.caixa_dialogo.draw(self.tela)
            if self.estado == ESTADO_PAUSA:
                self._draw_overlay("PAUSADO", "ESC para continuar")
        elif self.estado == ESTADO_CARTAO_FASE:
            self.tela.fill(configuracoes.COR_FUNDO)
            self._draw_overlay(self.fase.nome, "Pressione ENTER para começar")
        elif self.estado == ESTADO_DERROTA:
            self.tela.fill((25, 10, 15))
            self._draw_overlay("VOCÊ FOI REPROVADO(A)...", "ENTER para voltar ao menu")
        elif self.estado == ESTADO_FIM_CONTEUDO:
            self.tela.fill((10, 25, 18))
            self._draw_overlay("A JORNADA CONTINUA", "Fim do conteúdo disponível. ENTER para voltar ao menu")
            texto = self.painel_informacoes.fonte_pequena.render(
                'A IFVania segue ativa. A energia da escola ainda precisa ser desligada.',
                True, configuracoes.COR_TEXTO)
            self.tela.blit(texto, texto.get_rect(center=(configuracoes.LARGURA_TELA//2, 340)))

        pygame.display.flip()

    def _draw_overlay(self, titulo, subtitulo):
        sobreposicao = pygame.Surface((configuracoes.LARGURA_TELA, configuracoes.ALTURA_TELA), pygame.SRCALPHA)
        sobreposicao.fill((0, 0, 0, 150))
        self.tela.blit(sobreposicao, (0, 0))
        self.painel_informacoes.draw_center_text(self.tela, titulo, subtitulo)

    def _draw_menu(self):
        self.interface_inicial.draw_menu(self.tela, self.indice_menu)
