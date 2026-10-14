# Documento de Requisitos — Escola dos Bugs

**Título do projeto:** Escola dos Bugs — A Vingança dos Professores  
**Versão do documento:** 1.0  
**Data:** 10/09/2026  
**Método:** análise estática do código-fonte, dos recursos e do README.

## 1. Objetivo e alcance do documento

Documentar os requisitos identificados na versão disponível do projeto, permitindo compreender seu funcionamento, orientar manutenção e estabelecer critérios de aceite verificáveis.

Este documento foi elaborado por engenharia reversa. Os requisitos classificados como **implementados** possuem suporte no código, mas essa classificação não representa aprovação em teste de execução. As divergências entre a documentação original e o comportamento programado estão registradas na seção 10. Recomendações dessa seção não constituem alterações já aprovadas.

Não foram executados testes de jogabilidade, desempenho ou compatibilidade durante esta análise. O README menciona uma validação automatizada anterior do fluxo completo, porém o respectivo script não foi encontrado entre os arquivos analisados.

## 2. Visão geral do produto

O produto é um jogo local, para um jogador, de plataforma 2D com elementos de metroidvania, desenvolvido em Python e Pygame. O protagonista é um aluno que percorre uma escola infectada pelo vírus fictício CODIGO.EXE e enfrenta seis professores de programação corrompidos.

A campanha progride linearmente. Cada um dos cinco primeiros chefes deixa um item que concede uma habilidade. A derrota do sexto chefe permite alcançar a saída final e concluir o jogo. Não há mapa interligado nem retorno a fases anteriores implementados.

O contexto escolar, os diálogos sobre programação e a estrutura orientada a objetos favorecem o uso didático do projeto. O público de estudantes e professores é inferido do README; não há especificação formal de faixa etária ou classificação indicativa.

### 2.1 Escopo incluído

- Menu inicial, introdução narrativa, apresentação de fase, pausa, derrota e vitória.
- Seis fases com plataformas, espinhos, inimigos comuns e um chefe por fase.
- Movimento, salto, combate corpo a corpo e cinco habilidades coletáveis.
- Vida, dano, invulnerabilidade temporária e recuperação de vida.
- Diálogos, câmera de acompanhamento, HUD e animações por sprites.
- Carregamento de imagens e geração opcional da arte por script.

### 2.2 Recursos ausentes do escopo implementado

Não foram encontrados salvamento persistente, contas, multiplayer, serviços de rede, ranking, inventário genérico, seleção de fase, dificuldade configurável, áudio, suporte a controle, remapeamento de teclas, localização para outros idiomas ou menu de configurações. A ausência desses recursos não representa, por si só, defeito.

## 3. Atores e ambiente

| Ator | Responsabilidade |
|---|---|
| Jogador | Iniciar a campanha, controlar o aluno, enfrentar inimigos, coletar habilidades e concluir as fases. |
| Mantenedor / professor / aluno desenvolvedor | Alterar código, mapas, diálogos, parâmetros e imagens; regenerar recursos quando necessário. |

Diretora, professores e Sistema são personagens ou emissores de mensagens internos à narrativa, não atores externos do software.

| Item | Condição identificada |
|---|---|
| Linguagem | Python; o README declara versão 3.9 ou superior, sem validação de compatibilidade nesta análise. |
| Dependência de execução | `pygame>=2.5.0`, conforme `requirements.txt`. |
| Dependência opcional | Pillow, somente para executar `generate_assets.py`. |
| Entrada | Teclado e evento de fechamento da janela. |
| Saída | Janela gráfica de 960 × 540 pixels. |
| Instalação | `pip install -r requirements.txt`. |
| Inicialização | `python main.py`, a partir da pasta do projeto. |
| Dados | Estado da partida em memória; mapas, diálogos e definições em código; imagens em arquivos PNG. |
| Conectividade | O fluxo de jogo analisado não utiliza rede; a instalação de dependências pode exigir acesso a um repositório de pacotes. |

Não há requisitos mínimos de CPU, memória, GPU ou matriz de sistemas operacionais homologados definidos no repositório.

## 4. Requisitos funcionais

**Status:** I = implementado segundo análise estática. As ressalvas da seção 10 prevalecem sobre descrições genéricas do README. Os critérios abaixo descrevem verificações a executar, não resultados de testes realizados.

### 4.1 Sessão e narrativa

| ID | Requisito | Critério de aceite | Status / origem |
|---|---|---|---|
| RF-01 | O sistema deve apresentar um menu inicial com título, instrução para iniciar e controles básicos. | Ao iniciar o programa, o menu é exibido; Enter ou Espaço inicia uma campanha. | I — `game.py` |
| RF-02 | O sistema deve iniciar uma nova campanha na primeira fase, com vida inicial e sem habilidades adquiridas. | Iniciar novamente após retornar ao menu cria um novo jogador com 6 pontos de vida e conjunto vazio de habilidades. | I — `Game._start_story`, `Player.__init__` |
| RF-03 | O sistema deve apresentar a introdução geral da história antes da primeira fase. | A sequência `STORY_INTRO` é exibida antes do cartão da primeira fase. | I — `game.py`, `world/levels_data.py` |
| RF-04 | O sistema deve apresentar um cartão com o nome da fase antes de liberar o jogo. | Enter ou Espaço encerra o cartão; sem entrada, ele termina após o contador ultrapassar 90 atualizações. | I — `game.py` |
| RF-05 | O sistema deve exibir diálogos com identificação do falante e revelação progressiva do texto. | E, Enter ou Espaço revela imediatamente a fala incompleta; com a fala completa, avança; ao terminar, executa a transição prevista. | I — `ui/dialogue.py` |
| RF-06 | O sistema deve apresentar um diálogo antes do combate com cada chefe e outro após sua derrota. | Entrar no gatilho pré-chefe ativa o encontro e exibe o diálogo uma vez; derrotar o chefe exibe o diálogo de vitória uma vez. | I — `world/level.py` |
| RF-07 | O sistema deve permitir pausar e retomar a partida durante a exploração ou combate. | Esc alterna entre jogo e pausa; a atualização da simulação fica suspensa durante a pausa. | I — `game.py` |
| RF-08 | O sistema deve permitir encerrar a aplicação. | Fechar a janela encerra o loop; Esc encerra quando o estado não é jogo nem pausa, inclusive durante diálogos. | I — `game.py` |
| RF-09 | O sistema deve apresentar derrota quando a vida do jogador se esgotar. | Com o jogador morto, é exibida a tela de reprovação; Enter ou Espaço retorna ao menu. | I — `game.py` |
| RF-10 | O sistema deve apresentar vitória ao concluir a última fase. | Após derrotar Assembly e alcançar a saída, é exibida a mensagem de escola salva; Enter ou Espaço retorna ao menu. | I — `game.py`, `world/level.py` |

### 4.2 Personagem e combate

| ID | Requisito | Critério de aceite | Status / origem |
|---|---|---|---|
| RF-11 | O jogador deve poder mover o personagem horizontalmente e saltar. | Setas ou A/D movem; Espaço, W ou seta para cima inicia salto quando permitido; pisos e paredes sólidos limitam o deslocamento. | I — `entities/player.py`, `entities/character.py` |
| RF-12 | O sistema deve aplicar gravidade e limitar a velocidade de queda. | Fora de apoio, a velocidade vertical aumenta até o limite configurado; contato descendente com piso restaura a disponibilidade de saltos. | I — `entities/character.py`, `entities/player.py` |
| RF-13 | O jogador deve poder atacar corpo a corpo na direção para a qual está voltado. | X inicia uma área temporária de ataque; sobreposição com inimigos ou chefe ativo aplica dano, respeitando o intervalo para iniciar novo ataque. | I — `entities/player.py`, `world/level.py` |
| RF-14 | O sistema deve aplicar dano por contato com bugs, chefe, projéteis hostis e espinhos. | Contato válido reduz a vida; sem escudo, o jogador recebe invulnerabilidade temporária e impulso de reação. | I — `world/level.py`, `entities/player.py` |
| RF-15 | O sistema deve disponibilizar inimigos comuns que patrulham o cenário. | Bugs invertem a direção ao atingir parede ou ultrapassar o alcance de patrulha; são removidos quando a vida chega a zero. | I — `entities/enemy.py` |
| RF-16 | O sistema deve disponibilizar seis chefes, com identidade visual, nome, matéria e vida próprios. | Cada fase instancia o chefe correspondente da tabela da seção 6. | I — `entities/boss.py`, `world/level.py` |
| RF-17 | Os chefes devem atacar somente após a ativação do encontro. | Antes da ativação, não executam ataques nem recebem dano; após ela, alternam aleatoriamente entre investida, disparo triplo e disparos laterais. | I — `entities/boss.py` |
| RF-18 | Os chefes devem intensificar o combate conforme a vida restante. | Ao alcançar no máximo 50% e 20% da vida máxima, entram respectivamente nas fases 2 e 3, com aumento do multiplicador de movimento e redução do intervalo entre ataques. | I — `entities/boss.py` |
| RF-19 | O sistema deve gerenciar o ciclo de vida dos projéteis. | Projéteis desaparecem ao atingir sólidos ou esgotar 90 atualizações; os do jogador também são removidos ao atingir um inimigo ou chefe ativo. | I — `entities/projectile.py`, `world/level.py` |

### 4.3 Habilidades e progressão

| ID | Requisito | Critério de aceite | Status / origem |
|---|---|---|---|
| RF-20 | O sistema deve criar um item de habilidade após a derrota de cada um dos cinco primeiros chefes. | Um único item correspondente à fase aparece; a habilidade é concedida ao colidir com ele, e o item é removido. | I — `world/level.py`, `powerups.py` |
| RF-21 | O sistema deve permitir pulo duplo após coletar a recompensa de Scratch. | O jogador pode realizar um salto adicional no ar, respeitando o contador de saltos. | I — `entities/player.py` |
| RF-22 | O sistema deve permitir dash após coletar a recompensa de Python. | Shift esquerdo inicia impulso horizontal na direção atual, sujeito à duração e recarga configuradas. | I — `entities/player.py`, `settings.py` |
| RF-23 | O sistema deve permitir deslizamento lento e salto na parede após coletar a recompensa de Java. | Ao pressionar o movimento contra uma parede durante a queda, a descida é limitada; o comando de salto aplica impulso para cima e para longe da parede. Não há subida automática. | I — `entities/player.py` |
| RF-24 | O sistema deve permitir disparos após coletar a recompensa de C. | F cria um projétil horizontal na direção do personagem quando o intervalo entre tiros permite. | I — `entities/player.py` |
| RF-25 | O sistema deve permitir proteção com escudo após coletar a recompensa de SQL. | Q ativa o escudo quando disponível; o próximo dano válido é absorvido, desativa a proteção e inicia sua recarga. | I — `entities/player.py`; ressalva D-05 |
| RF-26 | O sistema deve restaurar a vida ao coletar uma habilidade e aumentar a vida máxima nas quatro primeiras recompensas. | As recompensas de Scratch, Python, Java e C acrescentam 1 ponto cada; SQL apenas restaura a vida até o máximo vigente. | I — `Player.grant_ability` |
| RF-27 | O sistema deve liberar a saída de cada fase somente após a derrota do respectivo chefe. | Antes da derrota, sobrepor a saída não avança; depois dela, a mesma ação carrega a próxima fase ou conclui a campanha. | I — `world/level.py` |
| RF-28 | O sistema deve conservar habilidades e vida máxima ao avançar de fase. | A próxima fase posiciona o jogador em seu início, conserva os poderes coletados e restaura toda a vida. | I — `Game._load_level` |
| RF-29 | O sistema deve reposicionar o jogador no início da fase se detectar queda abaixo do mapa. | Quando o topo do jogador ultrapassa a altura do mapa em mais de 200 pixels, o personagem retorna ao ponto inicial com vida cheia; a fase não é recriada. | I — `world/level.py`, `Player.respawn`; ressalva D-09 |

### 4.4 Mundo e apresentação

| ID | Requisito | Critério de aceite | Status / origem |
|---|---|---|---|
| RF-30 | O sistema deve construir seis mapas a partir de geração determinística. | Chamadas com as mesmas definições produzem as mesmas grades, com blocos, pontos de surgimento, chefe, gatilho de diálogo e saída. | I — `world/levels_data.py`, `world/tilemap.py` |
| RF-31 | A câmera deve acompanhar o jogador respeitando os limites da fase. | O deslocamento da câmera mantém-se entre zero e o limite calculado pelas dimensões do mapa e da janela. | I — `world/camera.py` |
| RF-32 | O HUD deve exibir vida atual e máxima, nome da fase e habilidades adquiridas. | Perda de vida e aquisição de habilidades refletem-se na interface; chefe ativo e vivo possui nome e barra de vida visíveis. | I — `ui/hud.py` |
| RF-33 | A interface deve apresentar dicas de controle conforme as habilidades adquiridas. | A dica de cada poder passa a integrar o texto de ajuda após sua coleta. | I — `ui/hud.py`; legibilidade a validar |
| RF-34 | O sistema deve representar estados do personagem e inimigos por sprites e efeitos visuais. | O aluno possui imagens de repouso, caminhada, salto e dash, com espelhamento por direção; bugs alternam dois quadros; chefes possuem balanço visual e indicação de fases de combate. | I — `entities/player.py`, `entities/enemy.py`, `entities/boss.py` |

## 5. Regras de negócio e parâmetros

| ID | Regra |
|---|---|
| RN-01 | A ordem da campanha é Scratch → Python → Java → C → SQL → Assembly. |
| RN-02 | O jogador começa com 6 pontos de vida. Coletando todas as recompensas, chega a 10 pontos de vida máxima. |
| RN-03 | Uma habilidade depende da coleta física do item. Derrotar o chefe ou concluir o diálogo não a concede diretamente. |
| RN-04 | A condição atual para avançar é derrotar o chefe e alcançar a saída. Coletar a recompensa não é obrigatório para a transição. |
| RN-05 | Habilidades e vida máxima são conservadas entre fases da mesma campanha; uma nova campanha recria o jogador. |
| RN-06 | Todos os chefes compartilham a mesma lógica de ataques. A escolha de ataque é aleatória, embora os mapas sejam determinísticos. |
| RN-07 | O chefe final não concede poder adicional. Sua derrota não encerra imediatamente a partida: é necessário alcançar a saída. |
| RN-08 | Inimigos comuns possuem 2 pontos de vida; dano de contato padrão, espinhos e projéteis usados no fluxo atual causam 1 ponto. |
| RN-09 | O ataque corpo a corpo aplica 1 ponto por atualização com sobreposição; não há controle de um único acerto por alvo em cada golpe. |
| RN-10 | Pausa, diálogos e cartões de fase suspendem a atualização normal do mundo. |
| RN-11 | O tempo de física e recargas é contado em atualizações; a taxa-alvo é 60 FPS. Queda de FPS pode alterar a duração real das ações. |

### 5.1 Parâmetros de referência

Valores extraídos de `settings.py` e das classes de entidades. São parâmetros atuais de balanceamento, não garantias de desempenho.

| Parâmetro | Valor |
|---|---|
| Bloco do cenário | 32 × 32 pixels |
| Velocidade horizontal básica | 4,2 pixels por atualização |
| Gravidade / velocidade máxima de queda | 0,65 / 15 |
| Impulso de salto / segundo salto | −12,5 / −10,5 |
| Dash | Velocidade 11; duração configurada de 10 atualizações; recarga de 35 |
| Ataque corpo a corpo | Temporizador inicial de 10 atualizações; intervalo de 20 para iniciar outro |
| Tiro do jogador | Velocidade 9; intervalo de 30 atualizações |
| Invulnerabilidade após dano sem escudo | 90 atualizações |
| Escudo após absorver dano | Recarga de 60; invulnerabilidade de 30 atualizações |
| Reposicionamento pelo método `respawn` | Vida cheia e invulnerabilidade de 60 atualizações |

## 6. Conteúdo da campanha

Os nomes abaixo seguem os valores efetivamente usados pelo jogo. A primeira sala aparece como “Sala de Iniciação” no README e na narrativa, mas seu cartão utiliza “Fase 1: Lógica de Blocos”.

| Fase | Nome exibido após o número | Chefe | Vida do chefe | Recompensa | Largura em blocos | Bugs |
|---|---|---|---:|---|---:|---:|
| 1 | Lógica de Blocos | Prof. Scratch | 16 | Pulo Duplo | 46 | 3 |
| 2 | Laboratório de Lógica | Prof. Python | 20 | Dash Veloz | 52 | 4 |
| 3 | Sala de POO | Prof. Java | 24 | Escalada de Parede | 58 | 5 |
| 4 | Sala de Memória | Prof. C | 28 | Tiro de Ponteiro | 64 | 6 |
| 5 | Biblioteca de Dados | Prof. SQL | 32 | Escudo de Dados | 70 | 7 |
| 6 | Núcleo do Sistema | Prof. Assembly | 40 | Nenhuma | 78 | 8 |

Todos os mapas possuem 17 blocos de altura. A geração usa sementes `1000 + índice × 37`, com índice iniciado em zero. O cenário inclui bordas sólidas, piso, degraus, pequenos vãos, plataformas e possíveis espinhos conforme a geração.

## 7. Interfaces e controles

| Comando | Contexto / efeito |
|---|---|
| ← / → ou A / D | Movimento horizontal durante o jogo. |
| Espaço / W / ↑ | Salto; com poderes adquiridos, segundo salto ou salto de parede. |
| X | Ataque corpo a corpo. |
| Shift esquerdo | Dash, após sua aquisição. Shift direito não é tratado pelo código. |
| Movimento contra a parede + salto | Deslizamento lento e salto de parede, após adquirir a habilidade de Java. |
| F | Tiro, após sua aquisição. |
| Q | Ativação do escudo, quando adquirido e disponível. |
| E / Enter / Espaço | Revelar ou avançar fala durante diálogo. |
| Enter / Espaço | Iniciar campanha no menu, dispensar cartão de fase ou retornar ao menu após derrota/vitória. |
| Esc | Pausar durante jogo; retomar durante pausa; encerrar nos demais estados. |
| Fechar janela | Encerrar a aplicação. |

Os textos da interface e da narrativa estão em português. O jogo não oferece formulário, API pública ou integração com sistemas externos.

## 8. Requisitos não funcionais e restrições técnicas

| ID | Requisito ou restrição | Evidência e forma de verificação |
|---|---|---|
| RNF-01 | O jogo deve executar localmente em Python com Pygame. | `main.py` e `requirements.txt`; verificar instalação e inicialização em cada plataforma a homologar. |
| RNF-02 | A apresentação deve usar resolução fixa de 960 × 540 pixels. | `settings.py` e `pygame.display.set_mode`; verificar dimensões da janela. Não há redimensionamento configurado. |
| RNF-03 | O loop deve usar limitação configurada para 60 FPS. | `clock.tick(settings.FPS)`; existe controle de taxa, mas a manutenção de 60 FPS requer medição em hardware definido. |
| RNF-04 | A simulação de campanha deve funcionar sem comunicação de rede. | Não há chamadas de rede no fluxo analisado; verificar execução com dependências previamente instaladas e sem conectividade. |
| RNF-05 | A arquitetura deve separar controle de estados, entidades, mundo, interface, configurações e recursos. | Módulos correspondentes no repositório; revisar responsabilidades e dependências ao alterar funcionalidades. |
| RNF-06 | Personagens devem compartilhar uma base abstrata para estado e comportamento comum. | `Character` utiliza `ABC` e `update` abstrato; `Player`, `Enemy` e `Boss` especializam o comportamento. |
| RNF-07 | O carregamento de imagens deve reutilizar recursos em cache e suportar espelhamento. | `assets.load_image` e `assets.load_flipped`; verificar reutilização para caminho e tamanho equivalentes. |
| RNF-08 | A ausência de arquivo de imagem deve resultar em substituto visual e aviso, permitindo continuar a execução. | `assets.py`; verificar com caminho inexistente. O tratamento não cobre necessariamente PNG corrompido ou erro de leitura. |
| RNF-09 | A arte deve poder ser substituída preservando caminhos e nomes de arquivos. | Carregamento centralizado em `assets/images`; reiniciar o processo para avaliar a nova arte. Não há monitoramento de mudanças em tempo real. |
| RNF-10 | O projeto deve permitir regenerar sua arte por ferramenta opcional separada da execução do jogo. | `generate_assets.py` utiliza Pillow; o jogador não precisa executar esse script para usar os PNG existentes. |

Usabilidade, acessibilidade, consumo de recursos e compatibilidade ainda não possuem metas quantitativas ou homologação documentada. Não se presume conformidade com padrões externos.

## 9. Fluxos e critérios de validação integrada

### UC-01 — Iniciar e jogar uma campanha

**Ator:** jogador. **Pré-condição:** aplicação no menu.

1. O jogador pressiona Enter ou Espaço.
2. O sistema cria a primeira fase e um personagem sem poderes.
3. O sistema apresenta a introdução geral e, em seguida, o cartão da fase.
4. O jogador percorre plataformas e enfrenta bugs.
5. O jogador alcança o gatilho de diálogo do chefe.
6. O sistema apresenta o diálogo e libera o combate após seu término.

**Resultado esperado:** exploração e combate ocorrem na fase atual, com atualização da vida e da interface.

### UC-02 — Derrotar chefe, adquirir habilidade e avançar

**Ator:** jogador. **Pré-condição:** chefe ativo e jogador vivo.

1. O jogador reduz a vida do chefe a zero.
2. O sistema registra a derrota, cria a recompensa quando prevista e apresenta o diálogo de vitória.
3. Após o diálogo, o jogador toca o item para adquirir a habilidade.
4. O sistema atualiza habilidades, vida e HUD.
5. O jogador alcança a saída.
6. O sistema carrega a próxima fase, preservando poderes e vida máxima, ou apresenta vitória após a sexta saída.

**Alternativa existente:** o jogador pode alcançar a saída sem coletar o item; o código permite avançar sem a habilidade.

### UC-03 — Pausar, perder e recomeçar

**Ator:** jogador. **Pré-condição:** partida em andamento.

- Ao pressionar Esc durante o jogo, a simulação para; ao pressionar novamente, continua.
- Ao perder toda a vida, o sistema apresenta derrota.
- Enter ou Espaço retorna ao menu; iniciar outra campanha reinicia a progressão.
- Fechar a aplicação perde o estado da campanha, pois não existe salvamento persistente.

### 9.1 Roteiro mínimo de aceite proposto

| ID | Verificação | Requisitos relacionados |
|---|---|---|
| CA-01 | Iniciar uma campanha, avançar falas e entrar na primeira fase; repetir após derrota e verificar reinício. | RF-01 a RF-05, RF-09 |
| CA-02 | Exercitar movimento, colisões, salto, ataque e dano; observar vida e invulnerabilidade. | RF-11 a RF-15, RF-32 |
| CA-03 | Ativar cada chefe e verificar as transições nos limites de 50% e 20% de vida. | RF-06, RF-16 a RF-18 |
| CA-04 | Confirmar indisponibilidade dos cinco poderes antes da coleta e seu funcionamento depois dela. | RF-20 a RF-26 |
| CA-05 | Tentar sair antes e depois da derrota do chefe, incluindo tentativa sem coletar o item. | RF-27, RN-03, RN-04 |
| CA-06 | Avançar entre as seis fases e verificar manutenção das habilidades, recuperação da vida e vitória somente na saída final. | RF-10, RF-28, RN-07 |
| CA-07 | Pausar e dialogar enquanto há inimigos e projéteis; verificar suspensão da atualização do mundo. | RF-05, RF-07, RN-10 |
| CA-08 | Verificar câmera e legibilidade do HUD com todas as habilidades e o chefe ativo. | RF-31 a RF-34 |
| CA-09 | Simular posição abaixo do limite do mapa e confirmar reposicionamento, vida cheia e conservação do estado da fase. | RF-29 |
| CA-10 | Usar caminho de imagem inexistente e confirmar substituto visual; verificar cache e reinício após troca de arte. | RNF-07 a RNF-09 |

Esses cenários precisam ser executados para homologar o comportamento; a leitura do código não confirma equilíbrio de dificuldade nem a possibilidade de completar todas as fases por comandos normais.

## 10. Divergências, limitações e decisões pendentes

| ID | Constatação | Impacto / encaminhamento proposto |
|---|---|---|
| D-01 | O README afirma que cada fase começa com diálogo contextual, mas `intro_dialogue` é apenas armazenado nas definições. O fluxo exibe a introdução geral e cartões de fase. | Decidir entre integrar os diálogos individuais ao fluxo ou ajustar a descrição do produto. |
| D-02 | Comentários sugerem padrões próprios de cada chefe, e o README descreve Assembly usando todas as habilidades aprendidas. A implementação de ataques é compartilhada e não trata Assembly de forma especial. | Definir se chefes precisam de comportamentos exclusivos; a versão atual diferencia identidade e vida. |
| D-03 | O diálogo anuncia “Habilidade adquirida” antes de o jogador tocar no item. | Alinhar a mensagem à coleta efetiva ou alterar a forma de concessão, mediante decisão de produto. |
| D-04 | A saída exige somente derrota do chefe, sem exigir coleta da recompensa ou uso de habilidade. | A progressão por poderes não é imposta como bloqueio. Decidir se isso atende ao objetivo de metroidvania linear. |
| D-05 | `_toggle_shield` sugere ligar/desligar, mas a atualização mantém a recarga em 10 enquanto o escudo está ativo, impedindo normalmente desligá-lo por Q após uma atualização. | Definir se o escudo deve ser consumível até o próximo dano ou alternável; revisar implementação e ajuda conforme a decisão. |
| D-06 | “Escalada de Parede” corresponde a deslizamento lento e salto na parede; não há escalada automática ao segurar a direção. | Ajustar a instrução ou especificar uma mecânica adicional de subida. |
| D-07 | O README cita Shift genericamente e Esc como pausa. O código aceita somente Shift esquerdo e encerra com Esc fora de jogo/pausa. | Tornar os controles documentados consistentes com o comportamento desejado. |
| D-08 | Um golpe corpo a corpo pode aplicar dano em atualizações consecutivas ao mesmo alvo. | Avaliar equilíbrio do combate e decidir se cada golpe deve acertar uma única vez por alvo. |
| D-09 | Há recuperação por queda abaixo do mapa, mas os mapas gerados possuem uma borda inferior sólida. | O mecanismo existe; seu acionamento por jogabilidade normal não foi demonstrado. |
| D-10 | O README descreve pixel art sem suavização; `assets.py` usa `smoothscale` quando o tamanho da imagem difere do solicitado. | Definir se a preservação de bordas duras deve valer também para imagens substituídas em outras dimensões. |
| D-11 | O HUD acrescenta todas as dicas em uma única linha, sem quebra ou ajuste automático. | Verificar legibilidade com todos os poderes na janela fixa antes de homologar a interface. |
| D-12 | O README registra teste automatizado anterior, mas não há suíte ou script correspondente nos arquivos analisados. | Disponibilizar um roteiro reproduzível ou testes do fluxo para sustentar futuras homologações. |

As decisões acima devem ser priorizadas pelo responsável pelo projeto. Não foram atribuídos níveis de prioridade de negócio sem validação desse responsável.

## 11. Rastreabilidade técnica

| Arquivo / módulo | Responsabilidade e requisitos principais |
|---|---|
| `main.py` | Inicialização da aplicação; RNF-01. |
| `game.py` | Estados, campanha, cartões, pausa, derrota, vitória e troca de fase; RF-01 a RF-10, RF-28. |
| `settings.py` | Resolução, taxa-alvo, física e intervalos; RF-12, RF-22, RNF-02 e RNF-03. |
| `entities/character.py` | Base abstrata, vida, gravidade e colisão; RF-11, RF-12, RNF-06. |
| `entities/player.py` | Entradas, combate, poderes, dano, recuperação e animação; RF-11 a RF-14, RF-21 a RF-26, RF-29 e RF-34. |
| `entities/enemy.py` | Bugs, patrulha e remoção por morte; RF-15 e RF-34. |
| `entities/boss.py` | Definições, ativação, ataques e fases dos chefes; RF-16 a RF-18 e RF-34. |
| `entities/projectile.py` | Movimento, colisão e expiração de projéteis; RF-19. |
| `world/level.py` | Integração da fase, combate, gatilhos, recompensas e saída; RF-06, RF-13, RF-14, RF-20, RF-27 e RF-29. |
| `world/levels_data.py` | Campanha, geração de mapas, ordem de recompensas e textos; RF-03, RF-16, RF-20 e RF-30. |
| `world/tilemap.py` | Interpretação dos símbolos de mapa em geometria e gatilhos; RF-30. |
| `world/camera.py` | Acompanhamento e limites da câmera; RF-31. |
| `powerups.py` | Tipos, nomes e representação dos itens de habilidade; RF-20. |
| `ui/dialogue.py` | Apresentação e avanço de falas; RF-05. |
| `ui/hud.py` | Vida, habilidades, chefe e ajuda; RF-32 e RF-33. |
| `assets.py` e `assets/images/` | Carregamento e arquivos visuais; RNF-07 a RNF-09. |
| `generate_assets.py` | Geração opcional das imagens; RNF-10. |
| `README.md` e `requirements.txt` | Proposta, instruções de uso e dependências declaradas. |

## 12. Glossário

| Termo | Significado neste projeto |
|---|---|
| Metroidvania | Referência de gênero baseada em exploração e aquisição de habilidades; aqui adaptada a uma campanha linear. |
| HUD | Elementos de interface sobrepostos ao jogo, como vida, habilidades e barra do chefe. |
| Power-up | Item coletável que concede uma habilidade durante a campanha. |
| Sprite | Representação gráfica de personagem, objeto ou elemento visual. |
| Tile / bloco | Unidade de 32 × 32 pixels usada na construção dos mapas. |
| Gatilho | Região que dispara uma ação ao ser tocada pelo jogador. |
| Respawn | Reposicionamento do personagem no ponto inicial da fase. |
| Dash | Impulso horizontal de curta duração. |
| Atualização / frame | Passo do loop de jogo usado para movimento, temporizadores e processamento de regras. |
