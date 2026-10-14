# Artes do aluno e dos bugs

As imagens desta pasta foram produzidas com a ferramenta integrada `image_gen`,
a partir da descrição do usuário. Não foram usadas fotos de referência.
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
