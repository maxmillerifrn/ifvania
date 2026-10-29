# Ataques do primeiro chefe — RomerBug / SpeedBug

**Revisão:** 28/10/2026 — implementada. A homologação humana de dificuldade
permanece pendente. Esta especificação substitui a proposta inicial de dupla investida.

## RomerBug: sobrecarga de terminal

Patrulha curta, seguida de faixa de 96 pixels marcada no piso por 48 quadros
(0,8 s). A faixa é fixada na posição do aluno ao começar o aviso. A descarga
é baixa, dura 15 quadros (0,25 s) e causa 1 de dano. É possível sair da faixa
ou saltar. Depois, o professor fica exposto por 60 quadros (1 s), sem dano
de contato. Há uma única zona e ela não acompanha o aluno depois de marcada.

## Transição a 50%

Preserva a cena de joelho apoiado, entidade, fala “Ainda não terminou.”,
metamorfose e levantamento. Vida, corpo e posição são preservados. Ataques,
cargas, projéteis e zona de descarga são removidos. Pausa e fala funcionam
como antes; a retomada oferece proteção e aproximação antes do próximo aviso.

## SpeedBug: investida de ruptura

Aproximação a até 2,6 pixels por quadro, seguida de preparação de 36 quadros
(0,6 s), com direção fixada e seta no chão. A investida percorre até 160 pixels
a 6 pixels por quadro, respeitando paredes e os limites da arena. Não corrige
a direção, não dispara medalhas e não salta para perseguir o aluno. O salto
básico permite evitá-la, sem exigir esquiva.

Depois há 78 quadros (1,3 s) de recuperação, com a indicação “EXPOSTO” e sem
dano de contato. Essa abertura permite aproximar e escolher golpe rápido ou
carregado. Não há dupla investida nesta revisão.

## Arma e defesa

O mouse com cabo reforçado mantém o vínculo com a bolsa e o ambiente escolar.
Toque/soltura de X causa 1 de dano; carga de 36 quadros e soltura causa 2.
A carga reduz deslocamento a 75% e pode ser cancelada por dano ou esquiva.
O golpe tem arco tolerante, respeita paredes e acerta uma vez por alvo.

Shift permite passo evasivo de 15 quadros, protegido nos oito quadros centrais,
com recarga de 54 quadros. A esquiva é uma defesa básica disponível com o mouse,
sem conceder habilidades ou recompensas da campanha antiga.

## Validação

Testes cobrem aviso sem dano, alvo e direção fixos, limite da investida, parede,
recuperação, transição, carga e cancelamento. Cenários sem invulnerabilidade
artificial verificam saída da descarga e salto sobre a investida. A avaliação
de ritmo e dificuldade com jogadores permanece pendente, conforme
[ANALISE_JOGABILIDADE_COMBATE.md](ANALISE_JOGABILIDADE_COMBATE.md).
