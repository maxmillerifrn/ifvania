# IFVania

Jogo de plataforma 2D em **Python + Pygame**, com arquitetura orientada a objetos.
Escolha Menino ou Menina e acompanhe a revolta da IFVania, uma inteligência artificial
que assume o controle dos computadores da escola.

O fluxo principal implementa o início da história e a primeira fase do
[HistoryBoard](HISTORYBOARD.MD). As fases posteriores e o desligamento da energia
ainda não foram definidos. A saída da primeira fase apresenta **A jornada continua**;
a IFVania permanece ativa.

## Como executar

Em um ambiente Python com as dependências instaladas:

```bash
pip install -r requirements.txt
python main.py
```

Dependência: `pygame>=2.5.0`. Validação atual com Python 3.9.6 e Pygame 2.6.1.
O Python 3.15 do ambiente de desenvolvimento não compilou essa versão de Pygame;
os testes usaram um ambiente separado com Python 3.9.6.

## Fluxo disponível

1. Menu com fachada em pixel art, Jogar e Sair; navegação por clique ou setas/Enter.
2. Escolha Menino/Menina, com prévia animada e confirmação por botão ou Enter.
3. Aula de Max, apresentação da IFVania e revolta após o anúncio de desligamento.
4. Corredor navegável, entrada no A28 e encontro com Romerito por **E**.
5. Investida de Romerito, abdução e transporte ao mundo virtual.
6. Descoberta do mouse na bolsa; o chicote é liberado ao terminar esse diálogo.
7. Percurso com bugs e degraus de 32 ou 64 pixels, alcançável com o salto básico.
8. Reencontro com Romerito humano, fala sobre Brasília e corridas e infecção por um bug.
9. RomerBug lança aviões de papel; com até 50% da vida, vira SpeedBug, que persegue
   o protagonista e lança medalhas.
10. A derrota encerra as ameaças e libera a saída, sem conceder poderes. Alcançar
    a saída encerra o conteúdo disponível e permite voltar ao menu.

O prólogo e a fase virtual funcionam com os dois protagonistas, com os mesmos
atributos e corpo lógico de 40 × 40 pixels. Somente o protagonista e os bosses são desenhados
com escala visual de 110% (44 × 44), em todas as cenas e animações. Professores
como NPCs, bugs e a entidade mantêm a escala de 100%. A escolha é preservada nas transições.
O corredor é uma adaptação de cenário; o traçado interno real não foi homologado.
A referência oficial de A28 está no [documento de requisitos](DOCUMENTO_DE_REQUISITOS.md).

## Controles

| Comando | Ação |
|---|---|
| Setas esquerda/direita ou A/D | Mover |
| Espaço / W / seta para cima | Salto básico |
| X | Mouse-chicote, após encontrá-lo na bolsa |
| E | Entrar no A28 / falar com Romerito na escola, ao se aproximar |
| E / Enter / Espaço | Revelar ou avançar diálogo |
| Esc | Pausar e retomar exploração, combate, abdução e infecção |
| Enter / Espaço | Confirmar seleção, dispensar cartão ou voltar ao menu no encerramento |
| Esc na seleção | Voltar ao menu |
| Sair no menu / fechar janela | Encerrar a aplicação |

Não há desbloqueio de pulo duplo, dash, escalada, tiro ou escudo na campanha atual.
As dicas desses poderes não aparecem enquanto não estiverem disponíveis.

## Combate

O mouse-chicote tem preparação, extensão e recolhimento. Cada golpe causa um
acerto por alvo; as paredes interrompem seu alcance. A direção fica fixada no
início do golpe. O cabo e o mouse são desenhados pelo código; as poses do corpo
são sprites espelhados conforme a direção.

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
proteção. SpeedBug acelera e freia ao perseguir o alvo e ainda lança medalhas.

A alternativa de substituir aviões/medalhas por sobrecargas do piso e investidas
está em [PROPOSTA_BOSS_ROMERBUG.md](PROPOSTA_BOSS_ROMERBUG.md), como sugestão ainda
não aplicada. A campanha antiga mantém a transição curta para regressão.

Ao derrotar o boss, os projéteis dele e do jogador e os bugs restantes são
removidos. Não há recompensa coletável nem aumento de vida. A conversa posterior
deixa claro que o objetivo de desligar a energia ainda precisa ser cumprido.

## Arquitetura

| Área | Responsabilidade |
|---|---|
| `game.py` | Estados, seleção, prólogo, abdução, infecção e fim do conteúdo |
| `settings.py` | Dimensões comuns, resolução, física e temporizadores |
| `entities/character.py` | Base abstrata dos personagens |
| `entities/player.py` / `mouse_whip.py` | Protagonistas, movimento, arma e animações |
| `entities/npc.py` | Max e Romerito humano |
| `entities/boss.py` / `romer_bug.py` | Base abstrata de boss e encontro RomerBug/SpeedBug |
| `entities/teacher_bosses.py` | Classes e estratégias dos professores antigos |
| `world/school.py` / `school_data.py` | Sala, corredor, A28 e eventos do prólogo |
| `world/levels_data.py` | Mapa fixo e diálogos da campanha atual |
| `world/legacy_levels.py` | Mapas, diálogos e recompensas da campanha antiga |
| `world/level.py` | Combate, reencontro, saída e limpeza após a derrota |
| `world/tilemap.py` / `camera.py` | Colisões, pontos de surgimento e câmera |
| `ui/` | Tema, menu, seleção, diálogos e HUD |
| `world/boss_transition.py` | Cena dos 50%, entidade, metamorfose e zoom visual |
| `world/dark_school.py` | Fundo escolar e bancadas, sem alterar colisões |
| `assets.py` | Cache, substitutos visuais e normalização dos sprites |

Cada boss possui classe concreta própria. A base `Boss` exige uma estratégia
especializada, e tipos desconhecidos não recebem uma implementação genérica.

A campanha antiga de seis professores fica fora do menu principal. Seus dados
continuam disponíveis por `build_legacy_levels()` em `world/legacy_levels.py`,
para manutenção e regressão. Seus poderes e diálogos não são requisitos da
campanha atual.

## Arte

As fontes, referências e prompts estão em [assets/art_sources/README.md](assets/art_sources/README.md).
Os sprites preservam proporções, usam uma escala comum entre poses e têm os pés
alinhados dentro do corpo de 40 × 40 pixels. Armas e projéteis possuem áreas próprias.

Para reexportar as artes existentes com Pygame:

```bash
python prepare_character_sprites.py
python prepare_boss_sprites.py
python prepare_motion_sprites.py
python prepare_menu_assets.py
python prepare_school_assets.py
```

Alguns PNG antigos conservam suas dimensões de exportação originais; o carregador
normaliza todos para o contrato corporal comum em execução. `generate_assets.py`
é opcional, depende de Pillow e sobrescreve artes originais; os scripts acima
reaplicam as fontes atuais depois dessa geração.

O visual atual usa fachada noturna, HUD de integridade, painéis escuros com
acentos em âmbar e ciano e uma arena que representa o laboratório escolar:
computadores, quadros, portas e bancadas. Os objetos do cenário não alteram
os blocos de colisão nem exigem novas habilidades. As dicas de controle quebram
em linhas quando necessário, inclusive nos mapas antigos com todos os poderes.

Prévia atual: [menu](assets/art_sources/dark_menu_preview.png),
[arena](assets/art_sources/dark_battle_preview.png) e
[animação da transformação](assets/art_sources/boss_transformation_preview.gif).
Fontes e prompts da ferramenta integrada estão em
[dark_prompts.json](assets/art_sources/dark_prompts.json). Para reexportar essas
artes, execute `python prepare_dark_assets.py`.

Capturas anteriores da etapa 4: [reencontro](assets/art_sources/virtual_reunion_preview.png),
[infecção](assets/art_sources/virtual_infection_preview.png) e
[fim do conteúdo](assets/art_sources/content_end_preview.png).

## Validação e pendências

```bash
python -m unittest discover -s tests -v
```

**68 testes passaram**, incluindo o percurso com salto básico para ambos os
protagonistas, reencontro antes da infecção, transformação a 50%, projéteis,
pausa, limpeza de ameaças, ausência de recompensas e retorno ao menu. Os novos
testes também cobrem as seis poses da cena, fala da entidade, câmera visual,
pausa durante o diálogo, preservação do corpo/vida e retomada sem repetir a cena. O combate
com chicote foi verificado em condições controladas; isso não comprova o equilíbrio
de sobrevivência por controle manual.

As cenas da etapa 4 foram renderizadas e inspecionadas. A etapa 5 ainda inclui
homologação manual, revisão integrada de interface/câmera/controles e balanceamento.
Consulte o [plano](PLANO_DE_EXECUCAO.md) e os [requisitos](DOCUMENTO_DE_REQUISITOS.md).
