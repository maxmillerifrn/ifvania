# Revisão humana final — IFVania

## Atualização vigente — parasita humanoide, cenas e save (17/11/2026)

Bloqueio com Q permite caminhada animada na velocidade normal, salto e troca de direção, mantendo resistência e proteção frontal. Os bugs agora têm corpo humanoide, com poses próprias de repouso, corrida e dano. O golpe que eliminaria o último bug do A28 inicia uma cena: ele corre até Romerito e se funde ao professor. Entrar na arena sozinho não dispara mais a transformação. A metamorfose aos 50% permanece protegida e agora revela SpeedBug com armadura escura e corrupção violeta. Após a vitória, o parasita sai do corpo e se desintegra antes do diálogo de libertação.

Salvamento automático em `dados/salvamento.json`, ignorado pelo Git: um slot, com versão e gravação atômica. Checkpoints nas entradas, durante travessias seguras, antes do confronto e após vitória. F5 grava o checkpoint atual; R após morrer retoma nele com integridade completa. O menu oferece **Continuar** quando há arquivo válido. Nome, aparência, habilidades, objetivos, vitórias e inimigos já eliminados antes do checkpoint são preservados. Chefes não vencidos reiniciam com vida completa; não se salva no meio de um golpe/cena. O prólogo não possui checkpoint; o primeiro fica no mundo virtual. Novo jogo substitui o slot quando atinge esse ponto. Ferramentas de experimentação não sobrescrevem o save do jogador.

O novo contrato substitui as descrições anteriores de progresso somente em memória e movimento reduzido na guarda. Evidências, arquitetura do save e revisão pendente no [relatório](../avaliacao/parasita_e_save/RELATORIO.md).


## Revisão adicional de 17/11/2026

Conferir apoio dos pés e altura do bug na fusão, caminhada do A28 até a biblioteca e intensidade da brisa no jardim/recreio. As mudanças estão implementadas e cobertas por 193 testes; falta avaliar a naturalidade numa partida humana. [Evidências](../avaliacao/corredor_e_vento/RELATORIO.md).

## Atualização vigente — parasita humanoide, cenas e save (17/11/2026)

Bloqueio com Q permite caminhada animada na velocidade normal, salto e troca de direção, mantendo resistência e proteção frontal. Os bugs agora têm corpo humanoide, com poses próprias de repouso, corrida e dano. O golpe que eliminaria o último bug do A28 inicia uma cena: ele corre até Romerito e se funde ao professor. Entrar na arena sozinho não dispara mais a transformação. A metamorfose aos 50% permanece protegida e agora revela SpeedBug com armadura escura e corrupção violeta. Após a vitória, o parasita sai do corpo e se desintegra antes do diálogo de libertação.

Salvamento automático em `dados/salvamento.json`, ignorado pelo Git: um slot, com versão e gravação atômica. Checkpoints nas entradas, durante travessias seguras, antes do confronto e após vitória. F5 grava o checkpoint atual; R após morrer retoma nele com integridade completa. O menu oferece **Continuar** quando há arquivo válido. Nome, aparência, habilidades, objetivos, vitórias e inimigos já eliminados antes do checkpoint são preservados. Chefes não vencidos reiniciam com vida completa; não se salva no meio de um golpe/cena. O prólogo não possui checkpoint; o primeiro fica no mundo virtual. Novo jogo substitui o slot quando atinge esse ponto. Ferramentas de experimentação não sobrescrevem o save do jogador.

O novo contrato substitui as descrições anteriores de progresso somente em memória e movimento reduzido na guarda. Evidências, arquitetura do save e revisão pendente no [relatório](../avaliacao/parasita_e_save/RELATORIO.md).


## Revisão vigente — duelo corporal (17/11/2026)

A nova avaliação humana reprovou a fluidez da luta com RomerBug. O encontro foi redesenhado: aproximação livre, cruzado, varrida baixa e avanço curto substituem o roteiro automático de aviões/medalhas. RomerBug encadeia dois golpes; SpeedBug encadeia três, aproxima mais rápido e mantém a mesma reserva de vida. Cada golpe tem preparação sem dano, direção fixa durante execução e recuperação. Q bloqueia e cancela a sequência inteira, abrindo 44 atualizações de contra-ataque. A varrida tem aviso baixo e pode ser saltada.

Os primeiros dois acertos fora da execução/recuperação provocam recuo breve; depois o chefe firma a postura até completar sua resposta, continuando a receber dano. Isso limita aprisionamento por interrupções. O próximo toque do combo pode ser antecipado nas últimas oito atualizações do recolhimento; carga e ataque na soltura continuam preservados. Foram retirados o limite artificial de deslocamento e o balanço contínuo do corpo.

Experimentação direta: `.venv/bin/python -m ferramentas.experimentar_campus --duelo`. É um atalho de desenvolvimento sem habilidades futuras; não altera o menu nem a campanha. Fontes de inspiração, parâmetros e evidências em [RELATORIO.md](../avaliacao/duelo_romerbug/RELATORIO.md). A avaliação humana da nova dinâmica continua aberta; os registros de 16/11 abaixo descrevem a versão anterior quando divergirem deste trecho.


A implementação técnica H0–H9 foi integrada em 16/11/2026. Conforme orientação do responsável, decisões reversíveis foram tomadas e a avaliação humana foi adiada para esta lista. Não há solicitação de aprovação pendente que impeça jogar. Testes e capturas controladas não comprovam diversão ou uma partida completa.

## Decisões adotadas

- Q segurado bloqueia ataques frontais após descobrir o mouse. Movimento cai para 35%; ataques exigem soltar a guarda. Resistência 100, custo 26 por ponto de dano, janela de 12 atualizações por impacto, quebra de 48 e espera de 45 antes de regenerar. Ataques pelas costas e perigos ambientais atravessam a guarda. Bloquear investida interrompe seu avanço.
- SpeedBug limita o deslocamento antes de resolver colisões, pode voltar de uma extremidade quando o jogador troca de lado e usa deslocamento real para animar. Reposicionamentos entre ataques evitam longos períodos imóveis; preparação e recuperação continuam intencionais.
- As quatro classes concretas de guardiões compartilham primitivas em um módulo, mantendo repertório próprio. Factory, State Machine, Command, Strategy e Observer são obrigatórios e estão em uso.
- Ancoragem usa conectores fixos, sem balanço livre. Quedas retornam ao último apoio seguro, custam uma unidade de integridade sem matar e conservam objetivos. Revisitar fase concluída não ressuscita chefe nem cura.
- Progresso permanece em memória por sessão; salvar em disco e replay de chefes não integram este plano.
- Avatares são homenagens ficcionais; campus é uma adaptação espacial, sem pretensão de planta arquitetônica. Fontes e referências estão na proposta e nos registros de arte.
- Ambiências são sintetizadas localmente, em volume baixo. M alterna áudio. Desligamento final é seguro: monitores, nobreak e pendrive isolado são apresentados antes da sala física e fachada iluminada.

## Roteiro de revisão pendente

| Prioridade | Experimentação humana | Critério e registro esperado |
|---|---|---|
| Alta | Jogar seis fases e todas as travessias com as duas aparências | Anotar bloqueadores com fase, posição, ação e reprodução; confirmar orientação sem ferramentas de desenvolvimento |
| Alta | RomerBug/SpeedBug: aproximação, limites, parede, transformação e bloqueio | Distinguir pausas anunciadas de travamento; registrar qualquer imobilidade persistente com posição do jogador |
| Alta | Combo, carga, Q, esquiva e ancoragem sob pressão | Avaliar conforto, clareza do dano, utilidade de defender e ausência de combinações dominantes |
| Alta | Chefes e composição de inimigos | Avaliar diversão, justiça dos avisos, sobrevivência e variedade; sugerir ajuste de janelas/quantidades com exemplos |
| Média | Primeiro ciclo biblioteca → campus → Elias → campus | Cronometrar referência de 10–15 minutos e revisar caminhadas longas, placas, atalhos e pistas |
| Média | Queda, morte, revisita, pausa, foco e diálogos | Confirmar sensação de retomada justa, objetivos preservados e ausência de entradas involuntárias |
| Média | Áudio em equipamento real | Avaliar mix, repetição da ambiência, impacto de acertos e silêncio com M; execução sem áudio não valida mix |
| Média | Arte e referências | Rever fluidez de caminhada/poses, alunos, contraste, escala e caricaturas respeitosas; confirmar locais reais/adaptados quando necessário |
| Média | Desfecho completo | Confirmar compreensão de Francisco liberto, rede isolada, nobreak desligado, tarefa refeita e ausência de ameaça residual |
| Baixa | Desempenho e acessibilidade | Avaliar máquina alvo, legibilidade em movimento, conforto das teclas e intensidade de efeitos |

A homologação humana de H9 e da etapa 5 permanece aberta. Os itens acima são revisão de experiência e confirmação de referências, não funcionalidades técnicas que aguardem autorização para implementação.
