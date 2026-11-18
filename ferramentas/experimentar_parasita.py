"""Capturas controladas de fusão, forma sombria, libertação e menu com save temporário."""
import argparse
from collections import defaultdict
from pathlib import Path
from tempfile import TemporaryDirectory
import pygame
from sistema.jogo import Jogo, ESTADO_JOGANDO, ESTADO_DIALOGO, ESTADO_INFECCAO, ESTADO_TRANSFORMACAO_CHEFE


def capturar(destino):
    destino = Path(destino)
    destino.mkdir(parents=True,exist_ok=True)
    jogo = Jogo()
    jogo._load_level(0,novo_jogador=True)
    jogo.maquina_estados.estado = ESTADO_JOGANDO
    teclas = defaultdict(bool)
    fase = jogo.fase
    for inimigo in list(fase.inimigos)[:-1]: inimigo.take_damage(100)
    bug = fase.inimigos.sprites()[0]
    jogo.jogador.rect.topleft = (bug.rect.x-55,bug.rect.y)
    jogo.jogador.posicao.update(jogo.jogador.rect.topleft)
    bug.take_damage(100)
    jogo._update(teclas,[])

    def foto(nome):
        jogo._draw()
        pygame.image.save(jogo.tela,str(destino/f'{nome}.png'))

    cena = jogo.cena_parasita
    alvos = {25:'fuga',cena.corrida+22:'fusao'}
    while jogo.estado == ESTADO_INFECCAO:
        jogo._update(teclas,[])
        if cena.instante in alvos: foto(alvos[cena.instante])
    for _ in range(25):
        if jogo.estado != ESTADO_DIALOGO: break
        jogo._process_events([pygame.event.Event(pygame.KEYDOWN,key=pygame.K_e)])
    jogo.jogador.rect.midbottom = (fase.chefe.rect.centerx-110,fase.chefe.rect.bottom)
    jogo.jogador.posicao.update(jogo.jogador.rect.topleft)
    jogo.jogador.temporizador_invulnerabilidade = 0
    fase.camera.update(jogo.jogador.rect)
    jogo.jogador.tentar_bloqueio()
    teclas[pygame.K_d] = True
    for _ in range(8):
        jogo.jogador.handle_input(teclas,[])
        jogo.jogador.update(fase.mapa_blocos.solidos,[])
    foto('guarda_caminhando')
    teclas.clear()
    fase.chefe.take_damage(8)
    jogo._update(teclas,[])
    for _ in range(400):
        if jogo.estado != ESTADO_TRANSFORMACAO_CHEFE: break
        if jogo.caixa_dialogo.ativo:
            jogo._process_events([pygame.event.Event(pygame.KEYDOWN,key=pygame.K_e)])
        jogo._update(teclas,[])
        if jogo.transicao_chefe.etapa == 'morph' and jogo.transicao_chefe.instante == 25: foto('metamorfose_sombria')
    foto('speedbug_sombrio')
    fase.chefe.take_damage(8)
    jogo._update(teclas,[])
    for _ in range(150):
        jogo._update(teclas,[])
        if jogo.cena_parasita is not None:
            if jogo.cena_parasita.instante == 60: foto('expulsao')
            if jogo.cena_parasita.instante == 115: foto('desintegracao')
    with TemporaryDirectory(prefix='ifvania_previa_save_') as pasta:
        salvo = Jogo(caminho_salvamento=Path(pasta)/'save.json')
        salvo._load_level(0,novo_jogador=True)
        menu = Jogo(caminho_salvamento=Path(pasta)/'save.json')
        menu._draw()
        pygame.image.save(menu.tela,str(destino/'menu_continuar.png'))
    pygame.quit()


if __name__ == '__main__':
    argumentos = argparse.ArgumentParser()
    argumentos.add_argument('--destino',default='avaliacao/parasita_e_save')
    capturar(argumentos.parse_args().destino)
