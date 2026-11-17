# Revisão humana final — IFVania

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
