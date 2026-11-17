"""Defesa, regressões reais de movimento e acabamento da campanha."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
from collections import defaultdict
import unittest
import pygame
from entidades.jogador import Jogador
from entidades.romer_bug import RomerBug
from entidades.projetil import Projetil
from entidades.projeteis_campus import BolaVirtual
from sistema.jogo import Jogo, ESTADO_JOGANDO, ESTADO_DIALOGO, ESTADO_DESLIGAMENTO
from sistema.habilidades import Habilidade


class TestesBloqueioAcabamento(unittest.TestCase):
    def setUp(self):
        self.jogo = Jogo()
        self.jogo._load_level(0, novo_jogador=True)
        self.jogador = self.jogo.jogador
        self.jogador.temporizador_invulnerabilidade = 0
        self.jogador.direcao_olhar = 1
        self.teclas = defaultdict(bool)
        self.piso = [pygame.Rect(0, 448, 2000, 100)]

    def tearDown(self):
        pygame.quit()

    def test_bloqueio_frontal_consume_resistencia_uma_vez_por_janela(self):
        self.assertTrue(self.jogador.tentar_bloqueio())
        origem = (self.jogador.rect.right+20, self.jogador.rect.centery)
        vida = self.jogador.vida
        self.assertEqual(self.jogador.take_damage(1, origem=origem), 'bloqueado')
        self.assertEqual(self.jogador.defesa.resistencia, 74)
        for _ in range(5):
            self.jogador.take_damage(1, origem=origem)
        self.assertEqual((self.jogador.vida, self.jogador.defesa.resistencia), (vida, 74))
        self.jogador._try_melee()
        self.assertEqual(self.jogador.temporizador_golpe, 0)

    def test_costas_e_perigos_nao_sao_bloqueados(self):
        for bloqueavel, origem in ((True, (0, 300)), (False, (1000, 300))):
            jogador = Jogador(200, 408)
            jogador.tentar_bloqueio()
            jogador.take_damage(1, origem=origem, bloqueavel=bloqueavel)
            self.assertEqual(jogador.vida, 5)
            self.assertFalse(jogador.defesa.ativa)

    def test_quebra_de_guarda_e_recuperacao_exigem_soltar_e_esperar(self):
        self.jogador.tentar_bloqueio()
        for _ in range(4):
            self.jogador.defesa.janela_acerto = 0
            self.jogador.take_damage(1, origem=(1000, 300))
        self.assertEqual(self.jogador.vida, 5)
        self.assertEqual(self.jogador.defesa.resistencia, 0)
        self.assertGreater(self.jogador.defesa.quebra, 0)
        self.assertFalse(self.jogador.tentar_bloqueio())
        for _ in range(170):
            self.jogador.update(self.piso, [])
        self.assertEqual(self.jogador.defesa.resistencia, 100)
        self.assertTrue(self.jogador.tentar_bloqueio())

    def test_pausa_cancela_guarda_e_nao_recupera_postura_no_fundo(self):
        self.jogo.maquina_estados.estado = ESTADO_JOGANDO
        self.jogador.tentar_bloqueio()
        self.jogador.defesa.resistencia = 30
        self.jogo._process_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)])
        for _ in range(20):
            self.jogo._update(self.teclas, [])
        self.assertFalse(self.jogador.defesa.ativa)
        self.assertEqual(self.jogador.defesa.resistencia, 30)

    def test_projeteis_bloqueados_sao_removidos(self):
        fase = self.jogo.fase
        fase.chefe.activate()
        self.jogador.tentar_bloqueio()
        projetil = Projetil(self.jogador.rect.centerx+9, self.jogador.rect.centery, (1, 0), dono='boss', velocidade=1)
        fase.chefe.projeteis.add(projetil)
        fase.update(self.jogador, [])
        self.assertNotIn(projetil, fase.chefe.projeteis)
        self.assertEqual(self.jogador.vida, 6)

    def test_bloqueio_interrompe_investida_sem_acerto_pelas_costas(self):
        fase = self.jogo.fase
        chefe = fase.chefe
        fase.dialogo_exibido = True
        chefe.activate()
        chefe.estado_ataque = 'executar'
        chefe.temporizador_ataque = 27
        chefe.direcao_investida = 1
        chefe.rect.midbottom = (1500, 352)
        chefe.posicao.update(chefe.rect.topleft)
        self.jogador.rect.midbottom = (1530, 352)
        self.jogador.posicao.update(self.jogador.rect.topleft)
        self.jogador.direcao_olhar = -1
        self.jogador.tentar_bloqueio()
        fase.update(self.jogador, [])
        self.assertEqual(chefe.estado_ataque, 'recuperar')
        self.assertEqual(self.jogador.vida, 6)
        self.assertLess(self.jogador.defesa.resistencia, 100)

    def test_speedbug_retorna_do_limite_quando_jogador_muda_de_lado(self):
        chefe = RomerBug(400, 408, arena=pygame.Rect(0, 0, 1500, 448))
        chefe.activate()
        chefe.take_damage(8)
        chefe.temporizador_transformacao = 0
        chefe.temporizador_ataque = 400
        self.jogador.rect.x = 900
        for _ in range(100):
            chefe.update(self.jogador, self.piso)
        self.assertEqual(chefe.rect.x, 424)
        self.assertEqual(chefe.velocidade.x, 0)
        self.jogador.rect.x = 100
        for _ in range(60):
            chefe.update(self.jogador, self.piso)
        self.assertLess(chefe.rect.x, 424)
        self.assertGreaterEqual(chefe.rect.x, 376)

    def test_speedbug_na_parede_nao_oscila_subpixel_nem_atravessa_colisao(self):
        chefe = RomerBug(400, 408, arena=pygame.Rect(0, 0, 1500, 448))
        chefe.activate()
        chefe.take_damage(8)
        chefe.temporizador_transformacao = 0
        chefe.temporizador_ataque = 400
        parede = pygame.Rect(440, 0, 32, 448)
        self.jogador.rect.x = 900
        for _ in range(120):
            chefe.update(self.jogador, self.piso+[parede])
            self.assertFalse(chefe.rect.colliderect(parede))
        self.assertEqual(chefe.rect.x, 400)
        self.assertEqual(chefe.distancia_passada, 0)
        self.assertEqual(chefe.deslocamento_real, 0)

    def test_speedbug_corre_para_reposicionar_depois_da_recuperacao(self):
        chefe = RomerBug(400, 408, arena=pygame.Rect(0, 0, 1500, 448))
        chefe.activate()
        chefe.take_damage(8)
        chefe.temporizador_transformacao = 0
        chefe.estado_ataque = 'recuperar'
        chefe.temporizador_ataque = 1
        self.jogador.rect.x = 1000
        chefe.update(self.jogador, self.piso)
        self.assertEqual(chefe.estado_ataque, 'reposicionar')
        origem = chefe.rect.x
        for _ in range(65):
            chefe.update(self.jogador, self.piso)
        self.assertGreater(chefe.rect.x-origem, 100)
        self.assertFalse(chefe.get_all_hit_rects())

    def test_revisita_nao_recria_chefe_nem_cura(self):
        from sistema.eventos_campanha import FaseConcluida
        self.jogo.eventos_campanha.emitir(FaseConcluida('recreio'))
        self.jogador.vida = 2
        self.jogo._load_level(2, restaurar_integridade=False)
        self.assertTrue(self.jogo.fase.chefe.derrotado)
        self.assertFalse(self.jogo.fase.inimigos)
        self.assertEqual(self.jogador.vida, 2)
        self.assertEqual(len(self.jogo.fase.consultados), 3)

    def test_objetivos_concluidos_abrem_retomada_proxima_do_chefe(self):
        from sistema.eventos_campanha import ObjetivoConcluido
        for indice in range(3):
            self.jogo.eventos_campanha.emitir(ObjetivoConcluido('recreio', f'terminal_{indice}'))
        self.jogo._load_level(2)
        self.assertGreaterEqual(self.jogador.rect.left, self.jogo.fase.dados['arena_left'])
        self.assertFalse(self.jogo.fase.chefe.ativo)
        self.assertEqual(len(self.jogo.fase.consultados), 3)

    def test_queda_retorna_ao_apoio_e_conserva_objetivos(self):
        self.jogo._load_level(4)
        self.jogo.maquina_estados.estado = ESTADO_JOGANDO
        self.jogador.ultimo_apoio_seguro = (100, 408)
        self.jogador.rect.y = 1000
        self.jogador.posicao.update(self.jogador.rect.topleft)
        self.jogo.fase.consultados.add('terminal_0')
        self.jogo._update(self.teclas, [])
        self.assertEqual(self.jogador.rect.topleft, (100, 408))
        self.assertEqual(self.jogador.vida, 5)
        self.assertIn('terminal_0', self.jogo.fase.consultados)

    def test_atlas_novos_preservam_pes_e_geram_quatro_poses(self):
        for indice in range(2, 6):
            self.jogo._load_level(indice)
            chefe = self.jogo.fase.chefe
            quadros = chefe.figuras_guardiao[1]
            self.assertEqual(len(quadros), 4)
            for quadro in quadros:
                self.assertEqual(quadro.get_size(), (40, 40))
                self.assertEqual(quadro.get_bounding_rect().bottom, 40)

    def test_perigos_do_cenario_tem_aviso_e_desligam_por_objetivo(self):
        self.jogo._load_level(2)
        desafios = self.jogo.fase.desafios
        desafios.instante = 30
        self.assertNotIn(desafios.zonas[0], desafios.areas_ativas(set()))
        desafios.instante = 50
        self.assertIn(desafios.zonas[0], desafios.areas_ativas(set()))
        self.assertNotIn(desafios.zonas[0], desafios.areas_ativas({'terminal_0'}))

    def test_bola_ricocheteia_uma_vez_e_expira(self):
        bola = BolaVirtual(100, 433, 1)
        bola.velocidade.y = 5
        grupo = pygame.sprite.Group(bola)
        bola.update(self.piso)
        self.assertEqual(bola.ricochetes, 0)
        self.assertLess(bola.velocidade.y, 0)
        for _ in range(170):
            bola.update(self.piso)
        self.assertFalse(grupo)

    def test_max_muda_origem_real_e_invoca_bugs_com_limite(self):
        self.jogo._load_level(3)
        chefe = self.jogo.fase.chefe
        chefe.activate()
        origens = set()
        for _ in range(600):
            chefe.update(self.jogador, self.jogo.fase.mapa_blocos.solidos)
            origens.add(chefe.rect.x)
            if chefe.reforcos:
                chefe.quantidade_aliados += len(chefe.reforcos)
                chefe.reforcos.empty()
        self.assertGreater(len(origens), 1)
        self.assertEqual(chefe.quantidade_aliados, 2)

    def test_elevador_da_biblioteca_nao_cura_nem_remove_consultas(self):
        self.jogo._load_level(1)
        biblioteca = self.jogo.fase.biblioteca
        biblioteca.consultados.add(1)
        self.jogador.rect.midbottom = biblioteca.paineis[1].midbottom
        self.jogador.posicao.update(self.jogador.rect.topleft)
        self.jogador.vida = 2
        biblioteca.interagir(self.jogador, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)], self.jogo.fase.mapa_blocos.solidos)
        self.assertEqual(self.jogador.rect.bottom, biblioteca.y_piso)
        self.assertEqual(self.jogador.vida, 2)
        self.assertEqual(biblioteca.consultados, {1})

    def test_desligamento_pausa_antes_do_epilogo_e_monitores_apagam(self):
        self.jogo._load_school('lab')
        self.jogo.maquina_estados.estado = ESTADO_DIALOGO
        self.jogo._iniciar_desligamento()
        for _ in range(60):
            self.jogo._update(self.teclas, [])
        self.assertEqual(self.jogo.fase.arte.etapa_aula, 'desligado')
        self.jogo._process_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)])
        instante = self.jogo.encerramento.instante
        for _ in range(60):
            self.jogo._update(self.teclas, [])
        self.assertEqual(self.jogo.encerramento.instante, instante)
        self.jogo._process_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)])
        for _ in range(130):
            self.jogo._update(self.teclas, [])
        self.assertEqual(self.jogo.estado, ESTADO_DIALOGO)
        self.assertEqual(self.jogo.fase.ambiente, 'classroom')


if __name__ == '__main__':
    unittest.main()
