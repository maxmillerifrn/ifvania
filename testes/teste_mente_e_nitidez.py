"""Regressões de nitidez direcional, poderes e ausência de avisos gráficos."""
import os
os.environ.setdefault('SDL_VIDEODRIVER','dummy')
os.environ.setdefault('SDL_AUDIODRIVER','dummy')
import unittest
import pygame
from entidades.inimigo import Inimigo
from entidades.bug_combate import BugCombate
from entidades.mente_brilhante import MenteBrilhante
from entidades.poderes_chefes import RaioBrilhante, PulsoSombrio
from sistema.jogo import Jogo
from mundo.camera import Camera


class TestesMenteNitidez(unittest.TestCase):
    def setUp(self):
        self.jogo = Jogo()
        self.jogo._load_level(1,novo_jogador=True)
        self.chefe = self.jogo.fase.chefe
        self.jogador = self.jogo.jogador
        self.piso = self.jogo.fase.mapa_blocos.solidos

    def tearDown(self):
        pygame.quit()

    def test_biblioteca_constroi_mente_com_vida_e_repertorio_proprios(self):
        self.assertIsInstance(self.chefe,MenteBrilhante)
        self.assertEqual(self.chefe.nome,'Mente Brilhante')
        self.assertEqual(self.chefe.vida,18)
        self.jogador.rect.x = self.chefe.rect.x-70
        acoes = set()
        for ciclo in range(4):
            self.chefe.ciclo_combate = ciclo
            acoes.add(self.chefe.choose_attack(self.jogador))
        self.assertEqual(acoes,{'cruzado','chute','barrigada','raio'})

    def test_raio_sai_da_cabeca_so_na_execucao_e_segue_direcao_inicial(self):
        self.chefe.activate()
        self.chefe.ciclo_combate = 3
        self.jogador.rect.x = self.chefe.rect.x-100
        origem = self.chefe.rect.centerx-6,self.chefe.rect.bottom-72
        self.chefe.preparar_ataque(self.jogador)
        for _ in range(27):
            self.chefe.update(self.jogador,self.piso)
            self.assertFalse(self.chefe.projeteis)
        self.chefe.update(self.jogador,self.piso)
        raio = self.chefe.projeteis.sprites()[0]
        self.assertIsInstance(raio,RaioBrilhante)
        self.assertAlmostEqual((raio.posicao-pygame.Vector2(origem)).length(),7)
        self.assertLess(raio.velocidade.x,0)
        velocidade = raio.velocidade.copy()
        self.jogador.rect.x += 300
        for _ in range(5): self.chefe.update(self.jogador,self.piso)
        self.assertEqual(raio.velocidade,velocidade)
        self.assertEqual(len(self.chefe.get_all_hit_rects()),1)

    def test_mente_nao_vira_speedbug_ao_cruzar_metade_da_vida(self):
        self.chefe.activate()
        self.chefe.take_damage(10)
        self.assertEqual(self.chefe.vida,8)
        self.assertFalse(self.chefe.transformado)
        self.assertFalse(self.chefe.cinematica_pendente)
        self.assertEqual(self.chefe.nome,'Mente Brilhante')

    def test_barrigada_bloqueada_interrompe_avanco_e_abre_contra_ataque(self):
        self.chefe.activate()
        self.chefe.ciclo_combate = 2
        self.jogador.rect.x = self.chefe.rect.x-70
        self.chefe.preparar_ataque(self.jogador)
        for _ in range(28): self.chefe.update(self.jogador,self.piso)
        self.assertEqual(self.chefe.golpe_atual,'barrigada')
        self.chefe.reagir_bloqueio(self.chefe.get_all_hit_rects()[0][0])
        self.assertEqual(self.chefe.estado_ataque,'recuperar')
        self.assertFalse(self.chefe.get_all_hit_rects())

    def test_bug_espelhado_usa_a_mesma_fonte_hd_sem_reduzir_a_40(self):
        bug = Inimigo(0,0)
        from sistema import recursos
        for indice in range(4):
            direita = recursos.imagem_apresentacao(bug.figuras[1][indice],(80,80))
            esquerda = recursos.imagem_apresentacao(bug.figuras[-1][indice],(80,80))
            esperado = pygame.transform.flip(direita,True,False)
            self.assertEqual(pygame.image.tobytes(esquerda,'RGBA'),pygame.image.tobytes(esperado,'RGBA'))

    def test_preparacao_nao_desenha_setas_circulos_ou_faixas(self):
        camera = Camera(960,540)
        for ator in (BugCombate(400,300),self.chefe):
            ator.rect.topleft = (400,300)
            ator.posicao.update(400,300)
            if isinstance(ator,BugCombate):
                ator.estados.mudar('preparar')
            else:
                ator.activate()
                ator.preparar_ataque(self.jogador)
            tela = pygame.Surface((960,540),pygame.SRCALPHA)
            ator.draw(tela,camera)
            corpo = ator.get_draw_image().get_rect(midbottom=ator.rect.midbottom).inflate(10,0)
            tela.fill((0,0,0,0),corpo)
            self.assertEqual(pygame.mask.from_surface(tela).count(),0)

    def test_romer_e_speedbug_usam_soco_chute_e_poder_sombrio(self):
        self.jogo._load_level(0,novo_jogador=True)
        chefe = self.jogo.fase.chefe
        chefe.activate()
        chefe.ciclo_combate = 3
        chefe.preparar_ataque(self.jogador)
        for _ in range(28): chefe.update(self.jogador,self.jogo.fase.mapa_blocos.solidos)
        self.assertTrue(any(isinstance(p,PulsoSombrio) for p in chefe.projeteis))
        self.assertEqual(chefe.get_all_hit_rects(),[(p.rect,p.dano) for p in chefe.projeteis])
        self.assertNotEqual(pygame.image.tobytes(chefe.poses_corpo['romerbug'][1][3],'RGBA'),pygame.image.tobytes(chefe.poses_corpo['romerbug'][1][4],'RGBA'))
