"""Bustos HD dos falantes; figuras antigas só servem à campanha de regressão."""
import pygame
from sistema import recursos


class RetratosDialogo:
    def __init__(self):
        self.cache = {}

    def obter(self, falante, nome_jogador, personagem):
        identidade = ('protagonista', personagem) if falante == nome_jogador else ('falante', falante)
        if identidade in self.cache:
            return self.cache[identidade]
        nomes_hd = {'Professor Max': 'max', 'Professor Romerito': 'romerito',
                    'Max em Loop': 'max',
                    'Elias · Guardião do Compasso': 'guardiao_elias',
                    'Alessandro · Sentinela dos Enlaces': 'guardiao_alessandro',
                    'Francisco · Guardião da Continuidade': 'guardiao_francisco',
                    'Entidade': 'entidade', 'IFVania': 'entidade',
                    'Indexador': 'indexador', 'Sistema': 'sistema'}
        nome_hd = ('menina' if personagem == 'menina' else 'menino') if identidade[0] == 'protagonista' else nomes_hd.get(falante)
        if nome_hd:
            imagem = recursos.load_image(f'dialogos/{nome_hd}.png')
            self.cache[identidade] = imagem
            return imagem
        caminhos = {
            'Professor Max': 'professores/max_0.png',
            'Professor Romerito': 'professores/romerito_0.png',
            'RomerBug': 'chefes/romerbug_0.png',
            'SpeedBug': 'chefes/speedbug_0.png',
            'Entidade': 'chefes/transicao/entidade.png',
            'IFVania': 'chefes/transicao/entidade.png',
            **{f'Prof. {nome}': f'chefes/prof_{nome.lower()}.png'
               for nome in ('Python', 'Java', 'C', 'SQL', 'Assembly')},
        }
        if identidade[0] == 'protagonista':
            pasta = 'jogador/menina' if personagem == 'menina' else 'jogador'
            figura = recursos.load_character_frames([pasta+'/repouso_0.png'])[0]
        elif falante in caminhos:
            figura = recursos.load_character_frames([caminhos[falante]])[0]
        else:
            figura = self._simbolo(falante)
        limites = figura.get_bounding_rect()
        if falante != 'Sistema':
            limites.height = max(1, round(limites.height*0.68))
        recorte = figura.subsurface(limites)
        escala = min(80/max(1, recorte.get_width()), 88/max(1, recorte.get_height()))
        imagem = pygame.transform.scale(recorte, (max(1, round(recorte.get_width()*escala)),
                                                 max(1, round(recorte.get_height()*escala))))
        self.cache[identidade] = imagem
        return imagem

    def _simbolo(self, falante):
        figura = pygame.Surface((40, 40), pygame.SRCALPHA)
        if falante == 'Sistema':
            pygame.draw.rect(figura, (77, 122, 131), (2, 5, 36, 25), 2)
            pygame.draw.lines(figura, (126, 224, 204), False, [(8, 12), (13, 16), (8, 20)], 2)
            pygame.draw.line(figura, (226, 216, 164), (18, 21), (29, 21), 2)
            pygame.draw.rect(figura, (77, 122, 131), (18, 30, 4, 5))
            pygame.draw.rect(figura, (77, 122, 131), (11, 35, 18, 2))
        else:
            # Falante sem arte própria: busto neutro, sem atribuir a cara de outro.
            pygame.draw.circle(figura, (139, 161, 165), (20, 12), 9)
            pygame.draw.ellipse(figura, (66, 94, 105), (4, 21, 32, 19))
        return figura
