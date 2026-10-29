# Orientações para trabalhar no IFVania

## Projeto e referências

Jogo de plataforma em Python com Pygame. Leia `LEIA_ME.md`,
`DOCUMENTO_DE_REQUISITOS.md` e `ROTEIRO_HISTORIA.md` antes de alterar a campanha.
Use `PLANO_DE_EXECUCAO.md` para acompanhar implementação e pendências.
Instruções atuais do usuário prevalecem sobre estas orientações.

## Nomenclatura

- Classes e variáveis próprias do projeto devem ter nomes em português,
  inclusive constantes, parâmetros, atributos, testes e scripts de arte.
- Use `PascalCase` em classes (`Jogador`, `CaixaDialogo`), `snake_case` em
  variáveis (`nome_jogador`, `temporizador_ataque`) e `MAIUSCULAS_COM_SUBLINHADO`
  em constantes (`TAMANHO_PERSONAGEM`). Evite acentos nos identificadores.
- Preserve nomes próprios, como RomerBug, e convenções matemáticas, como
  coordenadas `x`/`y` e componentes RGB. Prefira nomes descritivos a abreviações.
- Preserve interfaces externas do Python, Pygame e bibliotecas: `__init__`,
  `self`, `cls`, `update`, `image` e `rect` no contrato de `pygame.sprite.Sprite`,
  propriedades de `pygame.Rect`, eventos e métodos de `unittest`.
- Não traduza nomes de APIs externas por substituição global. Ao renomear,
  confira herança, importações, argumentos nomeados, callbacks, `getattr` e
  dicionários repassados com `**`.
- Arquivos e pastas próprios também usam português, sem acentos. Ao renomear,
  atualize importações, caminhos de recursos, exportadores, testes e documentação.
  Preserve nomes técnicos de descoberta, como `AGENTS.md`, `__init__.py` e
  `.gitignore`. Chaves de dados e métodos existentes podem manter seus contratos.

## Organização

- `principal.py`: entrada; `jogo.py`: classe `Jogo` e máquina de estados.
- `configuracoes.py`: constantes de dimensão, física, escala e cores.
- `entidades/`: `Personagem`, `Jogador`, `Inimigo`, `Chefe`, `Professor`,
  `ChicoteMouse`, projéteis e classes concretas dos chefes.
- `mundo/`: mapas, cenas escolares, câmera, monitores e transição de chefe.
- `interface/`: `InterfaceInicial`, `CaixaDialogo`, `PainelInformacoes` e tema.
- `mundo/dados_fases.py`: campanha atual; `mundo/fases_antigas.py`: conteúdo
  antigo isolado. Não reincorpore fases ou recompensas antigas sem definição.
- `recursos.py`: carregamento e normalização; `preparar_*.py`: exportadores de
  arte. `gerar_recursos.py` é o gerador original e pode sobrescrever imagens.

## Contratos de jogabilidade

- Cada chefe precisa de classe concreta própria. RomerBug e SpeedBug são duas
  formas do mesmo encontro, com uma reserva de vida e uma transformação.
- Preserve o corpo lógico comum de `40 × 40`, definido em
  `configuracoes.TAMANHO_PERSONAGEM`. Jogador, chefes, professores e entidade usam
  escala visual de 200%; bugs permanecem em 100%. A arte se ancora pelos pés.
- Diálogos e pausa suspendem física e combate. Monitores podem animar durante
  diálogos, mas congelam na pausa. Eventos não devem avançar duas telas.
- A introdução é uma conversa do aluno com Max, sem narrador. O nome informado
  acompanha o jogador e personaliza as falas sem modificar textos compartilhados.
- O ataque carregado usa X na soltura; Shift oferece esquiva básica após a descoberta
  do mouse. RomerBug usa sobrecarga e SpeedBug investida anunciada, com recuperação
  sem dano de contato. Preserve cancelamento de carga em pausa, foco e transições.
- Caminhada acompanha deslocamento real; pressionar contra parede não deve
  manter o ciclo andando. Mudanças visuais não devem alterar colisões.

## Validação

Com um ambiente Python que tenha as dependências de `dependencias.txt`:

```bash
python principal.py
python -m unittest discover -s testes -v
```

Para testes sem janela ou áudio:

```bash
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy PYGAME_HIDE_SUPPORT_PROMPT=1 python -m unittest discover -s testes -v
```

Use testes relevantes para a alteração. Em refatorações amplas de nomenclatura,
execute a suíte completa e confira os exportadores em pasta temporária, sem
sobrescrever as artes aprovadas. Preserve fontes e registros de geração em
`recursos/fontes_arte/`. Pillow é necessário apenas para o gerador original;
ffmpeg é opcional para prévias, não para jogar.

Atualize a documentação quando mudar contratos ou comandos. Diferencie testes
automatizados de homologação manual; a etapa 5 não deve ser marcada concluída
apenas porque a suíte passou. Não crie commits nem publique sem solicitação.
