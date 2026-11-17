"""Bugs com ataques anunciados e reação de dano do inimigo comum."""
import pygame
from entidades.inimigo import Inimigo
from entidades.projetil import Projetil
from entidades.estrategias_inimigos import EstrategiaCorpoACorpo, EstrategiaLancador
from sistema.maquina_estados import MaquinaEstados


class BugCombate(Inimigo):
    def __init__(self, x, y, lancador=False, estrategia=None):
        super().__init__(x, y, vida=3 if lancador else 2)
        self.lancador = lancador
        self.estrategia = estrategia or (EstrategiaLancador() if lancador else EstrategiaCorpoACorpo())
        self.estados = MaquinaEstados('patrulhar', {
            'patrulhar': {'preparar'}, 'preparar': {'atacar', 'recuperar'},
            'atacar': {'recuperar'}, 'recuperar': {'patrulhar'}})
        self.tempo_acao = 40
        self.projeteis = pygame.sprite.Group()
        self.direcao_ataque = 1

    def atualizar_combate(self, jogador, solidos):
        self.projeteis.update(solidos)
        if self.temporizador_recuo:
            if self.estados.estado in ('preparar', 'atacar'):
                self.estados.mudar('recuperar')
            self.tempo_acao = 32
            super().update(solidos)
            return
        estado = self.estados.estado
        if estado == 'patrulhar':
            super().update(solidos)
        else:
            self.brilho_dano = max(0, self.brilho_dano-1)
            self.tempo_barra_vida = max(0, self.tempo_barra_vida-1)
            self.velocidade.x = self.direcao_ataque*4 if estado == 'atacar' and not self.lancador else 0
            self.move_and_collide_x(solidos)
            self.apply_gravity()
            self.move_and_collide_y(solidos)
        self.tempo_acao -= 1
        if self.tempo_acao > 0:
            return
        if estado == 'patrulhar':
            if self.estrategia.escolher(self, jogador) == 'preparar':
                self.direcao_ataque = 1 if jogador.rect.centerx >= self.rect.centerx else -1
                self.estados.mudar('preparar')
                self.tempo_acao = 32 if self.lancador else 24
        elif estado == 'preparar':
            self.estados.mudar('atacar')
            self.tempo_acao = 12
            if self.lancador:
                self.projeteis.add(self.criar_disparo())
        elif estado == 'atacar':
            self.estados.mudar('recuperar')
            self.tempo_acao = 38
        else:
            self.estados.mudar('patrulhar')
            self.velocidade.x = self.direcao_patrulha*self.rapidez
            self.tempo_acao = 30

    def criar_disparo(self):
        return Projetil(*self.rect.center, (self.direcao_ataque, 0), dono='boss', velocidade=4)

    def areas_dano(self):
        areas = [(projetil.rect, 1) for projetil in self.projeteis]
        if not self.lancador and self.estados.estado == 'atacar' and not self.temporizador_recuo:
            areas.append((self.rect, 1))
        return areas

    def reagir_bloqueio(self, area):
        if area is self.rect and self.estados.estado == 'atacar':
            self.estados.mudar('recuperar')
            self.tempo_acao = 38
            self.temporizador_recuo = 6
            self.velocidade.x = -self.direcao_ataque*3

    def draw(self, superficie, camera):
        super().draw(superficie, camera)
        destino = camera.apply(self.rect)
        if self.estados.estado == 'preparar':
            pygame.draw.line(superficie, (255, 197, 98), destino.midtop,
                             (destino.centerx+self.direcao_ataque*14, destino.top-6), 3)
        if self.lancador:
            pygame.draw.circle(superficie, (117, 204, 226), destino.center, 5, 2)
        for projetil in self.projeteis:
            projetil.draw(superficie, camera)


class BugGuarda(BugCombate):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.vida = self.vida_maxima = 4
        self.reforcado = False
        self.brilho_bloqueio = 0

    def take_damage(self, quantidade, recuo=(0, 0)):
        frontal = recuo[0]*self.direcao_ataque < 0
        protegido = self.estados.estado in ('patrulhar', 'preparar') or self.reforcado
        if self.vivo and quantidade == 1 and frontal and protegido:
            self.brilho_bloqueio = 8
            from sistema.sons import tocar
            tocar('bloqueio')
            return
        super().take_damage(quantidade, recuo)

    def atualizar_combate(self, jogador, solidos):
        self.brilho_bloqueio = max(0, self.brilho_bloqueio-1)
        super().atualizar_combate(jogador, solidos)

    def draw(self, superficie, camera):
        super().draw(superficie, camera)
        destino = camera.apply(self.rect)
        cor = (255, 231, 166) if self.brilho_bloqueio else (129, 194, 219)
        x = destino.centerx+self.direcao_ataque*21
        pygame.draw.line(superficie, cor, (x, destino.top+4), (x, destino.bottom-4), 4)


class BugRetransmissor(BugCombate):
    def __init__(self, x, y):
        super().__init__(x, y, lancador=True)

    def draw(self, superficie, camera):
        super().draw(superficie, camera)
        destino = camera.apply(self.rect)
        pygame.draw.circle(superficie, (198, 157, 241), destino.midtop, 9, 2)


class BugArquivo(BugCombate):
    def __init__(self, x, y):
        super().__init__(x, y, lancador=True)

    def criar_disparo(self):
        from entidades.projeteis_campus import FichaArquivo
        return FichaArquivo(*self.rect.center, self.direcao_ataque)


class BugRepetidor(BugCombate):
    """Repete uma sequência curta, legível antes da travessia da bancada."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.origem_repeticao = x

    def atualizar_combate(self, jogador, solidos):
        super().atualizar_combate(jogador, solidos)
        if self.estados.estado == 'patrulhar' and abs(self.rect.x-self.origem_repeticao) > 48:
            self.velocidade.x = -self.rapidez if self.rect.x > self.origem_repeticao else self.rapidez
            self.direcao_patrulha = 1 if self.velocidade.x > 0 else -1

    def draw(self, superficie, camera):
        super().draw(superficie, camera)
        destino = camera.apply(self.rect)
        pygame.draw.circle(superficie, (139, 217, 216), destino.center, 15, 1)
