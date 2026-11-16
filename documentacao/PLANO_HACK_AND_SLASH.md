# IFVania — Plano de implementação do hack and slash

**Data:** 16/11/2026. **Estado:** planejamento; nenhuma etapa de implementação concluída por este documento.

Design: [PROPOSTA_HACK_AND_SLASH.md](PROPOSTA_HACK_AND_SLASH.md). Registro geral: [PLANO_DE_EXECUCAO.md](PLANO_DE_EXECUCAO.md).

## 1. Objetivo e organização

Entregar uma campanha de seis fases conectada por um campus virtual controlável, com combate de combos, inimigos reativos e quatro novos chefes docentes. Prioridade: validar cedo o ciclo campus → entrada → fase → chefe → campus transformado → próxima entrada.

Este plano orienta o novo trabalho de evolução. As etapas antigas e seus registros continuam documentando o que existe; não devem ser marcadas retroativamente como concluídas por equivalência. As pendências de abertura, biblioteca e homologação continuam abertas. O novo plano altera o conteúdo futuro das antigas etapas 7–10 e amplia a infraestrutura prevista na etapa 5; a validação final continua sendo a última entrega.

Não há estimativa de calendário sem medir o primeiro protótipo. Executar em incrementos jogáveis, registrar evidências e só ampliar arte/conteúdo após verificar a base.

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

- [ ] Executar suíte completa e registrar ambiente/resultado atual, sem reutilizar contagem histórica como resultado novo.
- [ ] Percorrer abertura, RomerBug e biblioteca quando houver ambiente de jogo; registrar separadamente o que não pôde ser experimentado.
- [ ] Confirmar pontos de alteração de progressão, morte, entradas, dano e carregamento de habilidades.
- [ ] Mapear fábricas, estratégias e estados já existentes; definir evolução incremental para os padrões obrigatórios, reaproveitando estruturas adequadas.
- [ ] Registrar matriz inicial de arquitetura, transições globais/locais e responsabilidades de comandos/eventos, com cobertura prevista por marco.
- [ ] Registrar casos obrigatórios de regressão e alinhar roteiro/requisitos com a migração futura, identificando o que ainda não existe.

**Aceite:** base técnica conhecida; limitações manuais explícitas; campanha antiga continua isolada. Não bloquear protótipo por falta de arte final ou por pendências visuais independentes.

### H1 — Campus mínimo e progresso de sessão

**Dependências:** H0. **Entrega:** biblioteca → convivência → portão do ginásio; saída de fase com retorno espacial.

- [ ] Implementar `ProgressoCampanha`, setores, portas, requisitos e pontos de retorno.
- [ ] Introduzir fábrica de cenas/setores, State Machine explícita da aplicação e eventos locais de objetivo; garantir entrega/remoção de observadores e progresso antes da navegação.
- [ ] Fazer saída da biblioteca retornar ao campus, removendo fim provisório apenas quando houver continuação utilizável no incremento.
- [ ] Criar dois setores com colisões simples e arte reutilizada, sem acionar gatilhos escolares do prólogo.
- [ ] Separar troca de setor, entrada em fase e retomada; conservar identidade e limpar entradas/ameaças.
- [ ] Mostrar destino fechado, requisito e indicação espacial de forma compreensível.
- [ ] Criar acesso de desenvolvimento ao ponto inicial do protótipo por ferramenta de teste, sem adicionar atalhos de campanha ao menu final.

**Verificação automática:** portas condicionadas, surgimento seguro, ausência de transição dupla, identidade/habilidades, conclusão idempotente e nova campanha limpa.

**Aceite manual:** caminhar da biblioteca ao ginásio, voltar e reconhecer os espaços; nenhuma cura involuntária por alternar setor. Porta da próxima fase só passa a entrar de fato quando H3 entregar conteúdo.

### H2 — Combate terrestre e dois papéis de inimigo

**Dependências:** H0; integrar em H1 antes de H3. **Entrega:** combo de três golpes, esquiva e inimigos que reagem.

- [ ] Implementar janela de continuação, memória de ataque e escolha entre toque/carga.
- [ ] Implementar Command para intenções de entrada e State Machine de combate, preservando soltura, origem e prioridades dos comandos.
- [ ] Criar inimigos pela Factory e separar escolha de ação por Strategy de execução dos estados; validar tipos/configurações desconhecidos.
- [ ] Diferenciar rápido, alcance e varredura; terceiro golpe empurra em vez de apenas inflar dano.
- [ ] Preservar entrada proprietária da carga, bloqueio por parede e acerto único por golpe/alvo.
- [ ] Aplicar recuo/interrupção nos leves, respeitando paredes e bordas.
- [ ] Criar leve corpo a corpo e lançador com preparação, janela ativa e recuperação.
- [ ] Remover dano de contato passivo desses tipos apenas quando seus ataques estiverem funcionais.
- [ ] Definir prioridade de dano, esquiva, carga e recuperação; limpar sequência em pausa/foco/transição.
- [ ] Usar animação provisória legível e sons existentes antes de produzir atlas final.

**Verificação automática:** sequência/expiração, carregado fora do combo, teclas alternativas e simultâneas, acerto por golpe, colisões no recuo, interrupção do inimigo e congelamento de temporizadores.

**Aceite manual:** jogador distingue os três golpes e consegue optar por recuar; repetir ataque não mantém todos os alvos travados. Comparar primeiro par de inimigos com e sem finalizador.

### H3 — Protótipo completo da fase 3

**Dependências:** H1 e H2. **Entrega:** sessão de 10–15 minutos do pós-biblioteca à entrada M1.

- [ ] Criar recorte do ginásio com uma trava persistente, trecho de salto duplo e dois tipos de bug.
- [ ] Implementar `EliasGuardiaoCompasso` em módulo próprio e registrar o novo tipo de chefe.
- [ ] Instanciar Elias pela Factory e modelar preparação/ataque/recuperação/derrota como estados; integrar eventos de vitória sem callbacks duplicados ao revisitar.
- [ ] Atualizar matriz de arquitetura com módulos, símbolos e evidências dos cinco padrões no protótipo; verificar dependências explícitas das cenas.
- [ ] Implementar sequência de dois ataques, investida e bola, com poses antecipatórias e recuperações diferentes.
- [ ] Vitória limpa ameaças, restaura Elias, registra progresso e devolve à soleira do ginásio.
- [ ] Campus interrompe sinal repetido, mostra estudantes em segurança e abre caminho ao M1.
- [ ] Disponibilizar retomada no ginásio conservando trava; permitir caminhar até M1 e encerrar protótipo com mensagem clara de conteúdo disponível.
- [ ] Produzir capturas dos estados antes/depois e registrar partida manual.

**Verificação automática:** chefe concreto, preparação sem dano precoce, derrota/vitória sem projéteis residuais, trava preservada, mudança do campus, bloqueio pré-vitória e caminho pós-vitória.

**Aceite manual:** sem instrução verbal externa, identificar ginásio e M1; reconhecer ataques e aberturas; perceber por que vencer mudou a escola. Registrar mortes, locais de desorientação e comandos frustrados.

### H4 — Refinar protótipo e completar Recreio em repetição

**Dependências:** H3. **Entrega:** fase 3 completa e base de combate pronta para expansão.

- [ ] Ajustar janelas, quantidade de inimigos, alcance, recarga e duração do chefe conforme evidências.
- [ ] Completar três travas, arquibancadas, circuito de treino e rota segura dos estudantes.
- [ ] Integrar fala da IFVania em ponto seguro e contato de Max ao sair.
- [ ] Completar jardim, reunião e atalho A28; dar resposta visual a cada trava.
- [ ] Refinar poses e sons do encontro, preservando leitura mesmo sem áudio.
- [ ] Experimentar ambos os protagonistas e reprovar o marco se controles/orientação ainda falharem, mesmo com testes aprovados.

**Aceite:** combo, defesa e travessia compreensíveis; resgate sem escolta frágil; retorno repetido não recria bloqueios; arte final somente após validação da geometria.

### H5 — Laboratório das cópias, combate aéreo e ancoragem

**Dependências:** H4. **Entrega:** fase 4 e caminho controlável M1 → M5.

- [ ] Implementar laçada, golpe aéreo e descendente com pouso comprometido.
- [ ] Resolver modificadores de direção/salto no input e atualizar tutorial; impedir restauração infinita de salto e sequências aéreas.
- [ ] Estender comandos e estados para combate aéreo/ancoragem, mantendo arbitragem única entre interação e conector; não criar caminhos de entrada paralelos.
- [ ] Criar guarda frontal e cópias repetidoras com respostas distintas.
- [ ] Construir comparação de arquivos e atalhos por sala estabilizada.
- [ ] Implementar `MaxEmLoop`, cópia verdadeira conectada, varredura, bugs e recompilação vulnerável.
- [ ] Integrar revelações de autoria/autopreservação e confissão, sem monólogo longo.
- [ ] Liberar ancoragem depois da vitória, ensinar em piso seguro e construir travessia até M5.
- [ ] Preservar arquivos comparados na retomada; remover duplicações do campus e isolar pendrive com Max.

**Verificação automática:** limite de lançamento, não restauração de salto, guarda/flanco/carregado, origem verdadeira, tutorial antes do bloqueio obrigatório, prioridade E, conectores elegíveis e retorno seguro de queda.

**Aceite manual:** distinguir cópias e apoios; executar aéreo sem conflito recorrente de salto; aprender ancoragem antes de depender dela. O chefe pode ser vencido sem lançar seu corpo.

### H6 — Rede sem saída e isolamento visível

**Dependências:** H5. **Entrega:** fase 5 e percurso M5 → LIT.

- [ ] Construir três ramais, conectores, esperas seguras e retornos curtos.
- [ ] Implementar retransmissor e composição guarda/atirador sem sobrepor ameaças inevitáveis.
- [ ] Cada isolamento apaga monitores e persiste em queda, morte e revisita.
- [ ] Implementar `AlessandroSentinelaEnlaces`, barreira, portas sequenciais, varredura e oportunidades frontais/laterais.
- [ ] Permitir solução por espera ou flanco; não exigir ancoragem em uma janela única de precisão.
- [ ] Mostrar aliados reunidos, rede isolada e nobreak ativo; abrir caminho controlável ao LIT.

**Verificação automática:** três isolamentos independentes, não migração narrativa prematura, barreira/janelas, seleção de conector, invariantes da retomada e porta final condicionada.

**Aceite manual:** reconhecer efeito de cada corte; compreender prioridade do retransmissor e descobrir ao menos uma solução segura do chefe; queda não exige repetir ramais.

### H7 — A última chamada e epílogo

**Dependências:** H6. **Entrega:** fase 6, retorno final pelo campus e conclusão definitiva.

- [ ] Construir oficina, memória e núcleo com três desafios curtos de síntese.
- [ ] Implementar `FranciscoGuardiaoContinuidade` com vida compartilhada entre proteção automática e ocupação da estrutura pela IFVania.
- [ ] Transição liberta Francisco e o move à função de aliado sem duplicar vida, dano ou chefe.
- [ ] Usar padrões já ensinados, alternando grupo, pulso e abertura; preservar rota segura.
- [ ] Encerrar ameaças, devolver jogador à soleira LIT e liberar caminhada tranquila até A28.
- [ ] Terminal final exige resgate concluído, rede isolada e autopreservação encerrada.
- [ ] Encenação de desligamento incluindo nobreak, pendrive isolado, escola física e epílogo da tarefa refeita.

**Verificação automática:** transição única, reserva compartilhada, pausa/diálogo sem dano, condições finais, confirmação idempotente, preservação de nome/aparência e nova partida sem herança.

**Aceite manual:** nenhuma regra indispensável nova no final; Francisco é reconhecível como liberto; caminhada final mostra consequências; vitória sem surpresa, ameaça residual ou ambiguidade de IA sobrevivente.

### H8 — Integrar as duas primeiras fases e finalizar apresentação

**Dependências:** H7 para integração final; melhorias independentes podem ocorrer após H4. **Entrega:** campanha completa sem costuras de tutorial ou progressão.

- [ ] Ensinar combo básico na descoberta do mouse, sem exigir todas as técnicas avançadas imediatamente.
- [ ] Integrar retorno fase 1 → campus → biblioteca e preservar recompensa nula de RomerBug.
- [ ] Ajustar vida/invulnerabilidade de alvos iniciais ao combo sem descaracterizar os padrões de RomerBug/SpeedBug.
- [ ] Completar bugs de arquivo, atalhos por consulta e bilhete opcional da biblioteca.
- [ ] Revisar animação da bolsa e continuidade do reencontro; manter demais pendências antigas rastreáveis.
- [ ] Produzir recursos finais, variações corrompida/restaurada, retratos e áudio; preservar fontes e exportar em temporário.
- [ ] Revisar câmera, contraste, interações E, placas, escala e limites das áreas de combate.
- [ ] Sincronizar LEIA_ME, requisitos, roteiro, fontes e plano com o comportamento realmente entregue.

**Aceite:** primeira partida apresenta controles em ordem compreensível; campus conecta todas as seis fases; nova apresentação não muda colisões acidentalmente.

### H9 — Validação final e homologação da campanha

**Dependências:** H0–H8 entregues. **Entrega:** evidências técnicas e experiência manual homologada; corresponde à validação final da etapa 11 do plano geral.

- [ ] Executar suíte completa e critérios integrados, incluindo campanha antiga isolada.
- [ ] Auditar Factory, State Machine, Command, Strategy e Observer conforme matriz de arquitetura: uso real, responsabilidades, transições, cancelamento de entrada e ciclo de vida dos observadores.
- [ ] Executar exportadores pertinentes em temporário e conferir transparência, pés, quadros e tamanho.
- [ ] Percorrer seis fases e todas as travessias com ambos os protagonistas.
- [ ] Experimentar morte, queda, revisita, pausa, foco, diálogo e transição em cada sistema novo.
- [ ] Avaliar áudio, resposta dos controles, ritmo, orientação, sobrevivência, desempenho e leitura das arenas.
- [ ] Registrar problemas restantes com reprodução e prioridade; corrigir bloqueadores e repetir somente verificações afetadas.
- [ ] Confirmar desfecho e limpeza de progresso ao iniciar outra campanha.

**Aceite:** suíte aprovada e percurso manual completo sem bloqueadores; evidências automáticas, capturas e experiência humana identificadas separadamente. Capturas offscreen não homologam diversão, dificuldade ou áudio.

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
- [x] Padrões obrigatórios definidos com aplicação, marcos de introdução e critérios comportamentais de aceite; implementação pendente.
- [ ] H0 iniciado.
- [ ] Primeiro protótipo entregue e experimentado.
- [ ] Campanha completa e homologada.

**Próxima ação de implementação:** H0, seguido de H1 e H2 para construir H3. Este pedido entrega somente documentação e plano, sem iniciar alterações no jogo, gerar artes, criar commits ou publicar.
