# IFVania — Plano de implementação do hack and slash

## Revisão vigente — nitidez, golpes e Mente Brilhante (18/11/2026)

O estado anterior foi registrado no commit `fe13741`, antes destas melhorias. O bug agora conserva a apresentação HD ao se virar para a esquerda, corrigindo a ampliação indevida do quadro lógico de 40 px. RomerBug usa novo atlas sombrio mantendo terno, gravata e sapatos; SpeedBug mantém regata laranja, shorts, medalha e tênis de corrida. Ambos têm poses próprias de soco e chute e lançam um pulso de energia como especial.

Por solicitação do responsável, foram retirados os marcadores gráficos de preparação/recuperação e desenhos de áreas dos ataques de bugs e chefes. As etapas de preparação continuam existindo; poses corporais, sons, ataques efetivamente executados, projéteis e feedback de dano permanecem. Indicações de objetivos e perigos ambientais são sistemas distintos e continuam disponíveis.

Na fase 2, **Mente Brilhante** substitui o Indexador. É um avatar ficcional inspirado no professor Ricardo Rodrigues, identificado como diretor do IFRN Campus Caicó na [matéria da Agência Sebrae de 25/02/2025](https://rn.agenciasebrae.com.br/cultura-empreendedora/exposicao-e-desfile-como-experiencias-imersivas-marcaram-a-4a-mostra-serido-de-moda-cultura-e-design/). O personagem usa camisa rosa, jeans e crachá, luta com socos, chutes e barrigada e dispara raios pela cabeça. Os poderes e o aprisionamento pela IFVania são invenções do jogo. Módulo de salto duplo, consultas, mapa, checkpoints e saída da biblioteca foram preservados.

Evidências e decisões em [RELATORIO.md](../avaliacao/mente_brilhante/RELATORIO.md). Experimentação direta: `.venv/bin/python -m ferramentas.experimentar_mente_brilhante` (atalho de desenvolvimento, sem alterar o save real).


## Atualização vigente — parasita humanoide, cenas e save (17/11/2026)

Bloqueio com Q permite caminhada animada na velocidade normal, salto e troca de direção, mantendo resistência e proteção frontal. Os bugs agora têm corpo humanoide, com poses próprias de repouso, corrida e dano. O golpe que eliminaria o último bug do A28 inicia uma cena: ele corre até Romerito e se funde ao professor. Entrar na arena sozinho não dispara mais a transformação. A metamorfose aos 50% permanece protegida e agora revela SpeedBug com armadura escura e corrupção violeta. Após a vitória, o parasita sai do corpo e se desintegra antes do diálogo de libertação.

Salvamento automático em `dados/salvamento.json`, ignorado pelo Git: um slot, com versão e gravação atômica. Checkpoints nas entradas, durante travessias seguras, antes do confronto e após vitória. F5 grava o checkpoint atual; R após morrer retoma nele com integridade completa. O menu oferece **Continuar** quando há arquivo válido. Nome, aparência, habilidades, objetivos, vitórias e inimigos já eliminados antes do checkpoint são preservados. Chefes não vencidos reiniciam com vida completa; não se salva no meio de um golpe/cena. O prólogo não possui checkpoint; o primeiro fica no mundo virtual. Novo jogo substitui o slot quando atinge esse ponto. Ferramentas de experimentação não sobrescrevem o save do jogador.

O novo contrato substitui as descrições anteriores de progresso somente em memória e movimento reduzido na guarda. Evidências, arquitetura do save e revisão pendente no [relatório](../avaliacao/parasita_e_save/RELATORIO.md).


## Correção vigente — alinhamento, corredor e brisa (17/11/2026)

O bug humanoide agora usa a mesma escala visual de 80 px do protagonista, mantendo a colisão de 40 × 40. Na fuga para Romerito, posição, câmera e desenho usam os pés; o trajeto acompanha o piso. A fusão encolhe o bug até o tórax visual, com espelhamento quando ele corre para a esquerda. A expulsão foi ajustada à mesma referência.

Após a fase 1, o jogador sai do A28 no início do corredor de convivência (x=180) e precisa caminhar até a porta de madeira da biblioteca (x=1200), usando E para entrar na fase 2. O cenário recebeu panorama próprio, placas e janela para o jardim. A volta da biblioteca fica em x=1330, fora do gatilho; o ginásio está mais adiante, em x=1800. A travessia ao jardim continua acessível após o recreio.

Folhas e plantas do pátio, jardim, recreio e janelas do corredor recebem brisa com ritmos distintos. A animação é apenas visual, usa o relógio pausável da cena e mantém arquitetura, bancos e colisões. Fontes anteriores foram preservadas. Evidências em [RELATORIO.md](../avaliacao/corredor_e_vento/RELATORIO.md).


## Atualização vigente — parasita humanoide, cenas e save (17/11/2026)

Bloqueio com Q permite caminhada animada na velocidade normal, salto e troca de direção, mantendo resistência e proteção frontal. Os bugs agora têm corpo humanoide, com poses próprias de repouso, corrida e dano. O golpe que eliminaria o último bug do A28 inicia uma cena: ele corre até Romerito e se funde ao professor. Entrar na arena sozinho não dispara mais a transformação. A metamorfose aos 50% permanece protegida e agora revela SpeedBug com armadura escura e corrupção violeta. Após a vitória, o parasita sai do corpo e se desintegra antes do diálogo de libertação.

Salvamento automático em `dados/salvamento.json`, ignorado pelo Git: um slot, com versão e gravação atômica. Checkpoints nas entradas, durante travessias seguras, antes do confronto e após vitória. F5 grava o checkpoint atual; R após morrer retoma nele com integridade completa. O menu oferece **Continuar** quando há arquivo válido. Nome, aparência, habilidades, objetivos, vitórias e inimigos já eliminados antes do checkpoint são preservados. Chefes não vencidos reiniciam com vida completa; não se salva no meio de um golpe/cena. O prólogo não possui checkpoint; o primeiro fica no mundo virtual. Novo jogo substitui o slot quando atinge esse ponto. Ferramentas de experimentação não sobrescrevem o save do jogador.

O novo contrato substitui as descrições anteriores de progresso somente em memória e movimento reduzido na guarda. Evidências, arquitetura do save e revisão pendente no [relatório](../avaliacao/parasita_e_save/RELATORIO.md).


## Revisão vigente — duelo corporal (17/11/2026)

A nova avaliação humana reprovou a fluidez da luta com RomerBug. O encontro foi redesenhado: aproximação livre, cruzado, varrida baixa e avanço curto substituem o roteiro automático de aviões/medalhas. RomerBug encadeia dois golpes; SpeedBug encadeia três, aproxima mais rápido e mantém a mesma reserva de vida. Cada golpe tem preparação sem dano, direção fixa durante execução e recuperação. Q bloqueia e cancela a sequência inteira, abrindo 44 atualizações de contra-ataque. A varrida tem aviso baixo e pode ser saltada.

Os primeiros dois acertos fora da execução/recuperação provocam recuo breve; depois o chefe firma a postura até completar sua resposta, continuando a receber dano. Isso limita aprisionamento por interrupções. O próximo toque do combo pode ser antecipado nas últimas oito atualizações do recolhimento; carga e ataque na soltura continuam preservados. Foram retirados o limite artificial de deslocamento e o balanço contínuo do corpo.

Experimentação direta: `.venv/bin/python -m ferramentas.experimentar_campus --duelo`. É um atalho de desenvolvimento sem habilidades futuras; não altera o menu nem a campanha. Fontes de inspiração, parâmetros e evidências em [RELATORIO.md](../avaliacao/duelo_romerbug/RELATORIO.md). A avaliação humana da nova dinâmica continua aberta; os registros de 16/11 abaixo descrevem a versão anterior quando divergirem deste trecho.


**Data:** 16/11/2026. **Estado:** implementação técnica H0–H9 integrada; homologação humana final adiada. Pendências humanas em [REVISAO_HUMANA_FINAL.md](REVISAO_HUMANA_FINAL.md).

Design: [PROPOSTA_HACK_AND_SLASH.md](PROPOSTA_HACK_AND_SLASH.md). Registro geral: [PLANO_DE_EXECUCAO.md](PLANO_DE_EXECUCAO.md).

## Prioridade vigente e entrega implementada

O usuário autorizou implementar as correções e continuar o plano sem aguardar novos retornos manuais; considerações de ajuste ficam para a avaliação final. Critérios humanos continuam registrados, mas estão adiados e não bloqueiam os incrementos. Não marcar uma experiência humana como realizada por causa dessa dispensa.

Implementados: barras temporárias/clarão/recuo/impacto fatal, revisão da fluidez de RomerBug/SpeedBug, nova arte da turma, apresentação HD e caminhada interpolada, campus após cada fase, portas/retornos/requisitos, progresso de objetivos em memória, combo/direcionais, quatro tipos de bug, ancoragem, quatro guardiões concretos e desfecho dialogado. Os cinco padrões obrigatórios estão em uso. Ver [matriz de arquitetura](ARQUITETURA_HACK_AND_SLASH.md) e [relatório com evidências e limites](../avaliacao/hack_and_slash/RELATORIO.md).

Estado por marco:

| Marco | Estado real |
|---|---|
| H0 | Base técnica e relato humano registrados; nova avaliação adiada |
| H1 | Campus, progresso, portas/retornos, Factory, State Machine e eventos integrados |
| H2 | Combate terrestre/direcional, Command, Strategy, tipos de inimigos e reações integrados |
| H3 | Ciclo biblioteca → campus → Elias → campus → M1 funcional e coberto por testes; duração alvo/diversão não homologadas |
| H4 | Três travas, resgate animado, bola com ricochete e poses integrados |
| H5 | Max troca origem real entre cópias e invoca bugs; registros, atalhos, guarda, aéreo e ancoragem integrados |
| H6 | Ramais, perigos temporizados, conectores, guardas/retransmissores e portas sequenciais integrados |
| H7 | Francisco/IFVania na mesma vida, retorno A28, desligamento, sala e fachada integrados |
| H8 | Duas fases originais conectadas, bolsa animada, atalhos/bilhete da biblioteca, turma e poses integrados |
| H9 | Suíte e exportadores verificados; homologação humana final adiada, sem bloquear implementação |

As listas abaixo distinguem entrega técnica concluída e avaliação humana adiada. A marca técnica não representa homologação de diversão.

## 1. Objetivo e organização

Entregar uma campanha de seis fases conectada por um campus virtual controlável, com combate de combos, inimigos reativos e quatro novos chefes docentes. Prioridade: validar cedo o ciclo campus → entrada → fase → chefe → campus transformado → próxima entrada.

Este plano orienta o novo trabalho de evolução. As etapas antigas e seus registros continuam documentando o que existe; não devem ser marcadas retroativamente como concluídas por equivalência. Abertura e biblioteca foram integradas; homologação humana permanece aberta. O novo plano altera o conteúdo futuro das antigas etapas 7–10 e amplia a infraestrutura prevista na etapa 5; a validação final continua sendo a última entrega.

Não há estimativa de calendário sem medir o primeiro protótipo. Executar em incrementos jogáveis, registrar evidências e só ampliar arte/conteúdo após verificar a base.

### Avaliação manual fornecida pelo usuário — 16/11/2026

O responsável experimentou o jogo e relatou: controles razoáveis; câmera e cenários decentes, com exceção da qualidade dos alunos do laboratório; áudio razoável; diálogos e travessias bons; continuidade funcionando. Combate reprovado: previsível, fácil e sem graça. Faltam feedback visual de dano e barras temporárias nos bugs. Ataques de RomerBug precisam de fluidez; há um trecho aparentemente travado na passagem para SpeedBug. Personagens precisam de apresentação menos pixelada e caminhada mais fluida.

Esse relato conta como avaliação humana da base, sem atribuir ao agente uma partida que não realizou. Não foi informado se ambos os protagonistas foram experimentados. Conforto geral razoável não homologa balanceamento, arte ou todos os casos de pausa/foco.

**Prioridade revista:** antes de ampliar conteúdo, executar o ciclo de correção abaixo, antecipando feedback/reação de H2 e refinamento de H4. H1 pode continuar na infraestrutura, mas não deve consumir o próximo ciclo visual com expansão de cenários enquanto o combate segue reprovado. Os demais marcos e padrões obrigatórios permanecem.

1. **Resposta de dano:** clarão/silhueta breve e reação legível no bug; barra de vida surge após dano efetivamente recebido e some depois de intervalo sem novos acertos. Novo acerto renova visibilidade; inimigos intactos não exibem barra. Incluir impacto perceptível no golpe fatal, sem manter colisão de inimigo morto. Temporizadores congelam na pausa/diálogo; desenho não avança estado.
2. **Fluidez do encontro:** reproduzir o instante relatado e distinguir preparação intencional, pose estática na cena e atraso após retomada. Revisar poses, transições e recuperação sem eliminar pausas úteis ou alterar corpos lógicos. A cena contém poses mantidas e `finish_cinematic()` reinicia uma aproximação de 60 atualizações; são pontos de investigação, não diagnóstico confirmado do travamento.
3. **Diversão e desafio:** experimentar variantes de sequência e decisões por distância/posição, com sinais consistentes e limites contra repetição. Criar escolhas de alvo, pressão e contra-ataque; não tentar resolver apenas aumentando vida, dano ou velocidade, nem tornando os ataques aleatórios e ilegíveis. Integrar State Machine/Strategy na evolução dos padrões, preservando vida compartilhada das formas.
4. **Personagens e turma:** revisar fontes, resolução, recorte, escala e poses dos alunos; melhorar arte dos personagens e transições da caminhada mantendo identidade e pés. Não substituir essa revisão por simples desfoque da arte atual. Preservar fontes aprovadas e experimentar variações separadas; validar duas aparências e alunos sentados.
5. **Nova avaliação:** comparar o encontro anterior e revisado, incluindo bugs, RomerBug e SpeedBug. Registrar compreensão do dano, necessidade de defesa, decisões ofensivas e variedade percebida. Passar nos testes não encerra essa pendência: a luta precisa ser reavaliada por quem joga.

**Aceite deste ciclo:** jogador reconhece acertos e vida restante sem barras permanentes; golpe fatal comunica resultado; transformação não parece defeito ou congelamento; a luta exige decisões e mantém oportunidades justas. Colisões, pausa, entradas e continuidade preservadas. Câmera, diálogos e áudio recebem apenas ajustes necessários à revisão, sem reconstrução geral.

## 2. Contratos a preservar

- Corpo lógico comum de 40 × 40, arte ancorada pelos pés e escalas existentes.
- Nome/aparência/habilidades preservados nas transições; textos compartilhados não são mutados.
- Ataque na soltura de X/K/botão esquerdo, vinculado ao comando que iniciou a carga.
- Pausa e diálogos suspendem física/combate; monitores podem animar em diálogo, mas congelam na pausa.
- Pausa, perda de foco, dano e transições descartam cargas e comandos pendentes conforme as regras existentes.
- Um evento não confirma duas telas nem dispara ataque ao terminar diálogo.
- Golpes respeitam paredes, um acerto por alvo por golpe e janelas de invulnerabilidade.
- RomerBug/SpeedBug continuam duas formas com vida compartilhada; fase 1 não concede poder automático.
- Salto duplo continua na biblioteca; ancoragem entra depois da fase 4, com treino seguro.
- Chefes possuem classes concretas; não trocar apenas nome e imagem de um comportamento genérico.
- Arte aprovada e campanha antiga preservadas; exportadores verificados em pasta temporária.

## 3. Decisões técnicas iniciais

### Padrões de projeto obrigatórios

O uso de padrões de projeto é requisito de implementação e critério de aceite. Factory e State Machine são obrigatórios, assim como Command, Strategy e Observer nos pontos definidos abaixo. Aplicar cada padrão para resolver sua responsabilidade concreta, com identificadores em português e interfaces pequenas. Não basta nomear uma classe como fábrica ou estado; seu comportamento deve cumprir o contrato e ser exercitado pelo jogo.

| Padrão | Aplicação obrigatória | Responsabilidade e limite | Introdução |
|---|---|---|---|
| Factory, por registro de construtores | Criação de cenas/setores, inimigos e chefes a partir dos dados | Centralizar validação de tipo, configuração e construção; preservar classes concretas. Tipo desconhecido gera erro descritivo, sem chefe genérico silencioso. Funções de fábrica são suficientes; Abstract Factory não é exigido | Cenas em H1, inimigos em H2, chefes em H3 |
| State Machine / State | Estados da aplicação e do combate; ciclo dos inimigos/chefes | Declarar estados, transições válidas e ações de entrada/saída. Separar estado global de estados locais; impedir combinações incompatíveis de indicadores booleanos. Usar tabelas/enumerações ou objetos de estado conforme a complexidade, sem exigir uma classe por quadro de animação | Aplicação em H1, combate em H2, chefe em H3 |
| Command | Entrada de jogabilidade de teclado/mouse | Converter eventos em intenções como atacar, soltar carga, esquivar, interagir e ancorar. Preservar origem do comando, prioridade, consumo único e memória com prazo; cancelar pendências em pausa/foco/transição. Não exige desfazer ações nem gravar replay | H2, estendido em H5 |
| Strategy | Seleção de ações dos tipos de inimigo e políticas reutilizáveis de ataque | Separar escolha de ação de sua execução/temporização. Permitir estratégias determinísticas nos testes. Máquina de estados controla quando executar; estratégia escolhe o que executar. Chefes mantêm classe concreta e comportamento próprio, sem uma hierarquia paralela para cada golpe | H2 e H3 |
| Observer / eventos de domínio locais | Comunicação de objetivos e vitórias com progresso, campus e apresentação | Emitir fatos como `ObjetivoConcluido` e `ChefeDerrotado`; um responsável atualiza o progresso antes da navegação, outros consumidores atualizam HUD/áudio. Ordem determinística e inscrição/remoção vinculadas à cena; sem barramento global ou atualização de campanha em callbacks de desenho | H1, exercitado no ciclo completo em H3 |

Aplicar composição e injeção explícita de dependências como diretrizes transversais: `Jogo` fornece progresso, fábricas e serviços necessários às cenas; entidades não buscam a campanha em variáveis globais. Testes podem fornecer serviços substitutos sem inicializar toda a aplicação. Não introduzir contêiner de injeção, Singleton ou arquitetura ECS como pré-requisito.

O Observer não define uma infraestrutura de mensagens distribuída: um despachante local simples, com entrega síncrona em ponto controlado da atualização, atende ao escopo. Conclusão de objetivo é idempotente; evento repetido não duplica recompensa, restaura inimigos nem dispara uma segunda transição. Efeitos de apresentação não devem ser necessários para aplicar uma regra de campanha.

Na State Machine, pausa suspende a atualização dos estados locais e mantém o estado de retorno. Diálogo e cenas de transformação têm contrato explícito de suspensão. Em combate, carga, preparação, atividade, recuperação e esquiva possuem transições documentadas; o combo é um dado do estado de ataque. Movimento e animação não devem multiplicar artificialmente os estados de combate. O relógio do jogo, e não o tempo de parede, controla janelas pausáveis.

**Aceite de arquitetura:** documentar uma matriz padrão → módulo/símbolo → comportamento coberto ao entregar cada marco. Testar criação inválida, transição proibida, descarte de comandos, troca de estratégia e entrega única/remoção de observadores por seus efeitos observáveis. Não exigir testes de nomes de classes ou cópias da implementação. Padrões adicionais só entram com problema concreto, benefício esperado e validação registrados.

### Progresso e navegação

Criar `sistema/progresso_campanha.py` com `ProgressoCampanha`, responsável pelos dados persistentes da sessão: fases concluídas, objetivos locais, professores libertos, setores/atalhos abertos e ponto de retomada. A instância pertence à campanha, não a uma fase que será reconstruída.

Criar `mundo/campus_virtual.py` e `mundo/dados_campus.py`. Dados declaram setor, conexões, requisitos, porta de destino e ponto de surgimento. Começar com dois setores; não construir um mundo inteiro antes do protótipo.

`Jogo` coordena mudança de cena. Fase informa conclusão e destino; campus consulta progresso para escolher portas, personagens e variação visual. Representação não deve modificar o progresso por ser desenhada. Usar identificadores estáveis, por exemplo `recreio`, `trava_recreio_1`, `jardim`, `entrada_m1`.

Não usar `indice_fase + 1` como regra universal de navegação. Preservar as chaves externas dos dados existentes e adaptar consumidores conscientemente; novos identificadores internos usam português. Ao concluir uma fase, registrar conclusão uma vez antes de carregar o campus.

### Retomada, recuperação e travessia

- Progresso em memória no primeiro ciclo; nova campanha limpa tudo. Salvamento em disco não integra o protótipo.
- Derrota reinicia inimigos e chefe do encontro, conserva objetivos permanentes e habilidades, limpa ataques e restaura integridade até a capacidade atual.
- Entrada de fase conserva recuperação já existente. Retorno ao campus e troca comum de setor não curam automaticamente; pontos seguros de recuperação são explícitos.
- Falha em plataforma de ancoragem devolve ao apoio seguro recente, com reposicionamento sem sobreposição e proteção breve; não desfaz objetivos. Ajustar penalidade apenas após experimentação.
- Fase concluída não reativa chefe ao revisitar. Portas de arenas concluídas permitem passagem segura; replay de chefes fica fora deste escopo.
- Entrada por E exige proximidade, tecla nova e condição atendida; surgimento fica afastado do gatilho inverso para evitar ida e volta involuntária.
- Escolha de ancoragem: priorizar interação, depois conector elegível mais próximo na direção indicada; mostrar destino antes de aceitar comando. Não oferecer balanço livre.

### Combate

Separar etapa da sequência, temporização do golpe e reações do alvo. Extrair módulo de combate apenas se reduzir responsabilidades concretas do jogador; evitar refatoração ampla antes de um combo funcional.

Começar com combo terrestre e recuo/interrupção. Acrescentar lançamento, ar e ancoragem nos marcos seguintes. Ajustar invulnerabilidade dos inimigos para permitir acertos consecutivos legítimos sem permitir acerto repetido da mesma instância de golpe. Não alterar a proteção do jogador por consequência dessa mudança.

## 4. Etapas e critérios de aceite

### H0 — Preparar contratos e referência de regressão

**Dependências:** nenhuma. **Entrega:** critérios reproduzíveis e base preservada.

- [x] Executar suíte completa e registrar referência H0 em 16/11/2026: 127 testes aprovados, Python 3.14.4 / pygame-ce 2.5.8, SDL dummy. Experiência manual permanece pendente.
- [ ] Percorrer abertura, RomerBug e biblioteca quando houver ambiente de jogo; registrar separadamente o que não pôde ser experimentado.
- [x] Incorporar avaliação manual relatada pelo usuário em 16/11/2026; combate e arte reprovados, demais aspectos avaliados conforme registro acima. Cobertura das duas aparências e nova homologação após correções pendentes.
- [x] Confirmar pontos de alteração de progressão, morte, entradas, dano e carregamento de habilidades.
- [x] Mapear fábricas, estratégias e estados já existentes; definir evolução incremental para os padrões obrigatórios, reaproveitando estruturas adequadas.
- [x] Registrar levantamento e matriz inicial de arquitetura, estados e responsabilidades em [ARQUITETURA_HACK_AND_SLASH.md](ARQUITETURA_HACK_AND_SLASH.md); tabela formal e estados integrados.
- [x] Registrar casos obrigatórios de regressão e alinhar roteiro/requisitos com a migração futura, identificando o que ainda não existe.

**Aceite:** base técnica conhecida; limitações manuais explícitas; campanha antiga continua isolada. Não bloquear protótipo por falta de arte final ou por pendências visuais independentes.

### H1 — Campus mínimo e progresso de sessão

**Dependências:** H0. **Entrega:** biblioteca → convivência → portão do ginásio; saída de fase com retorno espacial.

- [x] Implementar `ProgressoCampanha`, setores, portas, requisitos e pontos de retorno.
- [x] Primeiro recorte de progresso integrado: chefes derrotados e fases concluídas, eventos locais e nova sessão sem herança. Setores/portas/retomadas integrados.
- [x] Fábrica de cenas escolares e fases utilizada por `Jogo`; validação de tipos/ambientes e registro extensível. Setores integrados.
- [x] Introduzir fábrica de cenas/setores, State Machine explícita da aplicação e eventos locais de objetivo; garantir entrega/remoção de observadores e progresso antes da navegação.
- [x] Fazer saída da biblioteca retornar ao campus, removendo fim provisório apenas quando houver continuação utilizável no incremento.
- [x] Criar dois setores com colisões simples e arte reutilizada, sem acionar gatilhos escolares do prólogo.
- [x] Separar troca de setor, entrada em fase e retomada; conservar identidade e limpar entradas/ameaças.
- [x] Mostrar destino fechado, requisito e indicação espacial de forma compreensível.
- [x] Criar acesso de desenvolvimento ao ponto inicial do protótipo por ferramenta de teste, sem adicionar atalhos de campanha ao menu final.

**Verificação automática:** portas condicionadas, surgimento seguro, ausência de transição dupla, identidade/habilidades, conclusão idempotente e nova campanha limpa.

**Aceite manual:** caminhar da biblioteca ao ginásio, voltar e reconhecer os espaços; nenhuma cura involuntária por alternar setor. Porta da próxima fase só passa a entrar de fato quando H3 entregar conteúdo.

### H2 — Combate terrestre e dois papéis de inimigo

**Dependências:** H0; integrar em H1 antes de H3. **Entrega:** combo de três golpes, esquiva e inimigos que reagem.

- [x] Implementar janela de continuação, memória de ataque e escolha entre toque/carga.
- [x] Implementar Command para intenções de entrada e State Machine de combate, preservando soltura, origem e prioridades dos comandos.
- [x] Criar inimigos pela Factory e separar escolha de ação por Strategy de execução dos estados; validar tipos/configurações desconhecidos.
- [x] Diferenciar rápido, alcance e varredura; terceiro golpe empurra em vez de apenas inflar dano.
- [x] Preservar entrada proprietária da carga, bloqueio por parede e acerto único por golpe/alvo.
- [x] Aplicar recuo/interrupção nos leves, respeitando paredes e bordas.
- [x] Criar leve corpo a corpo e lançador com preparação, janela ativa e recuperação.
- [x] Remover dano de contato passivo desses tipos apenas quando seus ataques estiverem funcionais.
- [x] Definir prioridade de dano, esquiva, carga e recuperação; limpar sequência em pausa/foco/transição.
- [x] Usar animação provisória legível e sons existentes antes de produzir atlas final.
- [x] Antecipar feedback visual de dano, barras temporárias dos inimigos e impacto de derrota, conforme avaliação do usuário; corrigir fluidez do encontro atual antes de aumentar conteúdo.

**Verificação automática:** sequência/expiração, carregado fora do combo, teclas alternativas e simultâneas, acerto por golpe, colisões no recuo, interrupção do inimigo e congelamento de temporizadores.

**Aceite manual:** jogador distingue os três golpes e consegue optar por recuar; repetir ataque não mantém todos os alvos travados. Comparar primeiro par de inimigos com e sem finalizador.

### H3 — Protótipo completo da fase 3

**Dependências:** H1 e H2. **Entrega:** sessão de 10–15 minutos do pós-biblioteca à entrada M1.

- [x] Criar recorte do ginásio com uma trava persistente, trecho de salto duplo e dois tipos de bug.
- [x] Implementar `EliasGuardiaoCompasso` como classe concreta no módulo compartilhado de guardiões e registrar o novo tipo de chefe.
- [x] Instanciar Elias pela Factory e modelar preparação/ataque/recuperação/derrota como estados; integrar eventos de vitória sem callbacks duplicados ao revisitar.
- [x] Atualizar matriz de arquitetura com módulos, símbolos e evidências dos cinco padrões no protótipo; verificar dependências explícitas das cenas.
- [x] Implementar sequência de dois ataques, investida e bola, com poses antecipatórias e recuperações diferentes.
- [x] Vitória limpa ameaças, restaura Elias, registra progresso e devolve à soleira do ginásio.
- [x] Campus interrompe sinal repetido, mostra estudantes em segurança e abre caminho ao M1.
- [x] Disponibilizar retomada no ginásio conservando trava; permitir caminhar até M1 e continuar a campanha integrada.
- [x] Produzir capturas dos estados antes/depois.
- [ ] Registrar partida manual completa — adiada para a revisão humana final.

**Verificação automática:** chefe concreto, preparação sem dano precoce, derrota/vitória sem projéteis residuais, trava preservada, mudança do campus, bloqueio pré-vitória e caminho pós-vitória.

**Aceite manual:** sem instrução verbal externa, identificar ginásio e M1; reconhecer ataques e aberturas; perceber por que vencer mudou a escola. Registrar mortes, locais de desorientação e comandos frustrados.

### H4 — Refinar protótipo e completar Recreio em repetição

**Dependências:** H3. **Entrega:** fase 3 completa e base de combate pronta para expansão.

- [x] Ajustar janelas, quantidade de inimigos, alcance, recarga e duração do chefe conforme evidências.
- [x] Completar três travas, arquibancadas, circuito de treino e rota segura dos estudantes.
- [x] Integrar fala da IFVania em ponto seguro e contato de Max ao sair.
- [x] Completar jardim, reunião e atalho A28; dar resposta visual a cada trava.
- [x] Refinar poses e sons do encontro, preservando leitura mesmo sem áudio.
- [ ] Experimentar ambos os protagonistas e reprovar o marco se controles/orientação ainda falharem, mesmo com testes aprovados.

**Aceite:** combo, defesa e travessia compreensíveis; resgate sem escolta frágil; retorno repetido não recria bloqueios; arte final somente após validação da geometria.

### H5 — Laboratório das cópias, combate aéreo e ancoragem

**Dependências:** H4. **Entrega:** fase 4 e caminho controlável M1 → M5.

- [x] Implementar laçada, golpe aéreo e descendente com pouso comprometido.
- [x] Resolver modificadores de direção/salto no input e atualizar tutorial; impedir restauração infinita de salto e sequências aéreas.
- [x] Estender comandos e estados para combate aéreo/ancoragem, mantendo arbitragem única entre interação e conector; não criar caminhos de entrada paralelos.
- [x] Criar guarda frontal e cópias repetidoras com respostas distintas.
- [x] Construir comparação de arquivos e atalhos por sala estabilizada.
- [x] Implementar `MaxEmLoop`, cópia verdadeira conectada, varredura, bugs e recompilação vulnerável.
- [x] Integrar revelações de autoria/autopreservação e confissão, sem monólogo longo.
- [x] Liberar ancoragem depois da vitória, ensinar em piso seguro e construir travessia até M5.
- [x] Preservar arquivos comparados na retomada; remover duplicações do campus e isolar pendrive com Max.

**Verificação automática:** limite de lançamento, não restauração de salto, guarda/flanco/carregado, origem verdadeira, tutorial antes do bloqueio obrigatório, prioridade E, conectores elegíveis e retorno seguro de queda.

**Aceite manual:** distinguir cópias e apoios; executar aéreo sem conflito recorrente de salto; aprender ancoragem antes de depender dela. O chefe pode ser vencido sem lançar seu corpo.

### H6 — Rede sem saída e isolamento visível

**Dependências:** H5. **Entrega:** fase 5 e percurso M5 → LIT.

- [x] Construir três ramais, conectores, esperas seguras e retornos curtos.
- [x] Implementar retransmissor e composição guarda/atirador sem sobrepor ameaças inevitáveis.
- [x] Cada isolamento apaga monitores e persiste em queda, morte e revisita.
- [x] Implementar `AlessandroSentinelaEnlaces`, barreira, portas sequenciais, varredura e oportunidades frontais/laterais.
- [x] Permitir solução por espera ou flanco; não exigir ancoragem em uma janela única de precisão.
- [x] Mostrar aliados reunidos, rede isolada e nobreak ativo; abrir caminho controlável ao LIT.

**Verificação automática:** três isolamentos independentes, não migração narrativa prematura, barreira/janelas, seleção de conector, invariantes da retomada e porta final condicionada.

**Aceite manual:** reconhecer efeito de cada corte; compreender prioridade do retransmissor e descobrir ao menos uma solução segura do chefe; queda não exige repetir ramais.

### H7 — A última chamada e epílogo

**Dependências:** H6. **Entrega:** fase 6, retorno final pelo campus e conclusão definitiva.

- [x] Construir oficina, memória e núcleo com três desafios curtos de síntese.
- [x] Implementar `FranciscoGuardiaoContinuidade` com vida compartilhada entre proteção automática e ocupação da estrutura pela IFVania.
- [x] Transição liberta Francisco e o move à função de aliado sem duplicar vida, dano ou chefe.
- [x] Usar padrões já ensinados, alternando grupo, pulso e abertura; preservar rota segura.
- [x] Encerrar ameaças, devolver jogador à soleira LIT e liberar caminhada tranquila até A28.
- [x] Terminal final exige resgate concluído, rede isolada e autopreservação encerrada.
- [x] Encenação de desligamento incluindo nobreak, pendrive isolado, escola física e epílogo da tarefa refeita.

**Verificação automática:** transição única, reserva compartilhada, pausa/diálogo sem dano, condições finais, confirmação idempotente, preservação de nome/aparência e nova partida sem herança.

**Aceite manual:** nenhuma regra indispensável nova no final; Francisco é reconhecível como liberto; caminhada final mostra consequências; vitória sem surpresa, ameaça residual ou ambiguidade de IA sobrevivente.

### H8 — Integrar as duas primeiras fases e finalizar apresentação

**Dependências:** H7 para integração final; melhorias independentes podem ocorrer após H4. **Entrega:** campanha completa sem costuras de tutorial ou progressão.

- [x] Ensinar combo básico na descoberta do mouse, sem exigir todas as técnicas avançadas imediatamente.
- [x] Integrar retorno fase 1 → campus → biblioteca e preservar recompensa nula de RomerBug.
- [x] Ajustar vida/invulnerabilidade de alvos iniciais ao combo sem descaracterizar os padrões de RomerBug/SpeedBug.
- [x] Completar bugs de arquivo, atalhos por consulta e bilhete opcional da biblioteca.
- [x] Revisar animação da bolsa e continuidade do reencontro; manter demais pendências antigas rastreáveis.
- [x] Produzir recursos finais, variações corrompida/restaurada, retratos e áudio; preservar fontes e exportar em temporário.
- [x] Revisar câmera, contraste, interações E, placas, escala e limites das áreas de combate.
- [x] Sincronizar LEIA_ME, requisitos, roteiro, fontes e plano com o comportamento realmente entregue.

**Aceite:** primeira partida apresenta controles em ordem compreensível; campus conecta todas as seis fases; nova apresentação não muda colisões acidentalmente.

### H9 — Validação final e homologação da campanha

**Dependências:** H0–H8 entregues. **Entrega:** evidências técnicas e experiência manual homologada; corresponde à validação final da etapa 11 do plano geral.

- [x] Executar suíte completa e critérios integrados, incluindo campanha antiga isolada.
- [x] Auditar Factory, State Machine, Command, Strategy e Observer conforme matriz de arquitetura: uso real, responsabilidades, transições, cancelamento de entrada e ciclo de vida dos observadores.
- [x] Executar exportadores pertinentes em temporário e conferir transparência, pés, quadros e tamanho.
- [ ] Percorrer seis fases e todas as travessias com ambos os protagonistas.
- [ ] Experimentar morte, queda, revisita, pausa, foco, diálogo e transição em cada sistema novo.
- [ ] Avaliar áudio, resposta dos controles, ritmo, orientação, sobrevivência, desempenho e leitura das arenas.
- [x] Registrar problemas restantes com reprodução e prioridade; corrigir bloqueadores e repetir somente verificações afetadas.
- [x] Confirmar desfecho e limpeza de progresso ao iniciar outra campanha.

**Aceite de homologação, ainda pendente:** suíte aprovada e percurso manual completo sem bloqueadores; evidências automáticas, capturas e experiência humana identificadas separadamente. Capturas offscreen não homologam diversão, dificuldade ou áudio.

## 5. Riscos e decisões a validar no protótipo

| Risco | Experimento/mitigação | Marco |
|---|---|---|
| Toque na soltura torna combo cansativo | Medir entradas perdidas e conforto; ajustar janela antes de mudar contrato | H2–H4 |
| Invulnerabilidade atual impede combo ou permite dano excessivo | Testar golpe único versus golpes consecutivos e separar regras jogador/inimigo | H2 |
| Campus vira corredor demorado | Primeira visita curta, marcos visuais, encontros e atalhos permanentes | H3–H4 |
| Ancoragem concorre com interação ou salto direcional | Prioridade explícita, prévia de destino e teste de comandos combinados | H5 |
| Muitos inimigos escondem preparação | Grupos pequenos, limites de ataques simultâneos e avisos corporais distintos | H4–H6 |
| Professor final perde protagonismo para IA | Uma estrutura e reserva; libertação visível e participação de Francisco como aliado | H7 |
| Cenário parece planta real sem ser | Legenda/documentação de espaços adaptados e validação de referências antes da arte final | H1–H8 |
| Fontes históricas confundem cargo ou área atual | Créditos com fontes e reconferência, sem atribuir especialidades não comprovadas | H8 |

## 6. Comandos e registro de evidências

Com dependências instaladas, usar `python principal.py`. Se `python` não existir no ambiente, usar `.venv/bin/python` conforme disponibilidade local.

```bash
python -m unittest discover -s testes -v
```

Sem janela/áudio:

```bash
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy PYGAME_HIDE_SUPPORT_PROMPT=1 python -m unittest discover -s testes -v
```

Criar testes de regras/estados por incremento. Suíte completa em alterações amplas de progressão, input e combate compartilhado, além de H0/H9. Usar capturas para apresentação e partida manual para controles/dificuldade. Não criar testes que apenas repitam estrutura de implementação.

Registrar por marco em `PLANO_DE_EXECUCAO.md`: data, arquivos/sistemas alterados, comportamento entregue, comando e resultado novos, inspeção visual, partida manual, limitações e próxima ação. Evidências visuais futuras podem ficar em `avaliacao/hack_and_slash/`; não criar capturas ou pastas vazias como comprovação de trabalho ainda não feito.

## 7. Estado e próxima ação

- [x] Proposta registrada com diagnóstico, mapa, combate, fases, docentes e fontes.
- [x] Plano de implementação registrado com dependências e critérios de aceite.
- [x] Padrões obrigatórios definidos, implementados e exercitados; ver matriz de arquitetura.
- [x] H0 iniciado: base automática e levantamento de arquitetura registrados; partida manual pendente.
- [x] H1 integrado com campus, Factory, Observer, progresso de sessão e State Machine explícita; ver matriz corrente no início do documento.
- [x] Primeiro protótipo entregue e exercitado automaticamente; avaliação humana de diversão/duração adiada.
- [ ] Homologação humana da campanha completa — adiada.

**Próxima ação humana:** experimentar a campanha conforme [roteiro final](REVISAO_HUMANA_FINAL.md) e registrar ajustes com reprodução. Não há incremento técnico do plano aguardando autorização rotineira.

## 8. Fechamento técnico — 16/11/2026

172 testes aprovados; 15 exportadores executados em cópia temporária, 203 PNGs distintos. Capturas controladas incluem guarda, descoberta do mouse, campus antes/depois, arenas e encerramento. Bloqueio Q, correções de deslocamento real de SpeedBug, novos projéteis, repertório dos guardiões, atalhos/checkpoints, perigos, resgates, ambiência e epílogo visual integrados. Evidências em [RELATORIO.md](../avaliacao/hack_and_slash/RELATORIO.md). Somente a homologação humana permanece aberta.
