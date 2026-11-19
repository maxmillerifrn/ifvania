"""Atuadores de alcance corporal; reutiliza o resolvedor de acertos e paredes."""
import math
import pygame
from entidades.chicote_mouse import ChicoteMouse


def desenhar_luva(superficie, centro, escala=1, direcao=1, abertura=0, brilho=False):
    """Sprite texturizado de perfil; escala proporcional, sem ícone luminoso."""
    from sistema import recursos
    nome = 'punho' if abertura >= .7 else 'aberta' if abertura < .25 else 'repouso'
    original = recursos.load_image(f'equipamentos/luva_robotica/{nome}.png')
    largura = max(1, round(48*escala))
    imagem = pygame.transform.smoothscale(original, (largura, max(1, round(original.get_height()*largura/original.get_width()))))
    if direcao < 0:
        imagem = pygame.transform.flip(imagem, True, False)
    destino = imagem.get_rect(center=centro)
    superficie.blit(imagem, destino)
    if brilho:
        # Apenas o indicador do controlador, sem cobrir materiais e articulações.
        pygame.draw.circle(superficie, (156, 205, 184),
                           (destino.centerx-round(largura*.3)*direcao, destino.centery+round(largura*.16)), max(1, largura//32))


class LuvaRobotica(ChicoteMouse):
    DURACAO = 24
    PREPARACAO = 4
    FIM_GOLPE = 14
    ALCANCE = 52
    RAIO_ACERTO = 13

    def points(self, jogador, solidos=()):
        from sistema.habilidades import Habilidade
        if (jogador.temporizador_golpe and self.tipo_golpe == 'descendente'
                and jogador.no_chao and jogador.has(Habilidade.ONDA_CHOQUE)):
            origem = pygame.Vector2(jogador.rect.centerx, jogador.rect.bottom-5)
            fim = origem+pygame.Vector2(self.direcao_olhar*100, 0)
            entradas = [parede.clipline(origem, fim) for parede in solidos]
            entradas = [pygame.Vector2(linha[0]) for linha in entradas if linha]
            if entradas:
                fim = min(entradas, key=lambda ponto: ponto.distance_squared_to(origem))
            return [origem.lerp(fim, indice/8) for indice in range(9)]
        if not jogador.temporizador_golpe:
            return []
        idade = self.age(jogador)
        extensao = math.sin(math.pi*max(0, min(1, (idade-2)/20)))
        alcance = 22+(self.ALCANCE-22)*extensao
        origem = pygame.Vector2(jogador.rect.centerx, jogador.rect.centery-26)
        altura = -35*extensao if self.tipo_golpe == 'ascendente' else 35*extensao if self.tipo_golpe == 'descendente' else -4*math.sin(idade/3)
        fim = origem+pygame.Vector2(alcance*self.direcao_olhar, altura)
        entradas = [parede.clipline(origem, fim) for parede in solidos]
        entradas = [pygame.Vector2(linha[0]) for linha in entradas if linha]
        if entradas:
            fim = min(entradas, key=lambda ponto: ponto.distance_squared_to(origem))
        return [origem.lerp(fim, indice/8) for indice in range(9)]

    def draw(self, superficie, camera, jogador, solidos):
        pontos = self.points(jogador, solidos)
        if not pontos:
            return
        origem, fim = pontos[0]-camera.deslocamento, pontos[-1]-camera.deslocamento
        cor = (201, 163, 111) if self.dano > 1 else (139, 163, 152)
        from sistema.habilidades import Habilidade
        if self.tipo_golpe == 'descendente' and jogador.no_chao and jogador.has(Habilidade.ONDA_CHOQUE):
            if self.is_striking(jogador):
                for indice in range(1, 5):
                    centro = origem.lerp(fim, indice/4)
                    pygame.draw.ellipse(superficie, cor, (centro.x-12, centro.y-8, 24, 12), 2)
            return

        if self.is_striking(jogador):
            pygame.draw.line(superficie, cor, origem+(fim-origem)*0.4, fim, 3)
            for indice in range(3):
                pygame.draw.line(superficie, cor, (fim.x-self.direcao_olhar*(20+indice*5), fim.y-10+indice*10), (fim.x, fim.y-8+indice*8), 2)
