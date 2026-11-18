"""Registra a carga e os retratos usando a renderização real do Pygame."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
from collections import defaultdict
from pathlib import Path
import argparse
import pygame
from sistema.jogo import Jogo, ESTADO_JOGANDO, ESTADO_DIALOGO


def principal(destino, salvar_quadros=False):
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    jogo = Jogo()
    teclas = defaultdict(bool)
    quadros = []
    for personagem in ('boy', 'menina'):
        jogo.personagem_escolhido = personagem
        jogo._load_level(0, novo_jogador=True)
        jogo.estado = ESTADO_JOGANDO
        jogador = jogo.jogador
        jogador.handle_input(teclas, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_k)])
        for instante in range(72):
            jogador.handle_input(defaultdict(bool, {pygame.K_d: instante < 45}), [])
            jogador.update(jogo.fase.mapa_blocos.solidos, [])
            jogo.fase.camera.update(jogador.rect)
            jogo._draw()
            if personagem == 'boy': quadros.append(jogo.tela.copy())
            if instante in (10, 26, 39, 61, 71):
                pygame.image.save(jogo.tela, str(destino/f'carga_{personagem}_{instante:02d}.png'))
    jogo.nome_jogador = 'Alex'
    jogo.nome_digitado = 'Alex'
    jogo._iniciar_prologo_escolar()
    for personagem in ('boy', 'menina'):
        jogo.personagem_escolhido = personagem
        jogo._iniciar_prologo_escolar()
        for falante in ('Alex', 'Professor Max', 'Professor Romerito', 'IFVania', 'Sistema', 'Indexador'):
            jogo.estado = ESTADO_DIALOGO
            jogo.caixa_dialogo.start([(falante, 'A carga continua enquanto eu caminho. Precisamos encontrar uma saída para a escola.')])
            jogo.caixa_dialogo._caracteres_exibidos = 1000
            jogo._draw()
            pygame.image.save(jogo.tela, str(destino/f'dialogo_{personagem}_{falante.lower().replace(" ", "_")}.png'))
    if salvar_quadros:
        for indice, quadro in enumerate(quadros):
            pygame.image.save(quadro, str(destino/f'animacao_{indice:03d}.png'))
    pygame.quit()
    print(f'Capturas em {destino}; animacao_*.png permite montar uma prévia com ffmpeg.')


if __name__ == '__main__':
    analisador = argparse.ArgumentParser(description=__doc__)
    analisador.add_argument('destino', nargs='?', type=Path,
                            default=Path(__file__).resolve().parents[1]/'avaliacao'/'carga_dialogos')
    analisador.add_argument('--quadros', action='store_true', help='Exportar sequência opcional para prévia animada.')
    argumentos = analisador.parse_args()
    principal(argumentos.destino, argumentos.quadros)
