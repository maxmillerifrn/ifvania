# Mochila e equipamento dos protagonistas — 19/11/2026

Gerados com a ferramenta integrada `image_gen`, usando a skill `imagegen` e os sprites existentes dos dois protagonistas como referência de identidade. Prompts completos em [instrucoes.json](instrucoes.json).

Fontes preservadas:
- `menino.png`: atlas 6 × 4, sem mochila, encenação de equipamento e combate com luva.
- `menina.png`: primeira geração, preservada para rastreabilidade.
- `menina_recorte.png`: revisão do contorno claro/transparência, fonte utilizada na exportação.
- `mochila.png`: mochila avulsa, sem personagem, utilizada em casa.

Exportador: `python -m ferramentas.preparar_equipamento_personagens --destino <pasta>`. Saída validada primeiro em `/tmp/ifvania_equipamento`, depois integrada em `recursos/imagens/equipamentos/personagens/`: 48 poses de 80 × 80 e uma mochila avulsa. Escala comum por atlas, pés ancorados, transparência normalizada pelo alpha. Não modifica atlas anteriores nem colisões.

As poses representam: repouso e caminhada sem mochila; ajoelhar e abrir a mochila; alcançar, retirar e vestir a luva; apertar a cinta; levantar com mochila e luva; repouso, soco, salto, esquiva e caminhada equipada. Os quadros não são uma composição do ícone da luva sobre a mão: o equipamento faz parte da figura gerada.
