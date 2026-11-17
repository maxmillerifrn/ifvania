"""Regressões encontradas na avaliação offscreen de novembro."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
import unittest
import pygame
from mundo.camera import Camera
from sistema.jogo import Jogo


class TestesAvaliacaoVisual(unittest.TestCase):
    def test_camera_estabiliza_salto_e_acompanha_subida_alta(self):
        camera = Camera(2500, 1200)
        alvo = pygame.Rect(400, 408, 40, 40)
        camera.update(alvo)
        inicio = camera.deslocamento.y
        alvo.y -= 80
        camera.update(alvo)
        self.assertEqual(camera.deslocamento.y, inicio)
        alvo.y -= 130
        camera.update(alvo)
        self.assertEqual(alvo.centery-camera.deslocamento.y, 180)
        alvo.y = 1150
        camera.update(alvo)
        self.assertLessEqual(camera.deslocamento.y, 660)
        alvo.y = -100
        camera.update(alvo)
        self.assertEqual(camera.deslocamento.y, 0)

    def test_sinal_do_portao_sobrevive_aos_solidos_e_acompanha_camera(self):
        jogo = Jogo()
        try:
            jogo._load_level(1, novo_jogador=True)
            fase = jogo.fase
            biblioteca = fase.biblioteca
            fase.camera.deslocamento.update(1400, 48)
            corpos = [r.copy() for r in fase.mapa_blocos.solidos]
            fase.draw(jogo.tela)
            destino = fase.camera.apply(biblioteca.portao)
            self.assertEqual(jogo.tela.get_at((destino.x+1, destino.top+33))[:3], (228, 191, 122))
            self.assertEqual(fase.mapa_blocos.solidos, corpos)
            biblioteca.consultados.update((0, 1, 2))
            fase.mapa_blocos.solidos.remove(biblioteca.portao)
            fase.draw(jogo.tela)
            self.assertNotEqual(jogo.tela.get_at((destino.x+1, destino.top+33))[:3], (228, 191, 122))
        finally:
            pygame.quit()

    def test_preparacao_dos_chefes_nao_desenha_miras_nem_rotulos(self):
        jogo = Jogo()
        try:
            for indice in (0, 1):
                jogo._load_level(indice, novo_jogador=True)
                chefe = jogo.fase.chefe
                chefe.activate()
                camera = Camera(960, 540)
                camera.deslocamento.update(chefe.rect.x-480, chefe.rect.bottom-400)
                imagem = chefe.get_draw_image()
                # Margem da inclinação corporal; continua proibindo marcas no cenário.
                corpo_visual = imagem.get_rect(midbottom=camera.apply(chefe.rect).midbottom).inflate(28, 28)
                estados = ('preparar_disparo', 'pausa', 'preparar', 'executar', 'recuperar') if indice == 0 else ('carimbar',)
                for estado in estados:
                    chefe.estado_ataque = estado
                    if indice == 1:
                        chefe.relogio_ataque = 24
                        chefe.faixas = [pygame.Rect(chefe.rect.x-140, 32, 56, 416)]
                    tela = pygame.Surface((960, 540))
                    tela.fill((1, 2, 3))
                    chefe.draw(tela, camera)
                    # Qualquer marca fora da figura revelaria mira, texto ou faixa.
                    tela.fill((1, 2, 3), corpo_visual)
                    esperado = pygame.Surface((960, 540))
                    esperado.fill((1, 2, 3))
                    self.assertEqual(pygame.image.tostring(tela, 'RGB'), pygame.image.tostring(esperado, 'RGB'), (indice, estado))
        finally:
            pygame.quit()

    def test_patio_tem_piso_abaixo_dos_bancos_e_porta_alinhada(self):
        from collections import defaultdict
        jogo = Jogo()
        try:
            jogo._load_school('corridor', novo_jogador=True)
            fase = jogo.fase
            self.assertEqual(jogo.jogador.rect.bottom, 440)
            self.assertEqual(fase.porta_a28.bottom, 440)
            for _ in range(12):
                jogo.jogador.handle_input(defaultdict(bool, {pygame.K_d: True}), [])
                jogo.jogador.update(fase.mapa_blocos.solidos, [])
            self.assertEqual(jogo.jogador.rect.bottom, 440)
            self.assertTrue(jogo.jogador.no_chao)
        finally:
            pygame.quit()
