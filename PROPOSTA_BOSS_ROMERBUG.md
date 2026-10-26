# Proposta de ataques — RomerBug / SpeedBug

**Data:** 25/10/2026

**Status:** sugestão de design. Os ataques de aviões e medalhas continuam no código;
esta proposta ainda não foi aplicada. A transição com a entidade já foi implementada.

A nova mecânica deve reforçar uma escola dominada pela IFVania: Romerito usa os
terminais e a instalação elétrica como armas. A pressão vem da antecipação dos
ataques e da ocupação da arena, com pausas claras para contra-atacar.

## Primeira forma — Sobrecarga dos terminais

Substituir os aviões por zonas de descarga no piso. O professor aponta para um
terminal; a tela acende, um aviso no chão marca uma faixa e só depois ocorre a
descarga. O alvo usa a posição do protagonista no início do aviso, sem perseguição
instantânea. O jogador pode sair da faixa ou saltar sobre o pulso baixo.

Parâmetros iniciais para prototipagem: faixa de 96 pixels, aviso de 0,8 segundo,
descarga de 0,25 segundo, dano de 1 ponto e recuperação do boss de 0,9 segundo.
Limitar a uma zona por vez, sem bloquear toda a arena e sem atingir o jogador
durante diálogos ou transições. Sinalizar por forma e luminosidade, além da cor.

## Transição a 50% — implementada

RomerBug interrompe o combate e cai de joelhos, com um pé apoiado. A câmera
aproxima, uma entidade surge e diz “Ainda não terminou.” A fala aguarda o comando
do jogador. A entidade conduz a metamorfose, SpeedBug se ergue e a câmera retorna.
A vida restante, a posição e o corpo são preservados. O combate e os projéteis
ficam suspensos; Esc pausa também a fala. A retomada oferece uma breve proteção.

A entidade permanece misteriosa: esta alteração não define sua origem ou resolve
a história da IFVania.

## Segunda forma — Investidas de ruptura

Substituir as medalhas por duas investidas em sequência. SpeedBug baixa a postura,
uma linha indica a direção e ele avança para o ponto previamente marcado, sem
corrigir a trajetória durante o avanço. Após o segundo avanço, há exaustão visível
para permitir dois ou três golpes de chicote conforme o balanceamento.

Parâmetros iniciais: preparação de 0,6 segundo na primeira investida e 0,45 na
segunda, deslocamento limitado à arena e recuperação de 1,1 segundo. Manter um
intervalo entre as investidas e impedir dano repetido do mesmo avanço. O salto
básico ou deslocamento lateral deve bastar para evitar o ataque; não exigir dash,
pulo duplo ou outro poder indisponível na campanha.

## Aceite sugerido para a implementação futura

- Nenhum ataque causa dano antes do aviso visual terminar.
- O alvo e a direção ficam definidos antes da execução; não há correção impossível de evitar.
- Sempre existe uma rota segura alcançável pelo movimento ou salto básicos.
- As pausas de recuperação são reconhecíveis e permitem contra-ataque.
- As duas formas continuam na classe `RomerBug`, com uma única reserva de vida.
- Pausa, derrota e transições removem ou suspendem todas as zonas ofensivas.
- Validar os parâmetros manualmente com Menino e Menina, sem invulnerabilidade de teste.
