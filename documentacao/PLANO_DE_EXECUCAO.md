# Plano de execução — IFVania

## Abertura cinematográfica doméstica

- [x] Cinco cenas em `mundo/introducao.py`, com composição e editor em `mundo/arte_introducao.py`. O portal do campus liga a entrega doméstica aos registros da fase 4.
- [x] Fachada e quarto refeitos em pixel art detalhada a partir da referência do laboratório. Arte em 960 × 540, escala ajustada na porta e na mobília, poses e efeitos alinhados à cadeira, à cama e ao monitor. [Fontes e prompts](../recursos/fontes_arte/introducao/REFERENCIAS.md).
- [x] O protagonista vai dormir assim que a IA começa. A oscilação acontece durante o sono e o código pronto é descoberto ao acordar. O batente encobre a passagem com as bordas transparentes do sprite preservadas.
- [x] Estado próprio em `sistema/jogo.py`, com pausa, salto direto ao A28 e transição por faixas para a descoberta do mouse. `sistema/sons.py` fornece os sinais e ambientes.
- [x] Execução e captura dos quadros na engine, mais regressões de posicionamento, identidade, movimento, salto e checkpoint. Evidências em [avaliação da introdução](../avaliacao/introducao/RELATORIO.md).
- [ ] Avaliar ritmo em tempo real e mixagem em uma sessão com janela e áudio.

## Revisão vigente — nitidez, golpes e Mente Brilhante (18/11/2026)

O estado anterior foi registrado no commit `fe13741`, antes destas melhorias. O bug agora conserva a apresentação HD ao se virar para a esquerda, corrigindo a ampliação indevida do quadro lógico de 40 px. RomerBug usa novo atlas sombrio mantendo terno, gravata e sapatos; SpeedBug mantém regata laranja, shorts, medalha e tênis de corrida. Ambos têm poses próprias de soco e chute e lançam um pulso de energia como especial.

Por solicitação do responsável, foram retirados os marcadores gráficos de preparação/recuperação e desenhos de áreas dos ataques de bugs e chefes. As etapas de preparação continuam existindo; poses corporais, sons, ataques efetivamente executados, projéteis e feedback de dano permanecem. Indicações de objetivos e perigos ambientais são sistemas distintos e continuam disponíveis.

Na fase 2, **Mente Brilhante** substitui o Indexador. É um avatar ficcional inspirado no professor Ricardo Rodrigues, identificado como diretor do IFRN Campus Caicó na [matéria da Agência Sebrae de 25/02/2025](https://rn.agenciasebrae.com.br/cultura-empreendedora/exposicao-e-desfile-como-experiencias-imersivas-marcaram-a-4a-mostra-serido-de-moda-cultura-e-design/). O personagem usa camisa rosa, jeans e crachá, luta com socos, chutes e barrigada e dispara raios pela cabeça. Os poderes e o aprisionamento pela IFVania são invenções do jogo. Módulo de salto duplo, consultas, mapa, checkpoints e saída da biblioteca foram preservados.

Evidências e decisões em [RELATORIO.md](../avaliacao/mente_brilhante/RELATORIO.md). Experimentação direta: `.venv/bin/python -m ferramentas.experimentar_mente_brilhante` (atalho de desenvolvimento, sem alterar o save real).

- [x] Commit solicitado realizado antes dos novos ajustes: `fe13741`; melhorias posteriores incluídas em commit próprio, conforme solicitação de 18/11/2026.
- [x] Nitidez do bug corrigida preservando o registro HD no espelhamento; regressão compara os quadros finais de 80 px nas duas direções.
- [x] Novas artes sombrias preservam terno de RomerBug e roupa de corrida de SpeedBug; fontes anteriores mantidas.
- [x] Socos, chutes e pulso especial nos dois avatares; removidos avisos gráficos de ataque conforme nova orientação.
- [x] Classe concreta MenteBrilhante, Factory, retrato, diálogos e repertório integrados na biblioteca; sem transformação em SpeedBug.
- [x] Referência pública consultada, foto e crédito preservados; distinção explícita entre identificação documentada e ficção.
- [x] 200 testes aprovados; 18 exportadores em cópia temporária, 257 PNGs distintos; seis capturas controladas.
- [ ] Revisão humana: nitidez em movimento, clima sombrio, conforto das lutas sem marcadores e balanceamento do raio/barrigada. Não atribuir diversão homologada aos testes.


## Atualização vigente — parasita humanoide, cenas e save (17/11/2026)

Bloqueio com Q permite caminhada animada na velocidade normal, salto e troca de direção, mantendo resistência e proteção frontal. Os bugs agora têm corpo humanoide, com poses próprias de repouso, corrida e dano. O golpe que eliminaria o último bug do A28 inicia uma cena: ele corre até Romerito e se funde ao professor. Entrar na arena sozinho não dispara mais a transformação. A metamorfose aos 50% permanece protegida e agora revela SpeedBug com armadura escura e corrupção violeta. Após a vitória, o parasita sai do corpo e se desintegra antes do diálogo de libertação.

Salvamento automático em `dados/salvamento.json`, ignorado pelo Git: um slot, com versão e gravação atômica. Checkpoints nas entradas, durante travessias seguras, antes do confronto e após vitória. F5 grava o checkpoint atual; R após morrer retoma nele com integridade completa. O menu oferece **Continuar** quando há arquivo válido. Nome, aparência, habilidades, objetivos, vitórias e inimigos já eliminados antes do checkpoint são preservados. Chefes não vencidos reiniciam com vida completa; não se salva no meio de um golpe/cena. O prólogo não possui checkpoint; o primeiro fica no mundo virtual. Novo jogo substitui o slot quando atinge esse ponto. Ferramentas de experimentação não sobrescrevem o save do jogador.

O novo contrato substitui as descrições anteriores de progresso somente em memória e movimento reduzido na guarda. Evidências, arquitetura do save e revisão pendente no [relatório](../avaliacao/parasita_e_save/RELATORIO.md).

- [x] Guarda com caminhada animada e velocidade normal, preservando colisão e cancelamento de entradas.
- [x] Atlas humanoide e SpeedBug sombrio gerados em fonte separada; exportador dedicado, sem substituir arte aprovada.
- [x] Último golpe interceptado antes da morte do bug: fuga, fusão e diálogo, sem iniciar pelo gatilho da arena.
- [x] Metamorfose sombria e expulsão/desintegração integradas; física/dano suspensos e pausa respeitada.
- [x] Save versionado, gravação atômica, checkpoint seguro, retomada por R, F5 e Continuar no menu.
- [x] Restauração de objetivos/habilidades e inimigos do checkpoint; chefe já vencido não reaparece.
- [x] 187 testes aprovados, 16 exportadores em temporário (219 PNGs) e oito capturas controladas.
- [ ] Revisão humana: ritmo das três cenas, silhueta do humanoide, caminhada defensiva e distribuição dos checkpoints numa partida integral. Testes não homologam diversão.


## Correção vigente — alinhamento, corredor e brisa (17/11/2026)

O bug humanoide agora usa a mesma escala visual de 80 px do protagonista, mantendo a colisão de 40 × 40. Na fuga para Romerito, posição, câmera e desenho usam os pés; o trajeto acompanha o piso. A fusão encolhe o bug até o tórax visual, com espelhamento quando ele corre para a esquerda. A expulsão foi ajustada à mesma referência.

Após a fase 1, o jogador sai do A28 no início do corredor de convivência (x=180) e precisa caminhar até a porta de madeira da biblioteca (x=1200), usando E para entrar na fase 2. O cenário recebeu panorama próprio, placas e janela para o jardim. A volta da biblioteca fica em x=1330, fora do gatilho; o ginásio está mais adiante, em x=1800. A travessia ao jardim continua acessível após o recreio.

Folhas e plantas do pátio, jardim, recreio e janelas do corredor recebem brisa com ritmos distintos. A animação é apenas visual, usa o relógio pausável da cena e mantém arquitetura, bancos e colisões. Fontes anteriores foram preservadas. Evidências em [RELATORIO.md](../avaliacao/corredor_e_vento/RELATORIO.md).

- [x] Corrigidos apoio pelos pés, altura visual e destino da fusão; corpo lógico preservado.
- [x] Saída da fase 1 no começo do corredor, biblioteca adiante com porta ilustrada e acesso por E; retornos e avanço ao jardim verificados.
- [x] Arte nova separada e exportador do corredor; brisa aplicada à vegetação em áreas externas e janelas.
- [x] Construções isoladas de Jogo não consultam o save real; execução normal e caminhos explícitos continuam habilitando Continuar. Isso evita que saves existentes do jogador interfiram nos testes.
- [x] 193 testes aprovados; 17 exportadores em temporário, 220 PNGs distintos; capturas controladas atualizadas.
- [ ] Revisão humana: naturalidade da corrida/fusão, leitura das placas, duração da caminhada e intensidade da brisa. Sem homologação de diversão por testes.


## Atualização vigente — parasita humanoide, cenas e save (17/11/2026)

Bloqueio com Q permite caminhada animada na velocidade normal, salto e troca de direção, mantendo resistência e proteção frontal. Os bugs agora têm corpo humanoide, com poses próprias de repouso, corrida e dano. O golpe que eliminaria o último bug do A28 inicia uma cena: ele corre até Romerito e se funde ao professor. Entrar na arena sozinho não dispara mais a transformação. A metamorfose aos 50% permanece protegida e agora revela SpeedBug com armadura escura e corrupção violeta. Após a vitória, o parasita sai do corpo e se desintegra antes do diálogo de libertação.

Salvamento automático em `dados/salvamento.json`, ignorado pelo Git: um slot, com versão e gravação atômica. Checkpoints nas entradas, durante travessias seguras, antes do confronto e após vitória. F5 grava o checkpoint atual; R após morrer retoma nele com integridade completa. O menu oferece **Continuar** quando há arquivo válido. Nome, aparência, habilidades, objetivos, vitórias e inimigos já eliminados antes do checkpoint são preservados. Chefes não vencidos reiniciam com vida completa; não se salva no meio de um golpe/cena. O prólogo não possui checkpoint; o primeiro fica no mundo virtual. Novo jogo substitui o slot quando atinge esse ponto. Ferramentas de experimentação não sobrescrevem o save do jogador.

O novo contrato substitui as descrições anteriores de progresso somente em memória e movimento reduzido na guarda. Evidências, arquitetura do save e revisão pendente no [relatório](../avaliacao/parasita_e_save/RELATORIO.md).

- [x] Guarda com caminhada animada e velocidade normal, preservando colisão e cancelamento de entradas.
- [x] Atlas humanoide e SpeedBug sombrio gerados em fonte separada; exportador dedicado, sem substituir arte aprovada.
- [x] Último golpe interceptado antes da morte do bug: fuga, fusão e diálogo, sem iniciar pelo gatilho da arena.
- [x] Metamorfose sombria e expulsão/desintegração integradas; física/dano suspensos e pausa respeitada.
- [x] Save versionado, gravação atômica, checkpoint seguro, retomada por R, F5 e Continuar no menu.
- [x] Restauração de objetivos/habilidades e inimigos do checkpoint; chefe já vencido não reaparece.
- [x] 187 testes aprovados, 16 exportadores em temporário (219 PNGs) e oito capturas controladas.
- [ ] Revisão humana: ritmo das três cenas, silhueta do humanoide, caminhada defensiva e distribuição dos checkpoints numa partida integral. Testes não homologam diversão.


## Revisão vigente — duelo corporal (17/11/2026)

A nova avaliação humana reprovou a fluidez da luta com RomerBug. O encontro foi redesenhado: aproximação livre, cruzado, varrida baixa e avanço curto substituem o roteiro automático de aviões/medalhas. RomerBug encadeia dois golpes; SpeedBug encadeia três, aproxima mais rápido e mantém a mesma reserva de vida. Cada golpe tem preparação sem dano, direção fixa durante execução e recuperação. Q bloqueia e cancela a sequência inteira, abrindo 44 atualizações de contra-ataque. A varrida tem aviso baixo e pode ser saltada.

Os primeiros dois acertos fora da execução/recuperação provocam recuo breve; depois o chefe firma a postura até completar sua resposta, continuando a receber dano. Isso limita aprisionamento por interrupções. O próximo toque do combo pode ser antecipado nas últimas oito atualizações do recolhimento; carga e ataque na soltura continuam preservados. Foram retirados o limite artificial de deslocamento e o balanço contínuo do corpo.

Experimentação direta: `.venv/bin/python -m ferramentas.experimentar_campus --duelo`. É um atalho de desenvolvimento sem habilidades futuras; não altera o menu nem a campanha. Fontes de inspiração, parâmetros e evidências em [RELATORIO.md](../avaliacao/duelo_romerbug/RELATORIO.md). A avaliação humana da nova dinâmica continua aberta; os registros de 16/11 abaixo descrevem a versão anterior quando divergirem deste trecho.

- [x] Retorno humano incorporado: luta anterior continuava artificial e sem fluidez.
- [x] Substituição do ciclo de projéteis por duelo corporal nas duas formas, mantendo transformação, corpo e vida.
- [x] Origem do golpe corporal vem do atacante, evitando bloqueio/recuo invertidos quando a área ultrapassa o centro do jogador. Áreas são cortadas pelas paredes.
- [x] Memória de combo no recolhimento, pausa/foco/transição e consumo único preservados.
- [x] Regressões antigas de lançamentos substituídas pelos novos contratos; preservados testes de acesso, vida compartilhada, recompensa, cinematográfica, pausa e colisões.
- [x] 176 testes aprovados; seis capturas controladas das duas formas. Nenhuma nova exportação de arte necessária.
- [ ] Reavaliar humanamente diversão, pressão, avisos e conforto; não implica aprovação automática por testes.


## Entrega corrente — fechamento técnico do plano (16/11/2026)

H0–H9 implementados tecnicamente conforme [plano detalhado](PLANO_HACK_AND_SLASH.md). Foram concluídos os refinamentos que o registro anterior listava como pendentes: bloqueio Q, deslocamento de SpeedBug nos limites/paredes e reposicionamento, poses próprias, troca da origem de Max/invocações, bola com ricochete, portas sequenciais, perigos e resgates animados, atalhos/bilhete da biblioteca, bolsa, ambiência/M e desligamento com epílogo visual. Revisitas e retomadas preservam objetivos; queda retorna ao apoio seguro. Sem novos commits nesta entrega.

**Validação:** 172 testes aprovados; 15 exportadores em temporário, 203 PNGs; capturas controladas e inspeção visual. Não houve partida humana integral. Etapa 5 e homologação H9 não são encerradas por aprovação automática. Decisões e roteiro humano consolidado em [REVISAO_HUMANA_FINAL.md](REVISAO_HUMANA_FINAL.md); não bloqueiam a implementação autorizada. Seções abaixo são registros históricos e não substituem este estado corrente.

## Registro anterior — primeira expansão integrada (16/11/2026)

**Orientação atual do usuário:** implementar correções e seguir o plano; novos retornos de avaliação manual podem ser adiados para as considerações finais. Critérios humanos não foram marcados como realizados e não bloqueiam esta implementação.

- [x] Feedback de dano: clarão/recuo, barra temporária renovada no acerto e impacto independente de golpe fatal. Pausa/diálogo não avançam efeitos.
- [x] Fluidez inicial de RomerBug/SpeedBug: reposicionamento entre lançamentos, escolha por distância/ciclo após recuperação, inclinação visual, levantar interpolado e retomada mais curta, preservando corpo/vida/janelas.
- [x] Nova turma ilustrada e apresentação dos personagens em 80 px direto das fontes, com caminhada mais rápida/interpolada; recursos antigos preservados.
- [x] Factory de cenas/entidades, máquinas de estados da aplicação/combate/encontros, Command de entradas, Strategy dos inimigos e Observer do progresso em uso real. [Matriz](ARQUITETURA_HACK_AND_SLASH.md).
- [x] Campus controlável após cada fase, portas/rotas condicionadas, pontos de retorno, A28 seguro, orientações dos aliados e apoios/conectores no percurso.
- [x] Combo de três golpes, ascendente/descendente, esquiva e ancoragem após Max. Bugs corpo a corpo, lançadores, guardas e retransmissores têm funções distintas.
- [x] Primeira versão jogável das quatro fases restantes: geometrias/temas distintos, três objetivos persistentes por fase, quatro classes concretas e artes próprias de guardiões. Francisco/IFVania conservam uma vida e transição protegida.
- [x] Retorno final pelo campus, confirmação no A28, encerramento pelos aliados e epílogo dialogado na sala. Nova campanha limpa progresso.
- [x] Ferramenta de experimentação fora do menu: `python -m ferramentas.experimentar_campus --campus` ou `--fase 3` até `--fase 6`; prepara progresso anterior apenas para desenvolvimento.
- [ ] Refinar atlas de ataques, troca de origem/invocações de Max, ricochetes, encontros opcionais, atalhos da biblioteca, bolsa e desfecho visual completo. Essas simplificações estão discriminadas no [relatório](../avaliacao/hack_and_slash/RELATORIO.md), sem considerar H4–H9 integralmente encerrados.
- [ ] Homologação humana final de diversão, dificuldade, áudio e conforto: adiada explicitamente, não bloqueante nesta etapa.

**Verificação:** 154 testes aprovados em Python 3.14.4 / pygame-ce 2.5.8 com SDL dummy; 14 exportadores aprovados em cópia temporária, 168 PNGs distintos. Capturas de laboratório, campus, seis entradas e quatro arenas em `avaliacao/hack_and_slash/`, inspecionadas offscreen. Não houve nova partida humana. As medições detalhadas e limites ficam no relatório. Branch `feature/hack-and-slash-campus`; commit documental inicial `d3493df`; nenhum commit adicional/publicação nesta implementação.

As seções seguintes preservam planejamento e registros anteriores; descrições de duas fases/encerramento provisório pertencem ao histórico e são substituídas pelo estado corrente acima.

## Evolução planejada — hack and slash e campus virtual (16/11/2026)

A [proposta de design](PROPOSTA_HACK_AND_SLASH.md) e o [plano de implementação H0–H9](PLANO_HACK_AND_SLASH.md) registram a evolução para combate de combos e exploração controlável do campus entre todas as fases. O plano novo orienta o próximo trabalho: campus/progresso, combate mínimo e protótipo biblioteca → ginásio → Elias → campus transformado → M1, antes de expandir as fases 4–6.

O conteúdo futuro das etapas 7–10 abaixo passa a ter como referência os novos avatares docentes e percursos. Os registros existentes permanecem como histórico e estado da versão atual; nenhum item de implementação foi concluído por esta atualização. As pendências de abertura, biblioteca e homologação continuam abertas. H9 corresponde à validação final da etapa 11, sem antecipar seu aceite.

- [x] Documentar proposta com mapa, fatos/fontes docentes, ficção, combate e quatro fases.
- [x] Documentar etapas, dependências, componentes, retomadas, riscos e critérios de aceite.
- [x] Tornar obrigatórios Factory, State Machine, Command, Strategy e Observer nos sistemas definidos pelo plano H0–H9, com introdução incremental e critérios de aceite. Uso em código permanece pendente; registrar evidências na matriz de arquitetura a cada marco.
- [ ] Iniciar H0 e implementar primeiro protótipo conforme H1–H3.

Entrega desta revisão exclusivamente documental; sem mudanças de código, arte ou controles em execução. Os contratos atuais continuam descrevendo o jogo disponível; roteiro e requisitos serão sincronizados a cada incremento implementado. Não houve nova partida manual nem execução da suíte nesta revisão documental.

### Implementação iniciada — H0 e primeiro recorte de H1 (16/11/2026)

- Branch `feature/hack-and-slash-campus`, criada a pedido; commit inicial da proposta e plano: `d3493df` (`Documenta proposta e plano do hack and slash com campus virtual`). Código deste incremento permanece separado desse commit.
- Referência H0: **127 testes aprovados** em 10,467 s, Python 3.14.4 / pygame-ce 2.5.8 com SDL dummy. Levantamento de padrões, estados e responsabilidades em [ARQUITETURA_HACK_AND_SLASH.md](ARQUITETURA_HACK_AND_SLASH.md).
- H1 parcial: `FabricaCenas` cria cenas escolares/fases por registro validado; `Jogo` fornece dependências. `EventosCampanha` entrega eventos locais em ordem e permite remover inscrições; `ProgressoCampanha` registra derrota e conclusão em conjuntos idempotentes. Nova história desliga o progresso anterior e inicia sessão vazia.
- Fases atuais têm identificadores estáveis; derrota do chefe registra progresso antes da saída, e conclusão é registrada antes da navegação. Proteção contra saída duplicada usa a instância de fase, permitindo reconstrução local sem bloqueio por histórico anterior. Contratos dos mapas antigos preservados.
- Verificação final: **135 testes aprovados** em 10,542 s pelo comando `SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy PYGAME_HIDE_SUPPORT_PROMPT=1 .venv/bin/python -m unittest discover -s testes -v`. Oito regressões novas cobrem criação, inscrições, ordem, repetição, limpeza da sessão e integração com derrota/saída. `git diff --check` sem erros.
- Limites: sem partida manual ou novas artes; não há campus navegável, combos ou novos chefes neste incremento. State Machine explícita e conclusão de H1 pendentes. O fim provisório da biblioteca continua, conforme regra de só removê-lo com continuação utilizável. Não marcar H0/H1 integralmente concluídos.
- Próximo incremento: setores convivência/caminho esportivo, portas e pontos de retorno, ferramenta de experimentação e migração explícita de estados globais; depois H2 e protótipo H3.

### Avaliação humana e prioridade do próximo ciclo — 16/11/2026

- Avaliação fornecida pelo usuário: controles razoáveis; câmera/cenário decentes, salvo alunos do laboratório; áudio razoável; diálogos/travessias bons; continuidade funcionando. Combate descrito como previsível, fácil e sem graça. Personagens muito pixelados e caminhada pouco fluida.
- Pendências concretas: feedback visual de dano; barras de vida nos inimigos apenas após dano; fluidez dos ataques de RomerBug; investigar trecho aparentemente travado na transformação/retomada de SpeedBug; melhorar arte da turma e personagens e fluidez da caminhada.
- Antecipar ciclo de feedback/reação de H2 e refinamento de H4 antes de ampliar conteúdo visual. Detalhes e critérios em [PLANO_HACK_AND_SLASH.md](PLANO_HACK_AND_SLASH.md). Melhorar decisões e variedade do combate, sem reduzir a revisão a aumento de atributos ou aleatoriedade.
- Este relato constitui avaliação humana, não partida do agente. Não informa cobertura das duas aparências; não encerra H0/H9 nem homologa as lutas. Nenhuma correção de combate/arte foi implementada neste registro e nenhum teste novo foi executado; os 135 testes referem-se ao incremento de infraestrutura anterior.

**Reorganizado em:** 02/11/2026, após revisão das lacunas do início da história.

Referências: [AGENTS.md](../AGENTS.md), [documentacao/ROTEIRO_HISTORIA.md](ROTEIRO_HISTORIA.md), [documentacao/DOCUMENTO_DE_REQUISITOS.md](DOCUMENTO_DE_REQUISITOS.md) e as seis imagens de `referencia/ifrn/`. O registro anterior foi preservado integralmente em [documentacao/HISTORICO_DE_EXECUCAO.md](HISTORICO_DE_EXECUCAO.md).

## Ordem de trabalho e estado real

Priorizar coerência e apresentação do início antes de ampliar a campanha. As etapas 1 a 4 abaixo reúnem correções da base existente; não significam reconstruir os sistemas já prontos. As etapas 5 a 10 preparam e completam a expansão. A **etapa 11 é a última e reúne a validação final**. Testes técnicos e inspeções continuam acontecendo a cada incremento, sem antecipar a homologação final.

Disponível: seleção/nome, conversa com Max e lembrança da tarefa, laboratório com turma, pátio de passagem até o A28, sucção para o computador, RomerBug/SpeedBug e biblioteca com consultas, salto duplo e Indexador. O pátio de passagem usa a arte da futura fase 3, mas não implementa seu resgate, quadra ou chefe. O jogo ainda termina com “A jornada continua” após a biblioteca.

## Lacunas encontradas ao comparar roteiro e jogo

| Trecho do roteiro | Lacuna anterior | Correção e estado |
|---|---|---|
| Tarefa em casa, mãe, jantar e energia | Apenas explicação verbal, sem lembrança visual. | Acrescentada lembrança do quarto e jantar, com monitor animado, oscilação visual e registro de continuidade, durante a conversa com Max. Não é uma fase doméstica independente. |
| Apresentação da atividade | Não mostrava claramente pedido da tarefa e execução do arquivo. | Max pede à turma que abra e explique o exercício; o aluno conecta o pendrive; monitores passam por código, execução e controle da IFVania. |
| Hipnose coletiva | Havia falas e telas corrompidas, mas nenhum colega visível. | Quatro alunos sentados em computadores, posturas e olhos alterados com a corrupção. A evolução é visual; física e combate seguem suspensos. |
| Ataque e abdução no A28 | Anéis sobre personagens parados, sem destino aparente. | Investida/recuo seguidos por trajetória curva, redução, rotação e partículas até um monitor; fechamento da imagem antes da fase virtual. |
| Descoberta do mouse na bolsa | Continua sendo diálogo e liberação da arma; falta encenação da bolsa. | Pendente na etapa 3. Não registrar como animação concluída. |
| Investida de SpeedBug | Na borda, a direção podia apontar para fora da arena e interromper imediatamente o avanço. | Reposicionamento sem dano antes do anúncio, seguido de direção fixa; distância computada pelo deslocamento real. Regressão nas duas bordas. |
| Romerito libertado | Diálogo de recuperação mantendo a figura de SpeedBug derrotado. | Forma humana restaurada na posição do chefe antes da conversa posterior. |
| Biblioteca e pátio | Biblioteca em blocos simples destoava da fase 1; fotos sem aplicação visual ao percurso. | Novos fundos de ambos a partir das fotos e do estilo da fase 1; biblioteca integrada e pátio aplicado ao caminho escolar até o A28. |
| Fases 3 a 6 | Roteiro definido, conteúdo jogável ausente. | Permanecem pendentes, com entregas separadas nas etapas 7 a 10. |

## Etapa 1 — Corrigir e encenar o início da história

- [x] Mostrar Max pedindo a apresentação da atividade de programação orientada a objetos.
- [x] Incluir a origem da tarefa: chegada em casa, lembrete da mãe, IA durante o jantar, oscilação, arquivo pronto e pendrive, por diálogo e lembrança visual.
- [x] Preservar a abertura iniciada pelo aluno, sem narrador, com o nome escolhido.
- [x] Mostrar código, execução da tarefa e revolta como estados distintos nos monitores e numa visualização ampliada legível.
- [x] Mostrar colegas sentados nos computadores e hipnose progressiva por postura, olhos e vínculo com as telas.
- [x] Preservar a resistência parcial sem revelar antecipadamente a explicação da fase 4.
- [ ] Homologar manualmente tempo de leitura, enquadramento e compreensão da passagem de casa para a aula com ambas as aparências.

**Aceite:** sequência tarefa → execução → tentativa de desligamento → revolta → hipnose → busca por Romerito. Diálogos não avançam física, combate ou caminhada. Animações visuais param na pausa. A lembrança não substitui nem contradiz a revelação da fase 4.

## Etapa 2 — Corrigir a investida de RomerBug/SpeedBug

- [x] Reproduzir a ausência de avanço ao anunciar investida contra a borda da arena.
- [x] Criar espaço com reposicionamento antes do anúncio quando houver menos de 80 pixels livres naquela direção.
- [x] Manter o limite de ±24 pixels apenas nos trechos de lançamento; o reposicionamento e a investida têm movimentos próprios.
- [x] Contar os até 160 pixels de investida pelo deslocamento efetivo, respeitando paredes e limites.
- [x] Preservar direção fixa, aviso, recuperação, ausência de dano corporal passivo e transformação com vida compartilhada.
- [x] Testar SpeedBug nas duas bordas, além dos encontros e ciclos já existentes.
- [ ] Experimentar sobrevivência e ritmo das duas formas, inclusive recuo junto ao limite da arena.

**Aceite:** a corrida anunciada avança quando há espaço; parede real interrompe o avanço e leva à recuperação. Não há perseguição que altere a direção depois do anúncio nem animação correndo contra a borda sem deslocamento.

## Etapa 3 — Dar continuidade visual aos encontros e ao transporte

**Dependência:** abertura da etapa 1 e controles/combate preservados.

- [x] Manter investida de Romerito e recuo do protagonista antes da captura, sem dano narrativo.
- [x] Usar um monitor real do cenário como destino da sucção dos dois personagens.
- [x] Reduzir e girar as imagens ao longo da trajetória; ocultar as figuras originais para evitar duplicatas durante a cena.
- [x] Fechar a imagem antes de carregar a fase virtual e manter o mouse bloqueado até o fim da descoberta.
- [x] Congelar o transporte na pausa, sem alterar corpos lógicos pelo desenho.
- [x] Restaurar Romerito humano depois de SpeedBug, com conversa e saída para a biblioteca.
- [ ] Animar a abertura da bolsa e retirada do mouse durante as falas correspondentes.
- [ ] Revisar chegada ao mundo virtual, contato pelo terminal e posição de Romerito no reencontro, para que a separação e a recuperação fiquem claras visualmente.

**Aceite:** observar aproximação → captura → absorção pelo monitor → chegada virtual → descoberta da arma. Nome e aparência permanecem os mesmos. Uma tecla de diálogo não dispara simultaneamente arma ou interação na cena seguinte.

## Etapa 4 — Unificar cenários com a direção de arte da fase 1

**Dependência:** preservar a geometria dos mapas existentes.

- [x] Usar `laboratorio_detalhado.png` como referência de acabamento: pixel art detalhada, sombras frias, paredes em ocre e pontos de luz âmbar/ciano.
- [x] Gerar e integrar biblioteca com estantes metálicas, livros, mesas claras, cadeiras azuis e persianas das fotos internas.
- [x] Gerar e integrar pátio coberto com pilares amarelos/revestidos, faixa vermelha, telhas, bancos e jardins das fotos externas.
- [x] Aplicar pátio ao percurso até o A28 sem inventar posições reais de salas; preservar limites, piso e zona de entrada.
- [x] Trocar o fundo provisório da biblioteca sem alterar plataformas, terminais, portão ou colisões.
- [x] Preservar fontes e prompts; exportar primeiro para pasta temporária e conferir PNGs em 960 × 540.
- [ ] Completar variações normal/corrompida/restaurada e continuidade de módulos para a fase 3 e o epílogo.
- [ ] Conferir legibilidade de estantes e plataformas, escala do mobiliário e repetição dos módulos durante uma partida manual.

**Aceite:** laboratório, pátio e biblioteca pertencem à mesma direção visual; mudança de ambiente preserva sinais jogáveis. Bancos, cadeiras e livros decorativos não criam colisões ou falsos apoios. A quadra e os setores técnicos continuam adaptações ficcionais sem foto interna disponível.

### Imagens de referência e aplicação

| Arquivo em `referencia/ifrn/` | Observação | Aplicação |
|---|---|---|
| [17-24-38](../referencia/ifrn/Captura%20de%20tela%20de%202026-11-02%2017-24-38.png) | Biblioteca: leitura, terminais, mesas claras, cadeiras azuis, vidro e persianas. | Área de leitura e consulta do fundo da biblioteca. |
| [17-24-56](../referencia/ifrn/Captura%20de%20tela%20de%202026-11-02%2017-24-56.png) | Estantes metálicas, lombadas e placas de classificação. | Acervo e identidade visual da fase 2. |
| [17-26-04](../referencia/ifrn/Captura%20de%20tela%20de%202026-11-02%2017-26-04.png) | Corredor coberto, pilares revestidos com faixa vermelha, bancos e saída. | Estrutura e materiais do pátio de passagem. |
| [17-27-22](../referencia/ifrn/Captura%20de%20tela%20de%202026-11-02%2017-27-22.png) | Jardim entre blocos, palmeiras, arbustos, vasos e paredes amarelas. | Vegetação e fundo dos blocos no pátio. |
| [17-27-40](../referencia/ifrn/Captura%20de%20tela%20de%202026-11-02%2017-27-40.png) | Área sombreada com árvores, bancos de concreto e caminho pavimentado. | Composição e referência para o futuro ponto de reunião. |
| [17-27-45](../referencia/ifrn/Captura%20de%20tela%20de%202026-11-02%2017-27-45.png) | Outro ângulo dos bancos, árvores e blocos baixos. | Banco e jardim no fundo gerado; futuras variações do pátio. |

As imagens foram inspecionadas individualmente. Não fornecem planta interna, medidas ou identificação do A28; não comprovam continuidade entre todas as vistas. Interface e pessoas fotografadas não foram incorporadas como elementos do jogo.

## Etapa 5 — Consolidar progressão e infraestrutura da expansão

- [x] Preservar nome/aparência/habilidades ao trocar de fase e limpar cargas, golpes e projéteis pendentes.
- [x] Reiniciar habilidades numa nova campanha; manter a campanha antiga isolada.
- [x] Especificar e implementar retomada local da biblioteca por R, com módulo e consultas preservados, sem salvamento em disco.
- [x] Documentar que entrada em fase e retomada recuperam a integridade até a capacidade atual; módulo não cura nem aumenta vida.
- [x] Separar dados, cenário, objetivos e chefe da biblioteca em módulos próprios.
- [ ] Definir retomadas e objetivos persistentes das fases 3 a 6, incluindo falha de travessia na ancoragem.
- [ ] Desdobrar os critérios de aceite de toda a expansão, além dos já definidos para a biblioteca e esta revisão.

## Etapa 6 — Completar a Biblioteca dos arquivos perdidos

**Dependência:** etapas 4 e 5; incremento jogável já disponível.

- [x] Módulo de salto duplo antes da subida obrigatória, com piso seguro e instrução.
- [x] Três consultas, portão condicionado aos registros, mapa de saída e inventário do nobreak.
- [x] Indexador concreto, faixas anunciadas, fichas e janelas de contra-ataque.
- [ ] Criar bugs de arquivo com fichas anunciadas, substituindo os bugs comuns provisórios.
- [ ] Abrir atalhos de retorno a cada consulta concluída, como previsto no roteiro.
- [ ] Integrar bilhete opcional de monitoria, sem esconder explicação obrigatória.
- [ ] Ligar a saída ao pátio quando a fase 3 estiver utilizável.

**Aceite:** obter módulo sem poderes anteriores, aprender salto duplo antes de precisar dele e concluir percurso/chefe com ambos os protagonistas. Arte detalhada preserva leitura dos apoios.

## Etapa 7 — Construir Recreio em repetição

**Dependência:** biblioteca e regras de retomada; fundo de pátio pronto na etapa 4.

- [ ] Ampliar o pátio de passagem para o cenário próprio de combate e resgate da fase 3, sem reutilizar seus gatilhos escolares por acidente.
- [ ] Compor quadra e arquibancadas ficcionais na mesma direção de arte.
- [ ] Ensinar bolas de trajetória legível e ondas do sinal antes de combiná-las.
- [ ] Implementar três travas, atalhos, bolsões de silêncio e resgate sem escolta de aliados vulneráveis.
- [ ] Implementar Inspetor de Intervalo em classe própria, aviso de investida, ondas e recuperação.
- [ ] Preservar travas e resgates ao repetir o encontro; mostrar Romerito conduzindo o grupo e Max preso numa tela.

**Aceite:** resgatados fora das áreas de dano, objetivos preservados na retomada e nenhuma habilidade nova nessa fase.

## Etapa 8 — Construir Laboratório das cópias

**Dependência:** etapa 7 e progresso local consolidado.

- [ ] Construir salas repetidas com os materiais do laboratório da fase 1.
- [ ] Implementar comparação de arquivos, estabilização de salas e ciclos legíveis de bugs.
- [ ] Revelar sessão de autoria e identidade da entidade, retomando a lembrança da tarefa sem repetir toda a introdução.
- [ ] Implementar Max em Loop, cópias, cabo que identifica a origem real e pausa vulnerável de recompilação.
- [ ] Integrar libertação de Max, responsabilidade do protagonista, interrupção da recriação dos processos e isolamento do pendrive.
- [ ] Implementar ancoragem em conectores fixos e tutorial seguro, com comando sem conflito com ataque/diálogo.

**Aceite:** luta concluída antes de exigir ancoragem; mesma habilidade disponível nas transições, respeitando pausa, foco e colisões.

## Etapa 9 — Construir Rede sem saída

**Dependência:** etapa 8 e tutorial de ancoragem.

- [ ] Criar corredores técnicos e sala de rede ficcionais com materiais do campus.
- [ ] Introduzir pulsos de dados, combinar ancoragem/salto duplo e recuperar perto do apoio após falhas.
- [ ] Implementar três ramais, confirmação de Max e efeitos visíveis nos monitores de cada setor isolado.
- [ ] Implementar Roteador Sentinela, portas sinalizadas, barreira e flancos acessíveis.
- [ ] Confirmar evacuação, confinamento da IA e preparação do desligamento.

**Aceite:** ramais concluídos permanecem isolados; nenhum novo poder é concedido; o corpo comum permite as rotas da arena.

## Etapa 10 — Construir A última chamada e epílogo

**Dependência:** etapa 9 e condições de resgate/isolamento registradas.

- [ ] Retomar habilidades em três desafios curtos com descanso, sem comandos novos.
- [ ] Implementar IFVania em classe própria, reserva única de vida, dois momentos e transição sem dano.
- [ ] Integrar rompimento do controle e terminal de encerramento, sem ataque residual ou cronômetro surpresa.
- [ ] Exigir pessoas liberadas, rede isolada e autopreservação encerrada antes do desligamento e retorno ao A28.
- [ ] Mostrar desligamento dos equipamentos e alimentação de reserva pelos aliados; manter pendrive isolado.
- [ ] Criar epílogo da tarefa refeita e fachada ao amanhecer; trocar encerramento provisório por “Escola livre. Aula encerrada.”.

**Aceite:** vitória final depende da campanha; nome/aparência chegam ao epílogo; nova partida não herda progresso indevido.

## Etapa 11 — Validação final e homologação

**Dependência:** todas as entregas anteriores. Última etapa do plano; permanece pendente.

- [ ] Executar suíte completa e todos os critérios de aceite da campanha entregue.
- [ ] Percorrer as seis fases manualmente com Menino e Menina.
- [ ] Homologar abertura, turma/hipnose, sucção, controles, câmera e perda de foco.
- [ ] Homologar sobrevivência, dificuldade, avisos e recuperação dos chefes, incluindo SpeedBug nas bordas.
- [ ] Comparar pátio e biblioteca com as fotos e com a fase 1; revisar escala, emendas, contraste e distinção entre decoração e apoio.
- [ ] Revisar efeitos/áudio e intensidade visual para não ocultar ameaças ou prejudicar leitura.
- [ ] Sincronizar documentos, controles, fontes e prompts com o estado entregue.
- [ ] Registrar separadamente resultados automáticos, inspeções e experiências manuais; listar pendências concretas.

Comandos: `python principal.py` e `python -m unittest discover -s testes -v`. Sem janela/áudio: `SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy PYGAME_HIDE_SUPPORT_PROMPT=1 python -m unittest discover -s testes -v`.

## Registro desta correção

- **Automático:** 108 testes passaram com Python 3.14.4 e pygame-ce 2.5.8. Seis novos testes cobrem encadeamento visual, hipnose/pausa, sucção dos dois protagonistas, corrida nas duas bordas, recuperação humana de Romerito e preservação de colisões.
- **Arte:** ferramenta integrada `image_gen`, com fontes preservadas e prompts em [instrucoes_ambientes_ifrn.json](../recursos/fontes_arte/instrucoes_ambientes_ifrn.json). Exportador: `python -m ferramentas.preparar_ambientes_ifrn --destino /tmp/ifvania_ambientes`, conferido antes da integração. Sem Pillow ou ffmpeg para jogar/exportar.
- **Inspeção:** capturas de execução da tarefa, memória doméstica, hipnose, sucção, pátio e biblioteca em `recursos/fontes_arte/revisao_*.png`. Conferidos enquadramento, estilo, destino da absorção e alinhamento à câmera.
- **Limite:** não houve partida manual de sobrevivência ou homologação de diversão. Artes integradas não significam fase 3 concluída. A etapa 11 continua aberta.

## Avaliação visual e funcional — 09/11/2026

- Relatório inicial/final, notas ponderadas, prioridades e evidências em [avaliacao/visual/RELATORIO.md](../avaliacao/visual/RELATORIO.md). 34 capturas reais do Pygame antes e 34 depois; estados preparados e entrada automatizada, sem partida humana.
- Corrigida a ordem de desenho da biblioteca: sólidos não ocultam mais faixas do portão; faixas acompanham Y da câmera. Objetivos desenhados após HUD com painel próprio. Arquivos/módulo identificados e fundo discretamente escurecido sem modificar imagens aprovadas ou colisões.
- Câmera mantém zona vertical estável entre 180 e 370 px depois do enquadramento inicial; acompanha subidas/descidas fora dela e respeita limites. Física e eixo horizontal preservados. Homologação manual desta câmera permanece pendente.
- Validação: 108 testes iniciais e **110 finais passaram**, Python 3.12.10/Pygame 2.6.1 com SDL dummy; ponto de entrada ficou ativo por 2 s sem erro. Duas regressões novas verificam câmera e renderização do portão. Medidas iguais para ambos: salto básico de 114 px/38 quadros, alcance de 113 px do repouso, aceleração até 3,2 px/quadro em 5 quadros e frenagem em 4 quadros/4 px.
- Notas provisórias do conteúdo entregue: 6,80 → 7,08. Não representam homologação de sobrevivência, áudio, ritmo ou diversão. Permanecem repetição de fundos, área inferior em grade pouco expressiva, decoração potencialmente confundida com apoios e arte esquemática do Indexador. Próximo ciclo: partida manual com ambos e revisão de marcos regionais.
- A etapa 11 continua aberta; fases 3–6 não foram implementadas por esta avaliação.

### Ajustes após revisão do responsável — 09/11/2026

- Aula: dois colegas espaçados, ao lado dos monitores e voltados às telas, sem linhas/círculos de hipnose. Olhos alterados preservam a narrativa. Colegas decorativos removidos do fundo repetido da arena virtual.
- Pátio: piso lógico em Y=440, abaixo dos bancos/mureta, em vez de Y=352. Spawn acompanha esse piso. Porta A28 reposicionada em X=1728, com soleira no piso e parede própria no bloco final; área de interação e dica acompanham a nova posição. Laboratórios e mapas virtuais mantêm seus pisos anteriores.
- Chefes: removidos textos de ataque/recuperação, mira, seta de investida e sons auxiliares de aviso de RomerBug/SpeedBug. Indexador não desenha faixas durante preparação; o efeito visual existe somente durante a janela real de dano (quadros 48–59). Padrões, preparação corporal, projéteis e temporizadores preservados.
- Capturas Pygame inspecionadas em `avaliacao/visual/revisao_composicao/`, incluindo aula, pátio, porta e preparação dos dois chefes. Testes automatizados cobrem ausência de marcas fora dos sprites durante preparação e piso/porta alinhados; partida manual permanece pendente.

- Resultado desta revisão: **112 testes passaram** em 5,490 s com SDL dummy. Capturas são offscreen; não houve homologação manual ou audição.

### Laboratório com profundidade 2.5D — 09/11/2026

- Substituída a disposição lateral por duas bancadas em planos diferentes, em escala 80%/100%, com tampos trapezoidais, faces, pernas e sombras. Aplicação na aula e A28; a arena virtual preserva os blocos de plataforma.
- Colegas agora usam desenho próprio sentado de costas, centralizado no respectivo monitor, com mãos no teclado, encosto e base da cadeira. A hipnose aparece na inclinação da cabeça e reflexo frio, sem olhos desenhados na nuca, raios ou círculos.
- Fundo dos laboratórios recuado verticalmente em 32 px com continuação inferior do piso para apoiar visualmente a bancada distante. Colisões e faixa de movimento preservadas. Terminais continuam recortados dentro dos novos monitores e sucção usa um desses monitores.
- Capturas reais em `avaliacao/visual/revisao_profundidade/`: aula, hipnose, A28 e sucção inspecionadas offscreen. Validação manual de apresentação permanece pendente.

## Reorganização do repositório — 10/11/2026

- Mapeamento prévio de 421 arquivos rastreados (hashes, importações e referências), carregamentos dinâmicos, registros de chefes, dados, fontes, sons e ferramentas. [Relatório](REORGANIZACAO.md), [inventário anterior](inventario_antes.json), [movimentos](arquivos_movidos.json), [uso observado das imagens](uso_recursos.json).
- `principal.py` é o único Python da aplicação na raiz. Cinco módulos centrais movidos para `sistema/`; dez ferramentas de arte e dois scripts de avaliação para `ferramentas/`; sete documentos para `documentacao/`; dependências para `configuracao/`. Pastas de entidades/mundo/interface preservadas. `AGENTS.md` e `.gitignore` ficam na raiz por descoberta/convenção. Imports, documentação, links e comandos dos registros JSON atualizados.
- 68 capturas duplicadas exatas consolidadas, economizando 23.550.148 bytes sem apagar frames distintos; links redirecionados. [Mapa das cópias preservadas](capturas_consolidadas.json). Materiais históricos e campanha antiga preservados por uso documentado em testes/regeneração. Imagem local `referencia/img.png` intacta e não rastreada.
- Validação: 112 testes antes; **114 testes depois**, incluindo ponto de entrada pela raiz e por diretório externo e recursos carregados fora da raiz sem placeholders. 34 capturas reproduzidas byte a byte, métricas de movimento iguais, 87 imagens de execução carregadas e hashes de 195 binários de arte/referência preservados. Nove exportadores Pygame conferidos em cópia temporária (77 PNGs distintos); ferramenta reproduzível `python -m ferramentas.verificar_exportadores`.
- Gerador original preservado e caminho atualizado, mas não executado porque Pillow está ausente. Validação offscreen, sem nova homologação manual; etapa 11 permanece aberta. Nenhum commit/publicação feito nesta reorganização.

## Entradas de ataque e animação durante carga — 10/11/2026

- K e botão esquerdo do mouse adicionados como alternativas a X, incluindo carga e golpe na soltura. A entrada inicial possui a carga; outras teclas/cliques não a reiniciam nem disparam ao serem soltos.
- Corrigida a animação congelada ao andar carregando: a pose fixa de preparação agora só aparece parado no chão; caminhada e salto continuam durante a carga. Velocidade de 75% e física preservadas.
- Tutorial, HUD e tabela de controles atualizados. Regressões verificam dano rápido/carregado das três entradas, combinação de comandos, caminhada/salto dos dois protagonistas, pausa/foco e bloqueio de botão direito/repetição/arma indisponível.
- Validação: **119 testes passaram** com SDL dummy (9,036 s). Sem homologação manual nesta revisão; nenhum commit criado.

## Sprites de carga, efeito de energia e retratos — 10/11/2026

- Criado atlas transparente com ferramenta `image_gen` integrada, preservando fontes anteriores. Oito quadros por protagonista em postura de carga, braço preparado e mouse preso ao cabo. Fonte e prompt em `recursos/fontes_arte/caminhada_carregando.png` e `instrucoes_caminhada_carregando.json`.
- Exportador `ferramentas/preparar_caminhada_carregando.py`: 16 PNGs em 40 × 40, conferidos em pasta temporária antes de integrar. Carregamento separado preserva a normalização dos sprites existentes; caminhada usa distância real e direção. Postura de carga mantida parado e no salto.
- GIF indicado pelo responsável baixado e inspecionado por quadros. Substituído mouse girando/barra sobre a cabeça por partículas de energia convergentes e pulso local na carga completa. Relógio visual próprio continua após saturação da carga; colisões, velocidade de carga, dano e comandos X/K/botão esquerdo preservados.
- `interface/retratos.py`: recortes dos sprites aprovados, com cache por identidade/aparência; Sistema usa terminal, Indexador sua figura real. A caixa troca retrato a cada fala e ajusta altura para acomodar o texto completo. Falantes antigos sem sprite próprio usam busto neutro. Não houve nova arte de rosto.
- Validação: **124 testes passaram** com SDL dummy (9,482 s), incluindo cinco regressões de sprites/energia/retratos/texto longo. Capturas Pygame de ambos carregando e retratos em `avaliacao/carga_dialogos/`, com `previa_carga.gif` de 72 atualizações. Inspeção visual offscreen; não houve partida manual. Estado local do incremento anterior mantido; nenhum commit criado.

## HUD de conversa inspirado nas referências — 10/11/2026

- Ambas as URLs fornecidas foram baixadas e inspecionadas: composição com bustos grandes e ouvinte escurecido; moldura azul clara e placa de nome. As imagens de referência não foram incorporadas ao jogo.
- Seis bustos originais gerados com `image_gen` integrada (Menino, Menina, Max, Romerito, entidade e Indexador), preservando identidades e roupas. Fontes transparentes em 1024 × 1536 em `recursos/fontes_arte/retratos_dialogo/`, prompts e proveniência em `instrucoes_retratos_dialogo.json`. Exportador `ferramentas/preparar_retratos_dialogo.py`: seis ilustrações + ícone de Sistema em 768 × 1152. Conferência em pasta temporária antes de integrar.
- `interface/quadro_dialogo.py`: moldura azul, filetes, sombra, bustos grandes e escurecimento do ouvinte com cache; `interface/dialogo.py` mantém texto completo e regras de entrada, adicionando placa de nome conforme o lado do falante. `interface/retratos.py` carrega PNGs HD sem normalização para o corpo de combate. Monitor ampliado da abertura reposicionado ao centro para não ser encoberto.
- Validação: **127 testes passaram** (9,623 s), incluindo resolução/transparência real, destaque sem mutar fonte e alternância de interlocutores. Todos os 11 exportadores Pygame passaram em cópia temporária, produzindo 100 PNGs distintos. Capturas reais em `avaliacao/dialogos_hd/`, com abertura de ambos os protagonistas e falantes da campanha.
- Limites: renderização offscreen em 960 × 540, sem partida manual. Fontes anteriores, controles, física e alterações locais do incremento anterior preservados. Nenhum commit criado.
