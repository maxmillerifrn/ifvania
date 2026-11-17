"""Regras de combate, navegação e campanha da primeira expansão integrada."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
from collections import defaultdict
import unittest
import pygame
from entidades.inimigo import Inimigo
from entidades.bug_combate import BugCombate
from entidades.fabrica_entidades import criar_inimigo, criar_chefe
from entidades.jogador import Jogador
from sistema.jogo import Jogo, ESTADO_JOGANDO, ESTADO_DIALOGO, ESTADO_PAUSA, ESTADO_VITORIA
from sistema.eventos_campanha import FaseConcluida, ChefeDerrotado
from sistema.habilidades import Habilidade
from sistema.comandos import interpretar
from mundo.camera import Camera
from mundo.campus_virtual import CampusVirtual


class TestesExpansao(unittest.TestCase):
    def setUp(self):
        self.jogo = Jogo()
        self.teclas = defaultdict(bool)
        self.interacao = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)]

    def tearDown(self):
        pygame.quit()

    def posicionar(self, centro):
        self.jogo.jogador.rect.center = centro
        self.jogo.jogador.posicao.update(self.jogo.jogador.rect.topleft)

    def test_barra_so_apos_dano_e_desenho_nao_avanca_temporizador(self):
        inimigo = Inimigo(100, 300, vida=3)
        self.assertEqual(inimigo.tempo_barra_vida, 0)
        inimigo.take_damage(1)
        self.assertEqual(inimigo.vida, 2)
        self.assertGreater(inimigo.brilho_dano, 0)
        tempo = inimigo.tempo_barra_vida
        for _ in range(10):
            inimigo.draw(self.jogo.tela, Camera(960, 540))
        self.assertEqual(inimigo.tempo_barra_vida, tempo)
        for _ in range(tempo):
            inimigo.update([pygame.Rect(0, 340, 960, 50)])
        self.assertEqual(inimigo.tempo_barra_vida, 0)
        inimigo.take_damage(1)
        self.assertEqual(inimigo.tempo_barra_vida, tempo)

    def test_recuo_respeita_parede_e_morte_remove_colisao_mas_preserva_impacto(self):
        self.jogo._load_level(0, novo_jogador=True)
        fase = self.jogo.fase
        inimigo = fase.inimigos.sprites()[0]
        inimigo.take_damage(1, recuo=(-8, -2))
        parede = pygame.Rect(inimigo.rect.left-10, 0, 10, 540)
        inimigo.update([parede])
        self.assertGreaterEqual(inimigo.rect.left, parede.right)
        fase.efeitos_combate.adicionar(inimigo.rect.center, True)
        inimigo.take_damage(99)
        self.assertNotIn(inimigo, fase.inimigos)
        self.assertTrue(fase.efeitos_combate.impactos)

    def test_combo_avanca_expira_e_esquiva_limpa_sequencia(self):
        jogador = Jogador(200, 300)
        jogador.no_chao = True
        for etapa in (1, 2, 3):
            jogador._try_melee()
            self.assertEqual(jogador.etapa_combo, etapa)
            for _ in range(30):
                jogador.update([] , [])
        jogador.cancelar_combate()
        jogador._try_melee(2)
        self.assertEqual(jogador.etapa_combo, 1)
        self.assertEqual(jogador.janela_combo, 0)

    def test_command_preserva_origem_e_descarta_repeticao(self):
        comando = interpretar(pygame.event.Event(pygame.KEYUP, key=pygame.K_k))
        self.assertEqual((comando.acao, comando.pressionado, comando.origem), ('ataque', False, ('tecla', pygame.K_k)))
        self.assertIsNone(interpretar(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_x, repeat=True)))

    def test_maquina_global_rejeita_transicao_invalida(self):
        with self.assertRaises(ValueError):
            self.jogo.estado = 'estado_inexistente'
        self.jogo.estado = ESTADO_JOGANDO
        self.jogo.estado = ESTADO_PAUSA
        with self.assertRaises(ValueError):
            self.jogo.estado = ESTADO_VITORIA

    def test_estrategia_pode_ser_substituida_e_preparacao_nao_causa_dano(self):
        class EstrategiaEsperar:
            def escolher(self, inimigo, jogador):
                return 'patrulhar'
        bug = BugCombate(100, 300, estrategia=EstrategiaEsperar())
        jogador = Jogador(160, 300)
        for _ in range(45):
            bug.atualizar_combate(jogador, [])
        self.assertEqual(bug.estados.estado, 'patrulhar')
        from entidades.estrategias_inimigos import EstrategiaCorpoACorpo
        bug.estrategia = EstrategiaCorpoACorpo()
        jogador.rect.center = bug.rect.center
        bug.atualizar_combate(jogador, [])
        self.assertEqual(bug.estados.estado, 'preparar')
        self.assertFalse(bug.areas_dano())

    def test_fabricas_rejeitam_tipo_desconhecido(self):
        with self.assertRaises(ValueError):
            criar_inimigo('invalido', 0, 0)
        with self.assertRaises(ValueError):
            criar_chefe('invalido')

    def test_guarda_bloqueia_frente_mas_permite_flanco_e_carregado(self):
        from entidades.bug_combate import BugGuarda
        guarda = BugGuarda(100, 100)
        guarda.direcao_ataque = -1
        guarda.take_damage(1, recuo=(5, 0))
        self.assertEqual(guarda.vida, 4)
        self.assertEqual(guarda.tempo_barra_vida, 0)
        self.assertGreater(guarda.brilho_bloqueio, 0)
        guarda.take_damage(1, recuo=(-5, 0))
        self.assertEqual(guarda.vida, 3)
        guarda.take_damage(2, recuo=(5, 0))
        self.assertEqual(guarda.vida, 1)

    def test_terminal_consultado_tem_prioridade_sobre_ancoragem(self):
        self.jogo._load_level(4, novo_jogador=True)
        jogador, fase = self.jogo.jogador, self.jogo.fase
        jogador.grant_ability(Habilidade.ANCORAGEM, aumentar_vida=False)
        self.posicionar(fase.objetivos[0].center)
        fase.conectores = [pygame.Vector2(jogador.rect.centerx+100, jogador.rect.centery-50)]
        fase.update(jogador, self.interacao)
        fase.update(jogador, self.interacao)
        self.assertEqual(jogador.temporizador_ancoragem, 0)

    def test_campus_nao_cura_na_troca_e_porta_exige_vitoria_anterior(self):
        self.jogo._load_level(1, novo_jogador=True)
        self.jogo.jogador.vida = 2
        self.jogo._load_campus('convivencia')
        self.assertEqual(self.jogo.jogador.vida, 2)
        self.posicionar((1510, 420))
        self.assertEqual(self.jogo.fase.update(self.jogo.jogador, self.interacao), (None, None))
        self.jogo.eventos_campanha.emitir(FaseConcluida('biblioteca'))
        self.assertEqual(self.jogo.fase.update(self.jogo.jogador, self.interacao), ('entrar_fase', 2))

    def test_objetivos_persistem_em_retomada_e_nao_duplicam(self):
        self.jogo._load_level(2, novo_jogador=True)
        fase = self.jogo.fase
        self.posicionar(fase.objetivos[0].center)
        self.assertEqual(fase.update(self.jogo.jogador, self.interacao)[0], 'dialogue')
        fase.update(self.jogo.jogador, self.interacao)
        self.assertEqual(len(fase.consultados), 1)
        self.jogo._load_level(2)
        self.assertEqual(len(self.jogo.fase.consultados), 1)
        self.assertIn(self.jogo.fase.portao_objetivos, self.jogo.fase.mapa_blocos.solidos)

    def test_objetivos_abrem_arena_e_chefes_tem_classes_distintas(self):
        classes = set()
        for indice in range(2, 6):
            self.jogo._load_level(indice, novo_jogador=True)
            fase = self.jogo.fase
            for terminal in fase.objetivos:
                self.posicionar(terminal.center)
                fase.update(self.jogo.jogador, self.interacao)
            self.assertNotIn(fase.portao_objetivos, fase.mapa_blocos.solidos)
            classes.add(type(fase.chefe))
        self.assertEqual(len(classes), 4)

    def test_boss_vencido_retorna_ao_campus_e_abre_caminho_seguinte(self):
        self.jogo._load_level(2, novo_jogador=True)
        fase = self.jogo.fase
        fase.chefe.activate()
        fase.chefe.take_damage(99)
        fase.update(self.jogo.jogador, [])
        self.jogo._advance_level()
        self.assertIsInstance(self.jogo.fase, CampusVirtual)
        self.assertIn('recreio', self.jogo.progresso_campanha.fases_concluidas)
        self.posicionar((1840, 420))
        self.assertEqual(self.jogo.fase.update(self.jogo.jogador, self.interacao), ('trocar_setor', ('jardim', 'inicio')))

    def test_ancoragem_liberada_apos_max_sem_cura_e_sem_resetar_salto(self):
        self.jogo._load_level(3, novo_jogador=True)
        jogador, fase = self.jogo.jogador, self.jogo.fase
        jogador.vida = 2
        fase.chefe.activate()
        fase.chefe.take_damage(99)
        fase.update(jogador, [])
        self.assertTrue(jogador.has(Habilidade.ANCORAGEM))
        self.assertEqual((jogador.vida, jogador.vida_maxima), (2, 6))
        self.jogo._load_level(4)
        self.posicionar((700, 310))
        jogador.saltos_usados = 2
        self.jogo.fase.update(jogador, self.interacao)
        self.assertGreater(jogador.temporizador_ancoragem, 0)
        jogador.update(self.jogo.fase.mapa_blocos.solidos, [])
        self.assertEqual(jogador.saltos_usados, 2)

    def test_nucleo_transforma_com_vida_compartilhada_e_sem_dano(self):
        self.jogo._load_level(5, novo_jogador=True)
        chefe = self.jogo.fase.chefe
        chefe.activate()
        chefe.take_damage(chefe.vida_maxima//2)
        vida = chefe.vida
        self.assertGreater(chefe.transicao_nucleo, 0)
        self.assertEqual(chefe.get_all_hit_rects(), [])
        chefe.take_damage(99)
        self.assertEqual(chefe.vida, vida)
        self.assertTrue(chefe.vinculo_rompido)

    def test_desfecho_exige_campanha_e_nova_historia_limpa_tudo(self):
        self.jogo._load_level(5, novo_jogador=True)
        self.jogo.maquina_estados.estado = ESTADO_JOGANDO
        self.jogo._encerrar_campanha()
        self.assertEqual(self.jogo.estado, ESTADO_JOGANDO)
        for dados in self.jogo.definicoes_fases:
            self.jogo.eventos_campanha.emitir(FaseConcluida(dados['identificador']))
        self.jogo._encerrar_campanha()
        self.assertEqual(self.jogo.estado, ESTADO_DIALOGO)
        for _ in range(20):
            self.jogo._process_events(self.interacao)
        for _ in range(181):
            self.jogo._update(self.teclas, [])
        for _ in range(12):
            self.jogo._process_events(self.interacao)
        self.assertEqual(self.jogo.estado, ESTADO_VITORIA)
        self.jogo._start_story()
        self.assertEqual(self.jogo.progresso_campanha.fases_concluidas, set())

    def test_apresentacao_hd_e_turma_preservam_corpo_e_transparencia(self):
        jogador = Jogador(200, 300)
        self.assertEqual(jogador.rect.size, (40, 40))
        self.assertEqual(jogador.get_draw_image().get_size(), (80, 80))
        from sistema import recursos
        self.assertIn(jogador.image, recursos._apresentacoes)
        for nome in ('aluno', 'aluna'):
            figura = recursos.load_image(f'cenarios/turma/{nome}_costas.png')
            self.assertEqual(figura.get_size(), (128, 168))
            self.assertEqual(figura.get_at((0, 0)).a, 0)

    def test_percursos_novos_alcancam_objetivos_com_fisica_real(self):
        for personagem in ('boy', 'menina'):
            self.jogo.personagem_escolhido = personagem
            for indice in range(2, 6):
                self.jogo._load_level(indice, novo_jogador=True)
                fase, aluno = self.jogo.fase, self.jogo.jogador
                aluno.grant_ability(Habilidade.SALTO_DUPLO, aumentar_vida=False)
                for terminal in fase.objetivos:
                    alcancou = False
                    for _ in range(700):
                        dx = terminal.centerx-aluno.rect.centerx
                        teclas = defaultdict(bool, {pygame.K_d: dx > 10, pygame.K_a: dx < -10})
                        saltar = aluno.no_chao or aluno.velocidade.y >= 0 and aluno.saltos_usados < 2
                        eventos = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)] if saltar else []
                        aluno.handle_input(teclas, eventos)
                        aluno.update(fase.mapa_blocos.solidos, [])
                        if aluno.rect.colliderect(terminal.inflate(60, 20)):
                            alcancou = True
                            break
                    self.assertTrue(alcancou, (personagem, indice, terminal))

    def test_pausa_congela_barras_recuo_e_efeitos(self):
        self.jogo._load_level(0, novo_jogador=True)
        self.jogo.maquina_estados.estado = ESTADO_JOGANDO
        fase = self.jogo.fase
        inimigo = fase.inimigos.sprites()[0]
        inimigo.take_damage(1, recuo=(5, -2))
        fase.efeitos_combate.adicionar(inimigo.rect.center)
        antes = (inimigo.tempo_barra_vida, inimigo.temporizador_recuo, inimigo.rect.copy(), fase.efeitos_combate.impactos[0][1])
        self.jogo._process_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)])
        for _ in range(30):
            self.jogo._update(self.teclas, [])
            self.jogo._draw()
        depois = (inimigo.tempo_barra_vida, inimigo.temporizador_recuo, inimigo.rect, fase.efeitos_combate.impactos[0][1])
        self.assertEqual(antes, depois)


if __name__ == '__main__':
    unittest.main()
