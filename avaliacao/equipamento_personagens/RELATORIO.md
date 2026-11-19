# Continuidade visual de mochila, luva e A28

Revisão de 19/11/2026.

## Implementação

- Duas artes de personagem distintas durante a abertura: com mochila ao chegar/sair e sem mochila durante a permanência em casa. A troca ocorre quando a mochila é colocada no chão e depois recolhida. A mochila no chão tem sprite próprio, substituindo o desenho geométrico.
- Artes de corpo inteiro com luva integrada para os dois protagonistas: repouso, seis quadros de caminhada, três poses de golpe, salto e esquiva. O atlas histórico continua disponível para o percurso escolar sem equipamento.
- Seis poses de equipamento, 30 quadros cada: abrir a mochila, alcançar a luva, retirá-la, vestir, apertar a cinta e levantar equipado. A cena acontece na posição real do jogador no A28; elimina a luva flutuante ampliada do diálogo anterior.
- A sequência pode avançar durante as falas; se elas terminarem cedo, a animação restante conclui antes do cartão da fase e da liberação de combate. Física, inimigos e entradas ficam suspensos. Pausa e perda de foco congelam a encenação, inclusive após fechar o diálogo.
- O acesso escolar ao A28 reutiliza `cenarios/corredor_biblioteca.png`, o panorama pós-chefe 1, espelhado para manter a porta no fim direito do percurso. Parede, piso, portas, bancos, jardim, iluminação e vegetação vêm dessa arte. Removida a fachada geométrica antiga. Porta lógica em x=1728, piso em y=440 e interação com E preservados.

## Verificação

- **216 testes aprovados**, suíte completa com SDL dummy (14,309 s).
- Novas regressões: troca de mochila; todos os seis estágios de equipamento; avanço rápido das falas; pausa/foco; inimigos e corpo congelados; luva integrada sem alterar colisões; panorama/porta do corredor.
- Exportador validado em pasta temporária antes de integrar 49 PNGs. Fontes e prompts preservados em [registro de arte](../../recursos/fontes_arte/equipamento_personagens/REFERENCIAS.md).
- `python -m ferramentas.capturar_equipamento`: 24 capturas preparadas na engine, para os dois protagonistas. Exemplos: [sem mochila](boy_sem_mochila.png), [retirando a luva](menina_equipando_070.png), [luva vestida](menina_luva_vestida.png), [acesso A28](boy_acesso_a28.png).
- `python -m ferramentas.capturar_luva`: percorreu novamente os 4.890 quadros da abertura e o fluxo sala → corredor → Romerito → A28; a ferramenta aguarda agora a conclusão da cena de equipamento.
- `git diff --check` sem erros.

A inspeção das capturas levou à revisão do contorno claro do atlas da menina. A validação foi automatizada e visual por imagens; o ritmo da animação e o acabamento em movimento ainda precisam de avaliação humana com janela. Nenhum commit criado.
