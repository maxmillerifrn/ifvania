"""Captura determinística de renderização real; estados preparados não são playthrough."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import sys
from pathlib import Path
from collections import defaultdict
import pygame
from sistema.jogo import *
from mundo.dados_fases import INDICE_MEMORIA_HISTORIA, INDICE_CORRUPCAO_HISTORIA


def capturar(destino):
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    jogo = Jogo()
    teclas = defaultdict(bool)
    def salvar(nome):
        jogo._draw()
        pygame.image.save(jogo.tela, str(destino / (nome+'.png')))
    def posicionar(x, y):
        jogo.jogador.rect.topleft = (x, y)
        jogo.jogador.posicao.update(x, y)
        jogo.jogador.velocidade.update(0, 0)
        jogo.fase.camera.update(jogo.jogador.rect)
    salvar('01_menu')
    jogo._process_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)])
    salvar('02_selecao')
    jogo._process_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)])
    salvar('03_nome')
    jogo._iniciar_prologo_escolar()
    jogo.caixa_dialogo._caracteres_exibidos = 1000
    salvar('04_aula')
    for indice, nome in [(INDICE_MEMORIA_HISTORIA, '05_memoria'), (INDICE_CORRUPCAO_HISTORIA, '06_hipnose')]:
        jogo.caixa_dialogo.indice = indice
        for _ in range(60): jogo._update(teclas, [])
        salvar(nome)
    jogo.na_introducao = False
    for ambiente in ('corridor', 'lab'):
        jogo._load_school(ambiente, novo_jogador=True)
        jogo.estado = ESTADO_JOGANDO
        salvar('07_'+ambiente+'_inicio')
        posicionar(1660 if ambiente == 'corridor' else 600, jogo.fase.Y_PISO-40)
        salvar('08_'+ambiente+'_destino')
    jogo._start_abduction()
    jogo.temporizador_abducao = 95
    salvar('09_succao')
    for indice in (0, 1):
        jogo._load_level(indice, novo_jogador=True)
        jogo.estado = ESTADO_JOGANDO
        jogo.jogador.chicote_desbloqueado = True
        salvar(f'fase{indice+1}_inicio')
        piso = jogo.jogador.rect.bottom
        for x in (500, 900, 1400, 2050):
            posicionar(x, piso-40)
            salvar(f'fase{indice+1}_regiao_{x}')
        posicionar(400, piso-40)
        jogo.jogador.no_chao = True
        for quadro in range(28):
            eventos = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)] if quadro == 10 else []
            jogo.jogador.handle_input(defaultdict(bool, {pygame.K_d: True}), eventos)
            jogo.jogador.update(jogo.fase.mapa_blocos.solidos, [])
            jogo.fase.camera.update(jogo.jogador.rect)
            if quadro in (7, 24): salvar(f'fase{indice+1}_'+('andando' if quadro == 7 else 'salto'))
        jogo.jogador.handle_input(teclas, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_x), pygame.event.Event(pygame.KEYUP, key=pygame.K_x)])
        for _ in range(8): jogo.jogador.update(jogo.fase.mapa_blocos.solidos, [])
        salvar(f'fase{indice+1}_ataque')
        posicionar(jogo.fase.chefe.rect.x-150, piso-40)
        jogo.fase.infectado = True
        jogo.fase.chefe.activate()
        for _ in range(55): jogo.fase.chefe.update(jogo.jogador, jogo.fase.mapa_blocos.solidos)
        salvar(f'fase{indice+1}_combate')
        jogo.estado_retorno_pausa = ESTADO_JOGANDO
        jogo.estado = ESTADO_PAUSA
        salvar(f'fase{indice+1}_pausa')
    for estado, nome in [(ESTADO_DERROTA, 'derrota'), (ESTADO_FIM_CONTEUDO, 'fim_conteudo'), (ESTADO_CARTAO_FASE, 'cartao')]:
        jogo.estado = estado
        salvar(nome)
    pygame.quit()
    print(f'{len(list(destino.glob("*.png")))} capturas em {destino}')

if __name__ == '__main__':
    capturar(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parents[1] / 'avaliacao' / 'visual' / 'atual')
