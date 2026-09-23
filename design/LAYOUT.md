# Identidade visual — autopost-instagram (@thiagorst.ia)

Redesenho de 2026-09-23, baseado em pesquisa real (Apify) dos posts de maior
engajamento no nicho de IA/produtividade/negócios, não em preferência estética
isolada. Ver achados completos na conversa que originou este repo — resumo:

- O carrossel antigo (`bigtech-instagram-autopost/`, paleta laranja/creme
  inspirada em @star.ex, ornamentos geométricos) publica com **0-2
  curtidas e 0 comentário**.
- O post de maior engajamento encontrado no nicho inteiro (@larissagomes.ia,
  2.359 curtidas / **2.467 comentários**) é visualmente quase sem marca:
  fundo branco, título preto bold, e a "prova" do valor prometido (capa de
  livro real + resumo visual) ocupando a maior parte do slide.
- Um segundo post forte (@odanilogato, 922 comentários) segue o mesmo
  padrão: afirmação direta + oferta clara, sem ornamento.
- **Conclusão prática: ornamento de marca não gera engajamento neste
  nicho — clareza + prova de valor real na tela, sim.**
- O maior alavancador de comentário não é visual, é a legenda: CTA pra
  comentar uma **palavra específica ligada ao que aquele post entrega**
  (ex: "comenta 'livro'"), não uma palavra fixa genérica tipo "CLAUDE".

## Paleta

```
BRAND_PRIMARY  = #E5241C   // vermelho — grifo de palavra-chave, CTA, números
BRAND_LIGHT    = #F0574F   // tag em fundo escuro
BRAND_DARK     = #9E1712   // texto de CTA sobre fundo claro
LIGHT_BG       = #FAF7F2   // fundo claro (nunca branco puro)
LIGHT_BORDER   = #E8E2D8   // divisores em slide claro
DARK_BG        = #141210   // fundo escuro quase preto
```

Cor usada **com moderação** — só pra grifar a palavra/número que carrega o
gancho. Nunca como bloco decorativo, borda de destaque ornamental, ou ícone
de marca. Sem ornamento geométrico (sem "— ///", sem círculos de fundo, sem
triângulo de canto) — isso pertencia ao sistema antigo e não converteu.

## Tipografia

- **Títulos:** Space Grotesk, peso 700 — tech/direto, sem serifa
- **Corpo:** Inter, peso 400
- Números/destaques: Space Grotesk 700, cor `BRAND_PRIMARY`

## Estrutura de slide

1. **Hero** (LIGHT_BG) — afirmação direta ou pergunta que dói, sem logo/marca
   grande, sem intro de marca
2. **Prova** (LIGHT_BG ou DARK_BG) — mostra o valor real prometido: captura
   de tela, trecho de código/prompt, checklist, comparação antes/depois.
   **Esse slide é obrigatório em todo carrossel** — é o que mais correlaciona
   com engajamento real nos dados coletados.
3. **Desenvolvimento** (1-4 slides, alternando fundo) — pontos numerados ou
   passos, sempre com texto curto (a legenda carrega o resto)
4. **CTA** (DARK_BG) — pede comentário de uma **palavra específica** ligada
   ao que foi prometido no post (nunca "CLAUDE" fixo), sem seta de swipe,
   barra de progresso 100%

Formato: 4:5 (1080×1350), progress bar + seta de swipe herdados da skill
`instagram-carousel` (são affordance de UX do Instagram, não ornamento de
marca — mantidos).

## Legenda (fora do slide, mas parte do sistema)

Formato validado pelos dados:
```
{Afirmação direta ou gancho}

{1-2 linhas de contexto/dor}

Comenta "{PALAVRA ESPECÍFICA DESTE POST}" que eu te mando {o que foi
prometido} no direct 👇

#hashtags relevantes ao tema do post (não fixas)
```

## Geração

`scripts/build_carousel.py` — lê um spec JSON (ver
`design/example_spec.json`), gera o HTML autocontido e exporta os PNGs
1080×1350 via Playwright. Ver docstring do script pra uso.
