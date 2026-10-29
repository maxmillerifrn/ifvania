"""Contratos de controle, carga, defesa e legibilidade do protótipo de combate."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
import unittest
from collections import defaultdict
import pygame
import configuracoes
from entidades.jogador import Jogador
from entidades.inimigo import Inimigo
from entidades.romer_bug import RomerBug
from jogo import Jogo, ESTADO_JOGANDO, ESTADO_PAUSA, ESTADO_DIALOGO
from mundo.escola_sombria import EscolaSombria
from mundo.camera import Camera


class TestesControleCombate(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((960, 540))
        self.piso = [pygame.Rect(0, 352, 3000, 100)]
        self.teclas = defaultdict(bool)
        self.jogador = Jogador(200, 312)
        self.jogador.no_chao = True

    def tearDown(self):
        pygame.quit()

    def evento(self, tipo, tecla):
        return pygame.event.Event(tipo, key=tecla)

    def quadro(self, eventos=()):
        self.jogador.handle_input(self.teclas, eventos)
        self.jogador.update(self.piso, [])

    def teste_aceleracao_frenagem_e_recuo_preservado(self):
        self.teclas[pygame.K_d] = True
        self.quadro()
        self.assertGreater(self.jogador.velocidade.x, 0)
        self.assertLess(self.jogador.velocidade.x, configuracoes.VELOCIDADE_JOGADOR)
        for _ in range(8):self.quadro()
        self.assertEqual(self.jogador.velocidade.x, configuracoes.VELOCIDADE_JOGADOR)
        self.teclas.clear()
        for _ in range(4):self.quadro()
        self.assertEqual(self.jogador.velocidade.x, 0)
        self.jogador.take_damage(1, recuo=(-6, -7))
        x = self.jogador.rect.x
        self.quadro()
        self.assertLess(self.jogador.rect.x, x)
        self.assertEqual(self.jogador.velocidade.x, -6)

    def teste_toque_carga_dano_e_um_acerto_por_golpe(self):
        for personagem in ('boy', 'menina'):
            for carga, dano in ((0, 1), (35, 1), (36, 2), (70, 2)):
                with self.subTest(personagem=personagem, carga=carga):
                    self.jogador = Jogador(200,312,personagem)
                    self.jogador.no_chao = True
                    alvo = Inimigo(295,312,vida=10)
                    self.jogador.handle_input(self.teclas,[self.evento(pygame.KEYDOWN,pygame.K_x)])
                    self.assertEqual(self.jogador.temporizador_golpe,0)
                    for _ in range(carga):self.quadro()
                    self.jogador.handle_input(self.teclas,[self.evento(pygame.KEYUP,pygame.K_x)])
                    self.assertEqual(self.jogador.chicote.dano,dano)
                    for _ in range(31):
                        self.jogador.update(self.piso,[])
                        self.jogador.try_melee_hit(alvo,self.piso)
                    self.assertEqual(alvo.vida,10-dano)

    def teste_esquiva_cancelamento_recarga_e_protecao_curta(self):
        self.quadro([self.evento(pygame.KEYDOWN,pygame.K_x)])
        self.jogador.tentar_esquiva()
        self.assertFalse(self.jogador.carregando)
        self.assertEqual(self.jogador.temporizador_esquiva,15)
        self.jogador.temporizador_esquiva=10
        self.jogador.take_damage(1)
        self.assertEqual(self.jogador.vida,6)
        for _ in range(12):self.quadro()
        self.jogador.tentar_esquiva()
        self.assertEqual(self.jogador.temporizador_esquiva,0)
        self.jogador.take_damage(1)
        self.assertEqual(self.jogador.vida,5)

    def teste_preparacao_nao_cancela_mas_recolhimento_permite_esquiva(self):
        self.jogador._try_melee()
        self.jogador.tentar_esquiva()
        self.assertEqual(self.jogador.temporizador_esquiva,0)
        self.jogador.temporizador_golpe=self.jogador.chicote.DURACAO-self.jogador.chicote.FIM_GOLPE
        self.jogador.tentar_esquiva()
        self.assertGreater(self.jogador.temporizador_esquiva,0)
        self.assertEqual(self.jogador.temporizador_golpe,0)

    def teste_carga_cancelada_por_dano_pausa_foco_e_reaparecimento(self):
        jogo=Jogo();jogo._load_level(0,novo_jogador=True);jogo.estado=ESTADO_JOGANDO
        for interrupcao in ('pausa','foco','dano','reaparecimento'):
            jogo.estado=ESTADO_JOGANDO
            jogador=jogo.jogador
            jogador.handle_input(self.teclas,[self.evento(pygame.KEYDOWN,pygame.K_x)])
            jogador.carga=36
            if interrupcao=='pausa':jogo._process_events([self.evento(pygame.KEYDOWN,pygame.K_ESCAPE)])
            elif interrupcao=='foco':jogo._process_events([pygame.event.Event(pygame.WINDOWFOCUSLOST)])
            elif interrupcao=='dano':
                jogador.temporizador_invulnerabilidade=0;jogador.take_damage(1)
            else:jogador.respawn(200,312)
            self.assertFalse(jogador.carregando)
            self.assertEqual(jogador.carga,0)
            jogador.handle_input(self.teclas,[self.evento(pygame.KEYUP,pygame.K_x)])
            self.assertEqual(jogador.temporizador_golpe,0)

    def teste_memoria_de_salto_antes_do_pouso_e_tolerancia_de_borda(self):
        self.jogador.no_chao=False;self.jogador.rect.bottom=351
        self.jogador.posicao.y=self.jogador.rect.y;self.jogador.velocidade.y=2
        self.quadro([self.evento(pygame.KEYDOWN,pygame.K_SPACE)])
        self.assertTrue(self.jogador.no_chao)
        self.quadro()
        self.assertLess(self.jogador.velocidade.y,0)
        self.jogador.no_chao=False;self.jogador.tolerancia_borda=3
        self.jogador.memoria_salto=6;self.jogador._try_jump()
        self.assertEqual(self.jogador.velocidade.y,configuracoes.FORCA_SALTO_JOGADOR)
        self.assertEqual(self.jogador.tolerancia_borda,0)

    def teste_filtragem_final_tolerante_sem_acertar_atras_de_parede(self):
        self.jogador._try_melee(2)
        alvo=Inimigo(310,296,vida=8)
        for idade in range(30):
            self.jogador.temporizador_golpe=30-idade
            area=self.jogador.get_melee_rect()
            if area and area.colliderect(self.jogador.chicote.area_alvo(alvo)):
                self.jogador.try_melee_hit(alvo,self.piso)
        self.assertEqual(alvo.vida,6)
        self.jogador.espera_ataque=0;self.jogador._try_melee(2)
        parede=pygame.Rect(280,200,12,152)
        for idade in range(30):
            self.jogador.temporizador_golpe=30-idade
            self.jogador.try_melee_hit(alvo,[parede])
        self.assertEqual(alvo.vida,6)

    def teste_superficie_destacada_apenas_no_topo_exposto(self):
        escola=EscolaSombria(1800,544,352);camera=Camera(1800,544)
        tela=pygame.Surface((960,540));tela.fill((0,0,0))
        escola.draw_block(tela,pygame.Rect(320,288,32,32),camera,1800,True)
        escola.draw_block(tela,pygame.Rect(320,320,32,32),camera,1800,False)
        self.assertEqual(tela.get_at((330,288))[:3],(235,213,156))
        self.assertNotEqual(tela.get_at((330,320))[:3],(235,213,156))

    def teste_jogador_escapa_descarga_e_salta_investida_sem_invulnerabilidade_artificial(self):
        chefe=RomerBug(450,312,arena=pygame.Rect(0,0,1600,500));chefe.activate()
        self.jogador.posicao.x=300;self.jogador.rect.x=300
        chefe.preparar_ataque(self.jogador,self.piso)
        self.teclas[pygame.K_a]=True
        for _ in range(65):
            self.quadro();chefe.update(self.jogador,self.piso)
            for area,dano in chefe.get_all_hit_rects():
                if area.colliderect(self.jogador.rect):self.jogador.take_damage(dano)
        self.assertEqual(self.jogador.vida,6)
        chefe.take_damage(8);chefe.temporizador_transformacao=0
        chefe.posicao.x=450;chefe.rect.x=450
        self.jogador.posicao.update(320,312);self.jogador.rect.topleft=(320,312)
        self.jogador.velocidade.update(0,0);self.jogador.no_chao=True;self.teclas.clear()
        chefe.preparar_ataque(self.jogador,self.piso)
        for instante in range(63):
            eventos=[self.evento(pygame.KEYDOWN,pygame.K_SPACE)] if instante==30 else []
            self.quadro(eventos);chefe.update(self.jogador,self.piso)
            for area,dano in chefe.get_all_hit_rects():
                if area.colliderect(self.jogador.rect):self.jogador.take_damage(dano)
        self.assertEqual(self.jogador.vida,6)
        self.assertEqual(chefe.estado_ataque,'recuperar')

    def teste_memoria_ataque_aceita_toque_na_recarga_sem_carga_automatica(self):
        self.jogador.espera_ataque=4
        self.quadro([self.evento(pygame.KEYDOWN,pygame.K_x),self.evento(pygame.KEYUP,pygame.K_x)])
        self.assertEqual(self.jogador.temporizador_golpe,0)
        for _ in range(4):self.quadro()
        self.assertGreater(self.jogador.temporizador_golpe,0)
        self.assertEqual(self.jogador.chicote.dano,1)
        self.jogador.cancelar_combate();self.jogador.espera_ataque=0
        self.quadro([self.evento(pygame.KEYDOWN,pygame.K_x)])
        for _ in range(70):self.quadro()
        self.assertTrue(self.jogador.carregando)
        self.assertEqual(self.jogador.carga,36)
        self.assertEqual(self.jogador.temporizador_golpe,0)

    def teste_impacto_preserva_comando_e_pausa_remove_eventos_antigos(self):
        jogo=Jogo();jogo._load_level(0,novo_jogador=True);jogo.estado=ESTADO_JOGANDO
        jogador=jogo.jogador;chefe=jogo.fase.chefe
        jogador.pausa_impacto=2;jogador.espera_ataque=2
        posicao=jogador.rect.copy();temporizador=chefe.temporizador_ataque
        eventos=[self.evento(pygame.KEYDOWN,pygame.K_x),self.evento(pygame.KEYUP,pygame.K_x)]
        jogo._update(self.teclas,eventos)
        jogo._update(self.teclas,[])
        self.assertEqual(jogador.rect,posicao)
        self.assertEqual(chefe.temporizador_ataque,temporizador)
        for _ in range(3):jogo._update(self.teclas,[])
        self.assertGreater(jogador.temporizador_golpe,0)
        eventos=jogo._process_events([self.evento(pygame.KEYDOWN,pygame.K_x),
            self.evento(pygame.KEYDOWN,pygame.K_ESCAPE),self.evento(pygame.KEYDOWN,pygame.K_ESCAPE)])
        self.assertEqual(jogo.estado,ESTADO_JOGANDO)
        self.assertEqual(eventos,[])
