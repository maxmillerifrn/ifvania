"""Escala legível, terminais recortados e animação visual independente da física."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')

from collections import defaultdict
import unittest
import pygame
from jogo import Jogo, ESTADO_DIALOGO, ESTADO_PAUSA, ESTADO_JOGANDO
from entidades.professor import Professor
from entidades.inimigo import Inimigo
from entidades.jogador import Jogador
from mundo.terminal import TelaTerminal
from mundo.camera import Camera
from mundo.arte_escolar import ArteEscolar


class TestesVisualEscolar(unittest.TestCase):
    def setUp(self):
        self.jogo = Jogo()
        self.teclas = defaultdict(bool)

    def tearDown(self):
        pygame.quit()

    def test_larger_cast_preserves_body_size_feet_and_distinction_from_bugs(self):
        self.jogo._load_level(0, novo_jogador=True)
        elenco = [Jogador(120, 312, 'boy'), Jogador(120, 312, 'menina'),
                Professor(700, 312, 'max'), Professor(700, 312, 'romerito'), self.jogo.fase.chefe]
        for ator in elenco:
            self.assertEqual(ator.get_draw_image().get_size(), (80, 80))
            self.assertEqual(ator.rect.size, (40, 40))
            visual = ator.get_draw_image().get_rect(midbottom=ator.rect.midbottom)
            self.assertEqual(visual.bottom, ator.rect.bottom)
        self.assertEqual(Inimigo(0, 0).get_draw_image().get_size(), (40, 40))

    def test_terminal_changes_information_only_inside_monitor_and_restores_clipping(self):
        terminal = TelaTerminal()
        retangulo = pygame.Rect(40, 35, 72, 46)
        inicial = pygame.Surface((160, 120))
        inicial.fill((190, 100, 20))
        imagens = []
        for instante in (0, 35, 160, 315):
            superficie = inicial.copy()
            recorte = superficie.get_clip()
            terminal.draw(superficie, retangulo, instante)
            self.assertEqual(superficie.get_clip(), recorte)
            for x in range(superficie.get_width()):
                for y in range(superficie.get_height()):
                    if not retangulo.collidepoint(x, y):
                        self.assertEqual(superficie.get_at((x, y)), inicial.get_at((x, y)))
            imagens.append(pygame.image.tostring(superficie, 'RGB'))
        self.assertGreater(len(set(imagens)), 2)

    def test_scenery_information_tracks_camera_and_does_not_paint_bezels(self):
        arte = ArteEscolar('lab', 1920)
        camera = Camera(1920, 540)
        camera.deslocamento.x = 960
        primeiro = pygame.Surface((960, 540))
        segundo = primeiro.copy()
        arte.draw(primeiro, camera, 0, False)
        arte.draw(segundo, camera, 70, False)
        antes = pygame.image.tostring(primeiro, 'RGB')
        depois = pygame.image.tostring(segundo, 'RGB')
        retangulos = [camera.apply(retangulo) for retangulo in arte.telas_monitores]
        alteracoes = 0
        for i in range(0, len(antes), 3):
            if antes[i:i+3] != depois[i:i+3]:
                pixel = i//3
                self.assertTrue(any(r.collidepoint(pixel % 960, pixel//960) for r in retangulos))
                alteracoes += 1
        self.assertGreater(alteracoes, 50)

    def test_monitors_animate_during_intro_without_advancing_world_and_pause_freezes_them(self):
        self.jogo._start_story()
        ambiente = self.jogo.fase
        corpo = self.jogo.jogador.rect.copy()
        for _ in range(60): self.jogo._update(self.teclas, [])
        self.assertEqual(self.jogo.estado, ESTADO_DIALOGO)
        self.assertEqual(ambiente.instantes, 0)
        self.assertEqual(ambiente.instantes_visuais, 60)
        self.assertEqual(self.jogo.jogador.rect, corpo)
        self.jogo._process_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)])
        self.assertEqual(self.jogo.estado, ESTADO_PAUSA)
        for _ in range(60): self.jogo._update(self.teclas, [])
        self.assertEqual(ambiente.instantes_visuais, 60)

    def test_battle_monitors_change_during_dialogue_and_pause_holds_frame(self):
        self.jogo._load_level(0, novo_jogador=True)
        fase = self.jogo.fase
        self.jogo.estado = ESTADO_DIALOGO
        self.jogo.caixa_dialogo.start([('Sistema', 'Acesso ao laboratório.')])
        inicial = (fase.chefe.rect.copy(), fase.chefe.temporizador_ataque)
        for _ in range(70): self.jogo._update(self.teclas, [])
        self.assertEqual(fase.cenario_escolar.instantes_visuais, 70)
        self.assertEqual((fase.chefe.rect, fase.chefe.temporizador_ataque), inicial)
        self.jogo._process_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)])
        for _ in range(70): self.jogo._update(self.teclas, [])
        self.assertEqual(fase.cenario_escolar.instantes_visuais, 70)

    def test_whip_follows_scaled_hand_without_extending_tip_trajectory(self):
        jogador = Jogador(200, 312)
        jogador._try_melee()
        jogador.temporizador_golpe = jogador.chicote.DURACAO-10
        jogador.ESCALA_VISUAL = 1.0
        normal = jogador.chicote.points(jogador)
        jogador.ESCALA_VISUAL = 2.0
        ampliado = jogador.chicote.points(jogador)
        self.assertNotEqual(normal[0], ampliado[0])
        self.assertEqual(normal[-1], ampliado[-1])
        self.assertEqual(jogador.rect.size, (40, 40))
        parede = pygame.Rect(jogador.rect.right, 250, 32, 150)
        self.assertTrue(all(p.x <= parede.left for p in jogador.chicote.points(jogador, [parede])))


if __name__ == '__main__':
    unittest.main()
