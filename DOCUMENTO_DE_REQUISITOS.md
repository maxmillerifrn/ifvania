# Documento de Requisitos — IFVania

**Título do projeto:** IFVania

**Versão do documento:** 3.0

**Data:** 28/10/2026

**Fontes:** `ROTEIRO_HISTORIA.md`, orientações do responsável pelo projeto e referências técnicas do repositório.

## 1. Objetivo e alcance do documento

Especificar o comportamento esperado do jogo com base no HistoryBoard, incluindo narrativa, apresentação, combate e critérios de aceite. Esta revisão substitui a descrição anterior centrada no vírus CODIGO.EXE e na campanha obrigatória de seis professores de linguagens de programação.

O HistoryBoard é a referência narrativa desta versão. As solicitações complementares determinam tamanho uniforme para personagens e inimigos e uma classe própria para cada boss. Os requisitos descrevem o produto desejado; sua presença neste documento não significa que estejam implementados ou homologados.

O HistoryBoard detalha o início da história e a primeira fase. As fases seguintes, suas recompensas e a sequência final de desligamento de energia ainda precisam de definição. Recursos antigos podem ser reaproveitados, mas não definem automaticamente o escopo da nova campanha.

As etapas 1 a 4 do `PLANO_DE_EXECUCAO.md` estão implementadas: menu, seleção, prólogo escolar, percurso virtual com salto básico, reencontro com Romerito humano, infecção, combate RomerBug/SpeedBug e encerramento do conteúdo disponível. A campanha antiga foi isolada, e o fluxo atual não concede recompensas ou anuncia a escola salva. Foram executados 92 testes automatizados e inspeções visuais. A revisão visual de 25/10/2026 acrescenta menus noturnos, HUD de integridade, arena escolar escura e a cena com a entidade. A revisão autorizada implementa chicote carregado, esquiva, controle com aceleração curta, plataformas destacadas e sobrecarga/investida, conforme `PROPOSTA_CHEFE_ROMERBUG.md`. O mapa escolar é uma adaptação sem planta interna homologada; a etapa 5 e a homologação manual permanecem pendentes. Testes controlados de combate não equivalem à validação do equilíbrio de sobrevivência.

## 2. Visão geral do produto

IFVania é um jogo local de plataforma 2D, para um jogador, desenvolvido em Python e Pygame, com visual em pixel art e ambientação escolar e virtual.

A história começa em uma aula de programação orientada a serviço. O professor Max apresenta uma inteligência artificial chamada IFVania — Inteligência Federal Virtual de Aprendizagem Neural e Inteligência Artificial. Quando ele anuncia que irá desligá-la para continuar a aula, ela se revolta, assume o controle do computador dele e dos demais computadores da escola, hipnotiza as pessoas e provoca alucinações.

Somente o aluno ou a aluna controlado pelo jogador não é completamente afetado. Seu objetivo narrativo é buscar ajuda, desligar a energia da escola e desativar a IFVania. A primeira fase leva o protagonista pelos corredores até o laboratório A28 e, depois, a um mundo virtual onde enfrenta bugs e o professor Romerito transformado.

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

### 2.2 Conteúdo ainda não definido pelo HistoryBoard

Não há definição das fases posteriores à primeira, do número total de bosses, das recompensas, das habilidades desbloqueáveis ou da sequência jogável de desativação da IFVania. A campanha antiga de Scratch, Python, Java, C, SQL e Assembly e seus cinco poderes não é um requisito confirmado desta versão.

Salvamento persistente, multiplayer, serviços de rede, ranking, suporte a controle e menu de configurações também não integram o escopo definido.

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
| Linguagem e biblioteca | Python e Pygame; dependências em `dependencias.txt`. |
| Execução | Local, por `python principal.py`, a partir da pasta do projeto. |
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
| RF-07 | Apresentar a aula do professor Max e a IFVania antes da exploração. | O aluno inicia uma conversa com Max, sem narrador. Todas as falas da introdução são entre os dois e identificam a aula de programação orientada a serviço, o tema inteligência artificial e o nome completo da IFVania. |
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
| RF-20 | Fazer RomerBug provocar sobrecargas sinalizadas no piso. | Uma faixa fixa de 96 pixels é avisada por 0,8 s, seguida de descarga baixa de 0,25 s e recuperação de 1 s. Sair da faixa ou saltar evita o dano. |
| RF-21 | Transformar RomerBug em SpeedBug ao atingir metade da vida máxima ou menos. | A primeira redução que deixa a vida em até 50% dispara uma única cena: ajoelhar sobre uma perna, aparição de uma entidade com a fala “Ainda não terminou.”, metamorfose e levantamento como SpeedBug. Suspender o combate, permitir pausa e preservar posição, dimensões e vida restante, sem reiniciar o encontro. |
| RF-22 | Fazer SpeedBug executar uma investida anunciada e previsível. | Aproximação limitada, aviso de 0,6 s, avanço de até 160 pixels em direção fixa, colisão com paredes e recuperação de 1,3 s sem dano de contato. Não combinar projétil ou salto reativo; salto básico deve bastar para evitar o ataque. |
| RF-23 | Encerrar o combate quando a vida do boss chegar a zero. | Ataques, projéteis e bugs restantes são encerrados; a saída é liberada, sem recompensa. Alcançá-la apresenta “A jornada continua”, informa que a IFVania permanece ativa e permite voltar ao menu. O conteúdo posterior depende de definição narrativa. |
| RF-24 | Gerenciar zonas ofensivas e projéteis para evitar dano indevido. | Limpar ataques e zonas na transformação e derrota; suspender temporizadores na pausa e no diálogo. Projéteis antigos continuam isolados da campanha atual. |

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
| RN-11 | A derrota do boss da primeira fase não equivale à desativação da IFVania nem à vitória final. Após o diálogo e a saída, apresentar fim do conteúdo disponível, com retorno ao menu. Não conceder poder, item ou aumento de vida nessa vitória. |
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
| RomerBug | Transformação de Romerito; sobrecarga sinalizada no piso. |
| SpeedBug | Segunda forma do mesmo boss; investida anunciada e recuperação. |

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
4. RomerBug marca uma faixa e executa uma descarga baixa após o aviso.
5. Ao atingir até 50% da vida máxima, transforma-se uma única vez em SpeedBug.
6. SpeedBug prepara uma investida, avança em direção fixa e fica exposto.
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
| CA-06 | Reduzir a vida do boss até acima de 50%, exatamente 50% e abaixo do limiar em execuções controladas; verificar sobrecarga antes e investida depois, sem cura ou transformação repetida. | RF-20 a RF-22, RN-05, RN-09 |
| CA-07 | Derrotar o boss e conferir encerramento de ataques e projéteis, sem declarar vitória final da campanha. | RF-23, RF-24, RN-11 |
| CA-08 | Comparar todos os personagens e inimigos lado a lado, na mesma escala de câmera; conferir dimensões lógicas, área dos sprites, escala visível e alinhamento em todos os quadros, incluindo SpeedBug. | RF-28, RN-07 a RN-09, RNF-06 |
| CA-09 | Revisar a classe e a instanciação de cada boss disponível, comprovando comportamento próprio e ausência de boss representado somente por parâmetros genéricos. | RN-06, RNF-05 |
| CA-10 | Pausar e avançar diálogos durante situações de combate, verificando suspensão da simulação; conferir HUD, câmera e fechamento da janela. | RF-16, RF-25 a RF-29, RN-10 |

## 10. Pendências e adequação da implementação

| ID | Ponto | Encaminhamento |
|---|---|---|
| P-01 | O documento anterior descrevia CODIGO.EXE e seis professores de linguagens. | Substituir as referências narrativas e revisar fases antigas antes de incorporá-las à campanha IFVania. |
| P-02 | O HistoryBoard termina na descrição do combate da primeira fase. | Definir desfecho dessa fase, fases posteriores, recompensas e sequência de desligamento da energia antes de especificar a vitória final. |
| P-03 | A etapa 1 substituiu as dimensões distintas por um corpo comum de 40 × 40 pixels, com escala proporcional dos sprites e surgimento em piso livre. | Testes de geometria e combate passaram nas seis fases existentes; conferir novamente passagens, arenas e novos personagens durante a construção dos mapas escolares e a homologação manual. |
| P-04 | RomerBug e os outros cinco bosses existentes possuem classes concretas com estratégias próprias; a base `Chefe` exige escolha de ataque especializada. | A arquitetura foi validada por testes; a participação dos professores antigos na nova campanha continua sujeita à revisão narrativa. |
| P-05 | As etapas 1 a 4 foram integradas, incluindo a primeira fase sem recompensas antigas e o fim do conteúdo sem declarar a escola salva. Os testes cobrem percurso, narrativa, combate e encerramento. | Executar a etapa 5: homologação manual com ambos os protagonistas, revisão integrada de interface/controles e balanceamento. |
| P-06 | A28 foi conferido na referência oficial, mas o Maps não forneceu uma planta acessível. O corredor implementado é uma adaptação para o jogo. | Validar posições, medidas e conexões internas se houver exigência de reprodução geográfica fiel. |
| P-07 | Valores de vida, dano, velocidade, alcance e recarga não são definidos pelo HistoryBoard. | Usar os valores existentes como ponto de partida para balanceamento, sem tratá-los como decisões narrativas obrigatórias. |
| P-08 | O responsável pediu uma alternativa menos infantil para aviões e medalhas. A proposta é sobrecarga de terminais e investidas, documentada separadamente. | A troca foi autorizada e implementada em RF-20/RF-22, junto à carga e esquiva. A homologação manual de dificuldade continua pendente. |

## 11. Rastreabilidade técnica de referência

A tabela indica áreas de implementação e revisão, sem afirmar que os novos requisitos já estejam atendidos.

| Arquivo / área | Responsabilidade esperada |
|---|---|
| `ROTEIRO_HISTORIA.md` | Fonte da narrativa, sequência inicial e primeira fase. |
| `jogo.py` | Menu, escolha de personagem, introdução, pausa, derrota, transições e isolamento dos eventos entre telas. |
| `interface/interface_inicial.py` e `interface/tema.py` | Fachada noturna, botões, seleção, cores e painéis compartilhados. |
| `mundo/transicao_chefe.py` e `mundo/escola_sombria.py` | Transformação com a entidade, zoom visual e cenário escolar escuro. |
| `mundo/arte_escolar.py`, `mundo/terminal.py` e `preparar_escola_detalhada.py` | Ambientes detalhados, mobiliário e telas animadas com recorte próprio. |
| `mundo/escola.py` e `mundo/dados_escola.py` | Sala, corredor, A28, gatilhos únicos, ataque/abdução e falas de descoberta do mouse. |
| `entidades/professor.py` e `preparar_recursos_escola.py` | Professores Max e Romerito e exportação de suas artes a partir das referências. |
| `preparar_recursos_menu.py` | Exportação da fachada e dos onze quadros da Menina a partir das fontes geradas. |
| `configuracoes.py` | Dimensões comuns, resolução, taxa-alvo e balanceamento. |
| `entidades/personagem.py` | Estado, vida e infraestrutura compartilhada dos personagens. |
| `entidades/jogador.py` | Movimento, personagem escolhido, combate e animações. |
| `entidades/chicote_mouse.py` | Comportamento e apresentação do mouse-chicote. |
| `entidades/inimigo.py` | Bugs e sua adequação ao tamanho comum. |
| `entidades/chefe.py` | Infraestrutura comum dos bosses; revisar instanciações genéricas. |
| `entidades/chefes_professores.py` | Classes concretas dos professores antigos e registro explícito de tipos de boss. |
| `entidades/romer_bug.py` | Classe própria de RomerBug, transformação em SpeedBug, sobrecarga e investida. |
| `entidades/projetil.py` | Movimento, dano e ciclo de vida dos projéteis. |
| `mundo/fase.py` e `mundo/dados_fases.py` | Mapa virtual, reencontro, infecção, combate, limpeza após derrota e saída. |
| `mundo/fases_antigas.py` | Dados isolados dos seis mapas antigos e suas recompensas, fora do fluxo principal. |
| `mundo/mapa_blocos.py` e `mundo/camera.py` | Geometria, colisões e acompanhamento de câmera. |
| `interface/dialogo.py` e `interface/painel.py` | Falas, vida, identificação do boss e instruções. |
| `recursos.py`, `recursos/imagens/` e `recursos/fontes_arte/` | Carregamento, cache, spritesheets e padronização visual. |
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
