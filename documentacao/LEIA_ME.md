# IFVania

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


## Comportamento vigente — fechamento de 16/11/2026

Q segurado oferece bloqueio frontal após descobrir o mouse, com resistência limitada e quebra de guarda; costas e perigos ambientais exigem reposicionamento/esquiva. A guarda reduz movimento e não permite ataque simultâneo. M alterna áudio também na pausa. Pausa, foco e transições cancelam guarda e cargas.

SpeedBug considera deslocamento real, colisões e retorno dos limites, com reposicionamento entre ataques. As quatro fases novas incluem poses dedicadas, Max com origem móvel/invocações, ricochetes e portas sequenciais. Biblioteca oferece atalhos por consulta e bilhete; quedas nas novas travessias retornam ao apoio seguro com custo de uma integridade, mínimo um. Revisitas concluídas não reiniciam chefes nem curam. Desfecho inclui monitores/nobreak desligados, pendrive isolado, sala física e fachada iluminada.

Implementação técnica concluída; [revisão humana final](REVISAO_HUMANA_FINAL.md) documenta decisões e homologação adiada. Evidências: 172 testes e 15 exportadores em temporário (203 PNGs). Registros anteriores abaixo descrevem a evolução e cedem a esta atualização quando divergirem.


## Evolução em andamento — campus virtual e hack and slash

Design em [PROPOSTA_HACK_AND_SLASH.md](PROPOSTA_HACK_AND_SLASH.md), etapas em [PLANO_HACK_AND_SLASH.md](PLANO_HACK_AND_SLASH.md) e estado técnico em [ARQUITETURA_HACK_AND_SLASH.md](ARQUITETURA_HACK_AND_SLASH.md). A primeira versão integrada oferece seis fases, campus controlável entre elas, combo de três golpes, ataques direcionais, ancoragem, quatro novos guardiões e desfecho. Factory, State Machine, Command, Strategy e Observer estão em uso. O registro de progresso é em memória, sem salvamento em disco. Trata-se de uma base funcional para refinamento; avaliação humana final foi adiada pelo usuário, sem bloquear implementação.

Jogo de plataforma 2D em **Python + Pygame**, com arquitetura orientada a objetos.
Escolha Menino ou Menina e acompanhe a revolta da IFVania, uma inteligência artificial
que assume o controle dos computadores da escola.

O fluxo inclui aula, A28, RomerBug/SpeedBug, biblioteca/Indexador e quatro novas
fases: Recreio em repetição, Laboratório das cópias, Rede sem saída e A última
chamada. Saídas retornam ao campus; o jogador caminha até as próximas entradas.
Depois do núcleo, retorna ao A28 pelo jardim e confirma o encerramento. O
[relatório da revisão](../avaliacao/hack_and_slash/RELATORIO.md) distingue implementação,
testes, capturas e limitações de conteúdo/apresentação.

## Como executar

Código central em `sistema/`, ferramentas em `ferramentas/` e documentos nesta
pasta. Veja o [mapa da reorganização](REORGANIZACAO.md) para estrutura, inventário,
remoções e comandos de manutenção. Recursos são resolvidos pelo local dos
módulos: de outro diretório, execute `python /caminho/ifvania/principal.py`.

Em um ambiente Python com as dependências instaladas:

```bash
pip install -r configuracao/dependencias.txt
python principal.py
```

Dependência declarada: `pygame>=2.5.0`. Este incremento foi verificado com
Python 3.14.4 e pygame-ce 2.5.8, que fornece o módulo `pygame`. As validações
anteriores usaram Python 3.9.6 e Pygame 2.6.1.

## Fluxo disponível

1. Menu com fachada em pixel art, Jogar e Sair; navegação por clique ou setas/Enter.
2. Escolha Menino/Menina, com prévia animada e confirmação por botão ou Enter.
3. Digitação do nome (obrigatório, até 20 caracteres); Enter confirma e Esc volta.
   A aula começa com o aluno conversando com Max, sem narrador, sobre a tarefa
   produzida por IA, com lembrança visual do quarto e jantar. Monitores exibem
   a execução e a corrupção; colegas sentados são hipnotizados diante das telas.
4. Pátio coberto navegável inspirado nas fotos do IFRN, entrada no A28 e encontro com Romerito por **E**.
5. Investida de Romerito e sucção dos dois personagens para um monitor,
   com trajetória, rotação e redução visual antes da chegada ao mundo virtual.
6. Descoberta do mouse na bolsa; o chicote é liberado ao terminar esse diálogo.
7. Percurso com bugs e degraus de 32 ou 64 pixels, alcançável com o salto básico.
8. Reencontro com Romerito humano, fala sobre Brasília e corridas e infecção por um bug.
9. RomerBug alterna dois aviões espaçados, pausa e investida; com até 50% da
   vida, vira SpeedBug, que lança duas medalhas com pouco deslocamento e depois
   faz uma pausa, investida anunciada e recuperação.
10. A derrota encerra ameaças e libera a saída, sem conceder poderes. Voltar ao
    campus e usar E na porta da biblioteca permite continuar.
11. Três terminais fornecem o mapa e os registros da rede. E examina o módulo
    que libera salto duplo e consulta os arquivos; o portão exige as três consultas.
12. Indexador alterna faixas de ataque e fichas. Sua saída retorna à convivência;
    caminhar até o ginásio e usar E abre Recreio em repetição.
13. Três travas e Elias abrem caminho pelo jardim, ponto seguro A28 e bloco M1.
14. Comparar registros e libertar Max revela a autopreservação e libera ancoragem.
15. Três ramais e Alessandro permitem isolar a rede e seguir ao LIT.
16. Francisco e IFVania compartilham a integridade do último encontro. Após a
    vitória, percorrer o campus até o ponto A28 no jardim e confirmar com E.
17. Confirmações, desligamento pelos aliados e epílogo dialogado encerram a campanha.

O prólogo e a fase virtual funcionam com os dois protagonistas, com os mesmos
atributos e corpo lógico de 40 × 40 pixels. Protagonista, bosses, professores
e entidade são apresentados em 80 × 80 pixels, em todas as cenas e animações.
Os bugs permanecem em 40 × 40. Os pés, as colisões e a geometria do mapa são
preservados. A escolha do protagonista e o nome permanecem nas transições. O nome identifica
as falas do aluno e aparece nas respostas dos professores. Não há gravação do
nome em disco. A caminhada usa oito quadros por personagem, sincronizados com
a distância percorrida; ao encontrar uma parede, o personagem para de caminhar.
O corredor é uma adaptação de cenário; o traçado interno real não foi homologado.
A referência oficial de A28 está no [documento de requisitos](DOCUMENTO_DE_REQUISITOS.md).

## Controles

| Comando | Ação |
|---|---|
| Setas esquerda/direita ou A/D | Mover |
| Espaço / W / seta para cima | Salto básico |
| Tocar e soltar X, K ou botão esquerdo do mouse | Golpe rápido de mouse com cabo reforçado: 1 de dano |
| Segurar X, K ou botão esquerdo do mouse por 0,6 s e soltar | Golpe carregado: 2 de dano |
| Shift | Esquiva curta, após encontrar o mouse; recarga de 0,9 s |
| E | Entrar no A28 / falar com Romerito / consultar terminais e módulo na biblioteca |
| Salto novamente no ar | Salto duplo após examinar o módulo na biblioteca |
| Toques consecutivos no ataque | Combo de três golpes: rápido, alcance e empurrão |
| Cima ao soltar ataque | Laçada ascendente |
| Baixo ao soltar ataque no ar | Finalização descendente |
| E junto aos anéis luminosos | Ancoragem após libertar Max; interações têm prioridade |
| E nas bordas dos setores do campus | Seguir ou voltar pelo campus |
| R na derrota | Retomar fase; biblioteca conserva módulo/consultas, expansão conserva objetivos; Enter volta ao menu |
| E / Enter / Espaço | Revelar ou avançar diálogo |
| Esc | Pausar e retomar exploração, combate, abdução e infecção |
| Enter / Espaço | Confirmar seleção, dispensar cartão ou voltar ao menu no encerramento |
| Esc na seleção | Voltar ao menu |
| Sair no menu / fechar janela | Encerrar a aplicação |

Salto duplo é obtido no módulo da biblioteca, sem cura ou aumento de vida.
Ancoragem é obtida após Max; dash antigo, escalada, tiro e escudo continuam fora da progressão principal.
Entrada em fase e retomada restauram a integridade atual, sem aumentar sua capacidade.

## Combate

O mouse mantém sua identidade de arma improvisada: carcaça gasta, cinta metálica
e cabo reforçado, com rastro discreto, som seco e pausa de impacto de 2–3 quadros.
O chicote tem alcance básico de 100 pixels, ampliado em 12/22 nos golpes 2/3 do combo, e tolerância em torno da curva;
paredes bloqueiam os golpes. Cada alvo recebe no máximo um acerto por golpe.
A direção fica fixada ao soltar o comando que iniciou a carga. Durante a carga, é possível andar a 75% da
velocidade, saltar e virar. Dano, diálogos e transformação cancelam a carga;
pausa e perda de foco descartam comandos pendentes sem disparar na retomada.

A velocidade máxima do aluno é 3,2 pixels por quadro, com aceleração e frenagem
curtas. O salto tem tolerância de 100 ms na borda e memória de 100 ms antes do
pouso. O recuo afasta o aluno da origem do dano e dura oito quadros. A esquiva
dura 15 quadros, com proteção nos oito quadros centrais; não pode interromper
a preparação ou a parte ativa do golpe, mas cancela a carga e o recolhimento.
O HUD informa carga e recarga da esquiva, e a descoberta do mouse ensina os comandos.

As bancadas e degraus sólidos têm contorno, tampo claro e faixa de segurança.
Só superfícies realmente expostas recebem a faixa; juntas internas não parecem
plataformas adicionais. A geometria física do mapa permanece a mesma.

Romerito permanece humano e sem dano de contato durante a conversa. A infecção
dura 60 atualizações, conserva posição, tamanho e vida e só libera ataques ao
terminar. Pausar congela esse efeito e os demais temporizadores.

RomerBug e SpeedBug são duas formas da mesma instância da classe `RomerBug`.
Na campanha atual, a transformação a 50% é uma cena: RomerBug cai de joelhos,
a câmera aproxima e uma entidade aparece para dizer **“Ainda não terminou.”**
A fala aguarda E/Enter. Seguem a metamorfose, a subida de SpeedBug e o retorno
suave da câmera. A cena dura aproximadamente 3,8 segundos, além do tempo de leitura.
Ela preserva vida, posição e dimensões; não causa nem recebe dano e limpa
projéteis e ataques em andamento. Esc pausa em qualquer trecho, inclusive na fala.
A retomada restaura o movimento do protagonista e oferece 60 atualizações de
proteção. Nas duas formas, o boss alterna lançamentos e investida. RomerBug
lança dois aviões separados por 2,3 s. SpeedBug lança duas medalhas separadas
por 1,5 s e se desloca no máximo 24 pixels para cada lado durante o ciclo.

Após os lançamentos, há uma pausa e espera pelos projéteis saírem de cena.
A investida tem preparação corporal e direção fixa e respeita paredes. RomerBug prepara
por 0,8 s e recupera por 1 s; SpeedBug prepara por 0,6 s e recupera por 1,3 s.
Não há dano corporal passivo nem projéteis simultâneos à investida. Os parâmetros
estão em [documentacao/PROPOSTA_CHEFE_ROMERBUG.md](PROPOSTA_CHEFE_ROMERBUG.md). A sobrecarga
no piso foi retirada nesta revisão.

Ao derrotar o boss, os projéteis dele e do jogador e os bugs restantes são
removidos. Não há recompensa coletável nem aumento de vida. A conversa posterior
deixa claro que o objetivo de desligar a energia ainda precisa ser cumprido.

## Arquitetura

| Área | Responsabilidade |
|---|---|
| `sistema/jogo.py` | Estados, seleção, prólogo, abdução, infecção e fim do conteúdo |
| `sistema/configuracoes.py` | Dimensões comuns, resolução, física e temporizadores |
| `entidades/personagem.py` | Base abstrata dos personagens |
| `entidades/jogador.py` / `chicote_mouse.py` | Protagonistas, movimento, arma e animações |
| `entidades/professor.py` | Max e Romerito humano |
| `entidades/chefe.py` / `romer_bug.py` | Base abstrata de boss e encontro RomerBug/SpeedBug |
| `entidades/chefes_professores.py` | Classes e estratégias dos professores antigos |
| `mundo/escola.py` / `dados_escola.py` | Sala, corredor, A28 e eventos do prólogo |
| `mundo/dados_fases.py` | Mapa fixo e diálogos da campanha atual |
| `mundo/fases_antigas.py` | Mapas, diálogos e recompensas da campanha antiga |
| `mundo/fase.py` | Combate, reencontro, saída e limpeza após a derrota |
| `mundo/mapa_blocos.py` / `camera.py` | Colisões, pontos de surgimento e câmera |
| `interface/` | Tema, menu, seleção, diálogos e HUD |
| `mundo/transicao_chefe.py` | Cena dos 50%, entidade, metamorfose e zoom visual |
| `mundo/escola_sombria.py` | Fundo escolar e bancadas, sem alterar colisões |
| `mundo/arte_escolar.py` / `terminal.py` | Arte em camadas e informações animadas nos monitores |
| `sistema/recursos.py` | Cache, substitutos visuais e normalização dos sprites |

Cada boss possui classe concreta própria. A base `Chefe` exige uma estratégia
especializada, e tipos desconhecidos não recebem uma implementação genérica.

A campanha antiga de seis professores fica fora do menu principal. Seus dados
continuam disponíveis por `build_legacy_levels()` em `mundo/fases_antigas.py`,
para manutenção e regressão. Seus poderes e diálogos não são requisitos da
campanha atual.

## Arte

As fontes, referências e prompts estão em [recursos/fontes_arte/LEIA_ME.md](../recursos/fontes_arte/LEIA_ME.md).
Os sprites preservam proporções, usam uma escala comum entre poses e têm os pés
alinhados dentro do corpo de 40 × 40 pixels. Armas e projéteis possuem áreas próprias.

Para reexportar as artes existentes com Pygame:

```bash
python -m ferramentas.preparar_figuras_personagens
python -m ferramentas.preparar_figuras_chefes
python -m ferramentas.preparar_figuras_movimento
python -m ferramentas.preparar_recursos_menu
python -m ferramentas.preparar_recursos_escola
python -m ferramentas.preparar_escola_detalhada
```

Alguns PNG antigos conservam suas dimensões de exportação originais; o carregador
normaliza todos para o contrato corporal comum em execução. `ferramentas/gerar_recursos.py`
é opcional, depende de Pillow e sobrescreve artes originais; os scripts acima
reaplicam as fontes atuais depois dessa geração.

O visual atual usa fachada noturna, HUD de integridade, painéis escuros com
acentos em âmbar e ciano e novos ambientes escolares em resolução nativa:
paredes texturizadas, quadros, murais, janelas, luminárias, conduítes e portas.
O mobiliário tem tampos, gavetas, gabinetes, teclados e cabos em camadas.

Os monitores alternam registros, CPU/memória, gráficos e estados da rede.
Tudo fica restrito à tela interna, acompanha a câmera e passa a mostrar a
IFVania após a corrupção. A animação visual continua nos diálogos, sem avançar
a física ou o combate, e congela na pausa. A saída do chicote acompanha a mão
maior, mantendo a trajetória final da ponta e o bloqueio pelas paredes. Os objetos do cenário não alteram
os blocos de colisão nem exigem novas habilidades. As dicas de controle quebram
em linhas quando necessário, inclusive nos mapas antigos com todos os poderes.

Prévias dos novos ambientes: [laboratório](../recursos/fontes_arte/previa_laboratorio_detalhado.png),
[corredor](../recursos/fontes_arte/previa_corredor_detalhado.png),
[arena](../recursos/fontes_arte/previa_batalha_detalhada.png) e
[monitores animados](../recursos/fontes_arte/previa_monitores_animados.gif).
Fontes e prompts: [instrucoes_escola_detalhada.json](../recursos/fontes_arte/instrucoes_escola_detalhada.json).
Exportação: `python -m ferramentas.preparar_escola_detalhada`.

Prévias da revisão anterior: [menu](../recursos/fontes_arte/previa_menu_sombrio.png),
[arena](../recursos/fontes_arte/previa_batalha_sombria.png) e
[animação da transformação](../recursos/fontes_arte/previa_transformacao_chefe.gif).
Fontes e prompts da ferramenta integrada estão em
[instrucoes_artes_sombrias.json](../recursos/fontes_arte/instrucoes_artes_sombrias.json). Para reexportar essas
artes, execute `python -m ferramentas.preparar_recursos_sombrios`.

Capturas anteriores da etapa 4: [reencontro](../recursos/fontes_arte/previa_reencontro_virtual.png),
[infecção](../recursos/fontes_arte/previa_infeccao_virtual.png) e
[fim do conteúdo](../recursos/fontes_arte/previa_fim_conteudo.png).

## Validação e pendências

```bash
python -m unittest discover -s testes -v
```

**95 testes passaram na revisão anterior**, incluindo o percurso com salto básico para ambos os
protagonistas, reencontro antes da infecção, transformação a 50%, projéteis,
pausa, limpeza de ameaças, ausência de recompensas e retorno ao menu. Os novos
testes também cobrem as seis poses da cena, fala da entidade, câmera visual,
pausa durante o diálogo, preservação do corpo/vida e retomada sem repetir a cena.
Os testes de arte verificam também o recorte dos monitores, o acompanhamento
da câmera, a escala ampliada e o congelamento visual na pausa. O combate
com chicote foi verificado em condições controladas; isso não comprova o equilíbrio
de sobrevivência por controle manual.

As cenas da etapa 4 foram renderizadas e inspecionadas. A etapa final de validação ainda inclui
homologação manual, revisão integrada de interface/câmera/controles e balanceamento.
Consulte o [plano](PLANO_DE_EXECUCAO.md) e os [requisitos](DOCUMENTO_DE_REQUISITOS.md).


## Nomenclatura e orientação para manutenção

As classes e variáveis próprias do projeto usam português, incluindo parâmetros,
atributos, constantes, testes e exportadores. Exemplos: `Jogo`, `Jogador`,
`Personagem`, `Chefe`, `Fase`, `CaixaDialogo`, `nome_jogador` e
`configuracoes.TAMANHO_PERSONAGEM`. As importações passam a usar esses nomes, como
`from entidades.jogador import Jogador`. Os arquivos e pastas também usam nomes em português. Métodos e chaves de
dados mantêm seus contratos.

Nomes de APIs externas continuam conforme suas bibliotecas: `image`, `rect` e
`update` fazem parte do contrato de Sprite do Pygame; propriedades de retângulos,
eventos e métodos de unittest também mantêm a grafia original. Nomes próprios
e coordenadas matemáticas permanecem reconhecíveis.

O [AGENTS.md](../AGENTS.md) reúne as convenções, a organização do código, os
contratos de jogabilidade e os comandos de validação. Na revisão de 28/10/2026,
os 81 testes passaram e os oito exportadores foram executados em pasta
temporária (74 PNGs), sem alterar as artes aprovadas. O gerador original
`ferramentas/gerar_recursos.py` foi conferido estaticamente; sua execução requer Pillow,
ausente no ambiente utilizado.


## Arquivos e pastas em português

O ponto de entrada é `principal.py`; a configuração fica em `sistema/configuracoes.py`
e a máquina de estados em `sistema/jogo.py`. O projeto usa as pastas `entidades/`,
`mundo/`, `interface/`, `testes/` e `recursos/`. As imagens ficam em
`recursos/imagens/` e suas fontes em `recursos/fontes_arte/`. Os exportadores
usam o prefixo `preparar_`. O roteiro está em `documentacao/ROTEIRO_HISTORIA.md`.

Instale com `pip install -r configuracao/dependencias.txt`, execute com `python principal.py`
e valide com `python -m unittest discover -s testes -v`. Nomes técnicos de
descoberta, como `AGENTS.md`, `__init__.py` e `.gitignore`, foram mantidos.
A renomeação preservou o conteúdo das 160 imagens e animações e passou pelos
81 testes e pelos oito exportadores de arte em pasta temporária.


## Expansão iniciada — 02/11/2026

A biblioteca recebeu fundo detalhado gerado a partir das referências internas
do IFRN e da direção de arte da fase 1. O pátio coberto também recebeu fundo
baseado nas fotos, aplicado ao caminho escolar até o A28. Código próprio em `mundo/biblioteca.py`, mapa e falas em
`mundo/dados_biblioteca.py`, encontro em `entidades/indexador.py`.
A antiga etapa 5 passou a integrar a etapa 11, validação final; a expansão ocupa
as etapas 5 a 10 do plano. A fase 3 ainda não está jogável: o fundo de pátio já integrado não inclui quadra, resgate ou chefe.

Validação do incremento: **102 testes passaram** sem janela/áudio. Capturas da biblioteca inspecionadas; sobrevivência, ritmo e comandos ainda precisam de homologação manual.


## Revisão do início e cenários — 02/11/2026

A abertura agora encena apresentação da tarefa, lembrança de casa, execução,
colegas nos computadores e hipnose. A abdução conduz as imagens de aluno e
Romerito até um monitor durante 150 atualizações, sem dano e com pausa.
SpeedBug recua antes de anunciar investida quando está sem espaço na borda;
Romerito volta à forma humana depois da derrota.

Fontes novas e prompts: [instrucoes_ambientes_ifrn.json](../recursos/fontes_arte/instrucoes_ambientes_ifrn.json).
Exportação: `python -m ferramentas.preparar_ambientes_ifrn`; para conferir sem substituir
recursos: `python -m ferramentas.preparar_ambientes_ifrn --destino /tmp/ifvania_ambientes`.

**108 testes passaram**. Capturas de abertura, hipnose, memória, sucção,
biblioteca e pátio inspecionadas; partida manual e balanceamento ainda pendentes.
O plano ativo prioriza as correções e mantém a validação final na etapa 11;
o histórico anterior está em [documentacao/HISTORICO_DE_EXECUCAO.md](HISTORICO_DE_EXECUCAO.md).

## Avaliação visual e funcional — 09/11/2026

A biblioteca recebeu rótulos para arquivos/módulo, painel de objetivo e correção
na sinalização do portão. O fundo fica discretamente mais escuro para distinguir
interativos. A câmera usa uma zona vertical estável durante os saltos, mantendo
acompanhamento de plataformas altas. Física, controles e colisões preservados.

[Relatório com 68 capturas antes/depois, notas e pendências](../avaliacao/visual/RELATORIO.md).
**110 testes passaram** em Python 3.12.10/Pygame 2.6.1 com SDL dummy.
Avaliação offscreen e automatizada; sobrevivência, áudio e conforto da câmera
continuam pendentes de partida manual. No ambiente desta revisão, use
`.venv/bin/python` nos comandos, pois `python` não está disponível no PATH.

Após revisão da composição: turma reduzida a dois colegas espaçados; pátio com
personagem no piso em primeiro plano e porta A28 integrada à parede de chegada.
Chefes não têm textos, miras, setas ou sons auxiliares anunciando ataques.
Preparação corporal e tempos permanecem; as faixas do Indexador só aparecem
quando o ataque está ativo. Capturas: `avaliacao/visual/revisao_composicao/`.

Os laboratórios da aula e A28 agora têm composição visual 2.5D: bancadas em
profundidades diferentes e colegas sentados de costas diante dos monitores.
A movimentação continua lateral, sem mudança de colisões. Capturas desta versão
em `avaliacao/visual/revisao_profundidade/`.

## Sprites de carga e retratos — 10/11/2026

Menino e Menina possuem oito quadros próprios para caminhar com o mouse
preparado. A postura permanece ao parar e saltar. Partículas pixeladas convergem
para o personagem; ao completar a carga, há um pulso ciano local. O efeito
continua animando enquanto o comando for mantido, inclusive após 0,6 s.

Diálogos exibem retrato do falante, incluindo a aparência e o nome escolhidos
para o protagonista. Max, Romerito, entidade/IFVania e Indexador usam suas
próprias figuras; Sistema usa um ícone de terminal. A caixa acomoda o texto
completo ao lado do retrato sem truncar falas longas. Os comandos de diálogo
continuam os mesmos.

Prévia: [animação da carga](../avaliacao/carga_dialogos/previa_carga.gif) e
[diálogo com retrato](../avaliacao/carga_dialogos/retrato_max.png).
Exportar sprites: `python -m ferramentas.preparar_caminhada_carregando`.
Capturar: `python -m ferramentas.capturar_carga_dialogos /tmp/ifvania_carga --quadros`.
ffmpeg é opcional para montar prévias; não é necessário para jogar ou exportar.

## HUD de conversa com bustos HD — 10/11/2026

A conversa usa moldura azul com filetes claros, placa de nome e bustos grandes
acima da caixa, inspirados nas referências fornecidas. Protagonista à esquerda,
interlocutor à direita; quem fala fica iluminado e quem escuta, escurecido.
O monitor ampliado da abertura ocupa o espaço central livre entre os bustos.

Seis ilustrações originais geradas com `image_gen` integrada: Menino, Menina,
Max, Romerito, IFVania/Entidade e Indexador, com fontes transparentes em
**1024 × 1536** e PNGs de jogo em **768 × 1152**. Sistema usa símbolo vetorial
na mesma resolução de exportação. Não são ampliações dos sprites de combate.
A resolução lógica do jogo continua 960 × 540, com redução suave dos bustos.

[Captura da conversa](../avaliacao/dialogos_hd/abertura_menina_1.png).
Fontes em `recursos/fontes_arte/retratos_dialogo/`; prompts, referências e
proveniência em `recursos/fontes_arte/instrucoes_retratos_dialogo.json`.
Exportar: `python -m ferramentas.preparar_retratos_dialogo`.
**127 testes passaram**; capturas e testes são offscreen, sem partida manual.
