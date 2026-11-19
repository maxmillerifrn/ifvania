"""Capturas da mochila, troca de traje, equipamento e acesso ao A28."""
import os
os.environ.setdefault('SDL_VIDEODRIVER','dummy')
os.environ.setdefault('SDL_AUDIODRIVER','dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT','1')
from pathlib import Path
from collections import defaultdict
import pygame
from sistema.jogo import Jogo


def executar():
    destino = Path('avaliacao/equipamento_personagens')
    destino.mkdir(parents=True,exist_ok=True)
    jogo = Jogo()
    teclas = defaultdict(bool)
    for personagem in ('boy','menina'):
        jogo.personagem_escolhido = personagem
        jogo._start_story()
        for indice, tempo, nome in ((0,7.8,'com_mochila'),(0,8.8,'sem_mochila'),(2,14,'pesquisa'),
                                    (5,1.5,'recolhendo'),(5,3.5,'mochila_recolocada')):
            jogo.introducao.indice = indice
            jogo.introducao.quadro = round(tempo*60)
            jogo._draw()
            pygame.image.save(jogo.tela,destino/f'{personagem}_{nome}.png')
        jogo._concluir_introducao()
        jogo._load_school('corridor')
        jogo.jogador.rect.x = 1700
        jogo.jogador.posicao.x = 1700
        jogo.fase.camera.update(jogo.jogador.rect)
        jogo.fase.draw(jogo.tela)
        jogo.jogador.draw(jogo.tela,jogo.fase.camera)
        pygame.image.save(jogo.tela,destino/f'{personagem}_acesso_a28.png')
        jogo._enter_virtual()
        jogo.caixa_dialogo.ativo = False
        jogo._grant_mouse()
        for quadro in range(180):
            jogo._update(teclas,[])
            if quadro in (10,70,100,130,160):
                jogo._draw()
                pygame.image.save(jogo.tela,destino/f'{personagem}_equipando_{quadro:03}.png')
        jogo.estado = 'playing'
        jogo.jogador.temporizador_invulnerabilidade = 0
        jogo.jogador._try_melee()
        for _ in range(8): jogo.jogador.update(jogo.fase.mapa_blocos.solidos,[])
        jogo._draw()
        pygame.image.save(jogo.tela,destino/f'{personagem}_luva_vestida.png')
        jogo.maquina_estados.estado = 'menu'
    pygame.quit()
    print(f'{len(list(destino.glob("*.png")))} capturas em {destino}')


if __name__ == '__main__':
    executar()
