# Nitidez, combate sombrio e Mente Brilhante — 18/11/2026

O commit solicitado foi feito antes desta revisão: `fe13741` — Integra duelo corporal, parasita humanoide, save, corredor e vegetacao animada. A revisão presente foi incluída em commit próprio, conforme solicitação de 18/11/2026.

## Fatos documentados e criação ficcional

A [matéria da Agência Sebrae RN, de 25/02/2025](https://rn.agenciasebrae.com.br/cultura-empreendedora/exposicao-e-desfile-como-experiencias-imersivas-marcaram-a-4a-mostra-serido-de-moda-cultura-e-design/) identifica Ricardo Rodrigues como professor e diretor do IFRN Campus Caicó naquele evento. A notícia trata de uma mostra do curso de Design de Moda realizada no campus. Não foi inferido que o cargo permaneça o mesmo em 2026.

A [fotografia da matéria](https://rn.agenciasebrae.com.br/wp-content/uploads/sites/20/2025/02/Ricardo-diretor-IFRN-CAICO-scaled.jpg), creditada a Isaac Lima, foi usada como referência de aparência. O avatar mantém cabeça calva, camisa rosa e crachá. A luta, o nome Mente Brilhante, os golpes e o controle pela IFVania são escolhas ficcionais: não descrevem o comportamento ou atributos profissionais da pessoa real.

Na biblioteca, a IFVania aprisionou os registros no avatar do professor. Derrotar o vínculo liberta Ricardo e permite continuar a investigação. Consultas, salto duplo e progressão ao campus continuam funcionando; o Indexador fica apenas como conteúdo legado fora da campanha atual.

## Implementação

- Nitidez: Inimigo agora usa recursos.espelhar_quadro, preservando a fonte de apresentação de 80 px. Antes, pygame.transform.flip produzia outro objeto sem registro HD, que era ampliado a partir de 40 px. O reparo preserva arte, colisões, pés e escala.
- Arte: atlas novo de três personagens e seis poses por personagem. RomerBug mantém terno azul-marinho, camisa, gravata e sapatos; SpeedBug mantém regata laranja, shorts pretos, medalha e tênis. Olhos violetas, tecido rasgado e corrupção reforçam o aspecto sombrio. Exportação separada em 40/80 px e retrato próprio de Mente Brilhante; fontes aprovadas preservadas.
- RomerBug/SpeedBug: soco cruzado, chute, avanço e pulso sombrio a cada quarto ciclo. Pose de chute coincide com alcance maior; especial é um projétil ativo, bloqueável e consumido em colisão. Transformação na metade da mesma vida e cinemáticas anteriores preservadas.
- Mente Brilhante: classe concreta registrada na fábrica, com 18 de vida. Reutiliza primitivas do duelo corporal e possui estratégia e especial próprios. Alterna soco, chute, barrigada e raio; barrigada avança e pode ser interrompida pela guarda. Raio nasce na cabeça visual de 80 px, fixa a trajetória no lançamento e não causa dano corporal simultâneo. Mente Brilhante não se transforma em SpeedBug.
- Retirada de indicadores: removidos setas, círculos de preparação/recuperação, halos de tipos de bugs e contornos de áreas dos golpes. Não se desenha aviso para o raio antes da execução. Poses naturais, sons, projéteis ativos, defesa e feedback de dano permanecem; indicações de objetivos e perigos do cenário não são avisos de ataques de inimigos.
- Saves existentes continuam usando o identificador biblioteca e o índice 1. Ao carregar, a fábrica usa o novo chefe; bibliotecas já concluídas não reativam a luta.

## Evidências

200 testes aprovados com SDL dummy. Novas regressões verificam fonte HD espelhada, ausência de marcadores fora do corpo, origem/tempo/trajetória do raio, guarda contra barrigada, repertório, especial sombrio e ausência de transformação indevida. O teste do antigo carimbo de faixas foi substituído pelo contrato corporal do novo chefe; demais testes de biblioteca, pausa, arma e progressão continuam ativos.

18 exportadores verificados em cópia temporária, 257 PNGs distintos. O novo exportador foi executado em `/tmp` antes de integrar os arquivos utilizados pelo jogo. Fundo residual de baixa opacidade do atlas é filtrado no exportador; fonte original preservada.

Capturas controladas: [Mente Brilhante — soco](mente_soco.png), [chute](mente_chute.png), [barrigada](mente_barrigada.png), [raio pela cabeça](mente_raio.png), [RomerBug de terno](romerbug_terno_sombrio.png), [SpeedBug corredor](speedbug_corrida_sombrio.png). Foram preparados estados de combate com física real; não representam uma partida humana completa.

Reprodução das capturas: `SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python -m ferramentas.experimentar_mente_brilhante --capturas avaliacao/mente_brilhante`. Para experimentar: `python -m ferramentas.experimentar_mente_brilhante`; para campanha completa: `python principal.py`.

A revisão humana de dificuldade sem marcadores, diversão, tom visual e caricatura permanece em [REVISAO_HUMANA_FINAL.md](../../documentacao/REVISAO_HUMANA_FINAL.md). Não foi solicitada nova aprovação para implementar as decisões já autorizadas.
