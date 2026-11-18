"""Regressões da primeira entrega da expansão: biblioteca e transições."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
from collections import defaultdict
import unittest
import pygame
from sistema.jogo import Jogo, ESTADO_JOGANDO, ESTADO_DIALOGO, ESTADO_PAUSA, ESTADO_DERROTA
from sistema.habilidades import Habilidade


class TestesBiblioteca(unittest.TestCase):
    def setUp(self):
        self.jogo = Jogo()
        self.jogo.indice_fase = 1
        self.jogo._load_level(1, novo_jogador=True)
        self.jogo.maquina_estados.estado = ESTADO_JOGANDO
        self.teclas = defaultdict(bool)

    def tearDown(self):
        pygame.quit()

    def posicionar(self, alvo):
        jogador = self.jogo.jogador
        jogador.rect.midbottom = alvo.midbottom
        jogador.posicao.update(jogador.rect.topleft)
        jogador.velocidade.update(0, 0)

    def consultar(self, alvo):
        self.posicionar(alvo)
        return self.jogo.fase.update(self.jogo.jogador, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)])

    def test_modulo_unico_nao_cura_nem_aumenta_vida(self):
        jogador = self.jogo.jogador
        jogador.vida = 3
        self.assertEqual(self.consultar(self.jogo.fase.biblioteca.modulo)[0], 'dialogue')
        self.assertTrue(jogador.has(Habilidade.SALTO_DUPLO))
        self.assertEqual((jogador.vida, jogador.vida_maxima), (3, 6))
        self.assertEqual(self.consultar(self.jogo.fase.biblioteca.modulo), (None, None))
        self.assertEqual((jogador.vida, jogador.vida_maxima), (3, 6))

    def test_portao_exige_tres_consultas_e_persiste_na_retomada(self):
        fase = self.jogo.fase
        biblioteca = fase.biblioteca
        self.assertIn(biblioteca.portao, fase.mapa_blocos.solidos)
        # Não consultar a estante de baixo apenas encostando a cabeça nela.
        jogador = self.jogo.jogador
        jogador.rect.midtop = (biblioteca.paineis[1].centerx, biblioteca.paineis[1].bottom)
        jogador.posicao.update(jogador.rect.topleft)
        fase.update(jogador, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)])
        self.assertFalse(biblioteca.consultados)
        self.consultar(biblioteca.modulo)
        for painel in biblioteca.paineis:
            self.assertEqual(self.consultar(painel)[0], 'dialogue')
        self.assertNotIn(biblioteca.portao, fase.mapa_blocos.solidos)
        self.jogo.maquina_estados.estado = ESTADO_DERROTA
        self.jogo._process_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)])
        self.assertEqual(self.jogo.fase.biblioteca.consultados, {0, 1, 2})
        self.assertTrue(self.jogo.fase.biblioteca.modulo_obtido)
        self.assertTrue(self.jogo.jogador.has(Habilidade.SALTO_DUPLO))
        self.assertFalse(self.jogo.fase.chefe.ativo)
        self.assertNotIn(self.jogo.fase.biblioteca.portao, self.jogo.fase.mapa_blocos.solidos)

    def test_dialogo_e_pausa_congelam_mente_e_consultas(self):
        chefe = self.jogo.fase.chefe
        chefe.activate()
        self.posicionar(self.jogo.fase.biblioteca.modulo)
        self.jogo._update(self.teclas, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)])
        self.assertEqual(self.jogo.estado, ESTADO_DIALOGO)
        antes = (chefe.temporizador_ataque, chefe.relogio_ataque)
        for _ in range(80):
            self.jogo._update(self.teclas, [])
        self.assertEqual((chefe.temporizador_ataque, chefe.relogio_ataque), antes)
        self.jogo._process_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)])
        self.assertEqual(self.jogo.estado, ESTADO_PAUSA)
        visual = self.jogo.fase.biblioteca.instantes_visuais
        for _ in range(80):
            self.jogo._update(self.teclas, [])
        self.assertEqual(self.jogo.fase.biblioteca.instantes_visuais, visual)
        self.assertEqual((chefe.temporizador_ataque, chefe.relogio_ataque), antes)

    def test_mente_prepara_sem_dano_fixa_direcao_e_oferece_recuperacao(self):
        chefe = self.jogo.fase.chefe
        jogador = self.jogo.jogador
        chefe.activate()
        jogador.rect.x = chefe.rect.x-260
        chefe.preparar_ataque(jogador)
        direcao = chefe.direcao_investida
        jogador.rect.x = chefe.rect.x+280
        for _ in range(28):
            self.assertFalse(chefe.get_all_hit_rects())
            chefe.update(jogador,self.jogo.fase.mapa_blocos.solidos)
        self.assertEqual(chefe.estado_ataque,'executar')
        self.assertEqual(chefe.direcao_investida,direcao)
        self.assertTrue(chefe.get_all_hit_rects())
        for _ in range(17): chefe.update(jogador,self.jogo.fase.mapa_blocos.solidos)
        self.assertEqual(chefe.estado_ataque,'recuperar')
        self.assertFalse(chefe.get_all_hit_rects())

    def test_identidade_e_limpeza_na_transicao_e_nova_partida(self):
        jogador = self.jogo.jogador
        jogador.nome = 'Márcia'
        jogador.grant_ability(Habilidade.SALTO_DUPLO, aumentar_vida=False)
        jogador.carregando = True
        jogador.carga = 30
        self.jogo._load_level(1)
        self.assertIs(self.jogo.jogador, jogador)
        self.assertEqual(jogador.nome, 'Márcia')
        self.assertTrue(jogador.has(Habilidade.SALTO_DUPLO))
        self.assertFalse(jogador.carregando)
        self.jogo.maquina_estados.estado = 'menu'
        self.jogo._start_story()
        self.assertFalse(self.jogo.jogador.habilidades)
        self.assertEqual(self.jogo.jogador.vida_maxima, 6)

    def test_subida_obrigatoria_alcancavel_com_salto_duplo_para_ambos(self):
        # Exercita física real para subir ao primeiro arquivo elevado (160 px).
        for personagem in ('boy', 'menina'):
            self.jogo.personagem_escolhido = personagem
            self.jogo._iniciar_sessao_campanha()
            self.jogo._load_level(1, novo_jogador=True)
            jogador = self.jogo.jogador
            jogador.rect.topleft = (24*32-40, 14*32-40)
            jogador.posicao.update(jogador.rect.topleft)
            jogador.grant_ability(Habilidade.SALTO_DUPLO, aumentar_vida=False)
            jogador.no_chao = True
            chegou = False
            for quadro in range(100):
                eventos = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)] if quadro in (0, 18) else []
                teclas = defaultdict(bool, {pygame.K_d: quadro >= 18 and jogador.rect.centerx < 27*32})
                jogador.handle_input(teclas, eventos)
                jogador.update(self.jogo.fase.mapa_blocos.solidos, [])
                if jogador.no_chao and jogador.rect.bottom == 9*32:
                    chegou = True
                    break
            self.assertTrue(chegou, personagem)

    def test_combater_mente_pelo_chicote_e_encerrar_conteudo(self):
        from sistema.jogo import ESTADO_FIM_CONTEUDO
        for personagem in ('boy', 'menina'):
            self.jogo._iniciar_sessao_campanha()
            self.jogo.personagem_escolhido = personagem
            self.jogo._load_level(1, novo_jogador=True)
            self.jogo.maquina_estados.estado = ESTADO_JOGANDO
            fase, jogador = self.jogo.fase, self.jogo.jogador
            fase.dialogo_exibido = True
            fase.chefe.activate()
            # Isola acerto, limpeza e transição; não homologa sobrevivência.
            jogador.temporizador_invulnerabilidade = 10000
            jogador.direcao_olhar = 1
            for _ in range(20):
                jogador.rect.midbottom = (fase.chefe.rect.centerx-75, fase.chefe.rect.bottom)
                jogador.posicao.update(jogador.rect.topleft)
                eventos = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_x),
                           pygame.event.Event(pygame.KEYUP, key=pygame.K_x)]
                self.jogo._update(self.teclas, eventos)
                for _ in range(35):
                    self.jogo._update(self.teclas, [])
                    if fase.chefe.derrotado:
                        break
                if fase.chefe.derrotado:
                    break
            self.assertTrue(fase.chefe.derrotado)
            self.assertFalse(fase.inimigos)
            self.assertFalse(fase.chefe.get_all_hit_rects())
            self.assertEqual(self.jogo.estado, ESTADO_DIALOGO)
            for _ in range(30):
                self.jogo._process_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)])
                if not self.jogo.caixa_dialogo.ativo:
                    break
            jogador.rect.right = fase.mapa_blocos.gatilho_saida.right
            jogador.rect.bottom = 14*32
            jogador.posicao.update(jogador.rect.topleft)
            self.jogo._update(self.teclas, [])
            from sistema.jogo import ESTADO_CARTAO_FASE
            self.assertEqual(self.jogo.estado, ESTADO_CARTAO_FASE)
            self.assertEqual(self.jogo.fase.setor, 'convivencia')
