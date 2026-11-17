"""Setores persistentes do campus, com portas explícitas e sem gatilhos do prólogo."""
from types import SimpleNamespace
import pygame
from mundo.camera import Camera
from mundo.arte_escolar import ArteEscolar
from mundo.dados_campus import SETORES, FALAS_CAMPUS
from entidades.professor import Professor
from sistema import configuracoes, recursos
from interface import tema
from sistema.comandos import houve_interacao
from sistema.eventos_campanha import ObjetivoConcluido


class CampusVirtual:
    def __init__(self, setor, progresso, chegada='inicio', eventos=None):
        if setor not in SETORES:
            raise ValueError(f'Setor desconhecido: {setor}')
        self.setor, self.progresso = setor, progresso
        self.eventos = eventos
        self.dados_setor = SETORES[setor]
        self.nome = 'Campus virtual · '+self.dados_setor['nome']
        self.chefe = None
        self.biblioteca = None
        self.largura = 1920
        self.piso = 440
        self.mapa_blocos = SimpleNamespace(largura=self.largura, altura=540, perigos=[], solidos=[
            pygame.Rect(0, self.piso, self.largura, 100), pygame.Rect(-32, 0, 32, 540), pygame.Rect(self.largura, 0, 32, 540)])
        self.apoios = [pygame.Rect(940, 408, 96, 32), pygame.Rect(1130, 376, 96, 64)] if setor == 'jardim' else []
        self.mapa_blocos.solidos.extend(self.apoios)
        self.conectores = [pygame.Vector2(1060, 300), pygame.Vector2(1320, 310)] if setor in ('jardim', 'informatica') else []
        self.camera = Camera(self.largura, 540)
        pontos_retorno = {'biblioteca': 320, 'recreio': 1410, 'copias': 620, 'rede': 1390, 'continuidade': 1220}
        self.surgimento_jogador = (1750 if chegada == 'fim' else pontos_retorno.get(chegada, 100), self.piso-40)
        self.arte = ArteEscolar('corridor', self.largura)
        self.instantes = 0
        self.fonte = pygame.font.Font(None, 25)
        self.fonte_pequena = pygame.font.Font(None, 21)
        self.aviso = 'E: portas e placas · caminhe pelo campus para encontrar a próxima fase'
        self.tempo_aviso = 0
        self.professor = Professor(830, self.piso-40, 'romerito' if setor in ('convivencia', 'jardim') else 'max')
        self.bilhete = pygame.Rect(970, 344, 24, 24)

    def update_visuals(self):
        self.instantes += 1
        self.professor.update()

    def update(self, jogador, eventos):
        self.camera.update(jogador.rect)
        self.tempo_aviso = max(0, self.tempo_aviso-1)
        if not houve_interacao(eventos):
            return None, None
        concluidas = self.progresso.fases_concluidas
        if jogador.rect.colliderect(self.bilhete.inflate(45, 24)):
            if self.eventos:
                self.eventos.emitir(ObjetivoConcluido('campus', 'bilhete_'+self.setor))
            falas = {'convivencia': 'O mural lembra: intervalo também faz parte de aprender. Ninguém precisa passar por tudo sozinho.',
                     'jardim': 'Bilhete da turma: o jardim parece maior quando a gente pode parar para conversar.',
                     'informatica': 'Registro de monitoria: explicar o erro foi o primeiro passo para sair do loop.',
                     'tecnico': 'Registro da manutenção: os equipamentos desligam. O que aprendemos fica com a gente.'}
            return 'dialogue', [('Aluno(a)', falas[self.setor])]
        if 'continuidade' in concluidas and self.setor == 'jardim' and abs(jogador.rect.centerx-370) < 90:
            return 'encerrar_campanha', None
        for x, nome, indice, requisito in self.dados_setor['entradas']:
            if abs(jogador.rect.centerx-x) < 85:
                if indice is None:
                    jogador.vida = jogador.vida_maxima
                    self.aviso = 'Ponto seguro · turma reunida · integridade restaurada'
                elif requisito is None or requisito in concluidas:
                    return 'entrar_fase', indice
                else:
                    self.aviso = 'Passagem bloqueada · conclua o setor anterior'
                self.tempo_aviso = 180
                return None, None
        if abs(jogador.rect.centerx-self.professor.rect.centerx) < 85:
            if self.setor == 'informatica' and 'copias' not in concluidas:
                return 'dialogue', [('Aluno(a)', 'Max repete a mesma aula na tela do M1. Preciso romper as cópias para libertá-lo.')]
            if self.setor == 'tecnico' and 'rede' not in concluidas:
                return 'dialogue', [('Aluno(a)', 'O núcleo ainda se comunica com os laboratórios. Primeiro preciso isolar os ramais no M5.')]
            return 'dialogue', FALAS_CAMPUS[self.setor]
        if jogador.rect.centerx > 1800 and 'proximo' in self.dados_setor:
            if self.dados_setor['requisito'] in concluidas:
                return 'trocar_setor', (self.dados_setor['proximo'], 'inicio')
            self.aviso, self.tempo_aviso = 'A interferência bloqueia a passagem. Procure a entrada da fase.', 180
        elif jogador.rect.centerx < 110 and 'anterior' in self.dados_setor:
            return 'trocar_setor', (self.dados_setor['anterior'], 'fim')
        jogador.tentar_ancoragem(self.conectores, self.mapa_blocos.solidos)
        return None, None

    def draw(self, superficie):
        self.arte.draw(superficie, self.camera, self.instantes, False)
        if self.setor == 'informatica' and 'copias' not in self.progresso.fases_concluidas:
            for x in (410, 630):
                copia = pygame.Surface((66, 116), pygame.SRCALPHA)
                pygame.draw.rect(copia, (103, 169, 176, 65), copia.get_rect(), 2)
                superficie.blit(copia, (x-self.camera.deslocamento.x, self.piso-116))
        pygame.draw.rect(superficie, (34, 47, 48), (0, self.piso, 960, 100))
        for apoio in self.apoios:
            destino = self.camera.apply(apoio)
            pygame.draw.rect(superficie, (55, 73, 76), destino)
            pygame.draw.line(superficie, (221, 208, 155), destino.topleft, destino.topright, 3)
        nota = self.camera.apply(self.bilhete)
        lido = 'bilhete_'+self.setor in self.progresso.objetivos_da_fase('campus')
        pygame.draw.rect(superficie, (117, 170, 147) if lido else (234, 212, 155), nota)
        pygame.draw.line(superficie, (53, 69, 71), nota.topleft, nota.bottomright)
        for ponto in self.conectores:
            pygame.draw.circle(superficie, (132, 223, 218), ponto-self.camera.deslocamento, 10, 3)
        if self.setor in ('convivencia', 'jardim') or 'copias' in self.progresso.fases_concluidas:
            self.professor.draw(superficie, self.camera)
        else:
            pygame.draw.rect(superficie, (74, 147, 157), self.camera.apply(self.professor.rect), 2)
        orientacao = self.fonte_pequena.render('E · orientações', True, (225, 218, 188))
        destino_orientacao = self.camera.apply(self.professor.rect)
        superficie.blit(orientacao, orientacao.get_rect(midbottom=(destino_orientacao.centerx, destino_orientacao.top-43)))
        for x, nome, indice, requisito in self.dados_setor['entradas']:
            posicao = self.camera.apply(pygame.Rect(x-35, self.piso-116, 70, 116))
            aberta = requisito is None or requisito in self.progresso.fases_concluidas
            cor = (74, 161, 132) if aberta else (124, 77, 72)
            pygame.draw.rect(superficie, (17, 29, 38), posicao)
            pygame.draw.rect(superficie, cor, posicao, 3)
            pygame.draw.circle(superficie, cor, (posicao.right-12, posicao.centery), 4)
            texto = self.fonte_pequena.render(nome, True, (241, 225, 192))
            superficie.blit(texto, texto.get_rect(midbottom=(posicao.centerx, posicao.top-10)))
        if self.progresso.chefes_derrotados:
            texto = self.fonte_pequena.render('Vínculos rompidos: '+str(len(self.progresso.chefes_derrotados)), True, (132, 221, 177))
            superficie.blit(texto, (24, 210))
        if 'recreio' in self.progresso.fases_concluidas and self.setor in ('jardim', 'convivencia'):
            for indice in range(3):
                caminho = 'apresentacao/jogador/'+('menina/' if indice % 2 else '')+'repouso_0.png'
                figura = recursos.load_image(caminho)
                centro = self.camera.apply(pygame.Rect(630+indice*64, self.piso-40, 40, 40))
                superficie.blit(figura, figura.get_rect(midbottom=centro.midbottom))
        texto = self.aviso if self.tempo_aviso else 'E nas bordas: trocar setor   |   E na porta: entrar   |   E no A28: recuperar integridade'
        tema.panel(superficie, pygame.Rect(18, 155, 924, 38))
        tema.text(superficie, self.fonte_pequena, texto, (30, 165), tema.PAPEL)
