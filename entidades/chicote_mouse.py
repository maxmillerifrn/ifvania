"""Mouse preso ao cabo: preparação, estalo e recolhimento do chicote.

O desenho e o dano usam a mesma curva, interrompida ao tocar uma parede.
"""
import math
import pygame


class ChicoteMouse:
    DURACAO = 30
    PREPARACAO = 5
    FIM_GOLPE = 19
    ALCANCE = 100
    RAIO_ACERTO = 12

    def __init__(self):
        self.direcao_olhar = 1
        self.alvos_atingidos = set()
        self.dano = 1
        self.limpar_trajetoria()

    def limpar_trajetoria(self):
        self.trajetoria_anterior = []
        self.trajetoria_atual = []
        self.idade_amostrada = -1

    def start(self, direcao_olhar, dano=1):
        self.direcao_olhar = direcao_olhar
        self.alvos_atingidos.clear()
        self.dano = dano
        self.limpar_trajetoria()

    def age(self, jogador):
        return self.DURACAO - jogador.temporizador_golpe

    def pose(self, jogador):
        idade = self.age(jogador)
        return 0 if idade < self.PREPARACAO else 1 if idade < self.FIM_GOLPE else 2

    def is_striking(self, jogador):
        return jogador.temporizador_golpe > 0 and self.PREPARACAO <= self.age(jogador) < self.FIM_GOLPE

    @staticmethod
    def _smooth(t):
        return t * t * (3 - 2 * t)

    def points(self, jogador, solidos=()):
        if jogador.temporizador_golpe <= 0:
            return []
        idade = self.age(jogador)
        # Pontos de fixação nas mãos das três poses, relativos ao corpo.
        maos = [(-9, -9), (15, -3), (2, 0)]
        hx, hy = maos[self.pose(jogador)]
        mao_logica = pygame.Vector2(jogador.rect.centerx + hx * self.direcao_olhar,
                                      jogador.rect.centery + hy)
        escala = jogador.ESCALA_VISUAL
        mao = pygame.Vector2(jogador.rect.centerx + hx*escala*self.direcao_olhar,
                              jogador.rect.bottom + (hy-jogador.altura/2)*escala)
        # O desenho ampliado da mão não permite iniciar o fio além de uma parede.
        entradas = [solido.clipline(mao_logica, mao) for solido in solidos]
        entradas = [pygame.Vector2(linha[0]) for linha in entradas if linha]
        if entradas:
            mao = min(entradas, key=lambda p: p.distance_squared_to(mao_logica))
        if idade < self.PREPARACAO:
            t = self._smooth(idade / self.PREPARACAO)
            fim = pygame.Vector2(-18 - 12 * t, 12 - 42 * t)
            flexao = -16
        elif idade < self.FIM_GOLPE:
            t = self._smooth((idade - self.PREPARACAO) / (self.FIM_GOLPE - self.PREPARACAO - 1))
            fim = pygame.Vector2(-8 + (self.ALCANCE + 8) * t, -34 + 37 * t)
            flexao = -25 * (1 - t)
        else:
            t = self._smooth((idade - self.FIM_GOLPE) / (self.DURACAO - self.FIM_GOLPE))
            fim = pygame.Vector2(self.ALCANCE * (1 - t) + 7 * t, 6 + 12 * t)
            flexao = 18 * math.sin(t * math.pi)
        fim.x *= self.direcao_olhar
        # A mão acompanha o sprite maior, mas a trajetória da ponta mantém o alcance.
        ponta = mao_logica + fim
        controle = (mao + ponta) / 2 + pygame.Vector2(0, flexao)
        pontos = [mao]
        for i in range(1, 25):
            t = i / 24
            ponto = mao * (1 - t) ** 2 + controle * (2 * (1 - t) * t) + ponta * t * t
            # Segue o fio a partir da mão e para na primeira superfície.
            intersecoes = [s.clipline(pontos[-1], ponto) for s in solidos]
            entradas = [pygame.Vector2(linha[0]) for linha in intersecoes if linha]
            if entradas:
                ponto = min(entradas, key=lambda p: p.distance_squared_to(pontos[-1]))
                pontos.append(ponto)
                break
            pontos.append(ponto)
        return pontos

    def trajetorias(self, jogador, solidos):
        idade = self.age(jogador)
        if idade != self.idade_amostrada:
            self.trajetoria_anterior = (self.trajetoria_atual
                if idade == self.idade_amostrada+1 else [])
            self.trajetoria_atual = self.points(jogador, solidos)
            self.idade_amostrada = idade
        return self.trajetoria_anterior + self.trajetoria_atual

    @staticmethod
    def area_alvo(alvo):
        area = alvo.rect.inflate(8, 16)
        area.midbottom = alvo.rect.midbottom
        return area

    def hit_bounds(self, jogador, solidos=()):
        if not self.is_striking(jogador):
            return None
        pontos = self.trajetorias(jogador, solidos)
        xs, ys = [p.x for p in pontos], [p.y for p in pontos]
        margem = self.RAIO_ACERTO
        return pygame.Rect(min(xs)-margem, min(ys)-margem,
                           max(xs)-min(xs)+2*margem+1, max(ys)-min(ys)+2*margem+1)

    def try_hit(self, jogador, alvo, solidos):
        if (not self.is_striking(jogador) or alvo in self.alvos_atingidos or not alvo.vivo
                or (alvo.rect.centerx-jogador.rect.centerx)*self.direcao_olhar < 0):
            return False
        # Tolerância não atravessa uma parede entre os corpos.
        origem = jogador.rect.center
        if any(parede.clipline(origem, alvo.rect.center) for parede in solidos):
            return False
        self.trajetorias(jogador, solidos)
        area = self.area_alvo(alvo).inflate(2*self.RAIO_ACERTO, 2*self.RAIO_ACERTO)
        segmentos = list(zip(self.trajetoria_atual, self.trajetoria_atual[1:]))
        segmentos += list(zip(self.trajetoria_anterior, self.trajetoria_atual))
        if any(area.clipline(a, b) for a, b in segmentos):
            vida = alvo.vida
            alvo.take_damage(self.dano)
            if alvo.vida < vida:
                from sons import tocar
                tocar('impacto')
                jogador.pausa_impacto = 3 if self.dano > 1 else 2
                self.alvos_atingidos.add(alvo)
                return True
        return False

    def desenhar_carga(self, superficie, camera, jogador):
        import configuracoes
        centro = camera.apply(jogador.rect).move(jogador.direcao_olhar*12, -36).center
        fracao = jogador.carga/configuracoes.TEMPO_CARGA
        angulo = jogador.carga*0.45
        ponta = (centro[0]+round(math.cos(angulo)*23), centro[1]+round(math.sin(angulo)*17))
        pygame.draw.line(superficie, (28, 33, 37), centro, ponta, 4)
        pygame.draw.line(superficie, (149, 151, 140), centro, ponta, 1)
        pygame.draw.rect(superficie, (46, 51, 56), (*ponta, 12, 9), border_radius=3)
        pygame.draw.rect(superficie, (195, 179, 130), (centro[0]-24, centro[1]-29, round(48*fracao), 4))
        if fracao >= 1:
            pygame.draw.circle(superficie, (231, 218, 173), ponta, 9, 2)

    def draw(self, superficie, camera, jogador, solidos):
        pontos = self.points(jogador, solidos)
        if not pontos:
            return
        pontos = [p - camera.deslocamento for p in pontos]
        coordenadas = [(round(p.x), round(p.y)) for p in pontos]
        if self.is_striking(jogador):
            rastro = pygame.Surface(superficie.get_size(), pygame.SRCALPHA)
            pygame.draw.lines(rastro, (190, 181, 148, 48 if self.dano == 1 else 82),
                              False, coordenadas, 2*self.RAIO_ACERTO)
            superficie.blit(rastro, (0, 0))
        # Cabo escuro com realce para permanecer visível no cenário.
        pygame.draw.lines(superficie, (12, 17, 24), False, coordenadas, 4)
        pygame.draw.lines(superficie, (160, 183, 192), False, coordenadas, 2)
        pygame.draw.circle(superficie, (191, 118, 65), coordenadas[0], 2)
        # Mouse visto por cima: carcaça, divisão dos botões e rodinha.
        mouse = pygame.Surface((18, 12), pygame.SRCALPHA)
        pygame.draw.ellipse(mouse, (10, 15, 24), (0, 0, 18, 12))
        pygame.draw.ellipse(mouse, (97, 103, 101), (1, 1, 16, 10))
        pygame.draw.line(mouse, (50, 66, 78), (7, 1), (7, 5), 1)
        pygame.draw.line(mouse, (50, 66, 78), (3, 5), (11, 5), 1)
        pygame.draw.rect(mouse, (55, 166, 165), (6, 2, 2, 3))
        # Cinta metálica sobre a carcaça gasta: peso, sem aparência de brinquedo.
        pygame.draw.line(mouse, (182, 174, 152), (3, 2), (5, 10), 2)
        pygame.draw.line(mouse, (32, 37, 40), (12, 2), (10, 9), 2)
        tangente = pontos[-1] - pontos[-2]
        angulo = -math.degrees(math.atan2(tangente.y, tangente.x)) - 90
        mouse = pygame.transform.rotate(mouse, angulo)
        superficie.blit(mouse, mouse.get_rect(center=coordenadas[-1]))
