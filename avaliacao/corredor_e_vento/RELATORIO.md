# Alinhamento, corredor da biblioteca e vegetação — 17/11/2026

## Entrega

Bug humanoide: escala visual 200%, como o protagonista, com quadros de apresentação em 80 px. Colisão permanece em 40 × 40. CenaParasita registra a origem e o destino pelos pés, amostra o piso durante a corrida e usa midbottom no desenho. O bug mantém a altura até tocar o professor; então encolhe e sobe até o tórax visual. A direção é espelhada se a origem estiver à direita. Partículas e expulsão usam a mesma referência.

Convivência: panorama novo em 1920 × 540, sem esticar o pátio antigo. O A28 fica no começo, a biblioteca tem porta dupla de madeira e sinalização própria adiante, e o ginásio ocupa o fim. Caminhada de cerca de mil pixels entre surgimento e biblioteca; entrada exige E e fase 1 concluída. A volta da biblioteca fica fora de seu gatilho. As rotas posteriores permanecem conectadas. É uma adaptação ficcional, não uma planta homologada do campus.

VegetacaoAoVento reutiliza regiões da arte e seleciona folhas por cor, excluindo bancos e arquitetura. Faixas de folhagem deslocam-se poucos pixels em ondas de períodos diferentes. O fundo original permanece intacto; o efeito não muda geometria nem depende de relógio de parede. Pausa congela a brisa, enquanto diálogos permitem animação visual. Aplicado no pátio do prólogo, jardim/setores, recreio e janelas do corredor novo.

Instâncias isoladas de Jogo mantêm checkpoints em memória e não consultam o slot real ao construir o menu. A execução normal ativa leitura/escrita antes do primeiro quadro; testes de persistência usam caminho explícito temporário. O save existente do jogador não foi modificado pela validação.

## Verificação

193 testes aprovados, incluindo seis regressões de escala/colisão, pés no piso, percurso A28 → biblioteca, retorno/avanço ao jardim, deformação restrita às folhas e congelamento na pausa. Os testes que fixavam bugs em 100% e a antiga posição da porta foram atualizados para o novo contrato.

17 exportadores executados em cópia temporária, com 220 PNGs distintos. O novo panorama foi exportado em `/tmp` antes de integrar o recurso. Fontes e artes anteriores preservadas.

Capturas: [saída do A28](saida_a28.png), [corredor](corredor.png), [porta da biblioteca](porta_biblioteca.png), [fuga alinhada](fuga.png), [fusão](fusao.png), [jardim no instante 0](jardim_vento_0.png) e [jardim no instante 35](jardim_vento_35.png). Há também quadros da metamorfose, expulsão e desintegração. São cenários controlados, não uma partida humana.

Reproduzir com `python -m ferramentas.experimentar_corredor_vento` e `python -m ferramentas.experimentar_parasita --destino avaliacao/corredor_e_vento`, usando SDL dummy se necessário.

Revisar humanamente fluidez da fusão, clareza do percurso e intensidade da brisa, conforme [REVISAO_HUMANA_FINAL.md](../../documentacao/REVISAO_HUMANA_FINAL.md).
