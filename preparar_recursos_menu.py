"""Prepara a fachada e os onze quadros da Menina sem redesenhar a arte.

Execute após atualizar as fontes em recursos/fontes_arte. Não altera os sprites
existentes do Menino. Extração e exportação usam o pipeline local de Pygame.
"""
import pygame
import configuracoes
from preparar_figuras_personagens import ORIGENS, DESTINO, extract_figures, export_frames


NOMES_QUADROS = [
    "repouso_0.png", "repouso_1.png",
    "caminhada_0.png", "caminhada_1.png", "caminhada_2.png", "caminhada_3.png",
    "salto.png", "arrancada.png", "ataque_0.png", "ataque_1.png", "ataque_2.png",
]


def principal():
    pygame.init()
    pygame.display.set_mode((1, 1))
    try:
        # Valida o atlas completo antes de escrever os quadros consumidos.
        figuras = extract_figures("aluna.png", fileiras=3, colunas=4)
        fachada = pygame.image.load(str(ORIGENS / "fachada_escola.png")).convert()
        export_frames(figuras[:11], "jogador/menina", NOMES_QUADROS, configuracoes.TAMANHO_PERSONAGEM)
        destino = DESTINO / "menu"
        destino.mkdir(parents=True, exist_ok=True)
        # Grade de 480 × 270 ampliada em escala inteira para a janela.
        fachada = pygame.transform.scale(fachada, (480, 270))
        pygame.image.save(fachada, str(destino / "fachada_escola.png"))
    finally:
        pygame.quit()


if __name__ == "__main__":
    principal()
