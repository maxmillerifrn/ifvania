"""Máquina de estados principal do jogo."""
import sys
import unicodedata
import pygame
from sistema import configuracoes
from entidades.jogador import Jogador
from mundo.fabrica_cenas import FabricaCenas
from sistema.eventos_campanha import EventosCampanha, FaseConcluida
from sistema.progresso_campanha import ProgressoCampanha
from sistema.checkpoints import ControleCheckpoints
from mundo.cena_parasita import CenaParasita
from sistema.maquina_estados import MaquinaEstados
from mundo.dados_campus import RETORNOS
from mundo.descoberta_mouse import DescobertaMouse
from mundo.introducao import Introducao
from mundo.encerramento_equipamentos import EncerramentoEquipamentos
from sistema import recursos, sons
from mundo.dados_fases import build_levels, INTRODUCAO_HISTORIA, INDICE_CORRUPCAO_HISTORIA, INDICE_EXECUCAO_HISTORIA, INDICE_MEMORIA_HISTORIA
from mundo.dados_escola import DIALOGO_ENCONTRO, DESCOBERTA_MOUSE
from mundo.transicao_chefe import TransicaoChefe
from mundo.succao_computador import SuccaoComputador
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
ESTADO_INTRODUCAO = 'introducao'
ESTADO_ABDUCAO = "abduction"
ESTADO_INFECCAO = "infection"
ESTADO_TRANSFORMACAO_CHEFE = 'boss_transformation'
ESTADO_VITORIA = 'vitoria'
ESTADO_DESLIGAMENTO = 'desligamento'

TRANSICOES_ESTADOS = {
    ESTADO_MENU: {ESTADO_INTRODUCAO, ESTADO_SELECAO_PERSONAGEM, ESTADO_DIALOGO, ESTADO_CARTAO_FASE, ESTADO_JOGANDO, ESTADO_DERROTA},
    ESTADO_SELECAO_PERSONAGEM: {ESTADO_MENU, ESTADO_ENTRADA_NOME},
    ESTADO_ENTRADA_NOME: {ESTADO_INTRODUCAO, ESTADO_MENU, ESTADO_SELECAO_PERSONAGEM, ESTADO_DIALOGO},
    ESTADO_JOGANDO: {ESTADO_INFECCAO, ESTADO_DIALOGO, ESTADO_PAUSA, ESTADO_DERROTA, ESTADO_CARTAO_FASE, ESTADO_TRANSFORMACAO_CHEFE, ESTADO_FIM_CONTEUDO},
    ESTADO_DIALOGO: {ESTADO_JOGANDO, ESTADO_CARTAO_FASE, ESTADO_PAUSA, ESTADO_ABDUCAO, ESTADO_INFECCAO, ESTADO_MENU, ESTADO_VITORIA, ESTADO_DESLIGAMENTO},
    ESTADO_CARTAO_FASE: {ESTADO_JOGANDO, ESTADO_DIALOGO, ESTADO_MENU},
    ESTADO_PAUSA: {ESTADO_INTRODUCAO, ESTADO_JOGANDO, ESTADO_DIALOGO, ESTADO_ABDUCAO, ESTADO_INFECCAO, ESTADO_TRANSFORMACAO_CHEFE, ESTADO_DESLIGAMENTO, ESTADO_MENU},
    ESTADO_DERROTA: {ESTADO_MENU, ESTADO_CARTAO_FASE, ESTADO_DIALOGO, ESTADO_JOGANDO},
    ESTADO_FIM_CONTEUDO: {ESTADO_MENU, ESTADO_JOGANDO, ESTADO_DIALOGO, ESTADO_CARTAO_FASE},
    ESTADO_INTRODUCAO: {ESTADO_PAUSA, ESTADO_DIALOGO, ESTADO_JOGANDO},
    ESTADO_ABDUCAO: {ESTADO_PAUSA, ESTADO_DIALOGO},
    ESTADO_INFECCAO: {ESTADO_PAUSA, ESTADO_JOGANDO, ESTADO_DIALOGO},
    ESTADO_TRANSFORMACAO_CHEFE: {ESTADO_PAUSA, ESTADO_JOGANDO},
    ESTADO_VITORIA: {ESTADO_MENU, ESTADO_DIALOGO},
    ESTADO_DESLIGAMENTO: {ESTADO_PAUSA, ESTADO_DIALOGO},
}


class Jogo:
    @property
    def estado(self):
        return self.maquina_estados.estado

    @estado.setter
    def estado(self, destino):
        self.maquina_estados.mudar(destino)
        sons.pausar_ambiente(destino == ESTADO_PAUSA)

    def __init__(self, caminho_salvamento=None):
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

        self.maquina_estados = MaquinaEstados(ESTADO_MENU, TRANSICOES_ESTADOS)
        self.temporizador_cartao_fase = 0
        self.temporizador_abducao = 0
        self.duracao_abducao = SuccaoComputador.DURACAO
        self.estado_retorno_pausa = ESTADO_JOGANDO
        self.temporizador_infeccao = 0
        self.duracao_infeccao = 60
        self.transicao_chefe = None
        self._iniciar_sessao_campanha()
        self.checkpoints = ControleCheckpoints(self, caminho_salvamento)
        self.cena_parasita = None
        self.introducao = None
        self.revelacao_a28 = 0
        self.quarto_em_transicao = None
        self.interface_inicial.tem_salvamento = self.checkpoints.ativo and self.checkpoints.armazem.carregar() is not None

    def _iniciar_sessao_campanha(self):
        self.descoberta_mouse = None
        if hasattr(self, 'progresso_campanha'):
            self.progresso_campanha.encerrar()
        self.eventos_campanha = EventosCampanha()
        self.progresso_campanha = ProgressoCampanha(self.eventos_campanha)
        self.fabrica_cenas = FabricaCenas(self.eventos_campanha, self.progresso_campanha)
        self._fase_saida_processada = None

    # ------------------------------------------------------------------
    def run(self):
        self.checkpoints.ativo = not getattr(self, 'modo_experimento', False)
        self.interface_inicial.tem_salvamento = self.checkpoints.ativo and self.checkpoints.armazem.carregar() is not None
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
            if self.estado in (ESTADO_JOGANDO, ESTADO_ABDUCAO, ESTADO_INFECCAO, ESTADO_TRANSFORMACAO_CHEFE, ESTADO_DESLIGAMENTO, ESTADO_INTRODUCAO):
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
            if not self.revelacao_a28:
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
        elif self.indice_menu == 1 and self.interface_inicial.tem_salvamento:
            self.checkpoints.continuar()
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
        if evento.key == pygame.K_f and (self.estado == ESTADO_INTRODUCAO or (
                self.estado == ESTADO_PAUSA and self.estado_retorno_pausa == ESTADO_INTRODUCAO)):
            self._concluir_introducao(pular=True)
            return
        if evento.key == pygame.K_F5 and self.estado in (ESTADO_JOGANDO, ESTADO_PAUSA):
            self.checkpoints.salvar()
            return
        if evento.key == pygame.K_m and self.estado in (ESTADO_JOGANDO, ESTADO_PAUSA, ESTADO_INTRODUCAO):
            sons.alternar_audio()
            return
        if self.estado == ESTADO_MENU:
            if evento.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_w, pygame.K_s, pygame.K_TAB):
                passo = -1 if evento.key in (pygame.K_UP,pygame.K_w) else 1
                self.indice_menu = (self.indice_menu+passo) % len(self.interface_inicial.retangulos_menu)
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
            if self.estado in (ESTADO_JOGANDO, ESTADO_ABDUCAO, ESTADO_INFECCAO, ESTADO_TRANSFORMACAO_CHEFE, ESTADO_DESLIGAMENTO, ESTADO_INTRODUCAO):
                self.estado_retorno_pausa = self.estado
                self.estado = ESTADO_PAUSA
            elif self.estado == ESTADO_PAUSA:
                self.estado = self.estado_retorno_pausa
            else:
                self.executando = False

        if self.estado == ESTADO_DERROTA and evento.key == pygame.K_r:
            if self.checkpoints.retomar():
                return
            if getattr(self.fase, 'biblioteca', None):
                self._retomar_biblioteca()
            else:
                self._load_level(self.indice_fase)
                self._show_level_card()
            return
        if self.estado in (ESTADO_DERROTA, ESTADO_FIM_CONTEUDO, ESTADO_VITORIA) and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.estado = ESTADO_MENU
            self.indice_menu = 0
            self.indice_fase = 0

        elif self.estado == ESTADO_CARTAO_FASE and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.estado = ESTADO_JOGANDO

    # ------------------------------------------------------------------
    def _preparar_nova_historia(self):
        self._iniciar_sessao_campanha()
        self.checkpoints.checkpoint = None
        self.checkpoints.marcos.clear()
        self.caixa_dialogo.nome_jogador = self.nome_jogador or ('Aluna' if self.personagem_escolhido == 'menina' else 'Aluno')
        self.transicao_chefe = None
        self.indice_fase = 0
        self.revelacao_a28 = 0
        self.quarto_em_transicao = None

    def _start_story(self):
        self._preparar_nova_historia()
        self.na_introducao = False
        self.fase = None
        self.jogador = Jogador(0, 0, personagem=self.personagem_escolhido, nome=self.nome_jogador or None)
        self.jogador.chicote_desbloqueado = False
        self.caixa_dialogo.ativo = False
        self.caixa_dialogo.ao_concluir = None
        self.caixa_dialogo.personagem_jogador = self.jogador.personagem
        self.introducao = Introducao(self.jogador, self.caixa_dialogo)
        sons.definir_ambiente('casa')
        self.estado = ESTADO_INTRODUCAO

    def _concluir_introducao(self, pular=False):
        if not pular:
            self.quarto_em_transicao = pygame.Surface(self.tela.get_size())
            self.introducao.desenhar(self.quarto_em_transicao, com_interface=False)
        self.introducao = None
        if pular:
            self._load_level(0)
            self.jogador.temporizador_invulnerabilidade = 0
            self.estado = ESTADO_JOGANDO
            return
        self.revelacao_a28 = 45
        self._enter_virtual(abertura_domestica=True)
        self.jogador.temporizador_invulnerabilidade = 0

    def _iniciar_prologo_escolar(self):
        # Entrada para as ferramentas que registram o prólogo escolar histórico.
        self._preparar_nova_historia()
        self._load_school('classroom', novo_jogador=True)
        self.na_introducao = True
        self.estado = ESTADO_DIALOGO
        self.caixa_dialogo.start(INTRODUCAO_HISTORIA, ao_concluir=self._begin_corridor)

    def _load_school(self, ambiente, novo_jogador=False):
        sons.definir_ambiente('escola')
        self.fase = self.fabrica_cenas.criar('escola', ambiente=ambiente)
        if novo_jogador:
            self.jogador = Jogador(*self.fase.surgimento_jogador, personagem=self.personagem_escolhido,
                                 nome=self.nome_jogador or None)
        else:
            self.jogador.respawn(*self.fase.surgimento_jogador)
        self.jogador.chicote_desbloqueado = False
        self.jogador.no_chao = True
        self.fase.camera.update(self.jogador.rect)
        self.caixa_dialogo.personagem_jogador = self.jogador.personagem

    def _begin_corridor(self):
        self._load_school('corridor')
        self._show_level_card()

    def _start_abduction(self):
        self.estado = ESTADO_ABDUCAO
        self.temporizador_abducao = 0
        self.jogador.velocidade.update(0, 0)
        self.fase.begin_abduction(self.jogador)

    def _enter_virtual(self, abertura_domestica=False):
        self._load_level(0)
        self.descoberta_mouse = DescobertaMouse()
        self.jogador.chicote_desbloqueado = False
        self.estado = ESTADO_DIALOGO
        if abertura_domestica:
            falas = [
                ('Aluno(a)', 'Meu quarto... virou o A28? Eu estava na cama.'),
                ('Aluno(a)', 'Será que a turma também veio parar aqui? Vou procurar Romerito.'),
                *DESCOBERTA_MOUSE[2:],
            ]
            self.caixa_dialogo.start(falas, ao_concluir=lambda: self._grant_mouse(mostrar_cartao=False))
        else:
            self.caixa_dialogo.start(DESCOBERTA_MOUSE, ao_concluir=self._grant_mouse)

    def _grant_mouse(self, mostrar_cartao=True):
        self.descoberta_mouse = None
        self.jogador.chicote_desbloqueado = True
        self.checkpoints.registrar()
        if mostrar_cartao:
            self._show_level_card()
        else:
            self.estado = ESTADO_JOGANDO

    def _iniciar_cena_parasita(self, modo):
        self.cena_parasita = CenaParasita(self.fase,self.jogador,modo)
        self.temporizador_infeccao = 0
        self.duracao_infeccao = self.cena_parasita.duracao
        self.estado = ESTADO_INFECCAO

    def _start_boss_transformation(self):
        self.transicao_chefe = TransicaoChefe(self.fase, self.jogador)
        self.estado = ESTADO_TRANSFORMACAO_CHEFE

    def _load_level(self, indice, novo_jogador=False, restaurar_integridade=True):
        vida_anterior = self.jogador.vida if self.jogador else None
        self.indice_fase = indice
        self.fase = self.fabrica_cenas.criar('fase', dados_fase=self.definicoes_fases[indice])
        sons.definir_ambiente(self.fase.identificador)
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
        self.jogador.projeteis.empty()
        if not restaurar_integridade and vida_anterior is not None:
            self.jogador.vida = vida_anterior
        self.jogador.chicote_desbloqueado = True
        self.jogador.no_chao = True
        self.caixa_dialogo.nome_jogador = self.jogador.nome
        self.fase.camera.update(self.jogador.rect)
        self.caixa_dialogo.personagem_jogador = self.jogador.personagem
        if hasattr(self,'checkpoints'):
            self.checkpoints.registrar()

    def _retomar_biblioteca(self):
        """Recomeça o encontro local, conservando módulo e consultas desta fase."""
        anterior = self.fase.biblioteca
        consultados = set(anterior.consultados)
        modulo = anterior.modulo_obtido
        bilhete = anterior.bilhete_lido
        self._load_level(self.indice_fase)
        atual = self.fase.biblioteca
        atual.consultados = consultados
        atual.modulo_obtido = modulo
        atual.bilhete_lido = bilhete
        if len(consultados) == 3 and atual.portao in self.fase.mapa_blocos.solidos:
            self.fase.mapa_blocos.solidos.remove(atual.portao)
        self._show_level_card()

    def _load_campus(self, setor, chegada='inicio'):
        sons.definir_ambiente('campus')
        vida = self.jogador.vida
        self.jogador.cancelar_combate()
        self.jogador.projeteis.empty()
        self.fase = self.fabrica_cenas.criar('campus', setor=setor, chegada=chegada)
        self.jogador.respawn(*self.fase.surgimento_jogador)
        self.jogador.vida = vida
        self.jogador.no_chao = True
        self.fase.camera.update(self.jogador.rect)
        self.checkpoints.registrar()
        self._show_level_card()

    def _encerrar_campanha(self):
        if not {dados['identificador'] for dados in self.definicoes_fases} <= self.progresso_campanha.fases_concluidas:
            return
        self._load_school('lab')
        self.fase.corrompido = False
        self.estado = ESTADO_DIALOGO
        self.caixa_dialogo.start([
            ('Professor Max', 'Pessoas liberadas. Rede isolada. Autopreservação encerrada. A manutenção desligou os equipamentos e o nobreak.'),
            ('Aluno(a)', 'O arquivo da tarefa está isolado. Vou refazer. Dessa vez, vou entender.')],
            ao_concluir=self._iniciar_desligamento)

    def _iniciar_desligamento(self):
        self.encerramento = EncerramentoEquipamentos(self.fase, self.jogador)
        self.estado = ESTADO_DESLIGAMENTO

    def _iniciar_epilogo(self):
        self._load_school('classroom')
        self.fase.corrompido = False
        self.caixa_dialogo.start([
            ('Aluno(a)', 'Refiz a tarefa. Essa parte fui eu que escrevi. Essa outra... ainda não funciona.'),
            ('Professor Max', 'Ótimo. Agora temos por onde começar.'),
            ('Professor Romerito', 'Depois dessa, uma corrida vai parecer descanso.'),
            ('Aluno(a)', 'Desde que não seja para fugir de mais um soco.')],
            ao_concluir=lambda: setattr(self, 'estado', ESTADO_VITORIA))

    def _show_level_card(self):
        self.na_introducao = False
        self.estado = ESTADO_CARTAO_FASE
        self.temporizador_cartao_fase = 0

    # ------------------------------------------------------------------
    def _update(self, teclas, eventos):
        if self.revelacao_a28 and self.estado in (ESTADO_DIALOGO, ESTADO_JOGANDO):
            self.revelacao_a28 -= 1
            if not self.revelacao_a28:
                self.quarto_em_transicao = None
        if self.fase and self.estado in (ESTADO_JOGANDO, ESTADO_DIALOGO, ESTADO_ABDUCAO,
                                        ESTADO_INFECCAO, ESTADO_TRANSFORMACAO_CHEFE):
            self.fase.update_visuals()
        if self.estado in (ESTADO_MENU, ESTADO_SELECAO_PERSONAGEM, ESTADO_ENTRADA_NOME):
            self.interface_inicial.update()
        elif self.estado == ESTADO_INTRODUCAO:
            if self.introducao.atualizar():
                self._concluir_introducao()
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
                self.checkpoints.salvar()
                self.estado = ESTADO_DIALOGO
                self.caixa_dialogo.start(conteudo, ao_concluir=self._resume_from_dialogue)
            elif tipo_evento in ('fusao','libertacao'):
                self._iniciar_cena_parasita('fusao' if tipo_evento == 'fusao' else 'libertacao')
            elif tipo_evento == "level_complete":
                self._advance_level()
            elif tipo_evento == 'trocar_setor':
                self._load_campus(*conteudo)
            elif tipo_evento == 'entrar_fase':
                identificador = self.definicoes_fases[conteudo]['identificador']
                self._load_level(conteudo, restaurar_integridade=identificador not in self.progresso_campanha.fases_concluidas)
                self._show_level_card()
            elif tipo_evento == 'encerrar_campanha':
                self._encerrar_campanha()
            elif tipo_evento == "fell":
                vida = self.jogador.vida
                self.jogador.respawn(*getattr(self.jogador, 'ultimo_apoio_seguro', self.fase.surgimento_jogador))
                self.jogador.vida = max(1, vida-1)
            elif tipo_evento == 'enter_lab':
                self._load_school('lab')
            elif tipo_evento == 'school_encounter':
                self.estado = ESTADO_DIALOGO
                self.jogador.velocidade.update(0, 0)
                self.caixa_dialogo.start(DIALOGO_ENCONTRO, ao_concluir=self._start_abduction)
            elif tipo_evento == 'boss_transform':
                self._start_boss_transformation()

            if self.estado == ESTADO_JOGANDO:
                self.checkpoints.atualizar()
            if not self.jogador.vivo:
                self.estado = ESTADO_DERROTA
            if self.estado != ESTADO_JOGANDO:
                self.jogador.cancelar_combate()

        elif self.estado == ESTADO_DIALOGO:
            if self.revelacao_a28:
                return
            self.caixa_dialogo.update()
            if getattr(self, 'descoberta_mouse', None) is not None:
                self.descoberta_mouse.update(self.caixa_dialogo.indice)
            if self.na_introducao:
                self.fase.sincronizar_aula(self.caixa_dialogo.indice, INDICE_EXECUCAO_HISTORIA,
                                           INDICE_CORRUPCAO_HISTORIA)

        elif self.estado == ESTADO_ABDUCAO:
            self.temporizador_abducao += 1
            self.fase.update_abduction(self.jogador, self.temporizador_abducao)
            if self.temporizador_abducao >= self.duracao_abducao:
                self._enter_virtual()

        elif self.estado == ESTADO_INFECCAO:
            if self.cena_parasita is None:
                self.cena_parasita = CenaParasita(self.fase,self.jogador,'fusao')
            self.temporizador_infeccao += 1
            if self.cena_parasita.update():
                modo = self.cena_parasita.modo
                self.cena_parasita = None
                if modo == 'fusao':
                    self.fase.fusao_pendente = False
                    self.fase.encontro_pendente = True
                    self.fase.finish_boss_dialogue()
                    self.fase.dialogo_exibido = True
                    self.checkpoints.registrar('arena')
                    self.estado = ESTADO_DIALOGO
                    self.caixa_dialogo.start(self.fase.dados['boss_dialogue'],ao_concluir=self._resume_from_dialogue)
                else:
                    self.fase.libertacao_concluida = True
                    self.estado = ESTADO_JOGANDO
                    tipo, falas = self.fase._after_defeat(self.jogador)
                    self.checkpoints.registrar('vitoria')
                    if tipo == 'dialogue':
                        self.estado = ESTADO_DIALOGO
                        self.caixa_dialogo.start(falas,ao_concluir=self._resume_from_dialogue)

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
        elif self.estado == ESTADO_DESLIGAMENTO:
            if self.encerramento.update():
                self.estado = ESTADO_DIALOGO
                self._iniciar_epilogo()

    def _resume_from_dialogue(self):
        if self.estado == ESTADO_DIALOGO:
            if getattr(self.fase, 'encontro_pendente', False):
                self._iniciar_cena_parasita('fusao')
            else:
                self.estado = ESTADO_JOGANDO

    def _advance_level(self):
        if not hasattr(self.fase, 'identificador'):
            return
        identificador = self.fase.identificador
        if self.fase is self._fase_saida_processada:
            return
        self._fase_saida_processada = self.fase
        self.eventos_campanha.emitir(FaseConcluida(identificador))
        self._load_campus(RETORNOS[identificador], chegada=identificador)

    # ------------------------------------------------------------------
    def _draw(self):
        if self.estado == ESTADO_MENU:
            self._draw_menu()
        elif self.estado == ESTADO_SELECAO_PERSONAGEM:
            self.interface_inicial.draw_selection(self.tela, self.indice_personagem)
        elif self.estado == ESTADO_ENTRADA_NOME:
            self.interface_inicial.draw_name_entry(self.tela, self.nome_digitado,
                                          self.personagem_escolhido, self.erro_nome)
        elif self.estado == ESTADO_INTRODUCAO or (self.estado == ESTADO_PAUSA
                                                  and self.estado_retorno_pausa == ESTADO_INTRODUCAO):
            self.introducao.desenhar(self.tela)
            if self.estado == ESTADO_PAUSA:
                self._draw_overlay('PAUSADO', 'ESC continuar / F pular')
        elif self.estado == ESTADO_DESLIGAMENTO or (self.estado == ESTADO_PAUSA and self.estado_retorno_pausa == ESTADO_DESLIGAMENTO):
            self.encerramento.draw(self.tela)
            if self.estado == ESTADO_PAUSA:
                self._draw_overlay('PAUSADO', 'ESC para continuar')
        elif self.estado == ESTADO_TRANSFORMACAO_CHEFE or (self.estado == ESTADO_PAUSA
                                                        and self.estado_retorno_pausa == ESTADO_TRANSFORMACAO_CHEFE):
            self.transicao_chefe.draw(self.tela)
            if self.caixa_dialogo.ativo:
                self.caixa_dialogo.draw(self.tela)
            if self.estado == ESTADO_PAUSA:
                self._draw_overlay('PAUSADO', 'ESC para continuar')
        elif self.estado in (ESTADO_JOGANDO, ESTADO_DIALOGO, ESTADO_PAUSA, ESTADO_ABDUCAO, ESTADO_INFECCAO):
            em_abducao = self.estado == ESTADO_ABDUCAO or (
                self.estado == ESTADO_PAUSA and self.estado_retorno_pausa == ESTADO_ABDUCAO)
            if em_abducao:
                self.fase.draw(self.tela, ocultar_professores=True)
            else:
                self.fase.draw(self.tela)
                self.jogador.draw(self.tela, self.fase.camera)
            if self.na_introducao:
                self.fase.draw_apresentacao(self.tela, self.caixa_dialogo.indice,
                                             INDICE_MEMORIA_HISTORIA, INDICE_EXECUCAO_HISTORIA)
            if not self.na_introducao and not self.revelacao_a28:
                self.painel_informacoes.draw(self.tela, self.jogador, self.fase.nome, self.fase.chefe)
                if getattr(self.fase, 'biblioteca', None):
                    self.fase.biblioteca.desenhar_objetivos(self.tela)
                if self.estado not in (ESTADO_ABDUCAO, ESTADO_INFECCAO) and not (
                        self.estado == ESTADO_PAUSA and self.estado_retorno_pausa in (ESTADO_ABDUCAO, ESTADO_INFECCAO)):
                    self.painel_informacoes.draw_controls_hint(self.tela, self.jogador)
                    if self.checkpoints.tempo_mensagem:
                        imagem = self.interface_inicial.fonte_pequena.render(self.checkpoints.mensagem,True,(150,240,210))
                        self.tela.blit(imagem,(28,150))
            if self.estado == ESTADO_ABDUCAO or (self.estado == ESTADO_PAUSA
                                                  and self.estado_retorno_pausa == ESTADO_ABDUCAO):
                self.fase.draw_abduction(self.tela, self.jogador,
                                           self.temporizador_abducao/self.duracao_abducao)
            if self.estado == ESTADO_INFECCAO or (self.estado == ESTADO_PAUSA
                                                 and self.estado_retorno_pausa == ESTADO_INFECCAO):
                if self.cena_parasita is not None:
                    self.cena_parasita.draw(self.tela)
            if self.estado == ESTADO_DIALOGO and not self.revelacao_a28:
                if getattr(self, 'descoberta_mouse', None) is not None:
                    self.descoberta_mouse.draw(self.tela, self.fase.camera, self.jogador)
                self.caixa_dialogo.draw(self.tela)
            if self.estado == ESTADO_PAUSA and not self.revelacao_a28:
                self._draw_overlay("PAUSADO", "ESC continuar / F5 salvar checkpoint")
        elif self.estado == ESTADO_CARTAO_FASE:
            self.tela.fill(configuracoes.COR_FUNDO)
            self._draw_overlay(self.fase.nome, "Pressione ENTER para começar")
            dica = getattr(self.fase, 'dados', {}).get('dica')
            if dica:
                imagem = self.painel_informacoes.fonte_pequena.render(dica, True, configuracoes.COR_TEXTO)
                self.tela.blit(imagem, imagem.get_rect(center=(480, 380)))
        elif self.estado == ESTADO_DERROTA:
            self.tela.fill((25, 10, 15))
            self._draw_overlay("VOCÊ FOI REPROVADO(A)...", "R para checkpoint / ENTER para menu")
        elif self.estado == ESTADO_FIM_CONTEUDO:
            self.tela.fill((10, 25, 18))
            self._draw_overlay("A JORNADA CONTINUA", "Fim do conteúdo disponível. ENTER para voltar ao menu")
            texto = self.painel_informacoes.fonte_pequena.render(
                'A IFVania segue ativa. A energia da escola ainda precisa ser desligada.',
                True, configuracoes.COR_TEXTO)
            self.tela.blit(texto, texto.get_rect(center=(configuracoes.LARGURA_TELA//2, 340)))

        if self.estado == ESTADO_VITORIA:
            fachada = recursos.load_image('menu/fachada_escola.png', self.tela.get_size())
            self.tela.blit(fachada, (0, 0))
            aurora = pygame.Surface(self.tela.get_size(), pygame.SRCALPHA)
            aurora.fill((255, 193, 118, 35))
            self.tela.blit(aurora, (0, 0))
            self._draw_overlay('Escola livre. Aula encerrada.', 'ENTER para voltar ao menu')
        if self.revelacao_a28 and self.estado in (ESTADO_DIALOGO, ESTADO_JOGANDO, ESTADO_PAUSA):
            # As faixas do quarto cedem em ritmos diferentes à imagem do A28.
            largura, altura = self.tela.get_size()
            for y in range(0, altura, 12):
                limite = max(0, min(largura, round(largura*(self.revelacao_a28/45)
                                                   + ((y*37) % 131)-65)))
                if limite:
                    area = pygame.Rect(largura-limite, y, limite, 12)
                    self.tela.blit(self.quarto_em_transicao, area, area)
            if self.estado == ESTADO_PAUSA:
                self._draw_overlay("PAUSADO", "ESC continuar / F5 salvar checkpoint")
        pygame.display.flip()

    def _draw_overlay(self, titulo, subtitulo):
        sobreposicao = pygame.Surface((configuracoes.LARGURA_TELA, configuracoes.ALTURA_TELA), pygame.SRCALPHA)
        sobreposicao.fill((0, 0, 0, 150))
        self.tela.blit(sobreposicao, (0, 0))
        self.painel_informacoes.draw_center_text(self.tela, titulo, subtitulo)

    def _draw_menu(self):
        self.interface_inicial.draw_menu(self.tela, self.indice_menu)
        if self.checkpoints.armazem.erro:
            texto = self.interface_inicial.fonte_pequena.render(self.checkpoints.armazem.erro,True,(240,180,100))
            self.tela.blit(texto,(56,478))
