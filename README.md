# Escola dos Bugs - A Vingança dos Professores

Jogo 2D estilo **metroidvania**, feito em **Python + Pygame**, com arquitetura orientada a objetos.
Você é um(a) aluno(a) que precisa atravessar 6 salas de aula corrompidas por um vírus e
derrotar os 6 professores de programação transformados em chefes de fase, recuperando
habilidades (power-ups) a cada vitória.

## Como executar

```bash
pip install -r requirements.txt
python main.py
```

Requer Python 3.9+ e Pygame 2.5+.

## Controles

| Tecla | Ação |
|---|---|
| Seta ← / → ou A / D | Mover |
| Espaço / W / ↑ | Pular (pulo duplo depois de derrotar RomerBug/SpeedBug e coletar o poder) |
| X | Chicote de mouse com fio (preparação, estalo e recolhimento) |
| SHIFT | Dash (depois do Prof. Python) |
| Segurar contra a parede | Escalar parede (depois do Prof. Java) |
| F | Tiro de ponteiro (depois do Prof. C) |
| Q | Escudo de dados (depois do Prof. SQL) |
| E / Enter / Espaço | Avançar diálogo |
| ESC | Pausar |

## As 6 fases e professores-chefe

1. **RomerBug → SpeedBug** — Lógica de Blocos → concede *Pulo Duplo*
2. **Prof. Python** — Laboratório de Lógica → concede *Dash Veloz*
3. **Prof. Java** — Sala de POO → concede *Escalada de Parede*
4. **Prof. C** — Sala de Memória → concede *Tiro de Ponteiro*
5. **Prof. SQL** — Biblioteca de Dados → concede *Escudo de Dados*
6. **Prof. Assembly** — Núcleo do Sistema (chefe final, usa todas as habilidades já aprendidas)

Cada fase começa com um pequeno diálogo de contexto, um trigger de diálogo antes da luta
contra o professor, e um diálogo de vitória que entrega a habilidade. A saída da fase só é
liberada depois que o chefe é derrotado — estrutura clássica de metroidvania (progressão
ligada a poderes, mesmo que aqui de forma linear fase-a-fase).

## Arquitetura (orientação a objetos)

```
main.py                  -> ponto de entrada
game.py                  -> Game: máquina de estados (menu, diálogo, jogo, vitória...)
settings.py               -> constantes globais (física, cores, tamanhos)
assets.py                  -> carregamento/cache de imagens (assets/images/)
generate_assets.py          -> script que gerou as imagens placeholder (Pillow)
powerups.py                -> Ability (Enum) + PowerUp (sprite coletável)
entities/
    character.py           -> Character: classe base ABSTRATA (vida, dano, gravidade/colisão, desenho)
    player.py             -> Player(Character): movimento, pulo duplo, dash, escalada, tiro, escudo
    enemy.py               -> Enemy(Character): inimigo comum ("bug") com patrulha
    boss.py                 -> Boss(Character): professor-chefe com fases e padrões de ataque + BOSS_DEFS
    romer_bug.py            -> RomerBug(Boss): forma formal, transformação e perseguição; aviões e medalhas
    mouse_whip.py           -> MouseWhip: curva do cabo, desenho do mouse e colisão do golpe
    projectile.py            -> Projectile: tiros do jogador e dos chefes
world/
    tilemap.py              -> TileMap: converte mapa ASCII em colisões/spawns
    levels_data.py            -> geração determinística das 6 fases + todos os diálogos
    level.py                   -> Level: liga tilemap + inimigos + chefe + power-up + câmera
    camera.py                   -> Camera: rolagem de tela
ui/
    dialogue.py                -> DialogueBox: caixa de diálogo com efeito de digitação
    hud.py                       -> HUD: vida, ícones de habilidades, barra de vida do chefe
```

O visual usa **imagens (sprites)** carregadas de `assets/images/`, através do módulo
`assets.py` (cache + fallback). Se algum arquivo de imagem for apagado, o jogo não
quebra: ele mostra um retângulo magenta de aviso no lugar, para facilitar o
desenvolvimento incremental em sala de aula.

A arte é **pixel art** (contorno escuro, poucas cores por material, bordas duras -
sem suavização), no espírito de personagens de Castlevania/Metroid. O(a) aluno(a)
protagonista veste a farda do IFRN (camisa polo verde institucional, mochila e
emblema no peito) e tem quadros de animação próprios para cada ação: parado(a)
(2 quadros), andando (4 quadros), pulo e dash. Os "bugs" comuns também têm 2
quadros (rastejo), e os professores-chefe têm um leve balanço (bob) de respiração
enquanto esperam para atacar.

```
assets/images/
    player/       idle_0.png, idle_1.png,           parado(a) - 2 quadros
                  walk_0.png .. walk_3.png,          andando - 4 quadros
                  jump.png,                          no ar
                  dash.png                           dash
    enemies/      bug_0.png, bug_1.png               "bug" comum - 2 quadros
    bosses/       prof_scratch.png, prof_python.png, prof_java.png,
                  prof_c.png, prof_sql.png, prof_assembly.png
    tiles/        ground.png, spike.png
    background/   panel.png
    ui/           powerup.png
```

Só é preciso desenhar virado(a) para a **direita**: o espelhamento para a
esquerda é feito em tempo de execução por `assets.load_flipped()`.

Os cenários e professores-chefe usam imagens **geradas por código**
(`generate_assets.py`, usando Pillow). O aluno e os bugs receberam novas artes
geradas com a ferramenta de imagens, preparadas para as animações do jogo.
Para os alunos desenharem a arte própria da turma, basta:

1. Abrir cada PNG em um editor (Piskel, Aseprite, GIMP, Photopea etc.) e redesenhar
   por cima, mantendo o mesmo nome de arquivo e fundo transparente.
2. Rodar o jogo de novo — não precisa mexer em nenhuma linha de código, o
   `assets.py` recarrega os arquivos automaticamente.
3. Para regenerar os recursos originais: `pip install pillow` e depois
   `python generate_assets.py`. Esse comando sobrescreve os PNG, inclusive o
   aluno e os bugs. Depois, execute `python prepare_character_sprites.py` para
   reaplicar as novas artes desses personagens.

## Aluno do IFRN Caicó e bugs

O protagonista possui pele morena, cabelo black power, óculos, farda verde
com gola branca, mochila e um tênis verde e outro vermelho. Os bugs lembram
vírus/bactérias amarelo-esverdeados, com olhos, manchas e pequenas projeções.

Foram atualizados os oito quadros do aluno em `assets/images/player/`
(26 × 40 pixels) e os dois quadros dos bugs em `assets/images/enemies/`
(26 × 24 pixels), com fundo transparente. A física e as caixas de colisão
continuam usando os mesmos tamanhos.

- [Prévia ampliada dos sprites](assets/art_sources/sprite_preview.png).
- [Captura no jogo](assets/art_sources/game_preview.png).
- Artes em alta resolução: `assets/art_sources/student_ifrn_caico.png` e
  `assets/art_sources/bugs_microbes.png`.
- Prompts de criação e revisão: `assets/art_sources/prompts.json`.
- Cópia dos sprites anteriores: `assets/art_sources/originals/`.

`python prepare_character_sprites.py` separa as figuras dos atlas e exporta
os dez arquivos usados pelo jogo. A exportação usa Pygame, preserva as
proporções com escala comum por personagem e redimensiona sem suavização.
As artes grandes guardam mais detalhes do que os sprites de baixa resolução.

## Módulo `assets.py`

Centraliza o carregamento de imagens com cache (evita ler o mesmo arquivo várias
vezes), redimensionamento automático para o tamanho de cada entidade, e uma versão
espelhada (`load_flipped`) usada para virar o personagem/inimigos para a esquerda.

## Primeiro chefe: RomerBug → SpeedBug

A campanha continua com seis chefes. O primeiro usa a classe `RomerBug`, que
herda de `Boss`; os outros cinco usam a classe base existente.

- **RomerBug:** professor moreno, cabelo curto, terno, camisa e gravata.
  Caminha perto de sua posição inicial, freia para arremessar e lança aviões
  de papel mirando a posição do aluno.
- **SpeedBug:** ao atingir **50% de vida ou menos**, troca o terno por roupa
  de corrida. O nome no HUD muda, e ele passa a perseguir o aluno, saltando
  obstáculos e lançando medalhas direcionadas ao alvo.
- Caminhada e corrida usam seis quadros cada, sincronizados com a distância
  realmente percorrida. Há aceleração e frenagem antes das mudanças de direção;
  os pés deixam de ciclar quando uma parede impede o deslocamento.
- A transformação acontece uma vez, conserva a vida restante e dura 45
  atualizações (cerca de 0,75 s a 60 FPS). Durante o efeito o chefe não causa
  nem recebe dano, e os aviões anteriores são removidos.
- Aviões e medalhas seguem a direção calculada no lançamento, sem seguir
  automaticamente o alvo depois do disparo. Ambos causam 1 ponto de dano e
  desaparecem ao colidir com o cenário ou ao esgotar sua duração.
- A derrota libera a saída e deixa o item de pulo duplo, como antes.

[Prévia das formas e projéteis](assets/art_sources/romerbug_preview.png).
Os sprites estão em `assets/images/bosses/romerbug_*.png`,
`assets/images/bosses/speedbug_*.png` e `assets/images/projectiles/`.
As artes-fonte e os prompts da ferramenta integrada de imagens estão em
`assets/art_sources/romerbug_speedbug.png`, `romerbug_projectiles.png` e
`romerbug_prompts.json`. Para reexportar os seis novos PNG:

```bash
python prepare_boss_sprites.py
```

Os novos ciclos de locomoção e as poses do ataque do aluno são exportados com
`python prepare_motion_sprites.py`. As fontes `boss_motion.png` e
`student_whip.png`, junto com `motion_prompts.json`, estão em `assets/art_sources/`.

## Ataque com mouse de fio

Ao pressionar **X**, o aluno segura o cabo e usa o mouse na ponta como chicote.
O golpe possui preparação, extensão em arco e recolhimento, com três poses
próprias do braço. O cabo e o mouse são desenhados em tempo real pelo Pygame.

- Duração: 26 atualizações; intervalo entre inícios de golpe: 30 atualizações.
- Dano somente durante a extensão, uma vez por inimigo em cada golpe.
- Alcance máximo da ponta: aproximadamente 90 pixels a partir do centro do aluno.
- Cabo e colisão seguem a mesma curva; paredes interrompem o alcance.
- A direção é fixada no início do golpe, inclusive se o jogador virar durante a animação.
- As três poses usam telas transparentes de 36 × 40 para acomodar o braço;
  a caixa de colisão do aluno continua em 26 × 40.

[Prévia animada de caminhada, corrida e chicote](assets/art_sources/combat_motion_preview.gif)
e [etapas do golpe](assets/art_sources/mouse_whip_preview.png).

Testes de transformação, ataques, perseguição, colisão, recompensa e integração
com as seis fases:

```bash
python -m unittest discover -s tests -v
```

## Testado

O fluxo completo (menu → diálogo introdutório → 6 fases → diálogos de chefe → derrota de
cada chefe → coleta de power-up → saída de fase → tela de vitória) foi validado via script
automatizado rodando o loop de estados do jogo sem erros.
