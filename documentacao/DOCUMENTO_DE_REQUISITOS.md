# Documento de Requisitos — IFVania

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


## Comportamento vigente — fechamento de 16/11/2026

Q segurado oferece bloqueio frontal após descobrir o mouse, com resistência limitada e quebra de guarda; costas e perigos ambientais exigem reposicionamento/esquiva. A guarda reduz movimento e não permite ataque simultâneo. M alterna áudio também na pausa. Pausa, foco e transições cancelam guarda e cargas.

SpeedBug considera deslocamento real, colisões e retorno dos limites, com reposicionamento entre ataques. As quatro fases novas incluem poses dedicadas, Max com origem móvel/invocações, ricochetes e portas sequenciais. Biblioteca oferece atalhos por consulta e bilhete; quedas nas novas travessias retornam ao apoio seguro com custo de uma integridade, mínimo um. Revisitas concluídas não reiniciam chefes nem curam. Desfecho inclui monitores/nobreak desligados, pendrive isolado, sala física e fachada iluminada.

Implementação técnica concluída; [revisão humana final](REVISAO_HUMANA_FINAL.md) documenta decisões e homologação adiada. Evidências: 172 testes e 15 exportadores em temporário (203 PNGs). Registros anteriores abaixo descrevem a evolução e cedem a esta atualização quando divergirem.


## Expansão integrada e correções — 16/11/2026

Esta revisão prevalece sobre descrições antigas de campanha limitada a duas fases. Há seis fases e campus controlável após cada uma, portas condicionadas, objetivos intermediários preservados na retomada e final que exige conclusão da campanha. Nova história limpa progresso e habilidades; não há salvamento em disco. Entrada em fase/retomada restaura integridade, troca de setor não; A28 é ponto seguro explícito.

Ataque continua na soltura: três golpes encadeados variam alcance/empurrão, carregado causa 2 de dano, cima modifica para ascendente e baixo no ar para descendente. Shift mantém esquiva; E prioriza interação e usa ancoragem em conectores elegíveis após Max. R retoma também as novas fases. Barras dos bugs surgem apenas após dano efetivo, duram 100 atualizações e renovam a cada acerto; clarão/recuo e impacto fatal comunicam o resultado. Pausa/diálogo congelam os efeitos.

Factory, State Machine, Command, Strategy e Observer são usados conforme a [matriz atual](ARQUITETURA_HACK_AND_SLASH.md). Novas artes são versões separadas; colisões comuns de 40 × 40 preservadas. Detalhes de escopo, testes e simplificações da primeira versão estão no [relatório](../avaliacao/hack_and_slash/RELATORIO.md). Novos retornos de avaliação humana foram adiados pelo usuário, sem bloquear implementação; isso não homologa balanceamento ou diversão.

## Incremento de infraestrutura — 16/11/2026

O jogo utiliza fábrica de cenas escolares/fases e registra, em memória, identificadores de chefes derrotados e fases concluídas por eventos locais síncronos. Conclusão é registrada antes de navegar; eventos repetidos não duplicam registros. Uma nova história inicia progresso vazio e remove as inscrições do progresso anterior. A criação de tipo de cena ou ambiente escolar desconhecido falha explicitamente.

Esse incremento não implementa salvamento em disco, campus navegável, combos ou novas recompensas. A campanha disponível e o encerramento após a biblioteca permanecem. Design futuro e critérios de migração estão em [PROPOSTA_HACK_AND_SLASH.md](PROPOSTA_HACK_AND_SLASH.md), [PLANO_HACK_AND_SLASH.md](PLANO_HACK_AND_SLASH.md) e [ARQUITETURA_HACK_AND_SLASH.md](ARQUITETURA_HACK_AND_SLASH.md). Os padrões ainda pendentes não são considerados implementados por esta atualização.

**Título do projeto:** IFVania

**Versão do documento:** 3.4

**Data:** 02/11/2026

**Fontes:** `documentacao/ROTEIRO_HISTORIA.md`, orientações do responsável pelo projeto e referências técnicas do repositório.

## 1. Objetivo e alcance do documento

Especificar o comportamento esperado do jogo com base no HistoryBoard, incluindo narrativa, apresentação, combate e critérios de aceite. Esta revisão substitui a descrição anterior centrada no vírus CODIGO.EXE e na campanha obrigatória de seis professores de linguagens de programação.

O HistoryBoard é a referência narrativa desta versão. As solicitações complementares determinam tamanho uniforme para personagens e inimigos e uma classe própria para cada boss. Os requisitos descrevem o produto desejado; sua presença neste documento não significa que estejam implementados ou homologados.

O roteiro revisado em 02/11/2026 define uma campanha de seis fases, incluindo resgate, isolamento da rede e desligamento da IFVania. A expansão está planejada, ainda não implementada. Os requisitos RF-01 a RF-34 e os critérios CA-01 a CA-10 continuam descrevendo a entrega jogável da primeira fase; a expansão deverá receber critérios próprios antes da implementação. Recursos antigos não definem automaticamente o escopo da nova campanha.

As etapas 1 a 4 do `documentacao/PLANO_DE_EXECUCAO.md` estão implementadas: menu, seleção, prólogo escolar, percurso virtual com salto básico, reencontro com Romerito humano, infecção, combate RomerBug/SpeedBug e encerramento do conteúdo disponível. A campanha antiga foi isolada, e o fluxo atual não concede recompensas ou anuncia a escola salva. Foram executados 95 testes automatizados e inspeções visuais. A revisão visual de 25/10/2026 acrescenta menus noturnos, HUD de integridade, arena escolar escura e a cena com a entidade. A revisão autorizada implementa chicote carregado, esquiva, controle com aceleração curta, plataformas destacadas e aviões/medalhas alternados com investida, conforme `documentacao/PROPOSTA_CHEFE_ROMERBUG.md`. O mapa escolar é uma adaptação sem planta interna homologada; a etapa 11 e a homologação manual permanecem pendentes. Testes controlados de combate não equivalem à validação do equilíbrio de sobrevivência.

## 2. Visão geral do produto

IFVania é um jogo local de plataforma 2D, para um jogador, desenvolvido em Python e Pygame, com visual em pixel art e ambientação escolar e virtual.

Na narrativa revisada, o protagonista leva à aula de programação orientada a objetos uma tarefa produzida por IA sem conferir o código. Uma oscilação de energia na noite anterior desencadeou a rotina que dá origem à IFVania — Inteligência Federal Virtual de Aprendizagem Neural e Inteligência Artificial. Esse passado é apresentado na conversa inicial com Max e retomado durante a campanha, sem narrador na introdução. Ao executar a tarefa na escola, o programa se manifesta; o anúncio de desligamento provoca sua revolta e o controle dos computadores e das pessoas.

A sessão de autoria preserva parte da autonomia do protagonista, sem imunidade ao dano. O mundo virtual é uma alucinação compartilhada sobre a escola. A jornada passa por A28, biblioteca, pátio/quadra, laboratório de manutenção, sala de rede e núcleo da IFVania. Libertar pessoas, impedir a recriação e migração dos processos e romper a autopreservação permite que os aliados desliguem os equipamentos afetados, incluindo a alimentação de reserva. O roteiro detalha a sequência planejada; o executável agora inclui a biblioteca e encerra após a segunda fase.

### 2.1 Escopo definido

- Menu com a fachada da escola e opções Jogar e Sair.
- Escolha entre Menino e Menina antes da campanha.
- Introdução com professor Max e a revolta da IFVania.
- Exploração dos corredores e encontro com Romerito no laboratório A28.
- Transporte para o mundo virtual e combate com mouse com fio usado como chicote.
- Encontro final com Romerito, transformação em RomerBug e, a 50% da vida, em SpeedBug.
- Uniformidade de tamanho entre personagens, inimigos comuns e bosses.
- Classe específica para cada boss, com reaproveitamento de uma base comum.
- Movimento, salto, colisão, vida, dano, diálogos, câmera, HUD, pausa e derrota como infraestrutura de jogo.

### 2.2 Expansão narrativa e implementação incremental

As fases 2 a 6 estão detalhadas no `documentacao/ROTEIRO_HISTORIA.md`: Biblioteca dos arquivos perdidos, Recreio em repetição, Laboratório das cópias, Rede sem saída e A última chamada. Incluem os chefes Indexador, Inspetor de Intervalo, Max em Loop, Roteador Sentinela e IFVania; salto duplo na fase 2 e cabo de ancoragem após o encontro da fase 4. Romerito não concede poder na fase 1. O final prevê libertação das sessões, isolamento da rede e desligamento pela equipe aliada, seguido de epílogo.

A entidade de RomerBug passa a ser identificada, na fase 4 planejada, como manifestação da autopreservação da IFVania. A expansão não reincorpora automaticamente a campanha antiga de Scratch, Python, Java, C, SQL e Assembly. Mapas, artes, comandos da ancoragem, retomadas, parâmetros de combate e critérios de aceite da expansão ainda precisam ser especificados e validados.

Salvamento persistente, multiplayer, serviços de rede, ranking, suporte a controle e menu de configurações continuam fora do escopo definido.

## 3. Atores, personagens e ambiente

| Tipo | Elemento | Papel |
|---|---|---|
| Ator externo | Jogador | Escolher o protagonista, explorar, combater e acompanhar a história. |
| Ator externo | Mantenedor / desenvolvedor | Implementar e validar mapas, entidades, diálogos e recursos visuais. |
| Personagem | Aluno / aluna | Protagonista parcialmente resistente aos efeitos da IFVania. |
| Personagem | Professor Max | Apresentar a IA e anunciar seu desligamento na introdução. |
| Antagonista | IFVania | Controlar os computadores, hipnotizar as pessoas e provocar alucinações. |
| Personagem / boss | Professor Romerito / RomerBug / SpeedBug | Participar do encontro no A28 e do combate final da primeira fase. |

| Item técnico | Referência do projeto |
|---|---|
| Linguagem e biblioteca | Python e Pygame; dependências em `configuracao/dependencias.txt`. |
| Execução | Local, por `python principal.py`, pela raiz ou informando o caminho absoluto do arquivo a partir de outro diretório. |
| Entrada | Teclado; interação por clique no fluxo de seleção descrito no HistoryBoard. |
| Janela de referência | 960 × 540 pixels. |
| Taxa-alvo | 60 FPS, sujeita a validação em hardware definido. |
| Unidade de cenário atual | Blocos de 32 × 32 pixels. |
| Recursos | Imagens e spritesheets locais; Pillow é opcional para geração por script. |

## 4. Requisitos funcionais

Os critérios abaixo são verificações propostas para aceite, não resultados de testes. Os identificadores da versão 2.0 correspondem à nova especificação e não preservam o significado dos identificadores da versão 1.0.

### 4.1 Menu, seleção e introdução

| ID | Requisito | Critério de aceite |
|---|---|---|
| RF-01 | Exibir menu inicial com fachada da escola em pixel art baseada em `referencia/fachada_escola.png`. | A abertura apresenta a fachada e as opções visíveis Jogar e Sair. |
| RF-02 | Permitir iniciar o fluxo por Jogar e encerrar por Sair. | Clicar em Jogar abre a escolha de personagem; clicar em Sair encerra a aplicação. |
| RF-03 | Exibir as opções Menino e Menina antes de iniciar a história. | As duas opções podem ser selecionadas; a campanha só começa após a escolha. |
| RF-04 | Usar `recursos/fontes_arte/aluno_ifrn_caico.png` como referência do Menino. | O protagonista masculino mantém a identidade visual da referência nas animações do jogo. |
| RF-05 | Disponibilizar spritesheet completo da Menina baseado no Menino, com características femininas. | A Menina possui quadros para todos os estados usados pelo protagonista, inclusive ataque com chicote, sem quadros ausentes ou troca para sprites do Menino. |
| RF-06 | Manter a escolha do protagonista durante a campanha. | Diálogos e transições preservam a aparência escolhida; Menino e Menina têm os mesmos controles e capacidades. |
| RF-07 | Apresentar a aula do professor Max e a IFVania antes da exploração. | O aluno inicia uma conversa com Max, sem narrador. Todas as falas da introdução são entre os dois e identificam a aula de programação orientada a objetos, a origem da tarefa, o tema inteligência artificial e o nome completo da IFVania. |
| RF-08 | Apresentar a revolta da IA e o objetivo do protagonista. | A sequência mostra ou relata o anúncio de desligamento, o controle dos computadores, a hipnose e as alucinações, a resistência parcial do protagonista e sua busca por ajuda para cortar a energia. |

### 4.2 Primeira fase e narrativa

| ID | Requisito | Critério de aceite |
|---|---|---|
| RF-09 | Permitir percorrer os corredores da escola em busca de ajuda e entrar no laboratório A28. | O percurso leva a um laboratório identificado como A28 e ao encontro com Romerito. |
| RF-10 | Apresentar Romerito com base em `referencia/professor_romerito.png`. | Sua representação é reconhecível em relação à referência e respeita o padrão visual do jogo. |
| RF-11 | Disparar o ataque e a abdução pela IFVania quando o protagonista tenta falar com Romerito no A28. | O evento conduz ambos ao mundo virtual e acontece uma única vez no fluxo da fase. |
| RF-12 | Mostrar a descoberta do mouse com fio na bolsa e seu uso como chicote. | A obtenção é apresentada antes do primeiro combate que exige a arma; o ataque exibe o mouse e o fio. |
| RF-13 | Disponibilizar bugs como inimigos comuns no mundo virtual. | O jogador encontra bugs que podem causar e receber dano e são removidos quando derrotados. |
| RF-14 | Apresentar o reencontro e a fala de Romerito ao final da fase. | Antes do combate, Romerito menciona suas viagens a Brasília, suas corridas e o desejo de nunca mais passar por aquilo. |
| RF-15 | Apresentar a infecção por um bug e a transformação de Romerito em RomerBug após a fala. | O combate com o boss só começa depois dessa sequência, sem antecipar ataques durante o diálogo. |
| RF-16 | Apresentar diálogos em português com identificação do falante. | O jogador consegue acompanhar e avançar as falas na ordem narrativa; a física e o combate ficam suspensos durante o diálogo; as informações dos monitores podem continuar animadas. |

### 4.3 Combate e boss da primeira fase

| ID | Requisito | Critério de aceite |
|---|---|---|
| RF-17 | Permitir movimento horizontal, salto e colisão com o cenário. | O protagonista percorre o caminho previsto sem atravessar pisos e paredes sólidos. A caminhada possui oito quadros por protagonista e acompanha a distância efetivamente percorrida, sem caminhar parado contra uma parede; a pose inicial é de repouso. |
| RF-18 | Permitir ataque com mouse-chicote na direção do protagonista. | A animação corresponde à direção do ataque e a área ativa causa dano aos inimigos atingidos. |
| RF-19 | Controlar vida, dano e derrota do protagonista. | Dano válido reduz a vida e atualiza o HUD; vida igual a zero apresenta derrota e permite retornar ao menu. |
| RF-20 | Fazer RomerBug alternar aviões de papel e investida. | Dois aviões com direção fixa e preparação corporal de 0,5 s, separados por 2,3 s. Depois, pausa mínima de 0,8 s até os projéteis saírem, preparação de investida de 0,8 s, avanço de até 160 pixels e recuperação de 1 s. |
| RF-21 | Transformar RomerBug em SpeedBug ao atingir metade da vida máxima ou menos. | A primeira redução que deixa a vida em até 50% dispara uma única cena: ajoelhar sobre uma perna, aparição de uma entidade com a fala “Ainda não terminou.”, metamorfose e levantamento como SpeedBug. Suspender o combate, permitir pausa e preservar posição, dimensões e vida restante, sem reiniciar o encontro. |
| RF-22 | Fazer SpeedBug lançar medalhas com pouco movimento, pausar e investir. | Duas medalhas separadas por 1,5 s, preparação corporal de 0,4 s, movimento a até 0,55 px/quadro limitado a ±24 pixels. Depois, pausa mínima de 0,8 s até os projéteis saírem, preparação corporal de investida de 0,6 s, avanço de até 160 pixels e recuperação de 1,3 s. Direção fixa, sem salto reativo ou dano corporal passivo. |
| RF-23 | Encerrar o combate quando a vida do boss chegar a zero. | Ataques, projéteis e bugs restantes são encerrados; a saída é liberada, sem recompensa. Alcançá-la conduz à biblioteca, preservando nome e aparência. O cartão “A jornada continua” é apresentado após o Indexador e informa que a IFVania permanece ativa. |
| RF-24 | Gerenciar zonas ofensivas e projéteis para evitar dano indevido. | Limpar ataques e zonas na transformação e derrota; suspender temporizadores na pausa e no diálogo. Aviões e medalhas expiram, colidem com o cenário e são removidos na transformação/derrota; não sobrepor projéteis à investida. |

### 4.4 Apresentação e sessão

| ID | Requisito | Critério de aceite |
|---|---|---|
| RF-25 | Exibir vida do protagonista e, durante o combate, nome e vida do boss. | O HUD acompanha o dano e identifica a etapa RomerBug ou SpeedBug. |
| RF-26 | Acompanhar o protagonista com câmera limitada ao mapa. | O percurso e a arena permanecem visíveis sem revelar áreas externas aos limites previstos. |
| RF-27 | Permitir pausar e retomar a jogabilidade. | A pausa suspende movimento, dano, projéteis e temporizadores de combate; retomar conserva o estado. |
| RF-28 | Representar personagens e inimigos com tamanho uniforme e animações estáveis. | Menino, Menina, Max, Romerito, bugs, RomerBug e SpeedBug usam o padrão definido em RN-07, sem mudança de escala entre quadros ou formas. |
| RF-29 | Permitir encerrar a aplicação pelo fechamento da janela. | O evento de fechamento encerra a aplicação inclusive em menu, seleção, diálogo e pausa. |
| RF-30 | Exibir informações animadas nos monitores dos laboratórios, inclusive na arena virtual. | Texto, gráficos, indicadores e cursor mudam dentro da área interna dos monitores, acompanham a câmera e refletem a corrupção. A animação continua durante diálogos sem avançar física/combate e congela ao pausar. |

| RF-31 | Solicitar o nome do jogador após a escolha do personagem e antes da aula. | Aceitar nomes com acentos, limitar a 20 caracteres, rejeitar nome vazio, permitir apagar e voltar. O nome identifica as falas do aluno e é usado pelos professores nos diálogos personalizados. |

| RF-32 | Oferecer ataque carregado com mouse de cabo reforçado. | Carga de 0,6 s causa 2 de dano, golpe rápido causa 1; permitir andar a 75%, saltar e virar enquanto carrega. Dano ou transições cancelam carga sem ataque residual. |
| RF-33 | Oferecer esquiva básica com recarga e proteção curta. | Shift executa passo de 15 quadros com oito quadros centrais protegidos e recarga de 54 quadros. Cancela carga/recolhimento, mas não preparação/golpe ativo. |
| RF-34 | Distinguir plataformas sólidas do fundo decorativo. | Contorno, tampo claro e faixa só no topo exposto, sem mudar a geometria ou indicar apoios nas juntas internas. |

## 5. Regras de negócio

| ID | Regra |
|---|---|
| RN-01 | A sequência inicial é menu → escolha do personagem → entrada do nome → aula e revolta da IFVania → corredores → A28 → mundo virtual → reencontro com Romerito → RomerBug → SpeedBug. |
| RN-02 | A escolha entre Menino e Menina altera a representação do protagonista, mantendo as mesmas capacidades, vida inicial, dimensões e regras de combate. |
| RN-03 | O protagonista é parcialmente resistente à influência da IA; isso permite sua jornada, mas não concede imunidade a dano de combate. |
| RN-04 | O mouse com fio é a arma de combate da primeira fase e deve ser apresentado como encontrado na bolsa. |
| RN-05 | RomerBug e SpeedBug são duas formas do mesmo boss, com uma única reserva de vida. SpeedBug é ativado uma vez quando a vida restante chega a 50% ou menos da vida máxima. |
| RN-06 | Cada boss deve ter sua própria classe concreta, responsável por seus ataques, estados e transições. Uma classe base comum pode reunir vida, dano e infraestrutura compartilhada; trocar apenas nome, imagem ou parâmetros de uma classe genérica não satisfaz esta regra. RomerBug deve ter classe própria, e SpeedBug pode ser um estado dessa classe, pois representa sua transformação. Qualquer boss antigo mantido na campanha também deve possuir classe própria. |
| RN-07 | Todos os personagens e inimigos, incluindo bosses e suas transformações, devem adotar as mesmas dimensões lógicas de largura e altura, definidas em uma configuração central. Os sprites devem usar uma área normalizada comum, preservar proporções e seguir a escala de apresentação de RN-13, sem margens transparentes excessivas. Não há exceção nas dimensões lógicas dos bosses. O padrão técnico inicial é 40 × 40 pixels, centralizado em `configuracoes.TAMANHO_PERSONAGEM` e aplicado às entidades disponíveis; novos personagens devem seguir o mesmo contrato. |
| RN-08 | A padronização de tamanho deve valer para todos os quadros e direções. Os pés devem manter alinhamento com o chão, e as áreas de colisão corporal devem seguir o padrão comum sem variar com a animação. Armas, projéteis e efeitos podem se estender além do corpo e ter áreas próprias. |
| RN-09 | A transformação em SpeedBug preserva dimensões, alinhamento, posição, identidade e vida restante. A câmera aproxima e retorna apenas visualmente. A cena aguarda a leitura da fala da entidade, permite pausa, remove projéteis/ataques em andamento e oferece proteção breve na retomada. |
| RN-10 | Diálogos, seleção de personagem e pausa não podem permitir dano ou avanço de temporizadores de combate. |
| RN-11 | A derrota do boss da primeira fase não equivale à desativação da IFVania nem à vitória final. Após o diálogo e a saída, carregar a biblioteca. O fim do conteúdo disponível ocorre após a fase 2, com retorno ao menu. Não conceder poder, item ou aumento de vida nessa vitória. |
| RN-12 | A ordem antiga de seis professores, os poderes coletáveis e seus valores de balanceamento não são obrigatórios na nova campanha sem revisão narrativa. |
| RN-13 | Protagonista (Menino/Menina), bosses, professores como NPCs e entidade devem usar escala visual de 200% sobre a arte normalizada (80 × 80 pixels), durante toda a partida, incluindo ataque e transformação. A arte fica ancorada pelo centro dos pés. Bugs permanecem em 100% (40 × 40). O corpo lógico e as colisões permanecem em 40 × 40. |

| RN-14 | O nome acompanha o protagonista por toda a campanha e personaliza os diálogos sem modificar os textos compartilhados entre partidas. Espaços excedentes são normalizados. Ao iniciar outra campanha na mesma execução, o nome pode ser editado novamente; não há persistência em disco. |

| RN-15 | A esquiva básica é liberada com o mouse e não é recompensa de boss. Preservar vida inicial e a reserva única de RomerBug. O chicote causa no máximo um acerto por alvo por golpe e não atravessa paredes. Pausa/foco descartam carga e comandos pendentes. |

## 6. Conteúdo e referências visuais

| Elemento | Referência / conteúdo obrigatório |
|---|---|
| Fachada do menu | `referencia/fachada_escola.png`, adaptada para pixel art. |
| Menino | `recursos/fontes_arte/aluno_ifrn_caico.png`. |
| Menina | Spritesheet completo derivado da identidade visual do Menino, com características femininas e as mesmas dimensões. |
| Professor Max | `referencia/professor_max.png`. |
| Professor Romerito | `referencia/professor_romerito.png`. |
| Escola | Corredores e laboratório A28; usar a referência geográfica indicada no HistoryBoard como apoio à construção do mapa. |
| Mundo virtual | Bugs, combate com mouse-chicote e arena de RomerBug / SpeedBug. |
| RomerBug | Transformação de Romerito; aviões espaçados e investida. |
| SpeedBug | Segunda forma do mesmo boss; medalhas com pouco movimento, pausa e investida. |

O HistoryBoard fornece o [link de referência da escola no Google Maps](https://maps.app.goo.gl/UVNmd7iyYTM9kr3FA). A consulta não disponibilizou uma planta acessível. A [página oficial dos laboratórios do campus](https://portal.ifrn.edu.br/campus/caico/noticias/horarios-laboratorios-de-informatica/) confirma A28. O corredor implementado é uma adaptação lateral; as portas decorativas A25–A27 e as distâncias não representam localização real validada. A conferência geográfica detalhada permanece pendente, sem impedir a validação do fluxo narrativo.

## 7. Interfaces e controles

O menu deve aceitar clique em Jogar e Sair, e a seleção deve permitir escolher Menino ou Menina. A navegação por teclado pode complementar essas ações. Os controles atuais abaixo são referências para continuidade, sujeitos à adequação das novas telas.

| Ação | Controle de referência |
|---|---|
| Movimento horizontal | Setas esquerda/direita ou A/D. |
| Salto | Espaço, W ou seta para cima. |
| Mouse-chicote | Tocar/soltar X: 1 de dano; segurar por 0,6 s e soltar: 2 de dano. |
| Esquiva básica | Shift, após descobrir o mouse; recarga de 0,9 s. |
| Avançar diálogo | E, Enter ou Espaço. |
| Pausar / retomar | Esc durante a jogabilidade ou pausa. |
| Encerrar | Sair no menu ou fechar a janela. |

A interface deve informar os comandos efetivamente disponíveis. Dicas de dash, tiro, escudo e salto de parede só devem aparecer se essas habilidades forem incorporadas à nova campanha e estiverem disponíveis ao protagonista.

## 8. Requisitos não funcionais e restrições técnicas

| ID | Requisito | Verificação proposta |
|---|---|---|
| RNF-01 | Executar localmente em Python e Pygame, sem rede durante a campanha. | Instalar dependências e iniciar com recursos locais e sem conectividade. |
| RNF-02 | Usar a janela de referência de 960 × 540 pixels e taxa-alvo de 60 FPS. | Conferir configuração e medir fluidez no ambiente de homologação. |
| RNF-03 | Manter pixel art e identidade escolar sombria, com fachada noturna, laboratório reconhecível e interface escura legível. | Conferir proporções, superfícies de apoio distinguíveis, contraste dos textos e nitidez após escala. Não escurecer os personagens a ponto de ocultar ações ou ataques. |
| RNF-04 | Separar controle de estados, entidades, mundo, interface, configurações e recursos. | Revisar as responsabilidades dos módulos alterados. |
| RNF-05 | Compartilhar uma base de personagem e uma base de boss, mantendo uma classe concreta por boss. | Conferir herança e instanciação dos encontros conforme RN-06; comportamentos específicos devem residir na classe correspondente. |
| RNF-06 | Centralizar as dimensões comuns de personagens e inimigos. | Conferir que carregamento, desenho e colisões usam a configuração comum de RN-07 e RN-08, sem dimensões conflitantes nas subclasses. |
| RNF-07 | Reutilizar imagens em cache e permitir substituição dos arquivos de arte. | Verificar carregamento por caminho e tamanho, espelhamento e reinício após troca de imagens. |
| RNF-08 | Tratar imagens ausentes com substituto visual e aviso. | Conferir que um caminho ausente não impede a inicialização; substitutos não servem para homologação da arte final. |
| RNF-09 | Manter textos e instruções em português, legíveis na resolução de referência. | Conferir menu, seleção, diálogos e HUD, inclusive na transformação do boss. |

| RNF-10 | Usar português nos nomes de classes e variáveis próprias, incluindo constantes, parâmetros, atributos, testes e scripts de arte. | Conferir importações e referências, incluindo acesso dinâmico e herança. Preservar interfaces externas (Python/Pygame/unittest), nomes próprios e convenções matemáticas. Usar também arquivos e pastas com nomes em português e registrar as orientações em `AGENTS.md`. Preservar nomes técnicos de descoberta e atualizar importações, carregamento de recursos e documentação ao renomear. |

Não há metas homologadas de hardware mínimo, acessibilidade ou compatibilidade entre sistemas operacionais. A taxa-alvo não representa garantia de desempenho.

## 9. Fluxos e critérios de aceite integrado

### UC-01 — Iniciar a jornada

1. A aplicação exibe a fachada da escola com Jogar e Sair.
2. O jogador escolhe Jogar e seleciona Menino ou Menina.
3. A introdução apresenta Max, a IFVania e sua revolta.
4. O protagonista inicia a busca por ajuda nos corredores.
5. O jogador entra no A28 e tenta falar com Romerito.
6. Ocorrem o ataque e o transporte para o mundo virtual.
7. O protagonista encontra o mouse com fio na bolsa e passa a usá-lo como chicote.

**Resultado esperado:** início da exploração e dos combates virtuais com o personagem escolhido e sem saltos na sequência narrativa.

### UC-02 — Enfrentar RomerBug e SpeedBug

1. O protagonista enfrenta bugs até o reencontro com Romerito.
2. Romerito fala sobre viagens a Brasília, corridas e seu desejo de não repetir a experiência.
3. Um bug o infecta e ele se transforma em RomerBug.
4. RomerBug lança aviões espaçados, pausa e prepara uma investida.
5. Ao atingir até 50% da vida máxima, transforma-se uma única vez em SpeedBug.
6. SpeedBug lança medalhas com pouco deslocamento, pausa, prepara uma investida e fica exposto.
7. Ao chegar a zero de vida, o boss é derrotado e para de atacar.

**Resultado esperado:** encontro único, com vida contínua, tamanho uniforme e transição de comportamento no limiar especificado.

### 9.1 Roteiro de validação

| ID | Verificação | Requisitos relacionados |
|---|---|---|
| CA-01 | Conferir fachada e clicar em Jogar e Sair em sessões separadas. | RF-01, RF-02 |
| CA-02 | Iniciar uma campanha com cada opção e percorrer animações e transições, verificando identidade e capacidades equivalentes. | RF-03 a RF-06, RN-02 |
| CA-03 | Conferir aula, revolta da IA, objetivo, corredores, A28, abdução e obtenção do mouse, na ordem prevista. | RF-07 a RF-12, RN-01 |
| CA-04 | Exercitar movimento, salto, colisões, chicote, dano e derrota contra bugs. | RF-13, RF-17 a RF-19 |
| CA-05 | Conferir fala de Romerito e infecção antes de liberar ataques do boss. | RF-14 a RF-16 |
| CA-06 | Reduzir a vida do boss até acima de 50%, exatamente 50% e abaixo do limiar em execuções controladas; verificar aviões antes e medalhas depois, alternados com investida, sem cura ou transformação repetida. | RF-20 a RF-22, RN-05, RN-09 |
| CA-07 | Derrotar o boss e conferir encerramento de ataques e projéteis, sem declarar vitória final da campanha. | RF-23, RF-24, RN-11 |
| CA-08 | Comparar todos os personagens e inimigos lado a lado, na mesma escala de câmera; conferir dimensões lógicas, área dos sprites, escala visível e alinhamento em todos os quadros, incluindo SpeedBug. | RF-28, RN-07 a RN-09, RNF-06 |
| CA-09 | Revisar a classe e a instanciação de cada boss disponível, comprovando comportamento próprio e ausência de boss representado somente por parâmetros genéricos. | RN-06, RNF-05 |
| CA-10 | Pausar e avançar diálogos durante situações de combate, verificando suspensão da simulação; conferir HUD, câmera e fechamento da janela. | RF-16, RF-25 a RF-29, RN-10 |

## 10. Pendências e adequação da implementação

| ID | Ponto | Encaminhamento |
|---|---|---|
| P-01 | O documento anterior descrevia CODIGO.EXE e seis professores de linguagens. | Substituir as referências narrativas e revisar fases antigas antes de incorporá-las à campanha IFVania. |
| P-02 | A revisão narrativa de 02/11/2026 define seis fases e o epílogo; a primeira e um incremento da biblioteca estão implementados. | Especificar critérios de aceite da expansão, adaptar a introdução e a saída da fase 1 e implementar as fases 2 a 6 com tutoriais, retomadas e validação de dificuldade. |
| P-03 | A etapa 1 substituiu as dimensões distintas por um corpo comum de 40 × 40 pixels, com escala proporcional dos sprites e surgimento em piso livre. | Testes de geometria e combate passaram nas seis fases existentes; conferir novamente passagens, arenas e novos personagens durante a construção dos mapas escolares e a homologação manual. |
| P-04 | RomerBug e os outros cinco bosses existentes possuem classes concretas com estratégias próprias; a base `Chefe` exige escolha de ataque especializada. | A arquitetura foi validada por testes; a participação dos professores antigos na nova campanha continua sujeita à revisão narrativa. |
| P-05 | As etapas 1 a 4 foram integradas, incluindo a primeira fase sem recompensas antigas e o fim do conteúdo sem declarar a escola salva. Os testes cobrem percurso, narrativa, combate e encerramento. | Executar a etapa 11: homologação manual com ambos os protagonistas, revisão integrada de interface/controles e balanceamento. |
| P-06 | A28 foi conferido na referência oficial, mas o Maps não forneceu uma planta acessível. O corredor implementado é uma adaptação para o jogo. | Validar posições, medidas e conexões internas se houver exigência de reprodução geográfica fiel. |
| P-07 | Valores de vida, dano, velocidade, alcance e recarga não são definidos pelo HistoryBoard. | Usar os valores existentes como ponto de partida para balanceamento, sem tratá-los como decisões narrativas obrigatórias. |
| P-08 | O responsável pediu uma alternativa menos infantil para aviões e medalhas. A proposta é sobrecarga de terminais e investidas, documentada separadamente. | A troca foi autorizada e implementada em RF-20/RF-22, junto à carga e esquiva. A homologação manual de dificuldade continua pendente. |

## 11. Rastreabilidade técnica de referência

A tabela indica áreas de implementação e revisão, sem afirmar que os novos requisitos já estejam atendidos.

| Arquivo / área | Responsabilidade esperada |
|---|---|
| `documentacao/ROTEIRO_HISTORIA.md` | Fonte da narrativa, seis fases planejadas, progressão e epílogo; distingue conteúdo disponível e futuro. |
| `sistema/jogo.py` | Menu, escolha de personagem, introdução, pausa, derrota, transições e isolamento dos eventos entre telas. |
| `interface/interface_inicial.py` e `interface/tema.py` | Fachada noturna, botões, seleção, cores e painéis compartilhados. |
| `mundo/transicao_chefe.py` e `mundo/escola_sombria.py` | Transformação com a entidade, zoom visual e cenário escolar escuro. |
| `mundo/arte_escolar.py`, `mundo/terminal.py` e `ferramentas/preparar_escola_detalhada.py` | Ambientes detalhados, mobiliário e telas animadas com recorte próprio. |
| `mundo/escola.py` e `mundo/dados_escola.py` | Sala, corredor, A28, gatilhos únicos, ataque/abdução e falas de descoberta do mouse. |
| `entidades/professor.py` e `ferramentas/preparar_recursos_escola.py` | Professores Max e Romerito e exportação de suas artes a partir das referências. |
| `ferramentas/preparar_recursos_menu.py` | Exportação da fachada e dos onze quadros da Menina a partir das fontes geradas. |
| `sistema/configuracoes.py` | Dimensões comuns, resolução, taxa-alvo e balanceamento. |
| `entidades/personagem.py` | Estado, vida e infraestrutura compartilhada dos personagens. |
| `entidades/jogador.py` | Movimento, personagem escolhido, combate e animações. |
| `entidades/chicote_mouse.py` | Comportamento e apresentação do mouse-chicote. |
| `entidades/inimigo.py` | Bugs e sua adequação ao tamanho comum. |
| `entidades/chefe.py` | Infraestrutura comum dos bosses; revisar instanciações genéricas. |
| `entidades/chefes_professores.py` | Classes concretas dos professores antigos e registro explícito de tipos de boss. |
| `entidades/romer_bug.py` | Classe própria de RomerBug, transformação em SpeedBug, aviões, medalhas e investida. |
| `entidades/projetil.py` | Movimento, dano e ciclo de vida dos projéteis. |
| `mundo/fase.py` e `mundo/dados_fases.py` | Mapa virtual, reencontro, infecção, combate, limpeza após derrota e saída. |
| `mundo/fases_antigas.py` | Dados isolados dos seis mapas antigos e suas recompensas, fora do fluxo principal. |
| `mundo/mapa_blocos.py` e `mundo/camera.py` | Geometria, colisões e acompanhamento de câmera. |
| `interface/dialogo.py` e `interface/painel.py` | Falas, vida, identificação do boss e instruções. |
| `sistema/recursos.py`, `recursos/imagens/` e `recursos/fontes_arte/` | Carregamento, cache, spritesheets e padronização visual. |
| `referencia/` | Referências da fachada e dos professores. |

## 12. Glossário

| Termo | Significado |
|---|---|
| IFVania | Inteligência Federal Virtual de Aprendizagem Neural e Inteligência Artificial; antagonista da história. |
| Boss / chefe | Inimigo principal de um encontro, obrigatoriamente representado por classe própria. |
| RomerBug | Forma infectada de Romerito e primeira etapa do boss da fase 1. |
| SpeedBug | Transformação de RomerBug a partir de 50% da vida restante. |
| Mouse-chicote | Mouse com fio encontrado na bolsa e usado como arma. |
| Spritesheet | Conjunto de quadros de animação de uma entidade. |
| HUD | Interface sobreposta ao jogo com informações de vida e combate. |
| Dimensão lógica | Largura e altura corporais usadas no posicionamento e na colisão. |
| Pixel art | Estilo visual com pixels e contornos definidos. |


## 13. Incremento da biblioteca — 02/11/2026

Este registro atualiza o estado histórico de implementação descrito na seção 1.
A introdução e a continuação após RomerBug foram integradas; a campanha disponível
contém duas fases. As fases 3 a 6 seguem planejadas. A etapa final de validação é
agora a etapa 11; a antiga etapa 5 foi incorporada a ela.

| ID | Requisito do incremento | Critério de aceite |
|---|---|---|
| RF-35 | Obter salto duplo examinando o módulo da biblioteca por E. | Módulo antes dos patamares obrigatórios, diálogo de instrução, habilidade única sem cura ou bônus de vida. |
| RF-36 | Consultar três terminais para abrir o arquivo central. | Proximidade e E necessários; consultas não repetem falas e o portão só desaparece com as três concluídas. |
| RF-37 | Enfrentar Indexador em classe concreta própria. | Faixas com mira fixa anunciadas, fichas em alturas alternadas, recuperação e ausência de dano corporal passivo; derrota limpa ataques. |
| RF-38 | Retomar a biblioteca após derrota por R. | Conservar módulo e consultas na sessão, restaurar integridade e reiniciar chefe; Enter volta ao menu. |
| RF-39 | Preservar identidade e limpar combate na transição. | Nome, aparência e habilidades mantidos; descartar cargas, golpes e projéteis. Nova campanha reinicia habilidades. |

| ID | Validação proposta |
|---|---|
| CA-11 | Percorrer biblioteca com ambas as aparências; obter módulo e alcançar os arquivos elevados com física real. |
| CA-12 | Conferir três consultas, portão e preservação do progresso na retomada local. |
| CA-13 | Exercitar preparação sem indicativos auxiliares, dano, recuperação e derrota do Indexador; conferir congelamento em diálogos e pausa. |
| CA-14 | Conferir saída da fase 1 para biblioteca, fim provisório após fase 2 e reinício de campanha. |

A arte da biblioteca é provisória e feita em Pygame, usando os materiais das duas
capturas internas em `referencia/ifrn/`. Bugs especializados, atalhos, materiais
externos e homologação manual permanecem pendentes. A entrada em fase e a retomada
restauram a integridade até a capacidade existente; a obtenção do módulo não cura.


## 14. Correção da abertura, transporte e direção de arte

Atualização de 02/11/2026: os fundos provisórios da biblioteca foram substituídos
por arte detalhada baseada nas fotos internas e no estilo da fase 1; o pátio
baseado nas fotos externas integra o trajeto escolar até o A28. Isso não conclui
a fase 3. A lembrança doméstica aparece durante o diálogo de abertura, sem
narrador ou fase doméstica independente. A animação de abrir a bolsa e retirar
o mouse ainda está pendente, embora o diálogo e a liberação da arma funcionem.

| ID | Requisito | Critério de aceite |
|---|---|---|
| RF-40 | Mostrar tarefa e origem na abertura. | Max pede a atividade; lembrança visual acompanha relato de casa/jantar/oscilação; monitores mudam de código para execução e revolta conforme as falas. |
| RF-41 | Mostrar turma no laboratório e hipnose. | Alunos sentados em quatro postos; mudança visual de olhos e postura após corrupção, congelada na pausa e sem avançar física durante diálogo. |
| RF-42 | Mostrar absorção pelo computador. | Aluno e Romerito convergem para monitor do cenário, diminuem, giram e desaparecem antes de carregar a fase virtual; corpos lógicos não mudam por desenho. |
| RF-43 | Criar espaço para investida nas bordas. | Reposicionar antes do aviso quando necessário, sem dano passivo; direção fixa no avanço, distância efetiva até 160 pixels e recuperação ao parar. |
| RF-44 | Manter continuidade visual dos ambientes e da libertação. | Biblioteca e pátio seguem acabamento da fase 1, sem alterar colisões; Romerito reaparece humano depois de SpeedBug. |

| ID | Verificação |
|---|---|
| CA-15 | Conferir tarefa, memória, execução, revolta e hipnose na ordem; pausar e confirmar congelamento da animação. |
| CA-16 | Conferir sucção de ambas as aparências com Romerito, destino no monitor, ausência de duplicatas e corpo lógico preservado pelo desenho. |
| CA-17 | Exercitar investida nas duas bordas e contra paredes; conferir avanço real e recuperação, sem mudar direção depois do anúncio. |
| CA-18 | Comparar biblioteca/pátio com fotos e estilo da fase 1, preservar colisões e conferir forma humana na conversa posterior ao chefe. |

Testes automáticos e capturas cobrem as regressões acima; aceitação manual de
ritmo, apresentação e sobrevivência permanece aberta na etapa 11. O plano foi
reorganizado para priorizar a correção do início; o registro anterior foi preservado
em `documentacao/HISTORICO_DE_EXECUCAO.md`.

### Refinamento de apresentação — 09/11/2026

A câmera das cenas com `Camera` mantém o enquadramento vertical enquanto o
centro do alvo estiver entre 180 e 370 pixels da tela, após posicionamento
inicial; acompanha o alvo fora dessa faixa, respeitando limites do mapa.
O acompanhamento horizontal permanece centralizado. A biblioteca desenha
sinais de interativos após sólidos e objetivos após o HUD, com rótulos de
arquivo, leitura concluída e módulo de salto duplo. Não há mudança de colisões,
controles, habilidades ou campanha. Evidências e limites de validação em
[avaliacao/visual/RELATORIO.md](../avaliacao/visual/RELATORIO.md); homologação manual pendente.

### Revisão solicitada de composição e chefes — 09/11/2026

A aula apresenta dois colegas espaçados, sem efeitos de ligação entre olhos e
monitores. O piso físico do pátio de passagem está em Y=440, com surgimento e
soleira da porta A28 alinhados; a entrada está em X=1728 na parede do bloco final.
Por solicitação explícita, os chefes da campanha não exibem indicativos auxiliares
de ataque: textos, miras, setas e sons de aviso foram removidos. Preservam-se
preparação corporal, pausas, direção fixa e janelas de dano. Indexador mostra
faixas apenas durante o dano ativo; preparação não desenha marcações antecipadas.
Esta decisão substitui a apresentação de avisos descrita em revisões anteriores.

### Perspectiva dos laboratórios — 09/11/2026

A aula e o A28 usam profundidade visual 2.5D com bancadas em dois planos,
tampos em perspectiva e sombras. Colegas aparecem sentados de costas,
centralizados diante dos respectivos monitores; a hipnose é comunicada por
postura e reflexo da tela. A perspectiva é visual, com movimentação lateral e
colisões preservadas. A sucção continua usando o retângulo real de um monitor.

### Organização e resolução de recursos — 10/11/2026

Ponto de entrada mantido em `principal.py`; serviços centrais em `sistema/`,
ferramentas em `ferramentas/`, dependências em `configuracao/dependencias.txt`
e documentação em `documentacao/`. Os recursos são resolvidos relativamente
à localização dos módulos, inclusive ao iniciar por caminho absoluto de outro
diretório. Exportadores são executados como módulos (`python -m ferramentas.nome`).
Campanha, controles e apresentação preservados; detalhes e verificações em
[REORGANIZACAO.md](REORGANIZACAO.md).

### Entradas alternativas de ataque e caminhada durante carga — 10/11/2026

X, K e botão esquerdo do mouse são alternativas equivalentes para o chicote:
tocar e soltar causa 1 de dano; segurar por 0,6 s e soltar causa 2. O comando
que iniciou a carga é o que deve ser solto; outra entrada não reinicia a carga
nem dispara um golpe extra. Pausa, foco, dano e transições continuam cancelando
entradas pendentes. Menus e diálogos preservam suas funções de entrada.
Durante a carga, caminhada e salto acompanham o deslocamento real; a pose de
preparação fixa só é usada quando parado no chão. Velocidade de carga permanece
em 75% da velocidade normal, sem alterar colisões ou janelas de dano.

### Postura de carga, energia e retratos — 10/11/2026

O ciclo de carga usa oito sprites próprios por protagonista, preservando
braço/mouse preparado e passos sincronizados ao deslocamento. Parado usa pose
de apoio; no ar mantém postura de carga. Escala de 200%, pés e corpo lógico
40 × 40 preservados. Energia possui partículas convergentes, mudança para
ciano na carga completa e animação contínua enquanto o comando é mantido.
Pausa, foco, transições e dano mantêm cancelamento seguro.

Cada fala mostra imagem do falante: protagonista escolhido, Max, Romerito,
IFVania/Entidade, Indexador ou ícone do Sistema. Retratos aproveitam sprites
aprovados; falantes antigos sem arte própria usam busto neutro. Nomes
personalizados não alteram textos compartilhados. O texto determina a altura
da caixa, sem cortar falas ao reservar espaço para o retrato. Animação de
digitação e comandos de avanço preservados.

### Composição do diálogo e imagens em alta resolução — 10/11/2026

O HUD de conversa usa bustos grandes acima da caixa azul, com interlocutores
voltados ao centro e destaque do falante atual. Nome em placa alinhada ao lado
ativo; ouvinte escurecido, sem modificar a imagem original. Texto completo,
digitação, comandos de avanço, pausa e callbacks permanecem preservados.

Protagonistas, Max, Romerito, entidade e Indexador possuem ilustrações próprias
em 1024 × 1536 com transparência; o jogo carrega versões de 768 × 1152 e as
reduz suavemente para o HUD. Sistema usa ícone vetorial na mesma resolução.
A resolução lógica da janela permanece 960 × 540. Falantes exclusivos da
campanha antiga mantêm alternativas de compatibilidade; não foram redesenhados.
O monitor ampliado da abertura é centralizado para preservar a leitura entre
os bustos. Assets de combate, colisões e campanhas não foram modificados.
