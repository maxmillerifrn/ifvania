# Parasita humanoide e salvamento — 17/11/2026

## Alterações jogáveis

- Q permite movimentação normal em postura de guarda. Os quadros acompanham deslocamento real e o salto mantém a defesa. Ataque exige soltar Q; resistência, proteção frontal e quebra permanecem.
- Bugs receberam atlas humanoide em fonte separada. Repouso, duas passadas e reação ao dano preservam corpo lógico de 40 × 40. SpeedBug usa outra linha do atlas, com armadura escura e corrupção violeta; visual em 80 px e colisões preservadas.
- Ao receber o golpe fatal, o último bug da primeira fase é retirado do combate e corre até Romerito numa cena pausável. A câmera acompanha a fuga; o parasita encolhe e partículas convergem na fusão. RomerBug aparece e o diálogo antecede o combate.
- A transformação aos 50% conserva vida, posições e janelas de proteção; mistura as poses com a nova forma sombria e energia violeta.
- Na derrota, uma cena de 150 atualizações expulsa o bug, apresenta Romerito humano e dispersa fragmentos. Só depois são registrados a vitória e o diálogo de libertação.

## Save e checkpoints

`ArmazemSalvamento` valida JSON versão 1 e usa arquivo temporário, flush/fsync e substituição atômica. Erro de escrita preserva o save anterior e aparece como mensagem; arquivo ausente/inválido não habilita Continuar nem quebra o menu. Não se usa pickle.

`ControleCheckpoints` é composição de Jogo. Guarda nome, aparência, habilidades pelos nomes estáveis, capacidade de vida, conjuntos de progresso e cena/checkpoint. Registra inimigos ativos por identificador de spawn, evitando reintroduzir os já eliminados antes daquele ponto. Ao restaurar, a fábrica reconstrói a cena e os eventos reconstituem progresso; posições inválidas/sem apoio caem no surgimento seguro. Um checkpoint anterior à fusão mantém os bugs restantes; o checkpoint do confronto já considera a fusão concluída. Um chefe vencido não ressuscita.

Há checkpoint na entrada de cada fase/setor, em travessia após 46% do mapa quando há chão seguro, na aproximação da arena, ao concluir a fusão e após a libertação. Objetivos e habilidades atualizam o save nos diálogos e durante jogabilidade. Morte reinicia o encontro a partir do checkpoint com vida completa. Chefes não vencidos voltam à primeira forma com vida completa; dano parcial e posição no meio de uma animação não são persistidos.

F5 grava o checkpoint registrado; não cria uma posição arbitrária no ar ou durante uma luta. O menu apresenta Novo jogo, Continuar e Sair quando o slot existe. O arquivo fica em `dados/salvamento.json`, fora do versionamento. O prólogo não é salvo; um novo jogo substitui o slot no primeiro checkpoint virtual. A execução normal ativa escrita em disco; construção isolada de Jogo não grava por padrão. Testes de persistência fornecem caminho temporário explicitamente. Ferramentas de experimentação usam somente checkpoints em memória.

## Validação

187 testes aprovados com SDL dummy. Onze regressões novas exercitam arquivo real em pasta temporária, leitura por outra instância, seleção Continuar, morte/retomada, preservação de inimigos, corrupção, falha atômica, vitória, fusão acionada pelo último golpe, pausa, cenas e caminhada defensiva. A suíte anterior foi atualizada para o novo contrato narrativo: a fusão precede o diálogo e a expulsão precede a vitória.

16 exportadores executados em cópia temporária, com 219 PNGs distintos. A fonte anterior e os recursos aprovados foram preservados; nenhum gerador original foi executado sobre eles.

Capturas controladas: [fuga](fuga.png), [fusão](fusao.png), [guarda caminhando](guarda_caminhando.png), [metamorfose](metamorfose_sombria.png), [SpeedBug sombrio](speedbug_sombrio.png), [expulsão](expulsao.png), [desintegração](desintegracao.png), [menu com Continuar](menu_continuar.png).

Reprodução: `SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy .venv/bin/python -m ferramentas.experimentar_parasita`. O menu capturado usa save temporário; a ferramenta não modifica o slot real.

Não houve partida humana integral. Revisar duração das cenas, caminhada defensiva, legibilidade dos novos corpos e distância entre checkpoints. Esses pontos estão em [REVISAO_HUMANA_FINAL.md](../../documentacao/REVISAO_HUMANA_FINAL.md) e não impedem experimentar a implementação.
