"""Regressões de pés, travessia obrigatória e brisa pausável."""
import os
os.environ.setdefault('SDL_VIDEODRIVER','dummy')
os.environ.setdefault('SDL_AUDIODRIVER','dummy')
from collections import defaultdict
import unittest
import pygame
from entidades.inimigo import Inimigo
from mundo.cena_parasita import CenaParasita
from mundo.vegetacao_vento import VegetacaoAoVento
from sistema.jogo import Jogo, ESTADO_JOGANDO, ESTADO_PAUSA
from sistema.eventos_campanha import FaseConcluida


class TestesCorredorVento(unittest.TestCase):
    def setUp(self):
        self.jogo = Jogo()
        self.jogo._load_level(0,novo_jogador=True)
        self.jogo.maquina_estados.estado = ESTADO_JOGANDO

    def tearDown(self):
        pygame.quit()

    def test_bug_tem_altura_visual_do_jogador_sem_mudar_colisao(self):
        bug = Inimigo(500,312)
        self.assertEqual(bug.rect.size,self.jogo.jogador.rect.size)
        self.assertEqual(bug.get_draw_image().get_height(),self.jogo.jogador.get_draw_image().get_height())
        visual = bug.get_draw_image().get_rect(midbottom=bug.rect.midbottom)
        self.assertEqual(visual.bottom,352)

    def test_fusao_corre_com_pes_no_piso_e_termina_no_corpo(self):
        fase = self.jogo.fase
        fase.origem_fusao = (1050,352)
        cena = CenaParasita(fase,self.jogo.jogador,'fusao')
        self.assertEqual(cena.ponto_corrida(),pygame.Vector2(1050,352))
        self.assertEqual(cena.altura_visual,80)
        for instante in (0,20,40,cena.corrida):
            cena.instante = instante
            self.assertEqual(cena.ponto_corrida().y,352)
        self.assertEqual(cena.ponto_corrida(),pygame.Vector2(fase.chefe.rect.midbottom))
        self.assertLess(cena.torax.y,cena.destino.y)

    def test_saida_a28_exige_percorrer_corredor_ate_porta_da_biblioteca(self):
        self.jogo._advance_level()
        fase = self.jogo.fase
        self.assertEqual(fase.setor,'convivencia')
        porta = next(x for x,nome,indice,requisito in fase.dados_setor['entradas'] if indice == 1)
        self.assertGreater(porta-self.jogo.jogador.rect.centerx,800)
        interagir = [pygame.event.Event(pygame.KEYDOWN,key=pygame.K_e)]
        self.assertNotEqual(fase.update(self.jogo.jogador,interagir)[0],'entrar_fase')
        self.jogo.jogador.rect.centerx = porta
        self.assertEqual(fase.update(self.jogo.jogador,interagir),('entrar_fase',1))
        self.assertEqual(fase.corredor_biblioteca.get_size(),(fase.largura,540))

    def test_retorno_biblioteca_fica_fora_do_gatilho_e_proximo_setor_continua_acessivel(self):
        self.jogo.eventos_campanha.emitir(FaseConcluida('biblioteca'))
        self.jogo._load_campus('convivencia','biblioteca')
        self.assertGreater(abs(self.jogo.jogador.rect.centerx-1200),85)
        self.jogo.eventos_campanha.emitir(FaseConcluida('recreio'))
        self.jogo.jogador.rect.centerx = 1820
        self.assertEqual(self.jogo.fase.update(self.jogo.jogador,[pygame.event.Event(pygame.KEYDOWN,key=pygame.K_e)]),('trocar_setor',('jardim','inicio')))

    def test_vento_altera_folhas_mas_preserva_arquitetura_e_estado(self):
        imagem = pygame.Surface((100,100),pygame.SRCALPHA)
        imagem.fill((120,110,100))
        pygame.draw.rect(imagem,(20,110,25),(20,20,40,40))
        vento = VegetacaoAoVento(imagem,[(15,15,55,55)])
        antes = imagem.copy()
        depois = imagem.copy()
        vento.draw(antes,0)
        vento.draw(depois,35)
        self.assertNotEqual(pygame.image.tobytes(antes,'RGBA'),pygame.image.tobytes(depois,'RGBA'))
        self.assertEqual(antes.get_at((90,90)),depois.get_at((90,90)))
        self.assertEqual(imagem.get_at((19,20)),(120,110,100,255))

    def test_vento_congela_na_pausa_sem_mudar_colisoes(self):
        self.jogo._load_campus('jardim')
        self.jogo.maquina_estados.estado = ESTADO_JOGANDO
        fase = self.jogo.fase
        colisoes = [r.copy() for r in fase.mapa_blocos.solidos]
        for _ in range(5): self.jogo._update(defaultdict(bool),[])
        instante = fase.instantes
        self.jogo._process_events([pygame.event.Event(pygame.KEYDOWN,key=pygame.K_ESCAPE)])
        self.assertEqual(self.jogo.estado,ESTADO_PAUSA)
        for _ in range(30): self.jogo._update(defaultdict(bool),[])
        self.assertEqual(fase.instantes,instante)
        self.assertEqual(fase.mapa_blocos.solidos,colisoes)
