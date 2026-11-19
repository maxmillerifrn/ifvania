# Luva robótica e abertura — 18/11/2026

## Análise e decisões

A máquina de estados de `sistema/jogo.py` já separava introdução, diálogo, partida, pausa e transformações. A abertura doméstica tinha relógio próprio e fundos de fachada/quarto, mas a oscilação ocorria enquanto o protagonista dormia e terminava na descoberta de um mouse. O combate já oferecia três golpes, carga na soltura, ataques direcionais, guarda frontal, esquiva, recuo e pausa de impacto. A proposta foi integrada a esses sistemas, sem uma segunda simulação de combate.

`Jogador` conserva física e corpo lógico de 40 × 40. `LuvaRobotica` substitui a instância da arma e reutiliza de `ChicoteMouse` somente o resolvedor de acertos, janelas, paredes, invulnerabilidade e efeitos de carga. A trajetória e o desenho são próprios: extensão corporal curta, carcaça verde, articulações de cobre, núcleo ciano e dedos articulados. Os atributos `chicote`/`chicote_desbloqueado` permanecem como contratos internos de consumidores e ferramentas antigas; a arma ativa é sempre a luva. Arte aprovada e arquivos de imagens anteriores não foram sobrescritos.

`Fase` continua resolvendo inimigos, colisões e chefes. RomerBug/SpeedBug mantêm vida compartilhada e transformação; Mente Brilhante e os quatro guardiões mantêm suas classes. As recompensas novas entram pela conclusão do encontro. O enum de habilidades foi ampliado ao final, preservando valores anteriores. O save existente já grava nomes de habilidades e conserva os módulos, sem nova versão de arquivo.

## Sequência integrada

São seis cenas temporizadas (82,5 segundos) e um sétimo momento jogável:

1. Chegada do IFRN Campus Caicó, entrada na residência, mochila e materiais.
2. Atividade de programação delegada à IA enquanto o aluno prioriza a pesquisa.
3. Bancada com componentes, sensor, gráfico de preensão, ferramentas, transmissão e luva articulada; diálogo com Max sobre precisão, reabilitação e acessibilidade.
4. Oscilação com o aluno acordado e a luva conectada; código incorpora sensores, atuadores, força e defesa às regras do mundo.
5. Atividade concluída sem revisão; luva junto à cama, sono e monitor ainda ativo: “AMBIENTE VIRTUAL INICIALIZADO.”
6. Madrugada, despertar, luva equipada, fragmentação digital e atração ao monitor. A transição existente revela o A28.
7. Descoberta da luva modificada e tutorial sobre o primeiro bug real da fase. Objetivos observam movimento, guarda, esquiva, ataque e combo, encerrando após a derrota do bug. A primeira ameaça frontal pode ativar proteção automática; ataques pelas costas continuam perigosos. O tutorial não bloqueia a exploração.

F pula a cinematografia, inclusive a partir da pausa da introdução, e inicia o A28 com a luva básica e sem poderes futuros. ESC pausa o relógio e os efeitos. O caminho assistido inicia o tutorial; pular ou continuar um checkpoint dá acesso direto à campanha.

Max permanece orientador. O encontro anterior “Max em Loop” agora é “Eco de Max”: falas e registros identificam explicitamente uma cópia das mensagens da pesquisa controlada pela IFVania. Não representa uma decisão hostil do professor real.

## Controles e balanceamento inicial

- A/D ou setas: movimento; espaço: salto.
- X, K ou clique esquerdo: soco na soltura; três toques encadeiam combo. Carga básica causa 2, soco básico causa 1. O terceiro golpe aumenta o empurrão.
- Cima ao soltar: ascendente. Baixo ao soltar no ar: mergulho.
- Shift: esquiva com recuperação e janela curta de proteção.
- Q segurado: guarda frontal, com resistência finita; soltar permite regeneração. Um bloqueio abre 45 quadros para um ataque com +1 de dano.
- Após RomerBug: **Punho de Impacto**, +1 de dano na carga.
- Após Mente Brilhante: **Sobrecarga Mecânica**, R; cinco segundos de +1 de dano e animação mais rápida, recarga de quinze segundos contada desde a ativação.
- Após Elias: **Onda de Choque**, o mergulho ainda ativo ao pousar alcança 100 px à frente pelo solo. Não atravessa paredes nem repete dano no mesmo alvo.
- Após Eco de Max: **Defesa Reforçada**, custo por impacto de 26 para 17; ancoragem anterior preservada.
- Após Alessandro: **Combo Tecnológico**, +2 no terceiro golpe.

O HUD mostra força, resistência e controle e o estado da sobrecarga. Recompensas não aumentam vida automaticamente. O alcance básico passa de 100 para 52 px; os testes de alcance antigos foram ajustados, preservando os testes de parede, recuperação e acerto único.

## Evidências e limites

`python -m ferramentas.capturar_luva` percorre as seis cenas e renderiza todos os 4.950 quadros, passa ao diálogo do A28 e captura tutorial e soco. Usa SDL dummy e não escreve no save real. As nove imagens nesta pasta foram geradas pela engine; não são mockups. Capturas são momentos selecionados, não prova de uma partida manual.

Resultado final: **211 testes aprovados** em 13,469 segundos, com SDL de vídeo e áudio dummy. `git diff --check` sem erros.

A suíte completa valida os controles, dois protagonistas, chefes, pausa/foco, checkpoint, alcance, defesa, contra-ataque, recarga e módulos. O teste de organização inicia `principal.py` em processos reais, sem janela, pela raiz e por diretório externo.

Revisão visual encontrou e corrigiu luva abaixo da mão, sobreposição do rótulo do sensor e duplicação do protótipo na bancada durante o sono. Pendente: avaliação humana em tempo real de ritmo, mixagem, dificuldade com alcance menor e sensação do combate; animações usam poses existentes com articulações procedurais, não um novo atlas desenhado à mão. Onda de Choque exige ataque próximo ao chão; não é um poder radial irrestrito. Melhorias de força ainda não quebram novos obstáculos de cenário.
