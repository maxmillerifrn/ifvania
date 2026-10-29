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
python preparar_figuras_personagens.py
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

`gerar_recursos.py` continua sendo o gerador das artes originais e sobrescreve
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
python preparar_figuras_movimento.py
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
python preparar_recursos_menu.py
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
python preparar_recursos_escola.py
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
python preparar_recursos_sombrios.py
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
python preparar_escola_detalhada.py
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
python preparar_caminhada_jogador.py
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
sintetizados localmente em `sons.py`, sem dependência de arquivos ou rede.

Capturas renderizadas e inspecionadas: `previa_plataformas_legiveis.png`,
`previa_ataque_carregado.png`, `previa_mouse_reforcado.png`,
`previa_aviso_descarga.png` e `previa_aviso_investida.png`.


## Retorno dos projéteis e ciclo de investida — 29/10/2026

Reutilizadas as artes existentes de avião e medalha. Capturas atuais:
`previa_romerbug_aviao.png`, `previa_speedbug_medalha.png` e
`previa_ciclo_investida.png`. Não houve geração de novas artes nesta revisão.
As capturas anteriores da descarga documentam a mecânica substituída.
