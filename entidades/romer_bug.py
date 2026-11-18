"""Primeiro professor-chefe: RomerBug se transforma em SpeedBug a 50% de vida."""
import pygame

from sistema import recursos
from entidades.chefe import Chefe
from entidades.projetil import Projetil


class ProjetilProfessor(Projetil):
    """Avião de papel ou medalha, com colisão e expiração de Projetil."""

    def __init__(self, origem, direcao, tipo):
        self.tipo = tipo
        tamanho = (26, 14) if tipo == "plane" else (18, 22)
        velocidade = 4.5 if tipo == "plane" else 5.0
        super().__init__(*origem, direcao, dono="boss", velocidade=velocidade)
        nome_arquivo = "aviao_papel.png" if tipo == "plane" else "medalha.png"
        self.image = recursos.load_image(f"projeteis/{nome_arquivo}", tamanho)
        if tipo == "plane":
            self.image = pygame.transform.rotate(self.image, -self.velocidade.as_polar()[1])
        self.rect = self.image.get_rect(center=origem)
        self.posicao.update(self.rect.center)


class RomerBug(Chefe):
    """Duelista de curta distância: aproximação, sequência e contra-ataque.

    SpeedBug é a segunda forma da mesma instância: vida, recompensa e estado
    de derrota continuam pertencendo ao mesmo chefe.
    """

    VELOCIDADE_CORRIDA = 3.4
    VELOCIDADE_CAMINHADA = 2.15
    ACELERACAO = 0.35
    DURACAO_TRANSFORMACAO = 45

    def __init__(self, x, y, nome="RomerBug", disciplina="Lógica de Blocos",
                 cor=(50, 65, 105), vida=16, arena=None,
                 arquivo_figura="chefes/romerbug_0.png", transformacao_cinematica=False):
        super().__init__(x, y, nome, disciplina, cor, vida, arena, arquivo_figura)
        self.direcao_investida = 1
        self.distancia_investida = 0.0
        self.estado_ataque = 'aproximar'
        self.transformado = False
        self.transformacao_cinematica = transformacao_cinematica
        self.cinematica_pendente = False
        self.temporizador_transformacao = 0
        self.ciclo_combate = 0
        self.no_chao = False
        self.distancia_passada = 0.0
        self.deslocamento_real = 0.0
        self.quadro_movimento = 0
        self.solidos_combate = ()
        self.golpe_atual = 'cruzado'
        self.etapa_sequencia = 0
        self.interrupcoes = 0
        self.duracao_preparacao = 28
        self.temporizador_ataque = 24
        self.figuras_formas = {}
        self.figuras_movimento = {}
        self.poses_corpo = {}
        for forma,pasta in (('romerbug','romerbug_sombrio'),('speedbug','speedbug_corredor')):
            poses = recursos.load_character_frames([f'chefes/{pasta}/pose_{i}.png' for i in range(6)])
            self.poses_corpo[forma] = {1: poses, -1: [recursos.espelhar_quadro(p) for p in poses]}
            self.figuras_formas[forma] = {direcao:[quadros[0],quadros[3]] for direcao,quadros in self.poses_corpo[forma].items()}
            self.figuras_movimento[forma] = {direcao:[quadros[1],quadros[2]]*3 for direcao,quadros in self.poses_corpo[forma].items()}
        self._animate_form()

    def take_damage(self, quantidade, recuo=(0, 0)):
        if not self.ativo or not self.vivo or self.temporizador_transformacao > 0 or self.cinematica_pendente:
            return
        super().take_damage(quantidade, recuo)
        if not self.vivo:
            self.projeteis.empty()
            self.velocidade.x = 0
            return
        if not self.transformado and self.vida <= self.vida_maxima * 0.5:
            self.transformado = True
            self.cinematica_pendente = self.transformacao_cinematica
            self.nome = 'RomerBug' if self.cinematica_pendente else 'SpeedBug'
            self.temporizador_transformacao = self.DURACAO_TRANSFORMACAO
            self.estado_ataque = 'aproximar'
            self.temporizador_ataque = 18
            self.velocidade.update(0, 0)
            self.deslocamento_real = 0
            self.projeteis.empty()
            self._animate_form()
        elif self.estado_ataque not in ('executar', 'recuperar') and self.interrupcoes < 2:
            # Dois impactos podem interromper a aproximação/preparação. Depois,
            # a postura firme anuncia resposta e impede aprisionamento por combo.
            self.interrupcoes += 1
            self.estado_ataque = 'recuo'
            self.temporizador_ataque = 10
            self.velocidade.x = max(-4, min(4, recuo[0]))
        if self.transformado:
            self.etapa = 2

    def finish_cinematic(self):
        self.cinematica_pendente = False
        self.temporizador_transformacao = 0
        self.nome = 'SpeedBug'
        self.temporizador_ataque = 18
        self.estado_ataque = 'aproximar'
        self.velocidade.update(0, 0)
        self.brilho_dano = 0
        self.deslocamento_real = 0
        self.interrupcoes = 0
        self._animate_form()

    def choose_attack(self, jogador):
        distancia = abs(jogador.rect.centerx-self.rect.centerx)
        if self.ciclo_combate % 4 == 3:
            return 'especial'
        if distancia > 130:
            return 'avanco'
        return 'chute' if self.ciclo_combate % 2 else 'cruzado'

    def lancar_especial(self, jogador):
        from entidades.poderes_chefes import PulsoSombrio
        origem = (self.rect.centerx+self.direcao_investida*24,self.rect.bottom-36)
        self.projeteis.add(PulsoSombrio(origem,(self.direcao_investida,0)))

    def preparar_ataque(self, jogador, solidos=(), permitir_reposicionar=True):
        self.golpe_atual = self.choose_attack(jogador)
        self.etapa_sequencia = 0
        self._preparar_golpe(jogador)

    def _preparar_golpe(self, jogador):
        self.estado_ataque = 'preparar'
        self.direcao_investida = 1 if jogador.rect.centerx >= self.rect.centerx else -1
        self.direcao_olhar = self.direcao_investida
        self.distancia_investida = 0
        self.velocidade.x = 0
        # A direção fica fixa até o próximo golpe. Entre golpes há novo aviso.
        self.temporizador_ataque = (20 if self.transformado else 28) if self.etapa_sequencia == 0 else 18
        self.duracao_preparacao = self.temporizador_ataque
        from sistema.sons import tocar
        tocar('aviso_corporal')

    def _recuperar(self, bloqueado=False):
        self.estado_ataque = 'recuperar'
        self.temporizador_ataque = 44 if bloqueado else 32 if self.transformado else 40
        self.velocidade.x = 0
        self.deslocamento_real = 0
        self.ciclo_combate += 1

    def reagir_bloqueio(self, area):
        if self.estado_ataque == 'executar':
            self._recuperar(bloqueado=True)

    def _mover(self, solidos):
        anterior = self.posicao.x
        esquerda, direita = self.arena.left, self.arena.right-self.largura
        self.velocidade.x = max(esquerda, min(direita, anterior+self.velocidade.x))-anterior
        bloqueado = any(s.top < self.rect.bottom and s.bottom > self.rect.top and (
            self.velocidade.x < 0 and self.rect.left == s.right or
            self.velocidade.x > 0 and self.rect.right == s.left) for s in solidos)
        if bloqueado:
            self.velocidade.x = 0
            self.posicao.x = float(self.rect.x)
        parede = self.move_and_collide_x(solidos)
        self.apply_gravity()
        self.no_chao = self.move_and_collide_y(solidos)
        self.deslocamento_real = self.posicao.x-anterior
        if self.no_chao:
            self.distancia_passada += abs(self.deslocamento_real)
        if self.estado_ataque == 'executar':
            self.distancia_investida += abs(self.deslocamento_real)
            if parede or bloqueado:
                self._recuperar()

    def update(self, jogador, solidos):
        if not self.ativo or not self.vivo or self.cinematica_pendente:
            return
        self.solidos_combate = solidos
        self._tempo += 1
        self.brilho_dano = max(0, self.brilho_dano-1)
        if self.temporizador_transformacao > 0:
            self.temporizador_transformacao -= 1
            self._animate_form()
            return
        distancia = jogador.rect.centerx-self.rect.centerx
        self.temporizador_ataque = max(0, self.temporizador_ataque-1)
        if self.estado_ataque == 'aproximar':
            # Persegue o aluno em toda a arena, sem trilho de +/-24 px.
            self.direcao_olhar = 1 if distancia >= 0 else -1
            rapidez = self.VELOCIDADE_CORRIDA if self.transformado else self.VELOCIDADE_CAMINHADA
            alvo = self.direcao_olhar*rapidez if abs(distancia) > 74 else 0
            self.velocidade.x += max(-self.ACELERACAO, min(self.ACELERACAO, alvo-self.velocidade.x))
            if self.temporizador_ataque == 0 and (abs(distancia) <= 105 or abs(distancia) > 200):
                self.preparar_ataque(jogador)
        elif self.estado_ataque == 'preparar':
            self.velocidade.x = 0
            if self.temporizador_ataque == 0:
                self.estado_ataque = 'executar'
                self.temporizador_ataque = 18 if self.golpe_atual in ('especial','raio') else 16 if self.golpe_atual in ('avanco','barrigada') else 9
                if self.golpe_atual in ('especial','raio'):
                    self.lancar_especial(jogador)
                from sistema.sons import tocar
                tocar('golpe_corporal')
        elif self.estado_ataque == 'executar':
            rapidez = (6 if self.transformado else 4.5) if self.golpe_atual in ('avanco','barrigada') else 0 if self.golpe_atual in ('especial','raio') else 1.8
            self.velocidade.x = self.direcao_investida*rapidez
            if self.temporizador_ataque == 0:
                self.etapa_sequencia += 1
                limite = 3 if self.transformado else 2
                if self.golpe_atual not in ('especial','raio') and self.etapa_sequencia < limite and abs(distancia) < 145:
                    self.golpe_atual = ('chute' if self.etapa_sequencia == limite-1 else 'cruzado')
                    self._preparar_golpe(jogador)
                else:
                    self._recuperar()
        elif self.estado_ataque == 'recuo':
            self.velocidade.x *= 0.78
            if self.temporizador_ataque == 0:
                self.estado_ataque = 'aproximar'
                self.temporizador_ataque = 6
        elif self.estado_ataque == 'recuperar':
            self.velocidade.x = 0
            if self.temporizador_ataque == 0:
                self.interrupcoes = 0
                self.estado_ataque = 'aproximar'
                self.temporizador_ataque = 8
        self._mover(solidos)
        self.projeteis.update(solidos)
        self._animate_form()

    def _animate_form(self):
        forma = 'speedbug' if self.transformado else 'romerbug'
        if self.temporizador_transformacao > 0:
            self.image = self.figuras_formas[forma][self.direcao_olhar][0]
        elif self.estado_ataque == 'executar':
            indice = 5 if self.golpe_atual in ('especial','raio','barrigada') else 4 if self.golpe_atual in ('chute','varrida') else 3
            self.image = self.poses_corpo[forma][self.direcao_olhar][indice]
        elif self.estado_ataque == 'preparar':
            self.image = self.poses_corpo[forma][self.direcao_olhar][0]
        elif abs(self.deslocamento_real) > 0.01:
            passo = 11 if self.transformado else 7
            self.quadro_movimento = int(self.distancia_passada/passo) % 6
            self.image = self.figuras_movimento[forma][self.direcao_olhar][self.quadro_movimento]
        else:
            self.image = self.figuras_formas[forma][self.direcao_olhar][0]

    def area_golpe(self):
        largura = 86 if self.golpe_atual in ('chute','varrida') else 74 if self.golpe_atual == 'barrigada' else 62
        altura = 22 if self.golpe_atual == 'varrida' else 40
        area = pygame.Rect(0, 0, largura, altura)
        area.bottom = self.rect.bottom-2 if self.golpe_atual == 'varrida' else self.rect.bottom-16
        area.left = self.rect.centerx if self.direcao_investida > 0 else self.rect.centerx-largura
        for solido in self.solidos_combate:
            if area.colliderect(solido):
                if self.direcao_investida > 0:
                    area.width = max(0, solido.left-area.left)
                else:
                    direita = area.right
                    area.left = min(direita, solido.right)
                    area.width = direita-area.left
        return area

    def origem_ataque(self, area):
        if any(projetil.rect is area for projetil in self.projeteis):
            return area.center
        return self.rect.center

    def get_all_hit_rects(self):
        if (self.temporizador_transformacao > 0 or self.cinematica_pendente
                or not self.ativo or not self.vivo):
            return []
        ataques = [(p.rect, p.dano) for p in self.projeteis]
        if self.estado_ataque == 'executar' and self.golpe_atual not in ('especial','raio'):
            ataques.append((self.area_golpe(), 1))
        return ataques

    def draw(self, superficie, camera):
        imagem = self.get_draw_image()
        destino = imagem.get_rect(midbottom=camera.apply(self.rect).midbottom)
        # Peso ancorado pelos pés; retirar balanço e inclinação contínuos do corpo.
        if self.estado_ataque == 'preparar':
            destino.x -= self.direcao_olhar*3
        elif self.estado_ataque == 'executar':
            destino.x += self.direcao_olhar*5
        superficie.blit(imagem, destino)
        if self.vivo and self.brilho_dano > 0:
            clarao = imagem.copy()
            clarao.fill((255, 255, 255, 100), special_flags=pygame.BLEND_RGBA_MULT)
            superficie.blit(clarao, destino, special_flags=pygame.BLEND_RGBA_ADD)
        for projetil in self.projeteis:
            projetil.draw(superficie, camera)
        if self.temporizador_transformacao > 0 and not self.cinematica_pendente:
            retangulo = camera.apply(self.rect)
            pygame.draw.circle(superficie, (255, 200, 65), retangulo.center, 40, 3)
