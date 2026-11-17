# Artes do jogo

As primeiras imagens do aluno e dos bugs foram produzidas com a ferramenta integrada
`image_gen`, a partir da descrição do usuário, sem fotos de referência. A nova fachada
usa a fotografia da escola indicada no HistoryBoard; a Menina usa as artes do Menino.
A farda é uma interpretação em pixel art da descrição e do visual verde já
presente no projeto; não houve validação fotográfica do uniforme do campus.

## Arquivos

- `aluno_ifrn_caico.png`: atlas transparente em alta resolução com oito poses.
  Ordem: parado 1, parado 2, andar 1, andar 2, andar 3, andar 4, pulo, dash.
- `bugs_microbios.png`: atlas transparente com dois quadros do mesmo micróbio.
- `instrucoes_geracao.json`: prompts completos de criação, correção dos sapatos e
  remoção do fundo da revisão intermediária; ferramenta integrada, sem CLI/API.
- `originais/jogador/` e `originais/inimigos/`: cópias dos dez PNG anteriores.
- `previa_figuras.png`: prévia ampliada dos arquivos finais usados pelo jogo.
- `previa_jogo.png`: captura da primeira fase com as novas imagens.

## Exportação para o jogo

Na raiz do projeto, executar:

```bash
python -m ferramentas.preparar_figuras_personagens
```

O script usa Pygame para separar as figuras pelo canal alfa, ignorando pequenos
resíduos isolados, e redimensionar com vizinho mais próximo. A escala é comum
a todos os quadros de cada personagem, com alinhamento inferior e centralização
horizontal. Isso mantém as proporções entre as poses e os tamanhos de arquivo
esperados pelo jogo: aluno 26 × 40 e bugs 26 × 24 pixels.

O script foi preparado para estes dois atlas e valida a quantidade de figuras
antes de exportar. Um novo atlas com partes desconectadas ou outra disposição
pode precisar de ajustes no recorte. Os PNG exportados têm transparência;
nenhum fundo quadriculado é incorporado aos arquivos finais.

`ferramentas/gerar_recursos.py` continua sendo o gerador das artes originais e sobrescreve
os sprites. Para recuperar esta versão depois de executá-lo, repetir o comando
de exportação acima. Para usar os desenhos anteriores, copiar os PNG de
`originais/jogador/` e `originais/inimigos/` para as respectivas pastas em
`recursos/imagens/`.

## Verificação realizada

- Dez PNG com dimensões esperadas e transparência.
- Presença das cores vermelha e verde nos oito quadros do aluno.
- Inspeção visual da prévia ampliada e da captura da primeira fase.
- Carregamento e desenho dos estados parado, andando, pulando e dash nas duas
  direções, com Pygame em modo sem janela.
- Carregamento, atualização e desenho das seis fases em modo sem janela.

Essa verificação não equivale a concluir a campanha por controle manual.

## Locomoção do chefe e chicote de mouse

`movimento_chefe.png` contém seis quadros de caminhada de RomerBug e seis de
corrida de SpeedBug. `aluno_chicote.png` contém três poses do aluno: preparação,
golpe e recolhimento. Os prompts da ferramenta integrada estão em
`instrucoes_movimento.json`; as duas artes foram criadas com referência às imagens
anteriores. O cabo e o mouse são elementos desenhados pelo código do jogo.

Para exportar esses 15 PNG sem alterar os atlas:

```bash
python -m ferramentas.preparar_figuras_movimento
```

Destinos: `recursos/imagens/chefes/romerbug_caminhada_*.png`,
`recursos/imagens/chefes/speedbug_corrida_*.png` e `recursos/imagens/jogador/ataque_*.png`.
Os chefes usam 54 × 64 pixels; as poses de ataque usam 36 × 40, com o braço
ultrapassando visualmente a caixa de colisão de 26 × 40 do aluno.

`previa_movimento_combate.gif` foi renderizado com as classes do jogo e mostra
as animações; `previa_chicote_mouse.png` mostra as etapas do golpe e seu
espelhamento. A suíte possui testes adicionais de movimento, alcance,
colisão com paredes, um acerto por alvo e derrota do chefe usando o chicote.

## Menu e Menina — etapa 2

Fontes geradas pela ferramenta integrada `image_gen`, sem CLI/API:

- `fachada_escola.png`: fachada em pixel art baseada em `../../referencia/fachada_escola.png`.
- `aluna.png`: atlas transparente de 4 colunas × 3 linhas baseado em
  `aluno_ifrn_caico.png` e `aluno_chicote.png`; os primeiros onze quadros são usados.
- `instrucoes_interface_inicial.json`: prompts completos, referências e destinos das duas artes.

Para exportar sem alterar o Menino ou os bosses:

```bash
python -m ferramentas.preparar_recursos_menu
```

Destinos: `recursos/imagens/menu/fachada_escola.png` (480 × 270, ampliada sem
suavização na janela) e os onze PNG em `recursos/imagens/jogador/menina/` (40 × 40,
com transparência, escala compartilhada e pés alinhados). O jogo normaliza também
as artes antigas para o corpo comum de 40 × 40; os tamanhos de exportação antigos
mencionados acima documentam os arquivos de origem, não a dimensão corporal atual.

Ordem da Menina: repouso 1–2, caminhada 1–4, salto, dash, preparação do ataque,
extensão e recolhimento. O mouse e o fio são desenhados pelo código.

Capturas inspecionadas: `previa_menu.png`, `previa_selecao.png`,
`previa_introducao.png`, `previa_jogo_menina.png` e `previa_animacao_menina.png`.
A extração validou doze figuras e exportou onze estados. Os testes verificam
transparência, completude, espelhamento, identidade distinta e combate funcional.

## Professores e percurso escolar — etapa 3

`professores.png` é o atlas criado com a ferramenta integrada `image_gen` a partir
das fotos `referencia/professor_max.png` (Max), `referencia/professor_romerito.png` (Romerito) e da arte
do aluno como referência de estilo. `instrucoes_escola.json` registra o prompt
completo, as referências e os destinos. Há dois quadros de repouso por professor.

```bash
python -m ferramentas.preparar_recursos_escola
```

A exportação valida quatro figuras, espelha os professores para olharem ao aluno
e grava `recursos/imagens/professores/max_0.png`, `max_1.png`, `romerito_0.png` e
`romerito_1.png`, todos com transparência e 40 × 40 pixels. As fontes anteriores
não são substituídas. Sala, corredor, portas, computadores e efeitos de transporte
são geometria nativa editável em `mundo/escola.py`.

Capturas inspecionadas: `previa_sala_aula.png`, `previa_corredor_escolar.png`,
`previa_laboratorio_escolar.png`, `previa_abducao_escolar.png` e `previa_descoberta_mouse.png`.
As cenas foram renderizadas com os dois protagonistas. A fidelidade geográfica
do corredor não foi homologada: o link curto do Maps não disponibilizou planta
consultável. A referência oficial de A28 está no documento de requisitos.

## Primeira fase virtual — etapa 4

Foram reutilizados os sprites de Romerito humano, dos bugs e de RomerBug/SpeedBug;
nenhuma arte nova foi gerada nesta etapa. A infecção usa os sprites existentes e
anéis desenhados em código. O mapa e seus degraus ficam em `mundo/dados_fases.py`.

Capturas inspecionadas: `previa_percurso_virtual.png`, `previa_reencontro_virtual.png`,
`previa_infeccao_virtual.png`, `previa_speedbug_virtual.png`,
`previa_derrota_virtual.png` e `previa_fim_conteudo.png`.
O piso do mapa deixa os personagens visíveis acima da caixa de diálogo.
A tela final informa que a IFVania segue ativa e que a jornada continua.

## Escola sombria e transição com entidade — 25/10/2026

Fontes novas geradas com a ferramenta integrada `image_gen`, sem substituir as anteriores:

- `escola_noturna.png`: fachada noturna baseada em `fachada_escola.png`.
- `laboratorio_sombrio.png`: laboratório escolar escuro em vista lateral, sem personagens.
- `transicao_chefe.png`: seis poses, baseadas em `romerbug_speedbug.png`: queda,
  joelho apoiado, olhar para a entidade, SpeedBug ajoelhado, subida e prontidão.
- `entidade_chefe.png`: presença espectral com capuz e fragmentos digitais.
- `instrucoes_artes_sombrias.json`: prompts completos e referências das quatro gerações.

```bash
python -m ferramentas.preparar_recursos_sombrios
```

Destinos: `recursos/imagens/menu/escola_noturna.png`,
`recursos/imagens/cenarios/laboratorio_sombrio.png` e sete PNG de 40 × 40 em
`recursos/imagens/chefes/transicao/` (seis poses e entidade).
A exportação valida as figuras, mantém a transparência e preserva a altura
naturalmente menor das poses ajoelhadas dentro do mesmo corpo lógico.

Capturas: `previa_menu_sombrio.png`, `previa_selecao_sombria.png`,
`previa_batalha_sombria.png`, `previa_chefe_ajoelhado.png`, `previa_fala_entidade.png`,
`previa_metamorfose_chefe.png` e `previa_chefe_levantando.png`.
`previa_transformacao_chefe.gif` foi renderizado com o próprio jogo e convertido
para GIF com ffmpeg, usado somente para essa prévia; não é dependência do jogo.
As colisões e o mapa não mudam durante a aproximação visual da câmera.

## Laboratórios e corredores detalhados — 27/10/2026

Novas fontes geradas com a ferramenta integrada `image_gen`: `laboratorio_detalhado.png`
e `corredor_detalhado.png`. Os prompts completos estão em
`instrucoes_escola_detalhada.json`; as fontes anteriores foram preservadas.

```bash
python -m ferramentas.preparar_escola_detalhada
```

Exporta para `recursos/imagens/cenarios/laboratorio_detalhado.png` e
`recursos/imagens/cenarios/corredor_detalhado.png`, em 960 × 540 pixels.
Os ambientes recebem computadores e móveis em camadas editáveis de
`mundo/arte_escolar.py`. O conteúdo das telas é produzido por `mundo/terminal.py`,
com superfície própria para impedir texto ou gráficos fora do monitor.

Capturas: `previa_sala_aula_detalhada.png`, `previa_laboratorio_detalhado.png`,
`previa_corredor_detalhado.png`, `previa_batalha_detalhada.png`,
`previa_entidade_ampliada.png` e `large_whip_*_preview.png`.
A prévia `previa_monitores_animados.gif` foi renderizada pelo jogo e convertida
com ffmpeg, que continua sendo opcional e não integra a execução do jogo.

Personagens, bosses e NPCs agora têm apresentação visual de 80 × 80 pixels,
com colisões de 40 × 40 e pés alinhados. Bugs não foram ampliados.


## Nova caminhada — 27/10/2026

`ciclo_caminhada_jogador.png` foi criado com a ferramenta integrada `image_gen`,
usando os atlas anteriores dos dois alunos como referência. O prompt completo,
as referências e o destino estão em `instrucoes_caminhada_jogador.json`.

```bash
python -m ferramentas.preparar_caminhada_jogador
```

O exportador valida 16 figuras e grava oito quadros de 40 × 40 por personagem
em `recursos/imagens/jogador/ciclo_caminhada/` e `recursos/imagens/jogador/menina/ciclo_caminhada/`.
As caminhadas antigas foram preservadas. O jogo usa os novos quadros conforme
a distância percorrida, mantendo os pés alinhados e a escala visual de 200%.
`previa_caminhada_jogador.gif` mostra os dois protagonistas em movimento; ffmpeg
foi usado apenas na conversão da prévia. `previa_nome_jogador.png`,
`previa_introducao_aluno.png` e `previa_resposta_com_nome.png` registram o novo fluxo
de nome e a conversa inicial sem narrador.


## Combate e superfícies legíveis — 28/10/2026

Sem novas gerações raster: mouse reforçado, rastro, carga, sinais de ataque e
faixas de plataforma são desenhos nativos de Pygame sobre os sprites existentes.
As fontes antigas permanecem preservadas. Sons de carga, aviso e impacto são
sintetizados localmente em `sistema/sons.py`, sem dependência de arquivos ou rede.

Capturas renderizadas e inspecionadas: `previa_plataformas_legiveis.png`,
`previa_ataque_carregado.png`, `previa_mouse_reforcado.png`,
`previa_aviso_descarga.png` e `previa_aviso_investida.png`.


## Retorno dos projéteis e ciclo de investida — 29/10/2026

Reutilizadas as artes existentes de avião e medalha. Capturas atuais:
`previa_romerbug_aviao.png`, `previa_speedbug_medalha.png` e
`previa_ciclo_investida.png`. Não houve geração de novas artes nesta revisão.
As capturas anteriores da descarga documentam a mecânica substituída.


## Ambientes IFRN e encenação do início — 02/11/2026

Fontes novas: `biblioteca_ifrn.png`, `patio_ifrn.png` e `memoria_tarefa.png`,
geradas com a ferramenta integrada image_gen. Prompts completos e referências
em [instrucoes_ambientes_ifrn.json](instrucoes_ambientes_ifrn.json).
A arte de `laboratorio_detalhado.png` orienta estilo, acabamento e iluminação;
as capturas em `referencia/ifrn/` orientam biblioteca e espaços externos.
As fontes e as artes anteriores foram preservadas.

Exportar com `python -m ferramentas.preparar_ambientes_ifrn`, a partir da raiz do projeto.
Usar `--destino /tmp/ifvania_ambientes` para conferir antes da integração.
Os três fundos são normalizados para módulos de 960 × 540 sem suavização.

Alunos sentados são compostos em `mundo/turma_laboratorio.py` a partir das
artes existentes dos protagonistas, sem novas colisões. A sucção ao monitor
fica em `mundo/succao_computador.py`, com imagens transformadas apenas no desenho.
Capturas de inspeção desta revisão: `revisao_inicio_*.png`, `revisao_succao_*.png`,
`revisao_patio.png` e `revisao_biblioteca.png`. São capturas de estados controlados,
não evidência de partida manual ou homologação final.

## Caminhada mantendo carga — 10/11/2026

`caminhada_carregando.png` é um novo atlas transparente de 16 quadros (oito
por protagonista), criado com `image_gen.imagegen` integrada a partir do ciclo
normal. O braço permanece preparado com o mouse na mão enquanto as pernas
caminham. Atlas anteriores preservados. Prompt completo e proveniência em
[instrucoes_caminhada_carregando.json](instrucoes_caminhada_carregando.json).

Exportação: `python -m ferramentas.preparar_caminhada_carregando`. Conferida
primeiro em pasta temporária, depois integrada em
`recursos/imagens/jogador/caminhada_carregando/` e
`recursos/imagens/jogador/menina/caminhada_carregando/`.

O efeito de energia é desenhado em `entidades/efeito_carga.py`, inspirado nas
partículas convergentes da [referência fornecida](https://giffiles.alphacoders.com/124/12442.gif).
O GIF foi consultado; seus sprites não foram incorporados ao projeto. O efeito
mantém relógio visual próprio após carga máxima e não altera dano ou colisões.
Retratos usam recortes dos sprites aprovados, sem gerar ou substituir rostos.

## Bustos de conversa em alta resolução — 10/11/2026

`retratos_dialogo/` contém seis ilustrações novas, geradas individualmente com
`image_gen.imagegen` integrada a partir das identidades existentes. Cada fonte
possui 1024 × 1536 e canal alfa. Prompts completos, referências do HUD e destinos
estão em [instrucoes_retratos_dialogo.json](instrucoes_retratos_dialogo.json).

Exportação: `python -m ferramentas.preparar_retratos_dialogo`. As versões de
jogo têm 768 × 1152, em `recursos/imagens/dialogos/`; Sistema recebe símbolo
vetorial na mesma resolução. A entidade é espelhada na exportação para olhar
para o centro da conversa. O renderer reduz os bustos suavemente, sem aumentar
sprites de 40 × 40. Atlas e artes anteriores foram preservados.

Prévias reais: [conversa](../../avaliacao/dialogos_hd/abertura_menina_1.png) e
[entidade](../../avaliacao/dialogos_hd/ifvania.png).
# Revisão de combate, turma e guardiões — 16/11/2026

Novas fontes: `turma_laboratorio/turma_costas.png` (dois alunos sentados de costas) e `guardioes_campus/avatares.png` (avatares ficcionais de esporte, computação e eletroeletrônica, sem retratar pessoas reais). Max conserva sua arte anterior. Ferramenta: `image_gen` integrada, com geração e edição de transparência. Prompts completos e proveniência em [instrucoes_revisao_hack_and_slash.json](instrucoes_revisao_hack_and_slash.json).

Exportadores: `python -m ferramentas.preparar_turma_laboratorio`, `python -m ferramentas.preparar_apresentacao_personagens` e `python -m ferramentas.preparar_guardioes_campus`. Todos foram conferidos em destinos temporários antes de integrar. A apresentação HD é exportada dos atlas já aprovados, sem sobrescrever os PNGs lógicos ou fontes anteriores. O gerador original continua podendo sobrescrever recursos; reaplicar exportadores quando necessário.

## Poses de combate dos guardiões — 16/11/2026

Fonte preservada em `guardioes_campus/poses_combate.png`; prompt e referências em `instrucoes_poses_guardioes.json`. `python -m ferramentas.preparar_poses_guardioes` exporta quatro poses de cada guardião em 40 e 80 px. Retratos separados são derivados da fonte original pelo exportador de guardiões. O verificador executou os 15 exportadores em temporário, com 203 PNGs distintos; recursos aprovados anteriores preservados.
