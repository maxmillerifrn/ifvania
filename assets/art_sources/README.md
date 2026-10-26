# Artes do jogo

As primeiras imagens do aluno e dos bugs foram produzidas com a ferramenta integrada
`image_gen`, a partir da descrição do usuário, sem fotos de referência. A nova fachada
usa a fotografia da escola indicada no HistoryBoard; a Menina usa as artes do Menino.
A farda é uma interpretação em pixel art da descrição e do visual verde já
presente no projeto; não houve validação fotográfica do uniforme do campus.

## Arquivos

- `student_ifrn_caico.png`: atlas transparente em alta resolução com oito poses.
  Ordem: parado 1, parado 2, andar 1, andar 2, andar 3, andar 4, pulo, dash.
- `bugs_microbes.png`: atlas transparente com dois quadros do mesmo micróbio.
- `prompts.json`: prompts completos de criação, correção dos sapatos e
  remoção do fundo da revisão intermediária; ferramenta integrada, sem CLI/API.
- `originals/player/` e `originals/enemies/`: cópias dos dez PNG anteriores.
- `sprite_preview.png`: prévia ampliada dos arquivos finais usados pelo jogo.
- `game_preview.png`: captura da primeira fase com as novas imagens.

## Exportação para o jogo

Na raiz do projeto, executar:

```bash
python prepare_character_sprites.py
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

`generate_assets.py` continua sendo o gerador das artes originais e sobrescreve
os sprites. Para recuperar esta versão depois de executá-lo, repetir o comando
de exportação acima. Para usar os desenhos anteriores, copiar os PNG de
`originals/player/` e `originals/enemies/` para as respectivas pastas em
`assets/images/`.

## Verificação realizada

- Dez PNG com dimensões esperadas e transparência.
- Presença das cores vermelha e verde nos oito quadros do aluno.
- Inspeção visual da prévia ampliada e da captura da primeira fase.
- Carregamento e desenho dos estados parado, andando, pulando e dash nas duas
  direções, com Pygame em modo sem janela.
- Carregamento, atualização e desenho das seis fases em modo sem janela.

Essa verificação não equivale a concluir a campanha por controle manual.

## Locomoção do chefe e chicote de mouse

`boss_motion.png` contém seis quadros de caminhada de RomerBug e seis de
corrida de SpeedBug. `student_whip.png` contém três poses do aluno: preparação,
golpe e recolhimento. Os prompts da ferramenta integrada estão em
`motion_prompts.json`; as duas artes foram criadas com referência às imagens
anteriores. O cabo e o mouse são elementos desenhados pelo código do jogo.

Para exportar esses 15 PNG sem alterar os atlas:

```bash
python prepare_motion_sprites.py
```

Destinos: `assets/images/bosses/romerbug_walk_*.png`,
`assets/images/bosses/speedbug_run_*.png` e `assets/images/player/attack_*.png`.
Os chefes usam 54 × 64 pixels; as poses de ataque usam 36 × 40, com o braço
ultrapassando visualmente a caixa de colisão de 26 × 40 do aluno.

`combat_motion_preview.gif` foi renderizado com as classes do jogo e mostra
as animações; `mouse_whip_preview.png` mostra as etapas do golpe e seu
espelhamento. A suíte possui testes adicionais de movimento, alcance,
colisão com paredes, um acerto por alvo e derrota do chefe usando o chicote.

## Menu e Menina — etapa 2

Fontes geradas pela ferramenta integrada `image_gen`, sem CLI/API:

- `school_facade.png`: fachada em pixel art baseada em `../../referencia/img.png`.
- `student_girl.png`: atlas transparente de 4 colunas × 3 linhas baseado em
  `student_ifrn_caico.png` e `student_whip.png`; os primeiros onze quadros são usados.
- `frontend_prompts.json`: prompts completos, referências e destinos das duas artes.

Para exportar sem alterar o Menino ou os bosses:

```bash
python prepare_menu_assets.py
```

Destinos: `assets/images/menu/school_facade.png` (480 × 270, ampliada sem
suavização na janela) e os onze PNG em `assets/images/player/girl/` (40 × 40,
com transparência, escala compartilhada e pés alinhados). O jogo normaliza também
as artes antigas para o corpo comum de 40 × 40; os tamanhos de exportação antigos
mencionados acima documentam os arquivos de origem, não a dimensão corporal atual.

Ordem da Menina: repouso 1–2, caminhada 1–4, salto, dash, preparação do ataque,
extensão e recolhimento. O mouse e o fio são desenhados pelo código.

Capturas inspecionadas: `menu_preview.png`, `selection_preview.png`,
`intro_preview.png`, `girl_game_preview.png` e `girl_animation_preview.png`.
A extração validou doze figuras e exportou onze estados. Os testes verificam
transparência, completude, espelhamento, identidade distinta e combate funcional.

## Professores e percurso escolar — etapa 3

`teachers.png` é o atlas criado com a ferramenta integrada `image_gen` a partir
das fotos `referencia/img_1.png` (Max), `referencia/img_2.png` (Romerito) e da arte
do aluno como referência de estilo. `school_prompts.json` registra o prompt
completo, as referências e os destinos. Há dois quadros de repouso por professor.

```bash
python prepare_school_assets.py
```

A exportação valida quatro figuras, espelha os professores para olharem ao aluno
e grava `assets/images/npcs/max_0.png`, `max_1.png`, `romerito_0.png` e
`romerito_1.png`, todos com transparência e 40 × 40 pixels. As fontes anteriores
não são substituídas. Sala, corredor, portas, computadores e efeitos de transporte
são geometria nativa editável em `world/school.py`.

Capturas inspecionadas: `school_classroom_preview.png`, `school_corridor_preview.png`,
`school_lab_preview.png`, `school_abduction_preview.png` e `mouse_discovery_preview.png`.
As cenas foram renderizadas com os dois protagonistas. A fidelidade geográfica
do corredor não foi homologada: o link curto do Maps não disponibilizou planta
consultável. A referência oficial de A28 está no documento de requisitos.

## Primeira fase virtual — etapa 4

Foram reutilizados os sprites de Romerito humano, dos bugs e de RomerBug/SpeedBug;
nenhuma arte nova foi gerada nesta etapa. A infecção usa os sprites existentes e
anéis desenhados em código. O mapa e seus degraus ficam em `world/levels_data.py`.

Capturas inspecionadas: `virtual_path_preview.png`, `virtual_reunion_preview.png`,
`virtual_infection_preview.png`, `virtual_speedbug_preview.png`,
`virtual_defeat_preview.png` e `content_end_preview.png`.
O piso do mapa deixa os personagens visíveis acima da caixa de diálogo.
A tela final informa que a IFVania segue ativa e que a jornada continua.

## Escola sombria e transição com entidade — 25/10/2026

Fontes novas geradas com a ferramenta integrada `image_gen`, sem substituir as anteriores:

- `school_night.png`: fachada noturna baseada em `school_facade.png`.
- `dark_lab.png`: laboratório escolar escuro em vista lateral, sem personagens.
- `boss_transition.png`: seis poses, baseadas em `romerbug_speedbug.png`: queda,
  joelho apoiado, olhar para a entidade, SpeedBug ajoelhado, subida e prontidão.
- `boss_entity.png`: presença espectral com capuz e fragmentos digitais.
- `dark_prompts.json`: prompts completos e referências das quatro gerações.

```bash
python prepare_dark_assets.py
```

Destinos: `assets/images/menu/school_night.png`,
`assets/images/background/dark_lab.png` e sete PNG de 40 × 40 em
`assets/images/bosses/transition/` (seis poses e entidade).
A exportação valida as figuras, mantém a transparência e preserva a altura
naturalmente menor das poses ajoelhadas dentro do mesmo corpo lógico.

Capturas: `dark_menu_preview.png`, `dark_selection_preview.png`,
`dark_battle_preview.png`, `boss_kneel_preview.png`, `entity_speech_preview.png`,
`boss_morph_preview.png` e `boss_rise_preview.png`.
`boss_transformation_preview.gif` foi renderizado com o próprio jogo e convertido
para GIF com ffmpeg, usado somente para essa prévia; não é dependência do jogo.
As colisões e o mapa não mudam durante a aproximação visual da câmera.
