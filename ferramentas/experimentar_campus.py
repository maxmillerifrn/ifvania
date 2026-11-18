"""Entrada de desenvolvimento e capturas; não adiciona atalhos ao menu do jogo."""
import argparse
from pathlib import Path
import pygame
from sistema.jogo import Jogo, ESTADO_JOGANDO, ESTADO_DIALOGO, ESTADO_VITORIA
from sistema.habilidades import Habilidade
from sistema.eventos_campanha import FaseConcluida, ChefeDerrotado


def preparar(jogo, indice):
    jogo.modo_experimento = True
    jogo._iniciar_sessao_campanha()
    for dados in jogo.definicoes_fases[:indice]:
        jogo.eventos_campanha.emitir(FaseConcluida(dados['identificador']))
        jogo.eventos_campanha.emitir(ChefeDerrotado(dados['identificador']))
    jogo._load_level(indice, novo_jogador=True)
    jogo.jogador.grant_ability(Habilidade.SALTO_DUPLO, aumentar_vida=False)
    if indice >= 4:
        jogo.jogador.grant_ability(Habilidade.ANCORAGEM, aumentar_vida=False)
    jogo.maquina_estados.estado = ESTADO_JOGANDO


def preparar_duelo(jogo):
    """Encontro inicial sem habilidades futuras; somente atalho de desenvolvimento."""
    jogo.modo_experimento = True
    jogo._iniciar_sessao_campanha()
    jogo._load_level(0, novo_jogador=True)
    fase = jogo.fase
    fase.infectado = fase.dialogo_exibido = True
    fase.inimigos.empty()
    fase.chefe.activate()
    jogador = jogo.jogador
    jogador.rect.midbottom = (fase.chefe.rect.centerx-110, fase.chefe.rect.bottom)
    jogador.posicao.update(jogador.rect.topleft)
    jogador.direcao_olhar = 1
    fase.camera.update(jogador.rect)
    jogo.maquina_estados.estado = ESTADO_JOGANDO


def capturar(jogo, destino):
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    jogo._load_school('classroom', novo_jogador=True)
    jogo.maquina_estados.estado = ESTADO_JOGANDO
    jogo._draw()
    pygame.image.save(jogo.tela, str(destino/'laboratorio.png'))
    for indice in range(6):
        preparar(jogo, indice)
        jogo.fase.inimigos.sprites()[0].take_damage(1, recuo=(5, -2))
        jogo._draw()
        pygame.image.save(jogo.tela, str(destino/f'fase_{indice+1}.png'))
        if indice >= 2:
            chefe = jogo.fase.chefe
            jogo.jogador.rect.midbottom = (chefe.rect.centerx-130, chefe.rect.bottom)
            jogo.jogador.posicao.update(jogo.jogador.rect.topleft)
            jogo.fase.camera.update(jogo.jogador.rect)
            chefe.activate()
            chefe.preparar(jogo.jogador)
            jogo._draw()
            pygame.image.save(jogo.tela, str(destino/f'arena_{indice+1}.png'))
    jogo._load_campus('convivencia', 'recreio')
    jogo.maquina_estados.estado = ESTADO_JOGANDO
    jogo._draw()
    pygame.image.save(jogo.tela, str(destino/'campus.png'))
    for indice, nome in ((2, 'campus_antes'), (3, 'campus_depois')):
        preparar(jogo, indice)
        jogo._load_campus('convivencia', 'recreio')
        jogo.maquina_estados.estado = ESTADO_JOGANDO
        jogo._draw()
        pygame.image.save(jogo.tela, str(destino/f'{nome}.png'))
    preparar(jogo, 0)
    jogo.jogador.tentar_bloqueio()
    jogo.jogador.temporizador_invulnerabilidade = 0
    jogo.jogador.take_damage(1, origem=(jogo.jogador.rect.right+20, jogo.jogador.rect.centery))
    jogo._draw()
    pygame.image.save(jogo.tela, str(destino/'bloqueio.png'))
    jogo._enter_virtual()
    jogo.caixa_dialogo.indice = 2
    for _ in range(45):
        jogo._update({}, [])
    jogo._draw()
    pygame.image.save(jogo.tela, str(destino/'descoberta_mouse.png'))
    preparar(jogo, 5)
    jogo.eventos_campanha.emitir(FaseConcluida('continuidade'))
    jogo._encerrar_campanha()
    jogo._iniciar_desligamento()
    for _ in range(120):
        jogo._update({}, [])
    jogo._draw()
    pygame.image.save(jogo.tela, str(destino/'desligamento.png'))
    for _ in range(61):
        jogo._update({}, [])
    jogo._draw()
    pygame.image.save(jogo.tela, str(destino/'epilogo.png'))
    for _ in range(12):
        jogo._process_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)])
    if jogo.estado != ESTADO_VITORIA:
        raise RuntimeError('O epílogo não concluiu a campanha')
    jogo._draw()
    pygame.image.save(jogo.tela, str(destino/'fachada_final.png'))


def principal():
    argumentos = argparse.ArgumentParser()
    argumentos.add_argument('--fase', type=int, choices=range(1, 7), default=3)
    argumentos.add_argument('--campus', action='store_true')
    argumentos.add_argument('--duelo', action='store_true', help='Experimentar RomerBug diretamente, sem poderes futuros')
    argumentos.add_argument('--capturas')
    opcoes = argumentos.parse_args()
    jogo = Jogo()
    if opcoes.capturas:
        capturar(jogo, opcoes.capturas)
        pygame.quit()
        return
    if opcoes.duelo:
        preparar_duelo(jogo)
    else:
        preparar(jogo, opcoes.fase-1)
    if opcoes.campus:
        jogo._load_campus('convivencia', 'biblioteca')
        jogo.maquina_estados.estado = ESTADO_JOGANDO
    jogo.run()


if __name__ == '__main__':
    principal()
