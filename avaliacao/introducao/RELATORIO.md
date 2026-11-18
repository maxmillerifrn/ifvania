# Abertura cinematográfica do IFVania

A sequência dura 53 segundos a 60 quadros por segundo. O editor apresenta a lista de chamada solicitada por Max. O protagonista vai dormir enquanto a IA trabalha. Durante a oscilação da madrugada, a recuperação reescreve as linhas do programa à medida que aparecem regras, avatares e inimigos. Ao acordar, o protagonista encontra o código pronto e a entrega já sincronizada pelo portal, que conecta essa versão aos registros encontrados mais tarde no campus. O quarto se fragmenta em faixas que revelam o A28. O personagem encontra o mouse após chegar e pode começar imediatamente a se mover ao terminar o diálogo.

As capturas abaixo registram a revisão visual com fachada e quarto a 960 × 540, fundos gerados com o laboratório do jogo como referência e poses ajustadas aos pontos de apoio da mobília. [Imagens-fonte e prompts](../../recursos/fontes_arte/introducao/REFERENCIAS.md).

## Capturas

| Momento | Evidência |
|---|---|
| Caminhada até a porta | [Chegada](01-chegada.png) |
| Passagem pela soleira | [Soleira](01b-soleira.png) |
| Fim da tarde e mochila junto à mesa | [Quarto](02-quarto.png) |
| Falha no teste da lista de chamada | [Atividade](03-atividade.png) |
| Oscilação e console reescrito enquanto o personagem dorme | [Anomalia](04-anomalia.png) |
| Personagem acorda e encontra a entrega pronta | [Código concluído](05-codigo-pronto.png) |
| Luz, partículas e atração do personagem | [Sucção](06-succao.png) |
| Substituição do quarto pelo A28 em faixas | [Transição](07-transicao-a28.png) |
| Primeira fala no mundo virtual | [Despertar](08-despertar-a28.png) |
| Salto após recuperar o controle | [Em jogo](09-em-jogo.png) |

## Verificações

- Execução de `principal.py` com o relógio normal do jogo e entradas automatizadas pelo menu até o primeiro salto no A28. A sessão inteira, incluindo menu e diálogo, levou 71,9 segundos neste ambiente. As capturas desta revisão percorreram o mesmo fluxo sem o limitador de quadros.
- Inspeção das capturas e ajustes de enquadramento do editor, movimento ao despertar e transição de cenário.
- Suíte completa com 202 testes. Regressões específicas para preservação de nome e protagonista, pausa, atalho **F**, posição de surgimento, deslocamento, salto e retomada de checkpoint.
- A execução usou vídeo e áudio SDL simulados. A avaliação subjetiva de ritmo e mixagem em sessão presencial permanece aberta.
