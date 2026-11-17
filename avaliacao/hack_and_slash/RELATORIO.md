# Fechamento técnico da expansão — 16/11/2026

## Resultado e alcance

Implementadas as correções de feedback e a primeira versão jogável da progressão completa. A campanha agora retorna ao campus após cada fase, inclusive RomerBug. Portas por E levam à biblioteca, ginásio, M1, M5 e LIT; setores conectam convivência, jardim, informática e área técnica. A volta final ao ponto A28 do jardim permite confirmar o encerramento.

Este relatório registra execução automatizada e inspeção de capturas. Não registra partida humana nem aprovação de diversão. O usuário autorizou adiar novos retornos de avaliação manual e priorizar implementação; isso não equivale a considerar o acabamento homologado.

## Correções do relato humano

- Bugs exibem clarão, recuo e barra por 100 atualizações após dano. Acertos renovam a duração; bloqueio não revela barra. Impactos de 12/18 atualizações continuam visíveis mesmo no golpe fatal, sem colisão de inimigo morto.
- Pausa/diálogos suspendem efeitos, vida e temporizadores. Desenhar não avança a barra nem o impacto.
- RomerBug reposiciona também entre lançamentos. Ao recuperar, alterna resposta por distância/ciclo, podendo antecipar uma investida contra aproximação contínua. Preparação e lançamento têm inclinação corporal visual; mira e direção anunciadas continuam fixas.
- A metamorfose usa 42 atualizações, levantar usa 30 e liberação usa 18; levantar mistura poses e liberação mantém oscilação discreta. A espera inicial de SpeedBug cai de 60 para 18 atualizações. Corpo, vida compartilhada e pausa preservados.
- Alunos do laboratório usam duas ilustrações próprias vistas de costas, em vez das figuras geométricas anteriores. Monitores, bancadas e colisões preservados.
- Apresentação de protagonistas/professores usa PNGs de 80 px exportados diretamente das fontes, preservando detalhes perdidos na redução para 40. Caminhada usa passo visual mais curto e mistura entre quadros na segunda metade da passagem. Colisão continua 40 × 40 e animação para sem deslocamento real.

## Expansão funcional

- Combo de três golpes na soltura: primeiro rápido, segundo de maior alcance, terceiro de maior alcance/empurrão. Carregado continua 2 de dano; ascendente aplica lançamento curto; descendente acelera queda, sem devolver salto.
- Bugs corpo a corpo e lançadores possuem preparação, ataque e recuperação, substituindo contato passivo na campanha principal. Guardas bloqueiam golpes rápidos frontais; carregado/flanco funcionam. Retransmissores mantêm a defesa de guardas próximos.
- Quatro classes concretas de guardiões, com repertórios próprios sobre primitivas compartilhadas e estados explícitos. Novas artes de Elias, Alessandro e Francisco representam avatares ficcionais, não retratos pessoais; Max preserva sua identidade anterior.
- Cada fase nova tem geometria própria, três terminais elevados e portão condicionado aos objetivos. Registros persistem na retomada, com contexto narrativo específico. Rede apaga indicadores nos armários à medida que os ramais são isolados.
- Ancoragem é liberada após Max, sem cura ou aumento de vida. E escolhe conector elegível na direção do olhar, com limite de distância e bloqueio por parede. Terminal próximo tem prioridade, inclusive já consultado. Há treino em piso seguro e conectores no campus e nas fases avançadas.
- Francisco perde o vínculo na metade da mesma reserva. A transição dura 45 atualizações, sem causar/receber dano; a entidade continua sobre a vida restante, com Francisco visível como aliado.
- Final exige as seis fases concluídas; apresenta confirmações e epílogo dialogado no A28. Nova campanha limpa objetivos, fases e inscrições anteriores.

## Evidências

Comando: `SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy PYGAME_HIDE_SUPPORT_PROMPT=1 .venv/bin/python -m unittest discover -s testes -v`.

**172 testes aprovados**, Python 3.14.4 / pygame-ce 2.5.8 (aproximadamente 12 s). Incluem regras de barra/recuo, congelamento na pausa, comandos e estados inválidos, fábricas, estratégias substituíveis, guarda, prioridade de interação, progresso/retomada, ancoragem, mudança final e condições do desfecho. Percursos dos novos objetivos foram exercitados com física real e ambas as aparências; isso isola geometria e não comprova sobrevivência contra todos os inimigos.

**15 exportadores aprovados em cópia temporária, 203 PNGs distintos.** Novos exportadores de turma, apresentação e guardiões também foram executados em `/tmp` antes da integração. Artes anteriores não foram substituídas.

Capturas por `python -m ferramentas.experimentar_campus --capturas avaliacao/hack_and_slash`: [laboratório](laboratorio.png), [campus](campus.png), [quadra](arena_3.png), [Max](arena_4.png), [rede](arena_5.png), [núcleo](arena_6.png). Há também capturas da entrada das seis fases. Cenários foram preparados por ferramenta; não são screenshots de partida humana completa. Inspecionados turma, escala, personagens, guardiões e legibilidade dos setores. A primeira composição da quadra foi reduzida a marcações baixas para não sugerir paredes/plataformas falsas.

## Refinamentos concluídos e limites da evidência

Bloqueio frontal Q com resistência/quebra, interrupção de investidas e cancelamento seguro integrado. SpeedBug resolve limites antes da colisão, retorna de extremidades e anima deslocamento real, com reposicionamentos entre ciclos. Novas regressões cobrem parede, retorno, movimento e defesa.

Guardiões receberam quatro poses próprias por avatar e retratos separados; Max troca a origem real e invoca bugs limitados. Elias usa bola com um ricochete; Alessandro portas sequenciais; Francisco sintetiza pulsos/grupos sobre a reserva compartilhada. Há perigos temporizados, resgate animado, notas opcionais e apoios seguros. Biblioteca tem bugs de fichas, atalhos de consulta e bilhete persistente.

A bolsa tem descoberta animada. Final apresenta desligamento progressivo dos monitores/nobreak, pendrive isolado, aula física e fachada iluminada. Ambiência sintetizada e efeitos próprios acompanham capítulos; M alterna áudio. Ver [bloqueio](bloqueio.png), [descoberta](descoberta_mouse.png), [desligamento](desligamento.png), [epílogo](epilogo.png), [fachada](fachada_final.png) e campus [antes](campus_antes.png)/[depois](campus_depois.png).

São 19 capturas de cenários controlados, não uma partida humana. Testes verificam regras e trajetos isolados; não comprovam tempo total, sobrevivência, diversão, mix ou fidelidade arquitetônica. As decisões adotadas e todos os critérios humanos adiados estão em [REVISAO_HUMANA_FINAL.md](../../documentacao/REVISAO_HUMANA_FINAL.md). Não há pedido de aprovação técnica pendente.

## Experimentação

Jogo completo: `.venv/bin/python principal.py`.

Ferramenta de desenvolvimento, fora do menu: `.venv/bin/python -m ferramentas.experimentar_campus --campus` ou `--fase 3` até `--fase 6`. Ela prepara progresso anterior e habilidades apenas para experimentar diretamente; não representa uma partida iniciada pelo menu.
