# Revisão da arte e do percurso escolar

Ajuste solicitado após reprovação da arte procedural da luva e da retirada do percurso escolar.

## Resultado

- Luva com sprites texturizados de repouso, punho e mão aberta; tecido escuro, metal envelhecido, juntas discretas. Removidos núcleo circular luminoso e braço geométrico. A luva de combate acompanha a mão da pose, com alcance e colisões preservados.
- Removida a mesa sobreposta à cama e o painel de pesquisa. Materiais na escrivaninha existente, telemetria no monitor. A pesquisa assistiva e as falas de Max continuam.
- Após a noite, o protagonista leva pendrive e luva ao IFRN. A cena externa usa a fachada já existente.
- Na sala: “Professor Max, trouxe a atividade. Depois da apresentação, quero mostrar como ficou nossa luva!”. Max responde sobre os testes de preensão antes de apresentar a atividade.
- Arquivo executado na escola; crise, corredor jogável, Romerito, sucção e mundo virtual seguem a sequência original. Não há mais transporte doméstico. Memórias e falas do A28 foram ajustadas para a nova continuidade.
- F continua pulando a abertura diretamente para a campanha. Pausa, nome, aparência e equipamento preservados.

## Evidências

211 testes aprovados na suíte completa com SDL dummy. O teste da introdução percorre agora casa → sala → corredor → laboratório → sucção → A28, confirma identidade do jogador e impede combate antes da descoberta. Os testes históricos continuam cobrindo o percurso escolar dos dois protagonistas.

`python -m ferramentas.capturar_luva` renderiza os 4.890 quadros da abertura (81,5 s), caminha pelo corredor e laboratório por entradas simuladas, resolve diálogos e registra 12 capturas. Não altera o save real. `07_apresentacao_max.png` mostra a fala solicitada; `03_pesquisa.png` e `12_soco.png` mostram a nova arte em contexto. As imagens anteriores, na pasta superior, documentam a versão rejeitada, não esta revisão.

Exportação dos sprites verificada em pasta temporária antes da integração. Fonte, ferramenta e prompt: [registro de arte](../../../recursos/fontes_arte/luva_robotica/REFERENCIAS.md).

Revisão visual feita nas capturas da engine. Ainda não houve avaliação manual com janela e áudio nem aprovação do novo acabamento pelo usuário. Nenhum commit criado.
