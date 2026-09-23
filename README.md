# autopost-instagram

Publicação automática de carrossel no Instagram (**@thiagorst.ia**) via GitHub
Actions + Meta Graph API. Reconstruído em 2026-09 a partir de
`bigtech-instagram-autopost/`, com identidade visual e formato de carrossel
redesenhados a partir de engenharia reversa de posts reais que viralizaram no
nicho (ver `design/LAYOUT.md`).

## Como funciona

- Os carrosséis são gerados localmente com `scripts/build_carousel.py`, a
  partir de um spec JSON (ver `design/example_spec.json`).
- Os PNGs exportados (1080×1350) vão em `images/<slug>/slide_N.png`.
- Cada carrossel entra na fila em `fila.json`.
- Todo dia às 08:05 BRT, o GitHub Actions (`.github/workflows/daily-post.yml`)
  pega o próximo carrossel não postado, publica via Meta Graph API e marca
  como postado (commitando `fila.json` de volta).

## Estrutura

```
├── .github/workflows/daily-post.yml   # agendamento cron na nuvem
├── scripts/
│   ├── build_carousel.py              # gera HTML + exporta PNGs (Playwright)
│   ├── post_next.js                   # CLI que orquestra a publicação
│   └── publish_instagram.py           # chama a Meta Graph API
├── design/
│   ├── LAYOUT.md                      # identidade visual + pesquisa que a embasou
│   └── example_spec.json              # spec de referência (8 slides)
├── assets/                            # fotos reutilizadas nos slides (rosto, etc.)
├── images/                            # PNGs exportados por carrossel
├── preview/                           # HTML de preview de cada carrossel gerado
├── fila.json                          # fila de publicação
├── requirements.txt                   # deps Python (requests, python-dotenv, playwright)
└── .env.example                       # template de variáveis (real vai em GitHub Secrets)
```

## Gerando um carrossel novo

1. Escreva um spec JSON seguindo `design/example_spec.json` (lista de slides,
   cada um com `kind`: `capa`, `capa2`, `dor`, `prompt`, `resultado` ou `cta`).
2. Rode:
   ```bash
   python3 scripts/build_carousel.py caminho/do/spec.json
   ```
   Isso gera `preview/<slug>.html` (pra conferir no navegador) e
   `images/<slug>/slide_1.png ... slide_N.png`.
3. Adicione uma entrada em `fila.json`:
   ```json
   {
     "id": 2,
     "titulo": "Título interno do post",
     "images": ["images/<slug>/slide_1.png", "..."],
     "caption": "Legenda completa + CTA + hashtags",
     "postado": false
   }
   ```
4. `git add . && git commit -m "novo carrossel: <slug>" && git push`

## Identidade visual (resumo — ver `design/LAYOUT.md`)

- Paleta: laranja `#FF8C00` + creme `#F5F0E8` + preto `#12100D`.
- Tipografia: Bebas Neue (títulos) + Space Grotesk (corpo).
- Slide 1 (capa): foto real em full-bleed + card de prova flutuando
  (`_proof_card_stats` pra números/painel, `_proof_card_checklist` pra
  tarefas) — escolha o tipo de card conforme o conteúdo do post.
- Slide 2 (capa2): reforço de autoridade com números/stats.
- CTA final: sempre pedir para comentar uma **palavra específica ligada ao
  que foi prometido no post** (não uma palavra genérica fixa) — é o que mais
  correlaciona com volume de comentário nos dados analisados.

## Secrets necessários no GitHub

Settings → Secrets and variables → Actions:

| Nome | Valor |
|---|---|
| `INSTAGRAM_BUSINESS_ID` | ID da conta business do Instagram |
| `FACEBOOK_PAGE_ID` | ID da página do Facebook vinculada |
| `INSTAGRAM_ACCESS_TOKEN` | Token de longa duração da Meta Graph API |
| `META_API_VERSION` | ex: `v19.0` |

`GITHUB_RAW_BASE` é montado automaticamente pelo workflow — não precisa secret.

## Testar localmente

```bash
cp .env.example .env   # preencha com as credenciais reais
pip install -r requirements.txt
python3 -m playwright install chromium   # só na 1ª vez, pra gerar carrossel
node scripts/post_next.js                # publica de verdade
MANUAL_POST=1 node scripts/post_next.js  # ignora o guard anti-duplicação
```

## Logs / Falhas

Falha no workflow → email do GitHub + logs completos em Actions → clique na
execução vermelha.
