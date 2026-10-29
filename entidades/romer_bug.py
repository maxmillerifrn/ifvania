"""Primeiro professor-chefe: RomerBug se transforma em SpeedBug a 50% de vida."""
import pygame

import recursos
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
    """Professor que alterna lançamentos, pausa e investida nas duas formas.

    SpeedBug é a segunda forma da mesma instância: vida, recompensa e estado
    de derrota continuam pertencendo ao mesmo chefe.
    """

    VELOCIDADE_CORRIDA = 2.6
    VELOCIDADE_CAMINHADA = 1.15
    ACELERACAO = 0.20
    FRENAGEM = 0.32
    DURACAO_TRANSFORMACAO = 45
    DISPAROS_POR_CICLO = 2
    INTERVALO_AVIAO = 108
    INTERVALO_MEDALHA = 66
    PAUSA_ANTES_INVESTIDA = 48
    VELOCIDADE_DISPARANDO = 0.55

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
        self.temporizador_lancamento = 0
        self.disparos_no_ciclo = 0
        self.origem_ciclo = float(x)
        self.mira_disparo = pygame.Vector2(x, y)
        self.no_chao = False
        self.distancia_passada = 0.0
        self.quadro_movimento = 0
        self.alvo_patrulha = x - 80
        self.temporizador_ataque = 70
        caminhos = [f"chefes/{forma}_{i}.png"
                 for forma in ("romerbug", "speedbug") for i in range(2)]
        caminhos += [f"chefes/{forma}_{acao}_{i}.png"
                  for forma, acao in (("romerbug", "caminhada"), ("speedbug", "corrida"))
                  for i in range(6)]
        quadros = dict(zip(caminhos, recursos.load_character_frames(caminhos)))
        self.figuras_formas = {}
        for forma in ("romerbug", "speedbug"):
            self.figuras_formas[forma] = {
                1: [quadros[f"chefes/{forma}_{i}.png"] for i in range(2)],
                -1: [pygame.transform.flip(quadros[f"chefes/{forma}_{i}.png"], True, False) for i in range(2)],
            }
        self.figuras_movimento = {}
        for forma, acao in (("romerbug", "caminhada"), ("speedbug", "corrida")):
            self.figuras_movimento[forma] = {
                1: [quadros[f"chefes/{forma}_{acao}_{i}.png"] for i in range(6)],
                -1: [pygame.transform.flip(quadros[f"chefes/{forma}_{acao}_{i}.png"], True, False) for i in range(6)],
            }
        self.fonte_transformacao = pygame.font.Font(None, 22)
        self._animate_form()

    def take_damage(self, quantidade, recuo=(0, 0)):
        if not self.ativo or not self.vivo or self.temporizador_transformacao > 0:
            return
        super().take_damage(quantidade, recuo)
        if not self.vivo:
            self.projeteis.empty()
            return
        if not self.transformado and self.vida <= self.vida_maxima * 0.5:
            self.transformado = True
            self.cinematica_pendente = self.transformacao_cinematica
            self.nome = "RomerBug" if self.cinematica_pendente else "SpeedBug"
            self.etapa = 2
            self.temporizador_transformacao = self.DURACAO_TRANSFORMACAO
            self.temporizador_ataque = 30
            self.temporizador_lancamento = 0
            self.estado_ataque = 'aproximar'
            self.disparos_no_ciclo = 0
            self.origem_ciclo = self.posicao.x
            self.velocidade.update(0, 0)
            self.distancia_passada = 0
            self.projeteis.empty()
            self._animate_form()
        if self.transformado:
            # Este chefe possui duas formas, sem uma terceira fase a 20%.
            self.etapa = 2

    def finish_cinematic(self):
        self.cinematica_pendente = False
        self.temporizador_transformacao = 0
        self.nome = 'SpeedBug'
        self.temporizador_ataque = 60
        self.estado_ataque = 'aproximar'
        self.disparos_no_ciclo = 0
        self.origem_ciclo = self.posicao.x
        self.brilho_dano = 0
        self._animate_form()

    def choose_attack(self, jogador):
        return 'medalha' if self.transformado else 'aviao'

    def preparar_ataque(self, jogador, solidos):
        self.estado_ataque = 'preparar'
        self.temporizador_ataque = 36 if self.transformado else 48
        self.direcao_investida = 1 if jogador.rect.centerx >= self.rect.centerx else -1
        self.direcao_olhar = self.direcao_investida
        self.velocidade.x = 0
        self.distancia_investida = 0
        from sons import tocar
        tocar('aviso')

    def preparar_disparo(self, jogador):
        self.estado_ataque = 'preparar_disparo'
        self.temporizador_ataque = 24 if self.transformado else 30
        self.mira_disparo = pygame.Vector2(jogador.rect.center)
        self.direcao_olhar = 1 if self.mira_disparo.x >= self.rect.centerx else -1
        self.velocidade.x = 0
        from sons import tocar
        tocar('aviso')

    def lancar_projetil(self):
        origem = pygame.Vector2(self.rect.centerx+self.direcao_olhar*(self.largura//2+16),
                                self.rect.centery-5)
        direcao = self.mira_disparo-origem
        if direcao.length_squared() == 0:
            direcao.update(self.direcao_olhar, 0)
        self.projeteis.add(ProjetilProfessor(origem, direcao, 'medal' if self.transformado else 'plane'))
        self.disparos_no_ciclo += 1
        self.temporizador_lancamento = 12
        if self.disparos_no_ciclo >= self.DISPAROS_POR_CICLO:
            self.estado_ataque = 'pausa'
            self.temporizador_ataque = self.PAUSA_ANTES_INVESTIDA
        else:
            self.estado_ataque = 'intervalo_disparo'
            self.temporizador_ataque = self.INTERVALO_MEDALHA if self.transformado else self.INTERVALO_AVIAO

    def update(self, jogador, solidos):
        if not self.ativo or not self.vivo or self.cinematica_pendente:
            return
        self._tempo += 1
        self.brilho_dano = max(0, self.brilho_dano-1)
        if self.temporizador_transformacao > 0:
            self.temporizador_transformacao -= 1
            self._animate_form()
            return
        dx = jogador.rect.centerx-self.rect.centerx
        velocidade_alvo = 0
        if self.estado_ataque == 'aproximar':
            if self.transformado:
                velocidade_alvo = self.VELOCIDADE_DISPARANDO*(1 if dx > 0 else -1)
                if abs(self.posicao.x-self.origem_ciclo) >= 24:
                    velocidade_alvo = 0
            else:
                if abs(self.alvo_patrulha-self.posicao.x) < 10:
                    self.alvo_patrulha = self.x_inicial+65 if self.alvo_patrulha < self.x_inicial else self.x_inicial-80
                velocidade_alvo = max(-self.VELOCIDADE_CAMINHADA,
                                      min(self.VELOCIDADE_CAMINHADA, (self.alvo_patrulha-self.posicao.x)*0.1))
            aceleracao = self.FRENAGEM if velocidade_alvo*self.velocidade.x <= 0 else self.ACELERACAO
            self.velocidade.x += max(-aceleracao,min(aceleracao, velocidade_alvo-self.velocidade.x))
            if abs(self.velocidade.x) > 0.15:
                self.direcao_olhar = 1 if self.velocidade.x > 0 else -1
        elif self.estado_ataque == 'intervalo_disparo' and self.transformado:
            alvo = max(self.origem_ciclo-24, min(self.origem_ciclo+24, jogador.rect.x))
            self.velocidade.x = max(-self.VELOCIDADE_DISPARANDO, min(self.VELOCIDADE_DISPARANDO, alvo-self.posicao.x))
        elif self.estado_ataque == 'executar':
            passo = min(6, 160-self.distancia_investida)
            self.velocidade.x = self.direcao_investida*max(0, passo)
            self.distancia_investida += passo
        else:
            self.velocidade.x = 0
        x_anterior = self.rect.x
        parede = self.move_and_collide_x(solidos)
        if self.transformado and self.estado_ataque in ('aproximar','intervalo_disparo'):
            self.posicao.x = max(self.origem_ciclo-24,min(self.origem_ciclo+24,self.posicao.x))
            self.rect.x = round(self.posicao.x)
        x_limitado = max(self.arena.left, min(self.rect.x, self.arena.right-self.largura))
        if x_limitado != self.rect.x or parede:
            self.rect.x = x_limitado
            self.posicao.x = self.rect.x
            self.velocidade.x = 0
            if self.estado_ataque == 'aproximar':
                self.alvo_patrulha = self.posicao.x-parede*80
            elif self.estado_ataque == 'executar':
                self.temporizador_ataque = 1
        self.apply_gravity()
        self.no_chao = self.move_and_collide_y(solidos)
        if self.no_chao:
            self.distancia_passada += abs(self.rect.x-x_anterior)
        self.temporizador_lancamento = max(0, self.temporizador_lancamento-1)
        self.projeteis.update(solidos)
        self.temporizador_ataque -= 1
        if self.temporizador_ataque <= 0:
            if self.estado_ataque in ('aproximar', 'intervalo_disparo'):
                self.preparar_disparo(jogador)
            elif self.estado_ataque == 'preparar_disparo':
                self.lancar_projetil()
            elif self.estado_ataque == 'pausa':
                if self.projeteis:
                    self.temporizador_ataque = 1
                else:
                    self.preparar_ataque(jogador, solidos)
            elif self.estado_ataque == 'preparar':
                self.estado_ataque = 'executar'
                self.temporizador_ataque = 27
            elif self.estado_ataque == 'executar':
                self.estado_ataque = 'recuperar'
                self.temporizador_ataque = 78 if self.transformado else 60
                self.velocidade.x = 0
            else:
                self.disparos_no_ciclo = 0
                self.origem_ciclo = self.posicao.x
                self.estado_ataque = 'aproximar'
                self.temporizador_ataque = 60
        self._animate_form()

    def _animate_form(self):
        forma = "speedbug" if self.transformado else "romerbug"
        if self.temporizador_transformacao > 0:
            self.image = self.figuras_formas[forma][self.direcao_olhar][0]
        elif self.temporizador_lancamento > 0:
            self.image = self.figuras_formas[forma][self.direcao_olhar][1]
        elif self.estado_ataque in ('preparar', 'preparar_disparo', 'pausa', 'recuperar'):
            self.image = self.figuras_formas[forma][self.direcao_olhar][int(self.estado_ataque in ('preparar', 'preparar_disparo'))]
        elif self.transformado and not self.no_chao:
            self.image = self.figuras_movimento[forma][self.direcao_olhar][2]
        elif abs(self.velocidade.x) > 0.15:
            comprimento_passo = 11 if self.transformado else 7
            self.quadro_movimento = int(self.distancia_passada / comprimento_passo) % 6
            self.image = self.figuras_movimento[forma][self.direcao_olhar][self.quadro_movimento]
        else:
            self.image = self.figuras_movimento[forma][self.direcao_olhar][1]

    def get_all_hit_rects(self):
        if (self.temporizador_transformacao > 0 or self.cinematica_pendente
                or not self.ativo or not self.vivo):
            return []
        ataques = [(p.rect, p.dano) for p in self.projeteis]
        if self.estado_ataque == 'executar':
            ataques.append((self.rect, self.dano_contato))
        return ataques

    def draw(self, superficie, camera):
        # Os próprios quadros contêm a oscilação do corpo. Não aplicar o bob
        # flutuante de Chefe, que fazia os pés deslizarem acima do chão.
        self.desenhar_aviso(superficie, camera)
        imagem = self.get_draw_image()
        retangulo = imagem.get_rect(midbottom=camera.apply(self.rect).midbottom)
        superficie.blit(imagem, retangulo)
        if self.vivo and self.brilho_dano > 0:
            clarao = imagem.copy()
            clarao.fill((255, 255, 255, 100), special_flags=pygame.BLEND_RGBA_MULT)
            superficie.blit(clarao, retangulo, special_flags=pygame.BLEND_RGBA_ADD)
        for projetil in self.projeteis:
            projetil.draw(superficie, camera)
        if self.temporizador_transformacao > 0 and not self.cinematica_pendente:
            retangulo = camera.apply(self.rect)
            raio = 36 + (self.DURACAO_TRANSFORMACAO - self.temporizador_transformacao) // 3
            pygame.draw.circle(superficie, (255, 200, 65), retangulo.center, raio, 3)
            texto = self.fonte_transformacao.render("SpeedBug!", True, (255, 215, 80))
            superficie.blit(texto, texto.get_rect(midbottom=(retangulo.centerx, retangulo.top - 12)))

    def desenhar_aviso(self, superficie, camera):
        if not self.ativo or not self.vivo or self.cinematica_pendente or self.temporizador_transformacao:
            return
        if self.estado_ataque == 'recuperar':
            texto = self.fonte_transformacao.render('EXPOSTO', True, (176, 205, 181))
            posicao = camera.apply(self.rect).midbottom
            superficie.blit(texto, texto.get_rect(midbottom=(posicao[0], posicao[1]-85)))
        elif self.estado_ataque == 'preparar_disparo':
            centro = camera.apply(self.rect).center
            rotulo = 'MEDALHA' if self.transformado else 'AVIÃO'
            texto = self.fonte_transformacao.render(rotulo, True, (228, 190, 123))
            superficie.blit(texto, texto.get_rect(midbottom=(centro[0], centro[1]-64)))
            mira = self.mira_disparo-camera.deslocamento
            pygame.draw.circle(superficie, (203, 167, 106), (round(mira.x), round(mira.y)), 9, 1)
        elif self.estado_ataque == 'pausa':
            texto = self.fonte_transformacao.render('PREPARANDO AVANÇO', True, (188, 194, 179))
            centro = camera.apply(self.rect).center
            superficie.blit(texto, texto.get_rect(midbottom=(centro[0], centro[1]-64)))
        elif self.estado_ataque in ('preparar', 'executar'):
            origem = camera.apply(self.rect).midbottom
            destino_x = max(self.arena.left+self.largura//2,
                min(self.arena.right-self.largura//2, self.rect.centerx+self.direcao_investida*160))
            fim = (origem[0]+destino_x-self.rect.centerx, origem[1]-3)
            cor = (226, 172, 109)
            pygame.draw.line(superficie, cor, (origem[0], origem[1]-3), fim, 3)
            pygame.draw.lines(superficie, cor, False,
                [(fim[0]-self.direcao_investida*12, fim[1]-8), fim,
                 (fim[0]-self.direcao_investida*12, fim[1]+8)], 3)
            texto = self.fonte_transformacao.render('INVESTIDA' if self.estado_ataque == 'preparar' else 'RUPTURA', True, cor)
            superficie.blit(texto, texto.get_rect(midbottom=(origem[0], origem[1]-86)))
