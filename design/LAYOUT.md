# Identidade visual — autopost-instagram (@thiagorst.ia)

> Reescrito em 2026-09-23 depois de duas rodadas de iteração. Esta é a
> versão vigente — ver histórico da conversa que originou o repo pra
> entender por que passamos pela versão vermelho/minimalista antes de
> chegar aqui (foi rejeitada: o usuário quer manter o DNA visual já
> estabelecido da conta, não reinventar do zero).

## Regras permanentes (nunca renegociar sem o usuário pedir)

1. **Conteúdo sempre prático e de fácil entendimento.** Nada de jargão,
   nada de explicação abstrata sem exemplo concreto/copiável.
2. **Formato de contraste** — headline bold em alto contraste (branco/preto
   + 1 cor de destaque), nunca texto fraco sobre fundo fraco.
3. **Nunca fugir do assunto do perfil**: uso prático de IA pra vender mais,
   reduzir custo e automatizar negócio. Não é conteúdo sobre "crescer no
   Instagram", nem cases de empresas terceiras (ex: nada de "Klarna") — o
   case, quando existir, é sempre algo que o próprio Thiago construiu/testou.
4. **Estrutura fixa de 8 slides** (ver abaixo) — não improvisar outro número
   de slides sem o usuário pedir.
5. **Slide 1 (capa) SEM foto — fundo creme, igual ao padrão real dos posts
   de @thiagorst.ia** (referência enviada pelo usuário em 2026-09-23: grid
   de 9 capas reais, 150-358 compartilhamentos cada). Passou por 3 versões
   antes desta: full-bleed com texto sobre o rosto (rejeitado), foto em
   cima/texto embaixo em faixa sólida (rejeitado, "ficou ruim"), fundo
   escuro sólido com card de prova (rejeitado — não batia com a
   referência). **Esta é a versão final**: tag texto simples (sem pílula)
   + headline Bebas Neue (última linha laranja) + divisor + subtítulo,
   sobre o mesmo fundo creme decorado dos outros slides — sem foto, sem
   card. Não reintroduzir foto/card no slide 1 sem o usuário pedir de novo.

## Pesquisa que embasa o sistema

Baseado em engenharia reversa de posts reais que viralizaram no nicho de
IA/produtividade/negócios (dados via Apify + inspeção visual manual — ver
histórico da conversa pra a lista completa de contas/posts analisados:
@castilho.ia, @diegoalmeida.ia, @diegoampuero2, @wendellcarvalho,
@joaokepler, @joelsonmadeira_, @larissagomes.ia, @odanilogato).

DNA comum encontrado:
- Capa nunca é a marca — é uma foto real + afirmação de contraste/número,
  com 1 palavra em cor de destaque.
- Prova concreta na tela (screenshot de app real, painel de números,
  diagrama) — nunca só texto+ornamento.
- Slide 2 reforça a capa com autoridade: "quem é essa pessoa" ou "o que ela
  já provou" — número/caso concreto (do próprio autor, não de terceiro).
- CTA final pede uma **palavra específica ligada ao que foi prometido**
  numa caixa sólida — nunca "comenta aí" vago.
- Ornamento geométrico de marca (o antigo "— ///" excessivo, círculos de
  fundo) não converte sozinho — mas o slash mark discreto e o triângulo de
  canto, em doses pequenas, fazem parte do DNA já estabelecido da conta e
  foram mantidos.

## Paleta (congelada, herdada de `bigtech-instagram-autopost/layout_oficial.py` v3.0)

```
BP  (brand primary) = #FF8C00   // laranja — grifo, tags, CTA, números
BL  (brand light)   = #FFB84D   // tag sobre fundo escuro
BD  (brand dark)    = #C96A00   // reservado (texto de CTA sobre claro)
DBG (dark bg)       = #12100D   // fundo/cards escuros
LBG (light bg)      = #F5F0E8   // fundo creme — base dos slides de conteúdo
LBR (light border)  = #E4DCCB   // divisores em slide claro
INK                 = #1A1611   // texto principal
MUT                 = #6B6355   // texto secundário
```

## Tipografia (congelada)

- **Títulos:** Bebas Neue — condensada, alto impacto, última linha/palavra
  sempre em `BP` (laranja)
- **Corpo/tags/legendas:** Space Grotesk

## Estrutura de slide (8 slides — fixa)

| # | Tipo (`kind`) | Fundo | Conteúdo |
|---|---|---|---|
| 1 | `capa` | Creme | Gancho principal — afirmação/contradição curta (5-7 palavras), sem foto nem card, igual ao padrão real da conta |
| 2 | `capa2` | Escuro | Segunda capa / outro gancho — reforço de autoridade com números/stats do próprio case (não de empresa terceira) |
| 3 | `dor` | Creme | O problema — 3 bullets de dor reconhecível |
| 4-6 | `prompt` | Alternando | Os prompts/passos práticos, um por slide, sempre copiáveis (texto literal entre aspas) |
| 7 | `resultado` | Creme | O que muda na prática — lista com ícone+título+descrição |
| 8 | `cta` | Creme | CTA final — "Comenta {PALAVRA}" em botão sólido laranja + avatar circular |

### Slide 1 — regras específicas (o mais importante pra parar o scroll)

- Mesmo `_wrap_creme` dos slides de conteúdo (fundo creme, decoração
  técnica sutil, slash mark, triângulo de canto, rodapé com @handle).
- Tag em texto simples (`_tag()`, sem fundo/pílula) — igual à referência
  real, nunca `_tag_pill` nesse slide.
- Headline (`_h1`) com tamanho ajustado por `fit_size()` pra sempre ocupar
  bem a largura do slide, última linha em laranja.
- Sem foto, sem card de prova — a prova concreta (prompt copiável,
  números) vive nos slides de conteúdo (3-7), não na capa.

## Legenda (fora do slide, mas parte do sistema)

```
{Afirmação direta ligada ao gancho do slide 1}

{1-2 linhas de contexto}

Comenta "{PALAVRA ESPECÍFICA DESTE POST}" que eu te mando {o que foi
prometido} no direct 👇

#hashtags relevantes ao tema do post (variam por post, nunca fixas)
```

## Geração

`scripts/build_carousel.py` — lê um spec JSON no formato de
`design/example_spec.json` (lista de 8 slides, cada um com `kind`), gera o
HTML autocontido e exporta os PNGs 1080×1350 via Playwright.
