# Plano de execução — IFVania

**Data:** 29/10/2026

Referências: `DOCUMENTO_DE_REQUISITOS.md` versão 3.1 e `ROTEIRO_HISTORIA.md`.

## Estratégia

Implementar por etapas verificáveis. Preservar as alterações existentes no HistoryBoard e nas referências visuais. A campanha antiga permanece disponível durante a primeira etapa para validar regressões; sua permanência não representa aprovação narrativa das seis fases.

## Etapa 1 — Dimensões e arquitetura dos bosses

- [x] Definir dimensões corporais comuns em `configuracoes.py`, 40 × 40 pixels, mantendo a altura corporal e aproximando a escala visual de humanos e bugs.
- [x] Aplicar as dimensões ao jogador, bugs, bosses e às duas formas de RomerBug.
- [x] Carregar sequências de sprites com escala proporcional compartilhada, alinhamento dos pés e filtro sem suavização; tratar poses de ataque como exceção visual, sem alterar colisão corporal.
- [x] Adequar pontos de surgimento para manter os pés no piso e evitar sobreposição com blocos.
- [x] Dar classe própria a cada boss existente, com seleção de ataques própria e registro explícito de tipos, sem fallback para boss genérico.
- [x] Validar dimensões, transformações, chão das arenas, ataque com chicote e regressões existentes.

**Aceite:** CA-08 e CA-09 para as entidades disponíveis, junto aos testes existentes de encontro e combate. A validação visual definitiva inclui os personagens que serão criados nas próximas etapas.

## Etapa 2 — Menu e seleção do protagonista

- [x] Criar fachada em pixel art baseada em `referencia/fachada_escola.png`.
- [x] Implementar Jogar e Sair com clique e navegação por teclado.
- [x] Implementar tela de escolha Menino / Menina e persistência da seleção na campanha.
- [x] Criar e integrar spritesheet completo da Menina, cobrindo os mesmos estados do Menino e as dimensões comuns.
- [x] Verificar entrada, encerramento e ambas as opções de personagem: CA-01 e CA-02.

**Dependência:** etapa 1 para o contrato de dimensões e animações. Usar o fluxo de geração de imagens para arte nova; não considerar imagens substitutas como arte concluída.

## Etapa 3 — Introdução e percurso escolar

- [x] Substituir a introdução de CODIGO.EXE pela aula de Max, apresentação e revolta da IFVania.
- [x] Integrar representações de Max e Romerito baseadas nas referências, com dimensões comuns.
- [x] Construir corredores e A28 como adaptação lateral jogável; consulta ao link do Maps tentada, sem planta acessível. O laboratório A28 foi conferido na referência oficial; o traçado interno real continua sem homologação.
- [x] Implementar gatilhos únicos para encontro, ataque, abdução e transporte ao mundo virtual.
- [x] Apresentar a descoberta do mouse na bolsa antes de liberar seu uso.
- [x] Validar ordem narrativa e suspensão da simulação nos diálogos: CA-03 e CA-10.

## Etapa 4 — Primeira fase da nova campanha

- [x] Ajustar o percurso virtual para funcionar sem depender das habilidades da campanha antiga.
- [x] Inserir a fala de Romerito sobre Brasília e corridas e a infecção antes do combate.
- [x] Revisar aviões, medalhas, perseguição e transformação única a 50%, preservando vida e tamanho.
- [x] Encerrar ataques e projéteis ao derrotar o boss.
- [x] Remover recompensas e mensagens antigas sem respaldo no novo roteiro.
- [x] Separar a campanha antiga do fluxo principal; o fim do conteúdo disponível deve indicar que a jornada continua, sem anunciar a escola salva.
- [x] Validar CA-04 a CA-07 e repetir CA-08 com os novos personagens.

## Etapa 5 — Integração e homologação

- [ ] Revisar HUD, dicas de comandos, câmera, legibilidade, pausa e fechamento em cada tela.
- [ ] Executar os testes de regressão e o roteiro CA-01 a CA-10.
- [ ] Fazer inspeção visual e teste manual da primeira fase com Menino e Menina.
- [ ] Atualizar README, controles e estado de implementação no documento de requisitos.
- [ ] Registrar resultados, limitações e parâmetros de balanceamento sem declarar recursos pendentes como implementados.

## Decisões de conteúdo ainda necessárias

As fases após RomerBug, recompensas, quantidade final de bosses e sequência de desligamento da energia não foram descritas no HistoryBoard. Sua implementação depende de definição narrativa posterior; as etapas acima podem avançar sem inventar esse conteúdo.

## Registro de execução

- Etapa 1 implementada: dimensão lógica comum de 40 × 40 pixels, normalização proporcional das sequências, alinhamento dos pés, surgimento em piso livre e classes concretas com estratégias próprias para os seis bosses existentes.
- `Chefe` passou a ser abstrata para a escolha de ataques; tipos desconhecidos são rejeitados, sem substituição por um boss genérico.
- Inspeção visual feita com todas as entidades disponíveis lado a lado, incluindo SpeedBug. As silhuetas preservam suas proporções naturais dentro da mesma área; Max, Romerito humano e Menina serão verificados após a criação de suas artes.
- Validação: 31 testes passaram com Python 3.9.6 e Pygame 2.6.1, incluindo seis novos testes de dimensões, normalização, surgimento e estratégias. Comando: `python -m unittest discover -s testes -v`.
- O Python 3.15 instalado no sistema não compilou Pygame 2.6.1; a validação usou ambiente temporário com Python 3.9.6, sem mudar as dependências do projeto.
- Etapa 2 implementada: fachada baseada na fotografia, Jogar/Sair com mouse e teclado, seleção com prévia animada e confirmação, onze quadros da Menina e persistência da escolha entre fases e reaparecimentos.
- Introdução textual da etapa 3 atualizada: aula de Max, nome completo da IFVania, anúncio de desligamento, revolta, hipnose/alucinações e objetivo de cortar a energia. O percurso escolar e o combate virtual foram concluídos nas etapas 3 e 4 descritas abaixo.
- Artes geradas com a ferramenta integrada `image_gen`; fontes, prompts e PNG de execução estão no repositório. Exportação reproduzível: `python preparar_recursos_menu.py`.
- Validação ao concluir a etapa 2: 42 testes passaram com Python 3.9.6 e Pygame 2.6.1. Onze novos testes cobrem menu, ambas as opções, preservação da escolha, reinício de progresso, pausa da simulação e isolamento de eventos entre telas.
- Inspeção visual feita nas capturas de menu, seleção, introdução, primeira fase com Menina e todos os seus quadros nas duas direções. Também foram atualizadas e desenhadas as doze combinações entre dois protagonistas e seis mapas por 60 quadros cada, sem abrir janela.
- Etapa 3 implementada em 22/10/2026: aula com Max e mudança visual dos monitores na revolta da IA; corredor navegável com placas e acesso ao A28; encontro com Romerito por E; investida, recuo do protagonista e abdução animada; transporte para o mapa virtual e descoberta do mouse na bolsa antes de liberar o chicote.
- `FaseEscolar` mantém cenários sem inimigos/boss antecipado e gatilhos únicos. O mesmo protagonista atravessa as cenas. A arma fica bloqueada na escola e durante a descoberta; diálogos e pausa suspendem a simulação, inclusive o transporte.
- Max e Romerito possuem dois quadros cada, derivados das fotos de `referencia/`, com transparência e corpo comum de 40 × 40. Fontes e prompts salvos no projeto; exportação: `python preparar_recursos_escola.py`.
- Referência geográfica: o link curto do Maps não abriu uma planta consultável. A página oficial sobre horários dos laboratórios confirma A28: https://portal.ifrn.edu.br/campus/caico/noticias/horarios-laboratorios-de-informatica/ . As portas A25–A27 e as distâncias do corredor são composição de cenário, sem afirmação de posição real.
- Validação ao concluir a etapa 3: 51 testes passaram com Python 3.9.6 e Pygame 2.6.1. Os nove testes novos percorrem a rota com movimento real para Menino/Menina, conferem a ordem dos eventos, proximidade e tecla E, gatilhos únicos, ataque narrativo, arma bloqueada, pausa, dimensões, câmera e texto.
- Inspeção visual: aula, corredor, A28, abdução e descoberta do mouse; cenas escolares e transporte também renderizados sem janela com os dois protagonistas.
- Etapa 4 implementada em 23/10/2026: a campanha principal contém somente o mapa virtual previsto no HistoryBoard. Os seis mapas antigos, seus diálogos e poderes foram isolados em `mundo/fases_antigas.py`, fora do menu.
- O mapa fixo tem piso contínuo, degraus de 32/64 pixels, quatro bugs e arena plana. O piso mantém os personagens visíveis acima do diálogo. Foi percorrido com movimento e salto básicos, sem poderes, com ambos os protagonistas.
- Romerito aparece humano, fala de Brasília e corridas e é infectado por um bug em uma sequência de 60 atualizações. Ataques ficam bloqueados até seu término; a pausa suspende a infecção. O corpo e a vida são preservados.
- RomerBug/SpeedBug conservam a transformação única a 50%, os aviões, as medalhas e a perseguição. Após a derrota, ameaças e projéteis são removidos, sem item ou bônus de vida.
- A saída permanece bloqueada até a derrota. O fim do conteúdo apresenta “A jornada continua”, informa que a IFVania segue ativa e permite voltar ao menu e reiniciar a campanha.
- Validação ao concluir a etapa 4: 61 testes passaram com Python 3.9.6/Pygame 2.6.1. Os dez novos testes cobrem a campanha isolada, percurso básico, diálogo/infecção, pausa, dimensões, duas formas, limpeza, ausência de recompensa e encerramento/reinício. O combate por teclado foi verificado para Menino e Menina em condições controladas, sem representar homologação do balanceamento de sobrevivência.
- Inspeção visual: percurso, Romerito humano, infecção, SpeedBug, derrota e tela de continuação; capturas em `recursos/fontes_arte/virtual_*_preview.png` e `previa_fim_conteudo.png`.
- Próxima etapa: integração e homologação (etapa 5), incluindo teste manual, revisão integrada e balanceamento. O conteúdo narrativo posterior continua sem definição.

## Ajustes solicitados em 25/10/2026

- [x] Estilizar menu, seleção, cartões, pausa, diálogos e HUD com uma paleta escura legível.
- [x] Criar fachada noturna e fundo de laboratório escolar, preservando colisões e percurso.
- [x] Implementar a transição a 50%: uma perna apoiada, entidade, fala “Ainda não terminou.”, metamorfose e levantamento.
- [x] Aplicar aproximação/retorno suaves da câmera apenas no desenho; congelar combate e permitir pausa em toda a cena.
- [x] Preservar vida restante e corpo; limpar ataques/projéteis e oferecer proteção na retomada.
- [x] Apresentar proposta para substituir aviões/medalhas, sem aplicar mudança mecânica ainda não escolhida.

Artes feitas com a ferramenta integrada image_gen, fontes preservadas em
`recursos/fontes_arte/`, prompts em `instrucoes_artes_sombrias.json` e exportação reproduzível
com `python preparar_recursos_sombrios.py`. A entidade permanece de origem indefinida.

Validação da revisão de 25/10: 68 testes passaram. Os sete novos testes cobrem transição,
pausa e fala, vida/corpo, retomada, zoom visual, poses e legibilidade das dicas.
Foram inspecionadas capturas do menu, seleção, arena e etapas da transformação;
prévia animada em `recursos/fontes_arte/previa_transformacao_chefe.gif`.

A proposta está em `PROPOSTA_CHEFE_ROMERBUG.md`. A etapa 5 ainda requer homologação
manual e balanceamento; esta revisão não a declara concluída.

## Ajuste de proporção — 26/10/2026

Conforme a delimitação do responsável, somente o protagonista (Menino/Menina) e
os bosses recebem escala visual de 110%, durante toda a partida, incluindo
exploração, combate e transformação. São desenhados em 44 × 44 com apoio dos pés
preservado. Professores enquanto NPCs, bugs e entidade permanecem em 40 × 40. Colisões, velocidades, alcance e geometria do mapa permanecem iguais.
A escala fica centralizada em `configuracoes.ESCALA_VISUAL_PERSONAGEM`.

## Escala e arte escolar — 27/10/2026

A solicitação atual amplia também os NPCs e substitui a escala da revisão de
26/10: protagonista, bosses, professores e entidade usam 80 × 80 visuais; bugs
mantêm 40 × 40. Colisões de todos permanecem em 40 × 40. Os nomes dos NPCs,
a captura pela IFVania e a saída do chicote acompanham a nova apresentação.

Os laboratórios e corredores receberam novas fontes em resolução nativa de
960 × 540 por módulo, sem esticar um único painel para todo o corredor. Móveis,
portas e computadores recebem detalhes em camadas. Os terminais mudam texto,
gráficos e estados dentro da tela, acompanham a câmera e refletem a corrupção.
Seu relógio é visual: funciona em diálogos sem atualizar física/combate e congela
na pausa. A arena usa o mesmo sistema de monitores.

Artes novas feitas com image_gen e preservadas em `recursos/fontes_arte/`;
prompts em `instrucoes_escola_detalhada.json`. Exportação:
`python preparar_escola_detalhada.py`. Prévia animada:
`recursos/fontes_arte/previa_monitores_animados.gif`.

Validação atual: 74 testes passaram; seis novos testes cobrem escala, recorte
dos monitores, câmera, animação em diálogos/pausa e alcance da ponta do chicote.
Inspeção visual de aula, laboratório, corredor, arena, ataque e transformação.
A homologação manual e o balanceamento da etapa 5 continuam pendentes.


## Caminhada e diálogos personalizados — 27/10/2026

- [x] Criar ciclos de oito quadros para Menino e Menina, preservando as artes anteriores.
- [x] Sincronizar os quadros com o deslocamento real e interromper a caminhada contra paredes; corrigir a pose de entrada e reaparecimento.
- [x] Inserir tela de nome entre seleção e aula, com acentos, limite de 20 caracteres, validação, edição e retorno.
- [x] Reescrever a introdução como diálogo iniciado pelo aluno com Max, sem narrador.
- [x] Aplicar o nome nas falas do aluno e nas respostas dos professores, preservando-o nas transições.
- [x] Validar 81 testes automatizados e inspecionar capturas da entrada de nome e dos diálogos.

Prévias em `recursos/fontes_arte/previa_nome_jogador.png`,
`previa_introducao_aluno.png`, `previa_resposta_com_nome.png` e
`previa_caminhada_jogador.gif`. A homologação manual da etapa 5 permanece pendente.


## Nomenclatura em português e orientações — 28/10/2026

- [x] Renomear classes, variáveis, atributos, parâmetros e constantes próprios
  no jogo, testes e exportadores, preservando interfaces externas.
- [x] Atualizar importações, herança, callbacks, argumentos nomeados e acessos
  dinâmicos, sem modificar os caminhos dos módulos e imagens.
- [x] Criar `AGENTS.md` com convenções e contratos do projeto.
- [x] Atualizar referências técnicas na documentação.
- [x] Executar os 81 testes e os oito exportadores em pasta temporária (74 PNGs).

`gerar_recursos.py` passou por conferência estática de sintaxe e referências;
sua execução não foi realizada porque Pillow não está instalado no ambiente.
A homologação manual da etapa 5 continua pendente.


## Arquivos e pastas em português — 28/10/2026

- [x] Renomear código, testes, exportadores, documentação, imagens e pastas
  próprias: 224 caminhos atualizados.
- [x] Atualizar importações, carregamento de imagens, nomes de quadros gerados,
  comandos e links locais. Preservar nomes técnicos de descoberta.
- [x] Conferir os 81 testes, os oito exportadores e a entrada `principal.py`.
- [x] Conferir todos os links locais e preservar os bytes das 160 imagens/GIFs.

Os comandos atuais são `python principal.py` e
`python -m unittest discover -s testes -v`; dependências em `dependencias.txt`.
As fontes de arte ficam em `recursos/fontes_arte/`. A homologação manual
da etapa 5 continua pendente.


## Revisão de controle, combate e plataformas — 28/10/2026

- [x] Movimento a 3,2 px/quadro, aceleração/frenagem curtas, tolerância de borda e memória de salto.
- [x] Corrigir direção e persistência do recuo de dano.
- [x] Chicote tolerante com alcance 100, carga de 0,6 s/dano 2, cancelamento e efeitos de peso.
- [x] Esquiva básica com recarga e proteção curta, tutorial e HUD.
- [x] Sobrecarga anunciada e investida de direção fixa, com recuperação e sem dano de contato passivo.
- [x] Contorno e faixa nas superfícies de apoio expostas, sem alterar colisões.
- [x] Atualizar regressões dos ataques substituídos e validar 92 testes.
- [x] Renderizar e inspecionar carga, mouse reforçado, plataformas e avisos dos ataques.

Cenários determinísticos sem invulnerabilidade artificial cobrem fuga da descarga
e salto sobre a investida. Isso não substitui homologação humana de sobrevivência,
ritmo e dificuldade; a etapa 5 permanece pendente.


## Ciclo de projéteis e investida — 29/10/2026

- [x] Restaurar aviões de RomerBug, com 2,3 s entre lançamentos e aviso prévio.
- [x] Restaurar medalhas de SpeedBug a cada 1,5 s, com movimento curto limitado.
- [x] Alternar dois lançamentos, pausa, investida anunciada e recuperação.
- [x] Esperar os projéteis saírem antes de preparar a investida.
- [x] Manter transformação, proteção, controles do aluno e plataformas.
- [x] Validar 95 testes; homologação humana de ritmo/dificuldade segue pendente.
