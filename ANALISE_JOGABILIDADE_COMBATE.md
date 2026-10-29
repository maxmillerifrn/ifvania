# Análise de movimentação e combate — IFVania

**Data:** 28/10/2026
**Status:** diagnóstico anterior à implementação, preservado como registro. A revisão autorizada foi implementada em 28/10/2026; os parâmetros atuais estão em `PROPOSTA_CHEFE_ROMERBUG.md` e `LEIA_ME.md`.

A análise usa o código atual e sondagens determinísticas com Pygame sem janela.
Ela explica os problemas relatados, mas não substitui observar jogadores reais.
Os valores propostos são pontos de partida para experimentar, não balanceamento homologado.

## Diagnóstico

O primeiro encontro exige precisão de chicote e reposicionamento rápido antes
que o jogo ofereça ferramentas de defesa equivalentes. A transformação aumenta
velocidade, frequência e velocidade dos projéteis, acrescenta saltos de perseguição
e retira as pequenas pausas da primeira forma. A dificuldade cresce em várias
frentes ao mesmo tempo. O objetivo da revisão deve ser tornar as decisões legíveis:
ver o aviso, evitar o ataque e reconhecer a oportunidade de responder.

### Movimento do protagonista

Em `configuracoes.py`, a velocidade é 4,2 pixels por quadro: 252 pixels por segundo
a 60 FPS. Em `entidades/jogador.py`, a entrada aplica essa velocidade imediatamente;
um toque já alcança o máximo e inverter a direção troca de +4,2 para −4,2 em um
quadro. Não há aceleração, frenagem ou distinção entre controle no chão e no ar.
Isso favorece correções exageradas ao tentar parar na distância do chicote.
A animação de oito quadros já acompanha a distância, mas não corrige essa resposta física.

A redução de velocidade precisa considerar o adversário: SpeedBug chega a 3,4
pixels por quadro. Reduzir só o aluno para 3,2 deixaria a perseguição atual mais
rápida que ele e poderia piorar o encontro.

Proposta inicial:

| Parâmetro | Atual | Protótipo |
|---|---|---|
| Velocidade máxima horizontal | 4,2 px/quadro | 3,2 px/quadro: redução de 24% |
| Aceleração no chão | Instantânea | 0,65 px/quadro²: máximo em cerca de 5 quadros |
| Frenagem no chão | Instantânea | 0,9 px/quadro²: parada curta e previsível |
| Controle no ar | Mesma resposta instantânea | Aceleração de 0,4 px/quadro², conservando correção lateral |
| Tolerância após sair da borda | Ausente | 6 quadros / 100 ms para aceitar salto |
| Memória de comando de salto | Ausente | 6 quadros / 100 ms antes de aterrissar |

Manter inicialmente força de salto e gravidade. O caminho atual foi montado para
esse salto; alterar movimento e altura simultaneamente dificulta identificar a
causa de uma melhora ou regressão. Revalidar o percurso com ambos os protagonistas.
A frenagem não deve produzir deslizamento longo, nem a aceleração causar atraso perceptível.

### Chicote e áreas de acerto

`entidades/chicote_mouse.py` permite dano nas idades 6 a 15: dez quadros, ou
167 ms. O alcance nominal é 76 pixels, medido a partir da mão lógica. O teste
final usa segmentos finos da curva contra o corpo do alvo ampliado em apenas
6 pixels totais: aproximadamente 3 pixels de margem por lado. Não usa toda a
área retangular de `hit_bounds`, que serve apenas como filtragem inicial.
Aumentar somente esse retângulo não ampliaria o acerto real.

Sondagem com aluno e alvo imóveis, corpos de 40 × 40, pés na mesma altura,
aluno olhando à direita e sem paredes. Cada idade foi avaliada de forma
independente, reproduzindo as duas verificações usadas pela fase:

| Distância entre centros | Quadros do golpe capazes de acertar | Janela equivalente |
|---|---|---|
| 40 px | 10–15 | 100 ms |
| 60 px | 10–15 | 100 ms |
| 80 px | 12–15 | 67 ms |
| 100 px | 13–15 | 50 ms |
| 110 px | 14–15 | 33 ms |
| 120 px | Nenhum | — |

Esses tempos descrevem quando a curva encontra um alvo parado; não são uma
medição de tempo de reação ou taxa de acerto humana. Com perseguição, saltos e
movimento do aluno, a situação fica menos estável.

Existe também uma diferença visual: a arte ocupa uma superfície de 80 × 80,
enquanto o corpo usado para receber dano tem 40 × 40, alinhado pelos pés.
Nem todo contato aparente com o professor desenhado corresponde a contato com
sua área vulnerável. A área transparente do sprite impede tratar seus 80 × 80
inteiros como corpo sem inspeção adicional.

Proposta inicial:

- Alcance nominal de 100 pixels; experimentar até 110 somente se ainda necessário.
- Preparação de 5 quadros, dano por 14 e recolhimento de 11: ciclo de 30 quadros.
  Conservar espera mínima de 30 quadros e um acerto por alvo por golpe.
- Usar uma faixa espessa em torno da curva, com raio inicial de 12 pixels, e
  considerar o espaço percorrido desde o quadro anterior para evitar falhas entre
  amostras. Essa faixa deve ter representação visual coerente no rastro do golpe.
- Separar corpo de colisão do cenário e área que recebe ataques. Experimentar uma
  área vulnerável de 48 × 56, apoiada nos pés, para aproximar o acerto do tronco
  desenhado, mantendo o corpo lógico em 40 × 40. Ajustar junto à espessura da curva
  para não acumular tolerância excessiva.
- Atualizar a filtragem inicial e a colisão final juntas. Não usar um retângulo
  gigante e invisível como substituto de um golpe legível.
- Acrescentar memória de ataque de 6 quadros para aceitar uma pressão pouco antes
  do fim da recarga; não disparar automaticamente um comando antigo após diálogo,
  pausa ou transformação.
- Preservar direção fixada no início, bloqueio por paredes e ausência de acertos
  atrás do aluno. A tolerância e a varredura temporal também precisam respeitar
  paredes; ampliar o alvo não pode permitir dano do outro lado de um obstáculo.

### Ataque carregado — complemento solicitado

Incluir uma alternativa de maior dano no mesmo botão do chicote, disponível
a partir da descoberta do mouse. Esta seção especifica o protótipo; a mecânica
ainda não foi implementada.

| Entrada | Resultado inicial proposto |
|---|---|
| Tocar e soltar X antes de completar a carga | Golpe normal, 1 ponto de dano |
| Segurar X por 0,6 segundo e soltar | Golpe carregado, 2 pontos de dano |
| Continuar segurando após completar | Mantém pronto; não dispara automaticamente nem acumula dano extra |

O golpe normal sai ao soltar, sem esperar o tempo necessário para a carga.
Uma soltura antecipada sempre produz o golpe normal, sem exigir precisão para
alcançar um estágio intermediário. Começar com apenas dois níveis facilita a
leitura. Os tempos devem ser testados junto ao novo controle para evitar que
a troca do disparo na pressão para o disparo na soltura deixe o ataque lento.

Durante a carga, permitir deslocamento a 75% da velocidade normal, salto e
mudança de direção. Fixar a direção somente ao liberar o golpe. Não conceder
invulnerabilidade nem armadura: receber dano válido interrompe a carga. A esquiva,
se implementada, pode descartá-la imediatamente sem disparar. A preparação e o
golpe liberado continuam sujeitos às regras de compromisso do ataque.

Mostrar o aluno puxando o cabo e preparando o mouse, com indicador discreto
perto da mão ou do HUD. Ao completar, oferecer mudança de pose e brilho, além
de sinal sonoro quando houver áudio. O efeito sugere tensão mecânica no cabo,
sem definir um poder mágico novo. O golpe carregado tem rastro mais marcado e
impacto mais forte, mas usa a mesma regra de alcance e tolerância inicialmente.
Não aumentar simultaneamente dano, alcance e segurança.

O carregado conserva bloqueio por paredes e um acerto por alvo por golpe. Pode
atingir mais de um inimigo se o arco alcançar cada um, como o golpe normal.
Não atordoa chefes automaticamente, para evitar impedir suas ações repetidamente.
Uma carga não pode acumular durante recarga ou execução de outro golpe.

Ao pausar, abrir diálogo, iniciar transformação, perder foco da janela ou
reaparecer, descartar a carga e exigir soltar e pressionar novamente para
carregar. A retomada não pode executar ataque com uma soltura antiga. A memória
de comandos do golpe normal precisa distinguir uma pressão nova de uma carga
cancelada.

A função tática é causar dano concentrado quando o chefe termina uma ação.
O ataque normal mantém a vantagem de rapidez e menor exposição; o carregado
não deve ter maior dano sustentado garantido. Começar com dano 2, em vez de 3,
e manter inicialmente a vida dos chefes. Uma abertura precisa permitir um
carregado iniciado depois que o jogador reconhece a recuperação; antecipar a
carga durante o aviso pode ser uma escolha arriscada, nunca obrigação.
Revisar a recuperação de 1,1 segundo de SpeedBug junto ao tempo necessário
para aproximação, carga e impacto.

Validar toque rápido, soltura parcial, carga completa, mudança de direção,
movimento, salto, interrupção por dano, perda de foco e todas as transições.
Confirmar dano exato, ausência de acerto repetido, bloqueio por paredes e
transformação única mesmo quando um golpe atravessa o limiar de metade da vida.

### Defesa e resposta ao dano

Na campanha atual, escudo e arrancada exigem habilidades que o aluno não recebe.
As opções reais são deslocamento e salto. A invulnerabilidade após dano já dura
90 quadros / 1,5 segundo; aumentá-la não resolve a ausência de janelas de resposta.

Há dois problemas concretos de recuo:

1. Em `mundo/fase.py`, aluno à esquerda do inimigo produz `impulso = -1`, mas o
   recuo usa `impulso * -6`, resultando em +6: direção voltada para a ameaça.
   O caso à direita também fica invertido. Projéteis usam a posição do chefe
   para determinar esse lado, em vez da fonte do impacto.
2. `take_damage` aplica a velocidade horizontal depois da atualização do aluno.
   No quadro seguinte, `handle_input` a sobrescreve antes do movimento. Uma
   sondagem com teclas soltas confirmou a passagem de `(6, −7)` para `(0, −7)`.
   Na sequência normal, portanto, o empurrão horizontal é perdido.

Corrigir a direção e preservar o impulso por cerca de 6–8 quadros, ou tratá-lo
como componente independente da locomoção. Isso oferece separação física sem
retirar o controle por muito tempo. Fazer o lado do impacto considerar a fonte
real e não simplesmente o centro do chefe.

Primeiro validar o encontro com deslocamento, salto e chicote. Se ainda faltar
uma escolha defensiva interessante, prototipar um passo evasivo básico: duração
aproximada de 0,25 segundo, deslocamento de 60 pixels, invulnerabilidade central
curta e recarga de 0,9 segundo. Essa seria uma nova mecânica, distinta da habilidade
antiga de arrancada, e exigiria tutorial, indicação de disponibilidade e revisão
dos requisitos. Não é pré-requisito para tornar este primeiro chefe vencível.
Não começar por parry de precisão: ele acrescentaria outra exigência de timing.

### RomerBug e SpeedBug

| Pressão | RomerBug | SpeedBug atual |
|---|---|---|
| Movimento máximo | 1,15 px/quadro | 3,4 px/quadro: quase 3 vezes mais |
| Intervalo entre projéteis | 90 quadros / 1,5 s | 55 quadros / 0,92 s: frequência 64% maior |
| Velocidade do projétil | 5 px/quadro | 6,5 px/quadro: 30% maior |
| Aproximação | Patrulha com parada perto do lançamento | Perseguição recalculada a cada quadro |
| Salto | Não usa o salto de perseguição | Salta ao encontrar parede ou aluno acima |
| Recuperação ofensiva | Breve pausa no lançamento | Sem pausa equivalente de perseguição |

O temporizador de pose de lançamento começa depois que o projétil é criado.
Na segunda forma ele não estabelece uma preparação ofensiva explícita. Em curta
distância, um projétil a 390 pixels por segundo deixa pouco espaço para resposta:
80 pixels de percurso representam aproximadamente 205 ms, sem contar as áreas
de colisão. Perseguir, pular e disparar ao mesmo tempo exige mais leitura do que
esse primeiro encontro ensinou.

## Ajuste em duas passagens

### 1. Corrigir a sensação com os ataques existentes

Prioridade: movimento do aluno, tolerância do chicote, recuo e pausas do chefe.
Manter inicialmente 6 pontos de vida do aluno e 16 do chefe, para não mascarar
problemas de justiça com redução de vida do adversário.

Para um primeiro protótipo de SpeedBug:

- Limitar aproximação a 2,6 px/quadro, abaixo dos 3,2 propostos para o aluno.
- Separar aproximar, preparar, executar e recuperar; perseguição não acontece
  continuamente durante preparação e recuperação.
- Usar aviso de 0,6 segundo antes de lançar, intervalo mínimo de 1,5 segundo
  entre lançamentos e projétil a 5 px/quadro. A diferença de fase deve vir do
  padrão, sem aumentar simultaneamente todos os números.
- Oferecer recuperação visível de aproximadamente 0,9 segundo após lançar.
  O intervalo mínimo é uma restrição adicional: o ciclo completo não pode
  abreviar preparação nem recuperação para cumprir uma cadência fixa.
- Congelar a mira ao concluir a preparação; não corrigir o disparo após executado.
- Não combinar salto de perseguição e lançamento. Inicialmente retirar o salto
  reativo da segunda forma na arena plana, mantendo colisão com o cenário.
- Garantir distância segura e cerca de 1 segundo de preparação ao retomar a
  transformação. A proteção atual não deve ocultar um ataque que já começou.

Essa passagem permite avaliar a melhoria sem misturar uma troca completa de
mecânica ao ajuste de controle. Aviões e medalhas ainda seriam provisórios.

### 2. Substituir ataques para combinar com a escola sombria

Retomar `PROPOSTA_CHEFE_ROMERBUG.md`, com uma mudança de escopo: começar com
**uma única investida** na segunda forma. A dupla investida do documento anterior
fica como evolução opcional, depois de homologar a versão simples.

**RomerBug — sobrecarga de terminal:** aponta para o terminal e marca uma faixa
no piso durante 0,8 segundo. O alvo é fixo desde o início do aviso. Uma descarga
baixa ocupa uma faixa de 80–96 pixels por 0,25 segundo; o aluno pode sair ou saltar.
Depois, o professor fica exposto por 1 segundo. Uma zona por vez e nenhuma zona
sob o aluno sem aviso. O pulso precisa ter altura realmente saltável e tempo
suficiente para limpar a faixa com a velocidade reduzida.

**SpeedBug — investida de ruptura:** aproxima-se a 2,6 px/quadro e para para
preparar por 0,6 segundo. Fixa a direção antes de avançar; executa uma investida
de até 160 pixels a 6 px/quadro, sem seguir mudanças de lado do aluno. Em seguida
fica exausto por 1,1 segundo, com oportunidade de um ou dois golpes conforme o
reposicionamento. Sem medalhas simultâneas e sem dano de contato na recuperação.
A execução pode ser rápida porque tem aviso e término claros. O salto básico
deve bastar; não depender da esquiva proposta como opcional.

Preparação e recuperação precisam de poses, marca no chão e sinal sonoro quando
houver áudio disponível. Não depender apenas de cor. Usar o mesmo idioma visual
nos futuros chefes: avisos reconhecíveis, padrões próprios e vulnerabilidade clara.

Na implementação, a classe concreta de cada chefe controla seus estados e ataques.
A base compartilha apenas infraestrutura; a segunda forma continua na instância
`RomerBug`, com a mesma vida e transição cinematográfica existentes. Os professores
antigos seguem isolados até terem seu papel definido na campanha.

## Ordem de execução e aceite

1. Corrigir recuo e implementar movimento com aceleração curta. Validar corredores,
   degraus, salto, parede, mudança de lado e ambas as opções de protagonista.
2. Ajustar o chicote, incluindo área final, filtragem inicial e barreiras. Verificar
   alvos próximos, afastados, em alturas diferentes e cruzando a curva entre quadros.
   Depois prototipar toque/soltura e carga, verificando se o ataque rápido continua
   responsivo e se a carga oferece uma escolha útil durante as aberturas.
3. Reduzir sobreposição de pressões do SpeedBug, com estados e recuperação visíveis.
4. Testar sobrevivência sem invulnerabilidade artificial; depois substituir a temática
   dos ataques. Avaliar passo evasivo somente se as opções básicas ainda forem pobres.

Critérios para o protótipo:

- O aluno para onde espera, sem sensação de gelo nem entrada com atraso longo.
- Um contato visual plausível do chicote acerta dentro da tolerância definida;
  paredes, direção e um acerto por alvo continuam corretos.
- Todo ataque perigoso do chefe tem aviso, saída alcançável e fim reconhecível.
- SpeedBug não encurrala pela soma de perseguição, salto e projétil simultâneos.
- O jogador consegue explicar por que tomou dano e quando poderia contra-atacar.
- Nenhuma perda de vida ocorre em diálogos, pausa ou transformação.

Os testes atuais de vitória por chicote usam invulnerabilidade artificial e
reposicionamento para isolar o funcionamento da arma. Eles não demonstram justiça
nem dificuldade adequada do encontro. Preservá-los para regressão funcional e
acrescentar cenários de esquiva e contra-ataque sem esses auxílios.

Na avaliação humana, observar pelo menos cinco pessoas que ainda não conhecem
o padrão, nas duas opções de personagem. Registrar causas de morte, golpes
visualmente conectados que falharam, dano por contato, tempo para aprender o
aviso e duração do combate. Uma faixa inicial de 45–75 segundos de combate
ativo, excluindo fala e transformação, serve como hipótese de ritmo, não como
meta a atingir aumentando artificialmente a vida do chefe. Priorizar compreensão,
controle e possibilidade de recuperação sobre uma taxa arbitrária de derrotas.
