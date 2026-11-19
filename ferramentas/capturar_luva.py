"""Percorre o relógio completo da abertura e registra renderizações na engine.

Não substitui avaliação humana de controles e áudio. Não escreve no save real.
"""
from pathlib import Path
from collections import defaultdict
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import pygame
from sistema.jogo import Jogo, ESTADO_INTRODUCAO


def executar():
    destino = Path('avaliacao/luva_robotica/revisao_escola')
    destino.mkdir(parents=True, exist_ok=True)
    jogo = Jogo()
    jogo._start_story()
    teclas = defaultdict(bool)
    alvos = {0: 8.7, 1: 8, 2: 14, 3: 6, 4: 12, 5: 7}
    capturadas = set()
    quadros = 0
    while jogo.estado == ESTADO_INTRODUCAO:
        abertura = jogo.introducao
        # Desenha todos os quadros para exercitar animações e transições.
        jogo._draw()
        if abertura.indice not in capturadas and abertura.tempo >= alvos[abertura.indice]:
            pygame.image.save(jogo.tela, destino/f'{abertura.indice+1:02}_{abertura.CENAS[abertura.indice].encenar}.png')
            capturadas.add(abertura.indice)
        jogo._update(teclas, [])
        quadros += 1
    def salvar(nome):
        jogo._draw()
        pygame.image.save(jogo.tela, destino/f'{nome}.png')
    def tecla(codigo):
        return jogo._process_events([pygame.event.Event(pygame.KEYDOWN, key=codigo)])
    def concluir_dialogo():
        for _ in range(90):
            if not jogo.caixa_dialogo.ativo:
                if jogo.descoberta_mouse and jogo.descoberta_mouse.aguardando_conclusao:
                    for _ in range(jogo.descoberta_mouse.DURACAO):
                        jogo._update(teclas, [])
                return
            tecla(pygame.K_e)
            jogo._update(teclas, [])
        raise RuntimeError('Diálogo não terminou')
    def andar(destino_x):
        for _ in range(600):
            if jogo.jogador.rect.x >= destino_x:
                return
            jogo._update(defaultdict(bool, {pygame.K_d: True}), [])
        raise RuntimeError('Percurso não concluído')
    jogo.caixa_dialogo._caracteres_exibidos = 1000
    salvar('07_apresentacao_max')
    concluir_dialogo()
    tecla(pygame.K_RETURN)
    salvar('08_corredor')
    andar(jogo.fase.porta_a28.x-40)
    jogo._update(teclas, tecla(pygame.K_e))
    andar(630)
    jogo._update(teclas, tecla(pygame.K_e))
    jogo.caixa_dialogo._caracteres_exibidos = 1000
    salvar('09_romerito')
    concluir_dialogo()
    for _ in range(jogo.duracao_abducao):
        jogo._update(teclas, [])
    jogo.caixa_dialogo._caracteres_exibidos = 1000
    salvar('10_mundo_virtual')
    concluir_dialogo()
    tecla(pygame.K_RETURN)
    jogo._update(teclas, [])
    salvar('11_tutorial')
    jogador = jogo.jogador
    jogador.temporizador_invulnerabilidade = 0
    jogador._try_melee()
    for _ in range(9): jogador.update(jogo.fase.mapa_blocos.solidos, [])
    jogo._draw()
    pygame.image.save(jogo.tela, destino/'12_soco.png')
    pygame.quit()
    print(f'{quadros} quadros percorridos; 12 capturas em {destino}')


if __name__ == '__main__':
    executar()
