# Revisão do duelo com RomerBug — 17/11/2026

O responsável voltou a reprovar a fluidez da luta. A mudança atual substitui sua dinâmica, em vez de apenas ajustar tempos do ciclo de projéteis. Referência técnica anterior: commit `b869985`.

## Referências e decisões de design

O [manual de Castlevania: Dracula X para SNES, transcrito](https://www.world-of-nintendo.com/manuals/super_nes/castlevania_dracula_x.shtml) documenta ataque com chicote, salto e salto para trás. A inspiração adotada é controlar distância e combinar ataque frontal com mobilidade defensiva. Os tempos abaixo são escolhas do IFVania, não medições do jogo de referência.

O [manual de Streets of Rage publicado pela SEGA no Steam](https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/71164/manuals/08%20SOR1_PC_MG_EFIGS_US_v6.pdf) descreve sequência de golpes por repetição do ataque. A adaptação usa encadeamento, reação ao impacto e golpe final de varredura em um único plano de plataforma; não acrescenta deslocamento em profundidade nem agarrões. Esses elementos combinam-se com os controles existentes do IFVania.

## Encontro entregue

| Elemento | Regra |
|---|---|
| Aproximação | Livre em toda a arena; velocidades 2,15 e 3,4, aceleração 0,35; nenhuma limitação de 24 px |
| Ataques | Cruzado à altura do tronco, varrida baixa de maior alcance e avanço para fechar distância |
| Sequência | Dois golpes RomerBug, três SpeedBug; interrompe encadeamento se alvo estiver distante |
| Preparação | 28/20 atualizações no primeiro golpe, 18 nos seguintes; aviso sonoro e punho marcado na altura do ataque |
| Execução | 9 atualizações no golpe, 16 no avanço; direção fixa e dano apenas na área anunciada; paredes cortam alcance |
| Defesa | Q cancela o restante da sequência e deixa 44 atualizações de recuperação; varrida pode ser saltada |
| Contra-ataque | Recuperação natural 40/32 atualizações; dano durante recuperação não encerra a janela |
| Reação ao dano | Até duas interrupções de 10 atualizações antes da resposta; postura firme em laranja comunica limite; execução não é interrompida por dano |
| Transformação | Mesma vida, limiar de metade, cinemática e suspensão protegida preservados |
| Combo do jogador | Próximo toque aceito nas oito últimas atualizações do golpe, memória de dez; consome uma única vez após recolher; interrupções limpam a intenção |

Pés seguem deslocamento real; removidos o balanço e a inclinação contínuos. Arte existente foi reaproveitada. ProjetilProfessor permanece disponível para compatibilidade, mas não integra a escolha automática de ataques deste encontro. Novos padrões são exclusivos de RomerBug/SpeedBug; demais guardiões conservam repertórios próprios.

## Verificações e limites

Comando: `SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy PYGAME_HIDE_SUPPORT_PROMPT=1 .venv/bin/python -m unittest discover -s testes -v`.

176 testes aprovados. Cobrem sequência com novo aviso, perseguição sem trilho, direção fixa, varrida saltável, bloqueio/contra-ataque, interrupção limitada, paredes, combo antecipado/cancelamento, fluxo real de diálogo/dano e transformação com vida compartilhada. Testes que exigiam dois projéteis e longa espera foram atualizados porque esse contrato mudou explicitamente.

Capturas com estado avançado por `Jogo._update`, sem comandos ofensivos, nas duas formas: [RomerBug preparando](romerbug_preparar.png), [golpe](romerbug_executar.png), [recuperando](romerbug_recuperar.png), [SpeedBug preparando](speedbug_preparar.png), [golpe](speedbug_executar.png), [recuperando](speedbug_recuperar.png). A segunda forma foi preparada pelo limiar de dano e liberação cinematográfica. São cenários controlados, não partida humana. Um protagonista piscando por invulnerabilidade pode não aparecer em um quadro isolado.

Não foi homologada diversão, dificuldade ou mix em equipamento real. Reavaliar se o chefe pressiona sem impedir resposta, se as duas/três batidas são legíveis e se a reação ao chicote comunica peso. Referência consolidada em [REVISAO_HUMANA_FINAL.md](../../documentacao/REVISAO_HUMANA_FINAL.md).

Para experimentar diretamente: `.venv/bin/python -m ferramentas.experimentar_campus --duelo`. Para o fluxo integral: `.venv/bin/python principal.py`.
