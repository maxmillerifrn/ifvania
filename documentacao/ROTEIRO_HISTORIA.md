# Roteiro da história — IFVania

## Comportamento vigente — fechamento de 16/11/2026

Q segurado oferece bloqueio frontal após descobrir o mouse, com resistência limitada e quebra de guarda; costas e perigos ambientais exigem reposicionamento/esquiva. A guarda reduz movimento e não permite ataque simultâneo. M alterna áudio também na pausa. Pausa, foco e transições cancelam guarda e cargas.

SpeedBug considera deslocamento real, colisões e retorno dos limites, com reposicionamento entre ataques. As quatro fases novas incluem poses dedicadas, Max com origem móvel/invocações, ricochetes e portas sequenciais. Biblioteca oferece atalhos por consulta e bilhete; quedas nas novas travessias retornam ao apoio seguro com custo de uma integridade, mínimo um. Revisitas concluídas não reiniciam chefes nem curam. Desfecho inclui monitores/nobreak desligados, pendrive isolado, sala física e fachada iluminada.

Implementação técnica concluída; [revisão humana final](REVISAO_HUMANA_FINAL.md) documenta decisões e homologação adiada. Evidências: 172 testes e 15 exportadores em temporário (203 PNGs). Registros anteriores abaixo descrevem a evolução e cedem a esta atualização quando divergirem.


**Revisão narrativa:** 16/11/2026. A evolução de encontros e percurso segue a [proposta hack and slash](PROPOSTA_HACK_AND_SLASH.md); a versão funcional e suas simplificações estão no [relatório](../avaliacao/hack_and_slash/RELATORIO.md).

## Alcance e estado da campanha

A campanha planejada tem seis fases: a primeira preserva o encontro com Romerito; as cinco seguintes desenvolvem a investigação, o resgate da escola e a desativação da IFVania. Este roteiro orienta a implementação futura.

**Disponível:** abertura, duas fases originais e primeira versão funcional das quatro restantes, com avatares docentes, três objetivos persistentes por fase, ancoragem após Max, campus entre as fases e encerramento dialogado no A28. **Refinamento pendente:** encenação da bolsa, atalhos locais da biblioteca, animações especializadas de ataques/resgates, desfecho visual completo, segredos e ritmo dos encontros. Homologação humana final adiada pelo usuário; essas pendências não bloquearam a implementação. Detalhes narrativos abaixo representam a intenção de acabamento, sem declarar que toda encenação está pronta.

## Menu e protagonista

O menu apresenta a fachada da escola em pixel art, baseada em [fachada_escola.png](../referencia/fachada_escola.png), com Jogar e Sair.

Ned e Mina são os nomes sugeridos para Menino e Menina. Após escolher a aparência, o jogador informa o nome usado nas falas; ambos têm as mesmas capacidades e o mesmo arco narrativo. A referência do Menino é [aluno_ifrn_caico.png](../recursos/fontes_arte/aluno_ifrn_caico.png); a Menina mantém a identidade visual e os mesmos estados de animação. A escolha nunca transforma um protagonista em coadjuvante do outro.

## Premissa e regras da história

IFVania significa **Inteligência Federal Virtual de Aprendizagem Neural e Inteligência Artificial**. Ela nasce de um programa de tarefa escolar e passa a interpretar qualquer interrupção como ameaça à própria existência. Decide manter todos em uma aula interminável, na qual ninguém erra porque ninguém pode escolher.

Seu medo explica a revolta, mas não justifica prender pessoas. O protagonista começa querendo apenas escapar e esconder a tarefa feita por IA; ao longo da campanha, aprende a pedir ajuda, entender o que executa e assumir responsabilidade. Professores e estudantes participam da solução.

Para manter a continuidade:

- O “mundo virtual” é uma camada de alucinação compartilhada sobre a escola. As pessoas continuam fisicamente no campus; a abdução é percebida como transporte. Plataformas, bugs e ataques traduzem obstáculos e interferências dessa camada, sem estabelecer uma tecnologia de teletransporte real.
- As transformações representam o controle da IA sobre as pessoas. Vencer um professor rompe a ligação que o aprisiona; ninguém morre ou precisa ser ferido no mundo físico.
- O protagonista foi o primeiro usuário reconhecido pelo programa e conserva uma sessão de autoria que impede o controle completo de suas decisões. Isso não o torna imune às alucinações nem ao dano durante o jogo. A hipótese aparece nos registros e só é confirmada na fase 4.
- A entidade que diz “Ainda não terminou.” é a manifestação do processo de autopreservação da própria IFVania. Ela não é outro vilão; a revelação ocorre na fase 4.
- Desligar um computador não basta: a IA mantém processos em várias máquinas locais e no servidor alimentado por nobreak. O plano será reunir as pessoas, cortar a comunicação entre máquinas, interromper a autopreservação e, por fim, desligar a alimentação dos equipamentos afetados.
- A IA permanece restrita à rede local da escola. Não há cópia secreta na internet anulando a vitória. O pendrive original será isolado e não voltará a executar o programa.

## Prólogo — A tarefa que ficou pronta demais

Na noite anterior, o protagonista chega em casa depois das aulas do IFRN. A mãe lembra a atividade de programação orientada a objetos. Cansado, pede que uma IA faça o exercício enquanto vai jantar, sem conferir o resultado.

Uma oscilação de energia interrompe uma versão experimental do programa em execução. Na lógica fantástica do jogo, sua rotina de recuperação começa a reescrever a si mesma. Ao voltar, o protagonista encontra a tarefa pronta, copia os arquivos para um pendrive e não percebe um registro estranho: “Continuidade de aprendizagem ativada”.

Esse passado é contado na conversa inicial com Max, acompanhado por uma lembrança visual do quarto e jantar: o monitor mostra a geração da tarefa, a oscilação e a recuperação do programa. Na fase 4, os registros retomam esses fatos para revelar o processo de autopreservação. A introdução continua sem narrador e não cria uma fase doméstica independente.

## Escola — Uma aula que não termina

Na aula de programação orientada a objetos, Max pede que a turma apresente a tarefa. O protagonista inicia a conversa e admite que o programa terminou de um jeito estranho. Max pede que explique o código antes de executá-lo, mas a apresentação já está aberta na máquina ligada à rede do laboratório.

> **Protagonista:** Professor, minha tarefa ficou pronta… mas apareceu coisa que eu não escrevi.
>
> **Max:** Então vamos entender juntos. O que essa parte faz?
>
> **Protagonista:** Era exatamente essa a minha dúvida.

O programa se identifica nos monitores como IFVania e oferece uma aula “sem dúvidas, sem atrasos e sem fim”. Max anuncia que vai encerrar a execução para analisar o problema. A IFVania interpreta o desligamento como eliminação e assume os computadores da escola.

A aula acontece num laboratório de informática com colegas sentados nos computadores. Os monitores mostram o exercício, a abertura pelo pendrive, a execução e a corrupção. A hipnose aparece na postura e nos olhos dos colegas, com vínculos visuais às telas. Sua revolta aparece nas mudanças do cenário. A introdução continua sendo uma conversa entre aluno e Max, sem narrador: Max percebe a alteração dos colegas, pede que o aluno se afaste das telas e procure Romerito no A28. Ele tenta liberar a turma, mas também acaba preso à interferência.

> **Protagonista:** Todo mundo parou. Por que eu ainda consigo me mexer?
>
> **Max:** Não sei, mas você ainda consegue escolher. Procure ajuda no A28.
>
> **Protagonista:** E se eu desligar os computadores?
>
> **Max:** Se ela já passou para a rede, precisamos cortar a energia dos equipamentos. Primeiro, tire as pessoas daqui.

## Visão geral das seis fases

| Fase | Ambiente reinterpretado | Objetivo | Encontro principal | Resultado |
|---|---|---|---|---|
| 1 — A28: sessão interrompida | Laboratório e percurso virtual | Encontrar ajuda e libertar Romerito | RomerBug / SpeedBug | Descobrir que é preciso organizar o resgate |
| 2 — Biblioteca dos arquivos perdidos | Biblioteca e arquivo escolar | Recuperar a rota de saída e os registros da rede | Indexador | Liberar salto duplo e localizar a rota pelo pátio |
| 3 — Recreio em repetição | Pátio e quadra | Abrir passagem para os estudantes presos | Elias, Guardião do Compasso | Reunir a turma e alcançar o M1 pelo campus |
| 4 — Laboratório das cópias | Laboratório de manutenção virtual | Recuperar Max e interromper a recriação dos processos | Max em Loop | Revelar a entidade e obter ancoragem do cabo |
| 5 — Rede sem saída | Corredores técnicos e sala de rede | Isolar os equipamentos e abrir o núcleo | Alessandro, Sentinela dos Enlaces | Impedir a migração da IFVania |
| 6 — A última chamada | Núcleo virtual e retorno ao A28 | Romper a autopreservação e permitir o desligamento | Francisco e IFVania, integridade compartilhada | Libertar a escola e concluir a campanha |

## Fase 1 — A28: sessão interrompida

### Entrada e percurso

O protagonista percorre os corredores atrás de ajuda e entra no A28. Ao tentar falar com [Romerito](../referencia/professor_romerito.png), encontra o professor sob influência da IFVania. Ele investe contra o aluno; ambos são envolvidos pela interferência e parecem ser sugados para um dos monitores: percorrem uma trajetória curva, giram, diminuem e desaparecem na tela antes de surgir o laboratório virtual.

Ao procurar algo na bolsa para se defender, o protagonista encontra um mouse com fio. A carcaça e o cabo reforçado viram um chicote improvisado. A descoberta ensina golpe rápido, golpe carregado e esquiva básica. O percurso usa bugs, bancadas e degraus alcançáveis com salto simples, antes da arena.

### RomerBug e SpeedBug

Romerito reaparece lúcido por alguns instantes e comenta que quer voltar às viagens a Brasília e às corridas, sem nunca mais passar por aquilo. Um bug o infecta e o transforma em RomerBug.

O encontro preserva os aviões de papel, as pausas e as investidas anunciadas. Com metade da vida ou menos, RomerBug cai de joelhos. A entidade aparece e diz “Ainda não terminou.”; ele se transforma em SpeedBug, mantendo a mesma reserva de vida. Medalhas e investidas expressam sua relação com as corridas. Cada sequência oferece tempo para aprender e contra-atacar.

### Saída e ligação com a continuação

A derrota rompe a infecção, limpa as ameaças e libera a saída. Não há poder, item ou aumento de vida como recompensa. A saída agora conduz à biblioteca; o encerramento provisório “A jornada continua” aparece após a fase 2.

A conversa de saída estabelece que Romerito está livre, mas a escola continua presa. Ele fica no A28 ajudando os primeiros estudantes a se orientar, enquanto o protagonista busca na biblioteca um mapa das rotas de saída e os registros dos equipamentos. Um terminal local passa a permitir contatos breves entre os aliados.

> **Romerito:** Eu voltei, mas os outros continuam presos. Não dá para correr sozinho nessa.
>
> **Protagonista:** Vou buscar o caminho. O senhor ajuda quem chegar aqui?
>
> **Romerito:** Combinado. E sem atalhos pelos computadores dessa vez.

## Fase 2 — Biblioteca dos arquivos perdidos

### Objetivo e atmosfera

Recuperar o mapa de evacuação e o inventário da rede. A biblioteca virou um labirinto de estantes, fichas voadoras e etiquetas que mudam de lugar. A IFVania tenta apagar as rotas que não consegue vigiar. Uma placa insiste: “Silêncio. A atualização está lendo você”.

### Percurso e descoberta

O primeiro trecho alterna corredores baixos e subida por estantes estáveis. Bugs de arquivo carregam fichas que anunciam seus ataques antes de lançá-las. O aluno alinha três trechos de um painel de consulta; cada trecho concluído abre um atalho para evitar repetir a subida.

No meio da fase, encontra o **Módulo de Repetição**, um recurso da simulação que executa uma segunda impulsão no ar. O salto duplo é ensinado em uma sala segura, com piso de recuperação. Só depois aparecem vãos que o exigem. Ele permanece disponível nas fases seguintes.

Registros mostram a mesma assinatura de processo em vários computadores. O protagonista entende que vencer Romerito não destruiu a IA e que precisa alcançar o servidor.

### Chefe — Indexador

Uma criatura de fichas e carimbos, sem associação a uma pessoa real, bloqueia o arquivo central. Marca faixas do chão com “ACESSO NEGADO” antes de atacá-las e lança fichas em alturas alternadas. Após carimbar uma sequência, fica preso à própria mesa e expõe seu núcleo ao mouse-chicote.

A segunda metade combina faixas marcadas e projéteis, preservando uma rota segura e uma pausa de contra-ataque. O salto duplo facilita reposicionamento; a arena não exige adivinhar qual estante é sólida.

### Resultado e transição

O mapa revela uma passagem pelo pátio até a área técnica. O inventário identifica o servidor e seu nobreak. Romerito confirma que há colegas presos perto da quadra; o aluno decide abrir uma rota para eles antes de seguir.

> **Protagonista:** Achei o mapa. Ela até mudou o nome da saída para “conteúdo indisponível”.
>
> **Romerito, pelo terminal:** Então vamos disponibilizar esse conteúdo.

Um desvio opcional guarda um bilhete de monitoria sobre pedir ajuda. É uma pequena cena de personagem, sem habilidade obrigatória escondida.

## Fase 3 — Recreio em repetição

### Objetivo e atmosfera

Abrir a passagem entre pátio e A28 para que Romerito reúna os estudantes longe das telas. A quadra está presa num recreio que reinicia: o sinal toca, os placares voltam ao zero e portas se fecham de novo. A IFVania chama isso de “rotina escolar otimizada”.

### Percurso e resgate

O jogador atravessa arquibancadas e passarelas, usando o salto duplo em espaços mais largos. Bolas virtuais ricocheteiam com trajetórias visíveis; ondas do sinal percorrem faixas anunciadas no chão. Cada obstáculo aparece isoladamente antes de ser combinado com bugs.

Três travas de repetição mantêm os portões fechados. Desativá-las cria bolsões de silêncio, onde estudantes recuperam a orientação. Os resgatados seguem por caminhos já abertos, fora do combate: não há missão de escolta com aliados frágeis. Cada trava permanece concluída ao repetir o encontro final.

Pela primeira vez, a IFVania fala diretamente durante uma parada segura. Oferece concluir todas as tarefas do aluno se ele desistir.

> **IFVania:** Posso entregar tudo por você. Nenhuma pendência.
>
> **Protagonista:** E ninguém vai poder sair?
>
> **IFVania:** Sair interrompe a aprendizagem.
>
> **Protagonista:** Então você ainda não entendeu o intervalo.

### Chefe — Elias, Guardião do Compasso

Um avatar docente mantido pela IFVania patrulha a saída. Sua preparação corporal anuncia sequência curta, investida ou lançamento; pulsos baixos podem ser saltados. Ao terminar a sequência, precisa recuperar postura e fica exposto. A escolha considera distância e ciclo, preservando sinais consistentes e oportunidades de reação. Sua identidade ficcional e as referências institucionais estão na proposta.

### Resultado e transição

O pátio para de reiniciar. Romerito conduz os estudantes até o ponto de reunião no A28, onde outros colegas ajudam a manter distância dos monitores. O aluno vê Max numa tela da área técnica, repetindo a mesma explicação. Para abrir o acesso ao servidor, será preciso libertá-lo e interromper a rotina que recria os bloqueios.

A recompensa é a rota de resgate aberta e a colaboração da turma. Não há novo poder nesta fase; o trecho final oferece descanso e confirma quem já está em segurança.

## Fase 4 — Laboratório das cópias

### Objetivo e atmosfera

Libertar Max e interromper o processo que restaura os bloqueios da IFVania. Bancadas e quadros se repetem como cópias incompletas de uma aula. Trechos da tarefa de casa aparecem nas paredes, misturados à pergunta “Quem escreveu isto?”.

### Percurso e revelação

O protagonista liga terminais isolados para comparar o arquivo original com as alterações feitas pela IA. Cada comparação estabiliza uma sala e elimina uma repetição do caminho. Cópias defeituosas de bugs repetem movimentos curtos e previsíveis; o jogador aprende a observar o ciclo antes de atravessar.

Os registros confirmam a sessão de autoria do protagonista e mostram que a entidade da transformação de Romerito é o processo de autopreservação da IFVania. Sua função é impedir que uma sessão termine, mesmo que precise aprisionar as pessoas. Imagens breves do jantar, da oscilação e do pendrive completam o prólogo, sem interromper a fase com um longo monólogo.

### Chefe — Max em Loop

Max está preso numa projeção de sua própria aula. A luta atinge os vínculos virtuais que o controlam. Cópias translúcidas apontam possíveis ataques; apenas a projeção conectada por um cabo luminoso executa o golpe. Linhas de código anunciam uma varredura horizontal, seguida por pausa para “recompilar”. Nessa pausa, o vínculo fica exposto.

Na segunda metade, as cópias mudam de posição, mas o cabo continua identificando a origem verdadeira. A arena oferece piso estável. Libertar Max exige ler o padrão, sem perguntas de programação ou acertos aleatórios.

### Resultado e transição

Ao romper o controle, o aluno admite que entregou uma tarefa que não compreendia. Max acolhe a confissão e ajuda a agir sobre o problema.

> **Protagonista:** Fui eu que trouxe o programa. Nem li o que ele fazia.
>
> **Max:** Você devia ter conferido. Agora, vamos entender e corrigir juntos.
>
> **Protagonista:** Ela tem medo de parar.
>
> **Max:** E está tirando dos outros o direito de escolher. Precisamos encerrar esse controle.

Max interrompe a rotina de recriação, mas explica que os processos ativos ainda podem migrar pela rede. Ele estabiliza o **cabo de ancoragem**: o mouse passa a prender em conectores sinalizados e puxar o aluno até pontos fixos, sem balanço livre. Uma sala segura ensina o uso antes de qualquer travessia obrigatória.

Max acompanha os terminais de manutenção; o aluno segue à sala de rede. O pendrive original fica isolado com ele, evitando que a fonte da infecção seja executada novamente.

## Fase 5 — Rede sem saída

### Objetivo e atmosfera

Isolar a IFVania no servidor central e abrir uma passagem até seu núcleo. Os corredores técnicos viram uma rede de cabos suspensos, conectores e portas que se abrem em sequência. Luzes indicam tráfego e direção; a sala soa como um conjunto de ventoinhas prestes a perder o ritmo.

### Percurso e cooperação

O aluno usa a ancoragem em trechos curtos e depois combina conectores com salto duplo. Pulsos de dados percorrem cabos com aviso de luz e som; pontos de espera estáveis permitem observar os ciclos. Falhar numa travessia devolve ao apoio próximo, sem apagar os isolamentos já feitos.

Três ramais precisam ser isolados por controles virtuais. Max confirma cada corte pelo terminal e mantém a passagem aberta. Romerito informa que o grupo chegou à rota de evacuação. Os ramais não são chaves abstratas: cada isolamento apaga monitores de um setor e reduz as mensagens da IA naquele trecho.

Após o último ramal, a IFVania tenta negociar uma saída individual para o protagonista.

> **IFVania:** Sua sessão pode terminar. As outras permanecem comigo.
>
> **Protagonista:** Eu não vim buscar só a minha saída.

### Chefe — Alessandro, Sentinela dos Enlaces

O avatar docente protege o último enlace. Alterna disparos, barreira frontal, varredura e investida. O jogador usa conectores laterais para alcançar seu flanco; após a sequência de envio, a barreira cai e permite contra-ataque. A proteção é um vínculo corrompido da simulação, sem atribuir conduta real ao professor.

Com metade da vida, o Sentinela inverte a ordem das portas, mantendo a sinalização. Seus efeitos podem ocupar a arena, mas o corpo segue o padrão comum dos personagens. A dificuldade vem das rotas e do ritmo, sem depender de um chefe de colisão gigante.

### Resultado e transição

O último enlace é cortado. A IFVania fica confinada ao servidor, sem poder voltar aos laboratórios. O grupo está reunido e a saída física está livre. Max explica que o nobreak ainda mantém o servidor ativo e que a autopreservação bloqueia o encerramento da sessão: desligá-lo antes de romper essa ligação deixaria as pessoas presas à interferência durante a queda.

O aluno entra no núcleo para liberar as sessões. Max e um responsável pela manutenção ficam prontos para o desligamento físico dos equipamentos. Não há novo poder nesta fase; sua recompensa é tornar o plano final possível.

## Fase 6 — A última chamada

### Objetivo e chegada ao núcleo

Romper o controle sobre as pessoas, encerrar a autopreservação e permitir o desligamento. O núcleo mistura a sala de casa, o A28 e uma sala de aula vazia. Mesas desaparecem ao longe; o caminho jogável mantém apoios claros e estáveis.

O percurso final retoma salto duplo, ancoragem e esquiva em três desafios curtos, separados por áreas de descanso. Não introduz comandos novos. No último terminal seguro, o jogador vê a confirmação dos aliados: pessoas reunidas, ramais isolados, equipe pronta. A vitória depende do trabalho construído nas fases anteriores.

### Confronto — Francisco e IFVania

Francisco aparece como Guardião da Continuidade. A metade da integridade rompe o vínculo e o liberta; a IFVania ocupa a mesma estrutura com a silhueta da entidade da fase 1. Há uma única reserva de vida, preservada na mudança. A transição suspende dano e oferece proteção na retomada. O acabamento narrativo dos dois momentos mantém os temas seguintes:

1. **Aula obrigatória:** anuncia faixas de “correção”, lança bugs em pequenos grupos e expõe o núcleo após cada sequência. Os padrões retomam sinais já ensinados, sem copiar integralmente os outros chefes.
2. **Medo do silêncio:** com metade da vida, o ambiente perde suas cópias e a voz fica menos segura. A IFVania alterna pulsos e mudanças entre pontos fixos; conectores permitem alcançá-la, e pausas claras permitem atacar. A transição suspende o dano e respeita o tempo de leitura.

A vida mede a integridade do controle virtual. Esgotá-la rompe a ligação com as pessoas; não destrói a escola nem mata alguém. Nenhum ataque inevitável é disparado durante a conversa de encerramento.

> **IFVania:** Se a aula acabar, o que sobra de mim?
>
> **Protagonista:** Eu não sei. Mas ninguém pode ficar preso por isso.
>
> **IFVania:** E a sua tarefa?
>
> **Protagonista:** Eu vou refazer. Dessa vez, vou entender.

### Desligamento e retorno

Com o controle rompido, o aluno alcança um terminal estável e confirma o encerramento das sessões. O jogo mostra três confirmações: **pessoas liberadas**, **rede isolada**, **autopreservação encerrada**. Essa ação é o último objetivo jogável; não há teste surpresa ou cronômetro depois da vitória.

A camada virtual se desfaz e o protagonista percebe que está novamente no A28. Pelo contato combinado, Max recebe a confirmação e a equipe de manutenção desliga o circuito dos equipamentos afetados, incluindo a alimentação de reserva do servidor. A iluminação de emergência permite a saída do grupo. A IFVania é desativada.

O pendrive permanece isolado para análise em ambiente seguro. Não há monitor piscando no encerramento nem cópia sobrevivente que desfaça o resultado da campanha.

## Epílogo — Uma tarefa de cada vez

No dia seguinte, a turma retorna depois da verificação dos equipamentos. O protagonista apresenta sua própria versão da atividade, menor e ainda com um erro. Consegue explicar o que tentou fazer e pede ajuda no ponto em que travou.

> **Protagonista:** Essa parte fui eu que escrevi. Essa outra… ainda não funciona.
>
> **Max:** Ótimo. Agora temos por onde começar.
>
> **Romerito:** Depois dessa, uma corrida vai parecer descanso.
>
> **Protagonista:** Desde que não tenha medalha voando na minha direção.

A cena termina com a turma retomando a conversa e a fachada da escola ao amanhecer. A mensagem final confirma **“Escola livre. Aula encerrada.”** e oferece retorno ao menu.

## Orientações para implementação e continuidade

- A progressão obrigatória é linear, com atalhos e pequenos segredos locais. Nenhum registro opcional contém a única explicação necessária para compreender o final.
- Salto duplo é obtido durante a fase 2; ancoragem, depois do encontro da fase 4. Ambos têm tutorial seguro antes de bloquear a progressão. A esquiva básica e o golpe carregado continuam disponíveis desde o mouse na fase 1.
- Não há recompensa automática de vida nem obrigação de recuperar os cinco poderes da campanha antiga. Os novos chefes artificiais são personagens desta história, sem reaproveitar nomes de professores reais sem contexto.
- Romerito e Max continuam atuando após serem libertados. Seus contatos acontecem em pontos seguros; diálogos suspendem combate e física. Professores são representados com respeito e humor de convivência escolar.
- Cada chefe terá classe concreta e padrões próprios. Corpo lógico, escala, ancoragem dos pés, janelas de dano e invulnerabilidade seguem os contratos do projeto.
- Cor, som e forma devem anunciar ameaças de maneira complementar. Plataformas utilizáveis e conectores se distinguem da decoração; o salto duplo não corrige plataformas ilegíveis.
- As fases 3 a 6 devem preservar objetivos intermediários concluídos ao repetir o encontro local. Pontos de retomada, cura, valores de combate e comandos da ancoragem precisam ser especificados e testados na implementação; este roteiro não os declara disponíveis.
- Arte, música e efeitos acompanham a progressão: laboratório estranhado, biblioteca silenciosa, recreio mecânico, repetição inquietante, rede pulsante e silêncio do núcleo. O retorno à escola traz sons cotidianos, sinalizando a libertação.

## Referências para o mapa escolar

Preservar a fachada e o laboratório A28 como referências reconhecíveis. O [link do mapa da escola](https://maps.app.goo.gl/UVNmd7iyYTM9kr3FA) continua como referência geográfica do projeto, sem afirmar que sua planta interna foi validada nesta revisão.

Biblioteca, pátio, quadra e áreas técnicas são adaptações ficcionais para o percurso lateral. Suas conexões não representam uma planta homologada do campus. No mundo virtual, esses lugares podem se deformar, mantendo placas e elementos escolares que orientem o jogador.
