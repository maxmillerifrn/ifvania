# Arquitetura da evolução hack and slash

**Atualização:** 16/11/2026. Primeira expansão funcional integrada. [Plano](PLANO_HACK_AND_SLASH.md) · [evidências e limitações](../avaliacao/hack_and_slash/RELATORIO.md).

## Matriz de padrões obrigatórios

| Padrão | Módulos e símbolos | Uso real e evidência |
|---|---|---|
| Factory | `FabricaCenas`, `criar_inimigo`, `criar_chefe` | `Jogo` cria escola, fases e campus pelo registro; `Fase` constrói inimigos/chefes por tipo validado. Testes rejeitam tipos desconhecidos, ambientes inválidos e registros duplicados |
| State Machine | `MaquinaEstados`, `TRANSICOES_ESTADOS`, `Jogador.estados_combate`, `BugCombate.estados`, `GuardiaoCampus.estados` | Transições globais e de ação explícitas; preparação/ataque/recuperação não se confundem. Testes exercitam transições válidas, rejeitam estados/transições inválidos e verificam pausa e mudança final sem dano |
| Command | `Comando`, `interpretar`, `houve_interacao` | Intenções de ataque, soltura, salto, esquiva e interação; origem da carga e repetição são controladas. O contexto escolhe interação ou ancoragem, com terminal prioritário. Movimento contínuo permanece como eixo amostrado por quadro |
| Strategy | `EstrategiaCorpoACorpo`, `EstrategiaLancador`, `choose_attack` de cada guardião | Bugs recebem estratégia substituível; seleção de ação é separada de execução/temporização. Chefes preservam classes concretas e repertórios específicos; teste substitui estratégia sem reconstruir inimigo |
| Observer | `EventosCampanha`, `ChefeDerrotado`, `FaseConcluida`, `ObjetivoConcluido`, `ProgressoCampanha` | Entrega local síncrona ordenada; progresso atualizado antes de navegar, conclusão idempotente, inscrições removidas na troca de campanha. Sem dependência de desenho ou barramento global |

## Estado de campanha e navegação

`Jogo` possui eventos, progresso e fábrica por sessão. Cenas recebem dependências explicitamente; não procuram a campanha em variáveis globais. Fases têm identificadores estáveis `a28`, `biblioteca`, `recreio`, `copias`, `rede` e `continuidade`. Mapas antigos preservam seus contratos e identificadores de compatibilidade por índice.

Derrota emite `ChefeDerrotado`; consulta nova emite `ObjetivoConcluido`; saída emite `FaseConcluida` antes de carregar campus. Conjuntos são idempotentes e expostos por cópias imutáveis. Repetição de saída é protegida por instância, sem impedir reconstrução de fase. Nova história encerra inscrições anteriores e cria progresso vazio. Não há persistência em disco.

`CampusVirtual` usa `SETORES` e `RETORNOS`, sem depender de `indice_fase + 1`. Portas têm proximidade/requisitos; bordas exigem E novo. Surgimentos ficam fora de gatilhos imediatos. Retorno/troca de setor conserva integridade; A28 é ponto explícito de recuperação. Entrada em fase/retomada mantém a recuperação anterior até a capacidade atual. R recompõe o encontro conservando objetivos; biblioteca conserva sua retomada especializada.

No momento, entrada concluída não reativa chefe nem inicia replay. Setores são adaptações ficcionais, não uma planta interna homologada do IFRN.

## Estados e comandos

Aplicação: menu → seleção → nome → diálogo/prólogo → jogabilidade. Jogabilidade permite diálogo, pausa, derrota, cartão, transformação e saídas. Pausa retorna ao estado suspenso. Diálogo pode iniciar abdução/infecção ou retornar ao jogo; final exige as seis fases e leva a vitória. Transformações conservam corpo/vida e suspendem dano.

Combate do jogador: pronto, carga, golpe, esquiva, recuo e ancoragem. Temporizadores medem duração em atualizações do jogo; pausa não usa relógio de parede. Transições de ação pertencem ao jogador, decisões de alvo ao contexto da fase. Atacar na soltura mantém a origem do comando inicial. Sequência, memória e carga são descartadas nas interrupções previstas. Movimento/animação continuam separados do corpo lógico.

Estados dos novos inimigos/chefes: esperar/patrulhar, preparar, atacar e recuperar. Preparação não causa contato passivo; ataque expõe área de dano; recuperação oferece resposta. Guarda consulta direção/força e proteção do retransmissor; não muda a invulnerabilidade do jogador. Francisco acrescenta uma janela de transição protegida na mesma reserva de vida.

Testes que preparam uma cena isolada configuram diretamente o estado inicial da máquina. Isso não amplia as transições permitidas em produção; testes de navegação/entrada exercitam os comandos reais e há regressão específica de transição proibida.

## Representação e recursos

Corpo lógico continua 40 × 40. Apresentações de 80 px vêm das fontes originais e usam registro separado de quadros; espelhamento conserva a associação visual. Bugs ficam em 100%. Dano usa clarão/barra temporária no alvo e impactos independentes na fase, incluindo golpe fatal. Desenho não avança seus temporizadores.

Fontes geradas e prompts ficam em `recursos/fontes_arte/`; exportadores de apresentação, turma e guardiões escrevem destinos separados. Pygame basta; nenhuma dependência nova para jogar. O verificador executa 15 exportadores em cópia temporária.

## Defesa, ciclo final e continuidade

`DefesaMouse` é composição do jogador: resistência, janela de impacto e quebra são independentes do desenho e da vida. Command traduz Q; estado de bloqueio arbitra carga/esquiva. Resultado `bloqueado` consome projétil e interrompe investida. Origem do impacto decide frente/costas; perigo ambiental é não bloqueável.

`BugArquivo`, `BugRepetidor` e projéteis especializados preservam Factory/Strategy. `DescobertaMouse` e `EncerramentoEquipamentos` são encenações isoladas. Estado global de desligamento suspende combate e permite pausa, seguido pelo epílogo e fachada final. Ambiências usam canal reservado; M controla áudio.

Retomadas usam objetivos persistentes e apoio seguro; revisitas não reativam encontro nem curam. Novas poses exportam representação separada da colisão. H0–H9 estão tecnicamente integrados; homologação humana permanece adiada, com decisões e roteiro em [REVISAO_HUMANA_FINAL.md](REVISAO_HUMANA_FINAL.md).
