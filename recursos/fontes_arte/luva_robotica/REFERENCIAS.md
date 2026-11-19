# Luva e bancada — fonte procedural

Arte criada diretamente com primitivas Pygame, sem geração externa de imagens.

- `entidades/luva_robotica.py`: carcaça verde, metal claro, articulações de cobre, núcleo ciano, dedos articulados, rastros de impacto e onda no solo.
- `mundo/introducao.py`: bancada, componentes, sensor de preensão, ferramentas, cabo de teste e integração às poses existentes.
- Fachada e quarto reutilizam as fontes aprovadas de `../introducao/REFERENCIAS.md`; não foram sobrescritos.
- Prévia reproduzível: `python -m ferramentas.capturar_luva`. Resultado em `avaliacao/luva_robotica/`.

## Revisão texturizada — substitui a arte procedural anterior

Ferramenta: `image_gen` integrada, via skill `imagegen`; sem API/CLI externa.
Fonte preservada: `atlas_texturizado.png`. Três poses em `recursos/imagens/equipamentos/luva_robotica/`: `repouso.png`, `punho.png`, `aberta.png`.
Exportador: `python -m ferramentas.preparar_luva_robotica --destino <pasta>`. Verificado primeiro em `/tmp/ifvania_luva_texturizada`; recorte por alpha, proporção preservada, largura de 128 px, redução na engine. A arte procedural anterior continua registrada no histórico deste arquivo; não é mais a apresentação utilizada.

Prompt utilizado:

> Create a production-ready transparent sprite atlas for IFVania, a dark detailed 2D pixel-art Brazilian school platformer. THREE equally sized cells in ONE horizontal row, evenly spaced, no labels, no background. Each cell contains the SAME compact realistic assistive robotic glove, side view pointing RIGHT, wrist on LEFT, fingers on RIGHT: cell1 relaxed slightly open hand; cell2 tightly clenched punching fist; cell3 open articulated hand. ONLY glove, no arm, no person. Weathered charcoal textile glove underneath small brushed gunmetal dorsal plates, tiny aged brass hinges and tendon cables, muted olive wrist cuff, very tiny teal indicator LED, NO glowing round reactor, no giant armor, no cartoon icon, no neon. Fine hand-painted pixel-art texture with crisp edges, subtle warm upper-left lighting, deep brown shadows, 16-bit adventure RPG asset quality matching detailed warm wooden desks and moody school interiors. Natural hand proportions, readable silhouette at 24px wide. True transparent background, ample clear gutters. All three same side angle, size and wrist alignment.
