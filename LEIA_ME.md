# IFVania

Jogo de plataforma 2D em **Python + Pygame**, com arquitetura orientada a objetos.
Escolha Menino ou Menina e acompanhe a revolta da IFVania, uma inteligência artificial
que assume o controle dos computadores da escola.

O fluxo principal implementa o início da história e a primeira fase do
[HistoryBoard](ROTEIRO_HISTORIA.md). As fases posteriores e o desligamento da energia
ainda não foram definidos. A saída da primeira fase apresenta **A jornada continua**;
a IFVania permanece ativa.

## Como executar

Em um ambiente Python com as dependências instaladas:

```bash
pip install -r dependencias.txt
python principal.py
```

Dependência: `pygame>=2.5.0`. Validação atual com Python 3.9.6 e Pygame 2.6.1.
O Python 3.15 do ambiente de desenvolvimento não compilou essa versão de Pygame;
os testes usaram um ambiente separado com Python 3.9.6.

## Fluxo disponível

1. Menu com fachada em pixel art, Jogar e Sair; navegação por clique ou setas/Enter.
2. Escolha Menino/Menina, com prévia animada e confirmação por botão ou Enter.
3. Digitação do nome (obrigatório, até 20 caracteres); Enter confirma e Esc volta.
   A aula começa com o aluno conversando com Max, sem narrador, e apresenta a
   IFVania e sua revolta após o anúncio de desligamento.
4. Corredor navegável, entrada no A28 e encontro com Romerito por **E**.
5. Investida de Romerito, abdução e transporte ao mundo virtual.
6. Descoberta do mouse na bolsa; o chicote é liberado ao terminar esse diálogo.
7. Percurso com bugs e degraus de 32 ou 64 pixels, alcançável com o salto básico.
8. Reencontro com Romerito humano, fala sobre Brasília e corridas e infecção por um bug.
9. RomerBug marca descargas no piso; com até 50% da vida, vira SpeedBug, que
   prepara uma investida de direção fixa e fica exposto após executá-la.
10. A derrota encerra as ameaças e libera a saída, sem conceder poderes. Alcançar
    a saída encerra o conteúdo disponível e permite voltar ao menu.

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
| Tocar e soltar X | Golpe rápido de mouse com cabo reforçado: 1 de dano |
| Segurar X por 0,6 s e soltar | Golpe carregado: 2 de dano |
| Shift | Esquiva curta, após encontrar o mouse; recarga de 0,9 s |
| E | Entrar no A28 / falar com Romerito na escola, ao se aproximar |
| E / Enter / Espaço | Revelar ou avançar diálogo |
| Esc | Pausar e retomar exploração, combate, abdução e infecção |
| Enter / Espaço | Confirmar seleção, dispensar cartão ou voltar ao menu no encerramento |
| Esc na seleção | Voltar ao menu |
| Sair no menu / fechar janela | Encerrar a aplicação |

Não há desbloqueio de pulo duplo, dash, escalada, tiro ou escudo na campanha atual.
As dicas desses poderes não aparecem enquanto não estiverem disponíveis.

## Combate

O mouse mantém sua identidade de arma improvisada: carcaça gasta, cinta metálica
e cabo reforçado, com rastro discreto, som seco e pausa de impacto de 2–3 quadros.
O chicote tem alcance nominal de 100 pixels e tolerância em torno da curva;
paredes bloqueiam os golpes. Cada alvo recebe no máximo um acerto por golpe.
A direção fica fixada ao soltar X. Durante a carga, é possível andar a 75% da
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
proteção. SpeedBug se aproxima com velocidade limitada, avisa a investida por 0,6 segundo,
avança até 160 pixels sem corrigir a direção e recupera por 1,3 segundo.
Na recuperação não há dano de contato.

A substituição de aviões e medalhas por sobrecargas e investidas foi implementada.
RomerBug marca uma faixa de 96 pixels por 0,8 segundo, executa descarga baixa
por 0,25 segundo e recupera por 1 segundo. Os padrões e parâmetros estão em
[PROPOSTA_CHEFE_ROMERBUG.md](PROPOSTA_CHEFE_ROMERBUG.md). A campanha antiga mantém
a transição curta para regressão.

Ao derrotar o boss, os projéteis dele e do jogador e os bugs restantes são
removidos. Não há recompensa coletável nem aumento de vida. A conversa posterior
deixa claro que o objetivo de desligar a energia ainda precisa ser cumprido.

## Arquitetura

| Área | Responsabilidade |
|---|---|
| `jogo.py` | Estados, seleção, prólogo, abdução, infecção e fim do conteúdo |
| `configuracoes.py` | Dimensões comuns, resolução, física e temporizadores |
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
| `recursos.py` | Cache, substitutos visuais e normalização dos sprites |

Cada boss possui classe concreta própria. A base `Chefe` exige uma estratégia
especializada, e tipos desconhecidos não recebem uma implementação genérica.

A campanha antiga de seis professores fica fora do menu principal. Seus dados
continuam disponíveis por `build_legacy_levels()` em `mundo/fases_antigas.py`,
para manutenção e regressão. Seus poderes e diálogos não são requisitos da
campanha atual.

## Arte

As fontes, referências e prompts estão em [recursos/fontes_arte/LEIA_ME.md](recursos/fontes_arte/LEIA_ME.md).
Os sprites preservam proporções, usam uma escala comum entre poses e têm os pés
alinhados dentro do corpo de 40 × 40 pixels. Armas e projéteis possuem áreas próprias.

Para reexportar as artes existentes com Pygame:

```bash
python preparar_figuras_personagens.py
python preparar_figuras_chefes.py
python preparar_figuras_movimento.py
python preparar_recursos_menu.py
python preparar_recursos_escola.py
python preparar_escola_detalhada.py
```

Alguns PNG antigos conservam suas dimensões de exportação originais; o carregador
normaliza todos para o contrato corporal comum em execução. `gerar_recursos.py`
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

Prévias dos novos ambientes: [laboratório](recursos/fontes_arte/previa_laboratorio_detalhado.png),
[corredor](recursos/fontes_arte/previa_corredor_detalhado.png),
[arena](recursos/fontes_arte/previa_batalha_detalhada.png) e
[monitores animados](recursos/fontes_arte/previa_monitores_animados.gif).
Fontes e prompts: [instrucoes_escola_detalhada.json](recursos/fontes_arte/instrucoes_escola_detalhada.json).
Exportação: `python preparar_escola_detalhada.py`.

Prévias da revisão anterior: [menu](recursos/fontes_arte/previa_menu_sombrio.png),
[arena](recursos/fontes_arte/previa_batalha_sombria.png) e
[animação da transformação](recursos/fontes_arte/previa_transformacao_chefe.gif).
Fontes e prompts da ferramenta integrada estão em
[instrucoes_artes_sombrias.json](recursos/fontes_arte/instrucoes_artes_sombrias.json). Para reexportar essas
artes, execute `python preparar_recursos_sombrios.py`.

Capturas anteriores da etapa 4: [reencontro](recursos/fontes_arte/previa_reencontro_virtual.png),
[infecção](recursos/fontes_arte/previa_infeccao_virtual.png) e
[fim do conteúdo](recursos/fontes_arte/previa_fim_conteudo.png).

## Validação e pendências

```bash
python -m unittest discover -s testes -v
```

**92 testes passaram**, incluindo o percurso com salto básico para ambos os
protagonistas, reencontro antes da infecção, transformação a 50%, projéteis,
pausa, limpeza de ameaças, ausência de recompensas e retorno ao menu. Os novos
testes também cobrem as seis poses da cena, fala da entidade, câmera visual,
pausa durante o diálogo, preservação do corpo/vida e retomada sem repetir a cena.
Os testes de arte verificam também o recorte dos monitores, o acompanhamento
da câmera, a escala ampliada e o congelamento visual na pausa. O combate
com chicote foi verificado em condições controladas; isso não comprova o equilíbrio
de sobrevivência por controle manual.

As cenas da etapa 4 foram renderizadas e inspecionadas. A etapa 5 ainda inclui
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

O [AGENTS.md](AGENTS.md) reúne as convenções, a organização do código, os
contratos de jogabilidade e os comandos de validação. Na revisão de 28/10/2026,
os 81 testes passaram e os oito exportadores foram executados em pasta
temporária (74 PNGs), sem alterar as artes aprovadas. O gerador original
`gerar_recursos.py` foi conferido estaticamente; sua execução requer Pillow,
ausente no ambiente utilizado.


## Arquivos e pastas em português

O ponto de entrada é `principal.py`; a configuração fica em `configuracoes.py`
e a máquina de estados em `jogo.py`. O projeto usa as pastas `entidades/`,
`mundo/`, `interface/`, `testes/` e `recursos/`. As imagens ficam em
`recursos/imagens/` e suas fontes em `recursos/fontes_arte/`. Os exportadores
usam o prefixo `preparar_`. O roteiro está em `ROTEIRO_HISTORIA.md`.

Instale com `pip install -r dependencias.txt`, execute com `python principal.py`
e valide com `python -m unittest discover -s testes -v`. Nomes técnicos de
descoberta, como `AGENTS.md`, `__init__.py` e `.gitignore`, foram mantidos.
A renomeação preservou o conteúdo das 160 imagens e animações e passou pelos
81 testes e pelos oito exportadores de arte em pasta temporária.
