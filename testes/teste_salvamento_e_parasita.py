"""Persistência real em temporário e cenas acionadas pelo golpe final."""
import os
os.environ.setdefault('SDL_VIDEODRIVER','dummy')
os.environ.setdefault('SDL_AUDIODRIVER','dummy')
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import unittest
import pygame
from sistema.jogo import Jogo, ESTADO_JOGANDO, ESTADO_INFECCAO, ESTADO_DIALOGO, ESTADO_PAUSA, ESTADO_MENU, ESTADO_DERROTA
from sistema.habilidades import Habilidade
from sistema.salvamento import ArmazemSalvamento
from sistema.eventos_campanha import FaseConcluida, ChefeDerrotado, ObjetivoConcluido


class TestesSalvamentoParasita(unittest.TestCase):
    def setUp(self):
        self.pasta = TemporaryDirectory()
        self.caminho = Path(self.pasta.name)/'save.json'
        self.jogo = Jogo(caminho_salvamento=self.caminho)
        self.jogo._load_level(0,novo_jogador=True)
        self.jogo.maquina_estados.estado = ESTADO_JOGANDO
        self.teclas = defaultdict(bool)

    def tearDown(self):
        pygame.quit()
        self.pasta.cleanup()

    def ultimo_bug(self):
        fase = self.jogo.fase
        for inimigo in list(fase.inimigos)[:-1]: inimigo.take_damage(100)
        bug = fase.inimigos.sprites()[0]
        self.jogo.jogador.rect.topleft = (bug.rect.x-60,bug.rect.y)
        self.jogo.jogador.posicao.update(self.jogo.jogador.rect.topleft)
        return bug

    def concluir_cena(self):
        for _ in range(400):
            if self.jogo.estado != ESTADO_INFECCAO: return
            self.jogo._update(self.teclas,[])
        self.fail('Cena não terminou')

    def test_ultimo_golpe_inicia_fuga_fusao_e_dialogo_antes_do_combate(self):
        bug = self.ultimo_bug()
        bug.take_damage(100)
        self.assertTrue(self.jogo.fase.fusao_pendente)
        self.assertFalse(self.jogo.fase.inimigos)
        self.assertFalse(self.jogo.fase.infectado)
        self.jogo._update(self.teclas,[])
        self.assertEqual(self.jogo.estado,ESTADO_INFECCAO)
        corpo = self.jogo.fase.chefe.rect.copy()
        self.concluir_cena()
        self.assertEqual(self.jogo.estado,ESTADO_DIALOGO)
        self.assertTrue(self.jogo.fase.chefe.ativo)
        self.assertTrue(self.jogo.fase.infectado)
        self.assertEqual(self.jogo.fase.chefe.rect,corpo)
        self.assertEqual(self.jogo.checkpoints.checkpoint['cena']['marco'],'arena')

    def test_fusao_so_ocorre_no_ultimo_bug_e_nao_ao_entrar_arena(self):
        fase = self.jogo.fase
        fase.inimigos.sprites()[0].take_damage(100)
        self.assertFalse(fase.fusao_pendente)
        self.jogo.jogador.rect.topleft = fase.mapa_blocos.gatilho_dialogo.topleft
        self.assertNotEqual(fase.update(self.jogo.jogador,[])[0],'dialogue')
        self.assertFalse(fase.infectado)

    def test_pausa_congela_fusao_e_desenho_nao_atualiza_cena(self):
        self.ultimo_bug().take_damage(100)
        self.jogo._update(self.teclas,[])
        cena = self.jogo.cena_parasita
        self.jogo._draw()
        self.assertEqual(cena.instante,0)
        self.jogo._process_events([pygame.event.Event(pygame.KEYDOWN,key=pygame.K_ESCAPE)])
        self.assertEqual(self.jogo.estado,ESTADO_PAUSA)
        for _ in range(30): self.jogo._update(self.teclas,[])
        self.assertEqual(cena.instante,0)

    def test_vitoria_expulsa_desintegra_e_liberta_sem_repetir_cena(self):
        fase = self.jogo.fase
        fase.infectado = fase.dialogo_exibido = True
        fase.chefe.activate()
        fase.chefe.take_damage(8)
        fase.chefe.finish_cinematic()
        fase.chefe.take_damage(8)
        self.jogo._update(self.teclas,[])
        self.assertEqual(self.jogo.cena_parasita.modo,'libertacao')
        self.assertFalse(fase.professor_liberto)
        self.concluir_cena()
        self.assertTrue(fase.professor_liberto)
        self.assertTrue(fase.libertacao_concluida)
        self.assertEqual(self.jogo.estado,ESTADO_DIALOGO)
        self.assertIn('a28',self.jogo.progresso_campanha.chefes_derrotados)
        self.assertNotEqual(fase.update(self.jogo.jogador,[])[0],'libertacao')

    def test_bloqueio_permite_caminhada_com_animacao_e_velocidade_normal(self):
        jogador = self.jogo.jogador
        jogador.no_chao = True
        jogador.tentar_bloqueio()
        self.teclas[pygame.K_d] = True
        imagens = set()
        for _ in range(20):
            jogador.handle_input(self.teclas,[])
            jogador.update(self.jogo.fase.mapa_blocos.solidos,[])
            imagens.add(id(jogador.image))
        from sistema.configuracoes import VELOCIDADE_JOGADOR
        self.assertEqual(jogador.velocidade.x,VELOCIDADE_JOGADOR)
        self.assertTrue(jogador.defesa.ativa)
        self.assertGreater(len(imagens),2)

    def test_salvar_continuar_preserva_identidade_habilidades_e_objetivos(self):
        jogo = self.jogo
        jogo.jogador.nome = 'Lia'
        jogo.jogador.personagem = 'menina'
        jogo.jogador.grant_ability(Habilidade.SALTO_DUPLO,aumentar_vida=False)
        jogo.eventos_campanha.emitir(FaseConcluida('a28'))
        jogo.eventos_campanha.emitir(ObjetivoConcluido('recreio','terminal_0'))
        jogo.checkpoints.registrar()
        outro = Jogo(caminho_salvamento=self.caminho)
        self.assertTrue(outro.interface_inicial.tem_salvamento)
        outro.indice_menu = 1
        outro._activate_menu()
        self.assertEqual(outro.estado,ESTADO_JOGANDO)
        self.assertEqual(outro.jogador.nome,'Lia')
        self.assertEqual(outro.jogador.personagem,'menina')
        self.assertTrue(outro.jogador.has(Habilidade.SALTO_DUPLO))
        self.assertIn('a28',outro.progresso_campanha.fases_concluidas)
        self.assertIn('terminal_0',outro.progresso_campanha.objetivos_da_fase('recreio'))

    def test_morte_recomeca_no_checkpoint_com_integridade_e_inimigos_corretos(self):
        jogo = self.jogo
        jogo.fase.inimigos.sprites()[0].take_damage(100)
        jogador = jogo.jogador
        jogador.rect.topleft = jogo.fase._grounded_spawn(800,312)
        jogador.posicao.update(jogador.rect.topleft)
        jogo.checkpoints.registrar('travessia')
        ponto = jogador.rect.topleft
        vivos = len(jogo.fase.inimigos)
        jogador.vida = 0
        jogador.vivo = False
        jogo.estado = ESTADO_DERROTA
        jogo._process_events([pygame.event.Event(pygame.KEYDOWN,key=pygame.K_r)])
        self.assertEqual(jogo.estado,ESTADO_JOGANDO)
        self.assertEqual(jogo.jogador.rect.topleft,ponto)
        self.assertEqual(jogo.jogador.vida,jogo.jogador.vida_maxima)
        self.assertEqual(len(jogo.fase.inimigos),vivos)

    def test_save_corrompido_nao_quebra_menu_nem_habilita_continuar(self):
        self.caminho.write_text('{quebrado')
        outro = Jogo(caminho_salvamento=self.caminho)
        self.assertFalse(outro.interface_inicial.tem_salvamento)
        self.assertFalse(outro.checkpoints.continuar())
        self.assertEqual(outro.estado,ESTADO_MENU)

    def test_falha_de_gravacao_preserva_arquivo_anterior(self):
        anterior = self.caminho.read_bytes()
        dados = deepcopy(self.jogo.checkpoints.checkpoint)
        dados['nome'] = 'Novo'
        with patch('pathlib.Path.replace',side_effect=OSError('sem permissão')):
            self.assertFalse(self.jogo.checkpoints.armazem.salvar(dados))
        self.assertEqual(self.caminho.read_bytes(),anterior)

    def test_continuar_apos_vitoria_nao_recria_chefe_ou_parasita(self):
        jogo = self.jogo
        jogo.eventos_campanha.emitir(ChefeDerrotado('a28'))
        jogo.checkpoints.registrar('vitoria')
        outro = Jogo(caminho_salvamento=self.caminho)
        self.assertTrue(outro.checkpoints.continuar())
        self.assertTrue(outro.fase.chefe.derrotado)
        self.assertTrue(outro.fase.professor_liberto)
        self.assertNotEqual(outro.fase.update(outro.jogador,[])[0],'libertacao')

    def test_save_campus_reabre_setor_e_validacao_rejeita_habilidade_invalida(self):
        self.jogo.eventos_campanha.emitir(FaseConcluida('a28'))
        self.jogo._load_campus('jardim')
        outro = Jogo(caminho_salvamento=self.caminho)
        self.assertTrue(outro.checkpoints.continuar())
        self.assertEqual(outro.fase.setor,'jardim')
        dados = deepcopy(outro.checkpoints.checkpoint)
        dados['habilidades'] = ['EXECUTAR_CODIGO']
        self.assertFalse(ArmazemSalvamento.validar(dados))
