"""Checkpoint de campanha e adaptação entre dados versionados e cenas vivas."""
from copy import deepcopy
from sistema.salvamento import ArmazemSalvamento
from sistema.habilidades import Habilidade
from sistema.eventos_campanha import ChefeDerrotado, FaseConcluida, ObjetivoConcluido


class ControleCheckpoints:
    def __init__(self, jogo, caminho=None):
        self.jogo = jogo
        self.armazem = ArmazemSalvamento(caminho)
        self.ativo = caminho is not None
        self.restaurando = False
        self.checkpoint = None
        self.marcos = set()
        self.mensagem = ''
        self.tempo_mensagem = 0
        self.assinatura_progresso = None

    def progresso(self):
        progresso = self.jogo.progresso_campanha
        return {'chefes': sorted(progresso.chefes_derrotados),
                'fases': sorted(progresso.fases_concluidas),
                'objetivos': [list(item) for item in sorted(progresso.objetivos_concluidos)]}

    def registrar(self, marco='entrada'):
        jogo = self.jogo
        if self.restaurando or not jogo.jogador or not hasattr(jogo.fase, 'identificador') and not hasattr(jogo.fase, 'setor'):
            return
        fase, jogador = jogo.fase, jogo.jogador
        posicao = jogador.rect.topleft
        if hasattr(fase,'_grounded_spawn'):
            try:
                posicao = fase._grounded_spawn(*posicao)
            except ValueError:
                posicao = fase.surgimento_jogador
        corpo = jogador.rect.copy()
        corpo.topleft = posicao
        if any(corpo.colliderect(perigo) for perigo in fase.mapa_blocos.perigos):
            posicao = fase.surgimento_jogador
        cena = {'tipo': 'campus' if hasattr(fase,'setor') else 'fase', 'indice': jogo.indice_fase,
                'posicao': list(posicao), 'marco': marco}
        if cena['tipo'] == 'campus':
            cena['setor'] = fase.setor
        else:
            cena['infectado'] = fase.infectado
            cena['dialogo_exibido'] = fase.dialogo_exibido
            cena['inimigos_ativos'] = [getattr(inimigo,'identificador_checkpoint',-1) for inimigo in fase.inimigos]
        self.checkpoint = {'versao':1,'nome':jogador.nome,'personagem':jogador.personagem,
                           'vida_maxima':jogador.vida_maxima,'habilidades':sorted(h.name for h in jogador.habilidades),
                           'progresso':self.progresso(),'cena':cena}
        self.marcos.add((id(fase),marco))
        self.salvar()

    def salvar(self):
        if not self.checkpoint:
            return False
        dados = deepcopy(self.checkpoint)
        dados['progresso'] = self.progresso()
        dados['habilidades'] = sorted(h.name for h in self.jogo.jogador.habilidades)
        dados['vida_maxima'] = self.jogo.jogador.vida_maxima
        self.checkpoint = dados
        self.assinatura_progresso = repr(dados['progresso'])+repr(dados['habilidades'])
        sucesso = self.armazem.salvar(dados) if self.ativo else True
        if self.ativo and sucesso:
            self.jogo.interface_inicial.tem_salvamento = True
        self.mensagem = 'Checkpoint salvo' if sucesso else self.armazem.erro
        self.tempo_mensagem = 150
        return sucesso

    def atualizar(self):
        jogo = self.jogo
        self.tempo_mensagem = max(0,self.tempo_mensagem-1)
        fase = jogo.fase
        if not self.checkpoint or not hasattr(fase,'identificador'):
            return
        if jogo.jogador.no_chao and jogo.jogador.vivo:
            x = jogo.jogador.rect.x
            for marco, limite in (('travessia',fase.mapa_blocos.largura*0.46),('arena',fase.chefe.arena.left-80)):
                if x >= limite and (id(fase),marco) not in self.marcos and not fase.chefe.ativo:
                    self.registrar(marco)
        assinatura = repr(self.progresso())+repr(sorted(h.name for h in jogo.jogador.habilidades))
        if assinatura != self.assinatura_progresso:
            self.salvar()

    def continuar(self):
        dados = self.armazem.carregar()
        if dados is None:
            self.jogo.interface_inicial.tem_salvamento = False
            self.mensagem = self.armazem.erro or 'Nenhum jogo salvo.'
            self.tempo_mensagem = 180
            return False
        return self.restaurar(dados)

    def retomar(self):
        if not self.checkpoint:
            return False
        dados = deepcopy(self.checkpoint)
        dados['progresso'] = self.progresso()
        dados['habilidades'] = sorted(h.name for h in self.jogo.jogador.habilidades)
        return self.restaurar(dados)

    def restaurar(self, dados):
        if not self.armazem.validar(dados):
            return False
        jogo = self.jogo
        cena = dados['cena']
        self.restaurando = True
        try:
            jogo._iniciar_sessao_campanha()
            jogo.nome_jogador = dados['nome']
            jogo.personagem_escolhido = dados['personagem']
            progresso = dados['progresso']
            for identificador in progresso['chefes']: jogo.eventos_campanha.emitir(ChefeDerrotado(identificador))
            for identificador in progresso['fases']: jogo.eventos_campanha.emitir(FaseConcluida(identificador))
            for fase,objetivo in progresso['objetivos']: jogo.eventos_campanha.emitir(ObjetivoConcluido(fase,objetivo))
            jogo._load_level(cena['indice'],novo_jogador=True)
            jogador = jogo.jogador
            jogador.habilidades = {Habilidade[nome] for nome in dados['habilidades']}
            jogador.vida_maxima = dados['vida_maxima']
            if cena['tipo'] == 'campus':
                jogo._load_campus(cena['setor'])
            else:
                fase = jogo.fase
                ativos = cena.get('inimigos_ativos')
                if isinstance(ativos,list):
                    for inimigo in list(fase.inimigos):
                        if getattr(inimigo,'identificador_checkpoint',-1) not in ativos:
                            inimigo.kill()
                if cena.get('infectado') and fase.exige_infeccao:
                    fase.infectado = fase.dialogo_exibido = True
                    fase.encontro_pendente = False
                    fase.inimigos.empty()
                    fase.chefe.activate()
            posicao = tuple(cena['posicao'])
            corpo = jogador.rect.copy()
            corpo.topleft = posicao
            mapa = jogo.fase.mapa_blocos
            apoio = corpo.move(0,2)
            seguro = 0 <= corpo.left and corpo.right <= mapa.largura and not any(corpo.colliderect(s) for s in mapa.solidos) and any(apoio.colliderect(s) for s in mapa.solidos)
            jogador.respawn(*(posicao if seguro else jogo.fase.surgimento_jogador))
            jogador.no_chao = True
            jogo.fase.camera.update(jogador.rect)
            jogo.caixa_dialogo.ativo = False
            jogo.na_introducao = False
            jogo.tutorial_luva = None
            jogo.transicao_chefe = None
            jogo.cena_parasita = None
            jogo.estado = 'playing'
            self.checkpoint = deepcopy(dados)
            self.marcos = {(id(jogo.fase),cena.get('marco','entrada'))}
            self.assinatura_progresso = repr(self.progresso())+repr(sorted(h.name for h in jogador.habilidades))
            self.mensagem,self.tempo_mensagem = 'Checkpoint retomado',150
            return True
        finally:
            self.restaurando = False
