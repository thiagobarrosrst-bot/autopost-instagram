#!/usr/bin/env python3
"""
build_carousel.py — Gera o carrossel de 5 slides no DNA aprovado de
@thiagorst.ia (herdado de bigtech-instagram-autopost/layout_oficial.py v3.0,
estilo @star.ex) e exporta cada slide como PNG 1080x1350.

Diferença desta versão: o slide 1 usa a foto real em full-bleed (com
gradiente escuro na base segurando o texto) em vez de só texto sobre o
fundo creme — pra parar o scroll de verdade. Slides 2-5 mantêm o DNA
congelado (fundo creme/escuro, Bebas Neue + Space Grotesk, laranja
#FF8C00, box de dor/prompt/resultado, CTA "Comenta CLAUDE").

Uso:
    python3 scripts/build_carousel.py design/example_spec.json
    # gera:
    #   preview/<slug>.html
    #   images/<slug>/slide_1.png .. slide_5.png
"""
import asyncio
import base64
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ── paleta e fontes oficiais (congeladas em LAYOUT_OFICIAL.md) ──
BP = "#FF8C00"   # brand primary
BL = "#FFB84D"   # brand light
BD = "#C96A00"   # brand dark
DBG = "#12100D"  # fundo/cards escuros
LBG = "#F5F0E8"  # fundo creme (base de todo slide)
LBR = "#E4DCCB"  # borda clara
INK = "#1A1611"  # texto principal
MUT = "#6B6355"  # texto secundário

W, H = 420, 525
SCALE = 1080 / W

FOTO_PATH = ROOT / "assets" / "thiago_perfil.jpg"


def _img_data_uri(path: Path) -> str:
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


# ── decoração compartilhada ──
def _decor_bg() -> str:
    return f"""<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute;inset:0;z-index:0;" xmlns="http://www.w3.org/2000/svg">
      <circle cx="340" cy="90" r="70" fill="none" stroke="{INK}" stroke-opacity="0.07" stroke-width="1"/>
      <circle cx="340" cy="90" r="110" fill="none" stroke="{INK}" stroke-opacity="0.05" stroke-width="1"/>
      <circle cx="60" cy="430" r="50" fill="none" stroke="{INK}" stroke-opacity="0.06" stroke-width="1"/>
      <circle cx="380" cy="200" r="2" fill="{INK}" fill-opacity="0.15"/>
      <circle cx="30" cy="150" r="2" fill="{INK}" fill-opacity="0.12"/>
      <circle cx="370" cy="350" r="2" fill="{INK}" fill-opacity="0.12"/>
    </svg>"""


def _corner_glow() -> str:
    return f"""<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute;inset:0;z-index:1;pointer-events:none;" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="glow" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="{BP}" stop-opacity="0"/>
          <stop offset="100%" stop-color="{BP}" stop-opacity="0.55"/>
        </linearGradient>
      </defs>
      <polygon points="{W},{H} {W-150},{H} {W},{H-170}" fill="{DBG}" fill-opacity="0.94"/>
      <line x1="{W-170}" y1="{H-60}" x2="{W-20}" y2="{H-210}" stroke="url(#glow)" stroke-width="3"/>
    </svg>"""


def _slash_mark() -> str:
    return (f'<div style="position:absolute;top:20px;left:28px;z-index:10;display:flex;align-items:center;gap:6px;">'
            f'<div style="width:14px;height:2px;background:{INK};"></div>'
            f'<div style="display:flex;gap:2px;">'
            + "".join(f'<div style="width:2px;height:12px;background:{BP};transform:skewX(-20deg);"></div>' for _ in range(3))
            + '</div></div>')


def _slash_mark_light() -> str:
    """Versão clara do slash, pra usar sobre foto/fundo escuro."""
    return (f'<div style="position:absolute;top:20px;left:28px;z-index:10;display:flex;align-items:center;gap:6px;">'
            f'<div style="width:14px;height:2px;background:#fff;"></div>'
            f'<div style="display:flex;gap:2px;">'
            + "".join(f'<div style="width:2px;height:12px;background:{BP};transform:skewX(-20deg);"></div>' for _ in range(3))
            + '</div></div>')


def _footer(light=False) -> str:
    color = "rgba(255,255,255,0.75)" if light else MUT
    return (f'<div style="position:absolute;bottom:16px;left:28px;z-index:10;font-family:\'Space Grotesk\',sans-serif;'
            f'font-size:11px;font-weight:600;color:{color};">@thiagorst.ia</div>')


def _tag(t: str, light=False) -> str:
    color = BL if light else BP
    return (f'<div style="font-family:\'Space Grotesk\',sans-serif;font-size:10px;font-weight:700;'
            f'letter-spacing:2.5px;color:{color};text-transform:uppercase;margin-bottom:10px;">{t}</div>')


def _h1(lines, size=44, light=False) -> str:
    r = f'<div style="font-family:\'Bebas Neue\',Impact,sans-serif;font-size:{size}px;font-weight:400;line-height:0.96;">'
    for i, t in enumerate(lines):
        if i == len(lines) - 1:
            color = BP
        else:
            color = "#fff" if light else INK
        r += f'<div style="color:{color};">{t}</div>'
    return r + "</div>"


def _div() -> str:
    return f'<div style="width:44px;height:3px;background:{BP};margin:14px 0;"></div>'


def _body(html: str, light=False) -> str:
    color = "rgba(255,255,255,0.8)" if light else MUT
    return f'<div style="font-family:\'Space Grotesk\',sans-serif;font-size:13.5px;line-height:1.6;color:{color};font-weight:500;">{html}</div>'


def _box_pain(lines) -> str:
    items = "".join(
        f'<div style="display:flex;align-items:flex-start;gap:8px;padding:7px 0;">'
        f'<span style="color:{BP};font-weight:700;flex-shrink:0;margin-top:1px;">&#8594;</span>'
        f'<span style="font-family:\'Space Grotesk\',sans-serif;font-size:13px;color:{INK};line-height:1.45;font-weight:600;">{l}</span></div>'
        for l in lines
    )
    return (f'<div style="background:#ffffff;border:1.5px solid {LBR};border-radius:10px;padding:14px 16px;'
            f'margin-top:14px;box-shadow:0 2px 12px rgba(26,22,17,0.04);">{items}</div>')


def _box_prompt(prompt_text: str) -> str:
    return (f'<div style="background:{DBG};border-radius:10px;padding:14px 16px;margin-top:14px;">'
            f'<div style="font-family:\'Space Grotesk\',sans-serif;font-size:9px;font-weight:700;'
            f'letter-spacing:2px;color:{BP};text-transform:uppercase;margin-bottom:9px;">COPIA ESSE PROMPT &#8595;</div>'
            f'<div style="font-family:\'Space Grotesk\',sans-serif;font-size:12.5px;'
            f'color:rgba(245,240,232,0.92);line-height:1.6;font-style:italic;">{prompt_text}</div></div>')


def _box_result(items) -> str:
    rows = "".join(
        f'<div style="display:flex;align-items:flex-start;gap:10px;padding:10px 0;border-bottom:1px solid {LBR};">'
        f'<span style="font-size:16px;flex-shrink:0;">{icon}</span>'
        f'<div><div style="font-family:\'Space Grotesk\',sans-serif;font-size:13px;font-weight:700;color:{INK};">{title}</div>'
        f'<div style="font-family:\'Space Grotesk\',sans-serif;font-size:11px;color:{MUT};margin-top:2px;">{desc}</div></div></div>'
        for icon, title, desc in items
    )
    return (f'<div style="margin-top:14px;background:#ffffff;padding:6px 12px;border-radius:10px;'
            f'border:1.5px solid {LBR};box-shadow:0 2px 12px rgba(26,22,17,0.04);">{rows}</div>')


def _wrap_creme(inner: str) -> str:
    return (f'<div class="slide" style="width:{W}px;height:{H}px;position:relative;overflow:hidden;background:{LBG};box-sizing:border-box;">'
            f'{_decor_bg()}{_corner_glow()}{_slash_mark()}'
            f'<div style="position:relative;z-index:5;padding:56px 26px 44px;height:100%;box-sizing:border-box;overflow:hidden;">{inner}</div>'
            f'{_footer()}</div>')


def _proof_card_checklist(app_label: str, items) -> str:
    """Card flutuante estilo 'painel real' (screenshot-like) — items: lista de (checked:bool, texto).
    Modelado no post de maior conversão analisado (@castilho.ia): um print de app de verdade
    flutuando sobre a foto vende a prova muito mais que só texto."""
    rows = "".join(
        f'<div style="display:flex;align-items:center;gap:8px;padding:6px 0;">'
        f'<div style="width:15px;height:15px;border-radius:4px;flex-shrink:0;'
        f'background:{BP if checked else "transparent"};border:1.5px solid {BP if checked else "#C9C2B4"};'
        f'display:flex;align-items:center;justify-content:center;">'
        + ('<span style="color:#fff;font-size:10px;line-height:1;">&#10003;</span>' if checked else '')
        + f'</div><span style="font-family:\'Space Grotesk\',sans-serif;font-size:11.5px;'
          f'font-weight:600;color:{INK};">{text}</span></div>'
        for checked, text in items
    )
    return f"""<div style="position:absolute;left:24px;right:24px;background:#fff;border-radius:12px;
      padding:12px 14px;box-shadow:0 12px 30px rgba(0,0,0,0.35);z-index:3;">
      <div style="display:flex;align-items:center;gap:6px;margin-bottom:8px;padding-bottom:8px;
        border-bottom:1px solid {LBR};">
        <div style="width:8px;height:8px;border-radius:50%;background:{BP};"></div>
        <span style="font-family:\'Space Grotesk\',sans-serif;font-size:11px;font-weight:700;
          letter-spacing:0.5px;color:{INK};">{app_label}</span>
      </div>
      {rows}
    </div>"""


def _proof_card_stats(app_label: str, rows) -> str:
    """Card flutuante estilo 'painel/dashboard real' — rows: lista de (label, valor).
    Usar quando a prova é um painel/número (financeiro, métrica), não uma lista de tarefas
    (pra isso, ver _proof_card_checklist)."""
    body_rows = "".join(
        f'<div style="display:flex;justify-content:space-between;align-items:baseline;padding:7px 0;'
        f'{"border-bottom:1px solid " + LBR + ";" if i < len(rows) - 1 else ""}">'
        f'<span style="font-family:\'Space Grotesk\',sans-serif;font-size:12px;color:{MUT};font-weight:500;">{label}</span>'
        f'<span style="font-family:\'Bebas Neue\',Impact,sans-serif;font-size:20px;color:{INK};">{value}</span></div>'
        for i, (label, value) in enumerate(rows)
    )
    return f"""<div style="position:absolute;left:24px;right:24px;background:#fff;border-radius:12px;
      padding:12px 14px;box-shadow:0 12px 30px rgba(0,0,0,0.35);z-index:3;">
      <div style="display:flex;align-items:center;gap:6px;margin-bottom:8px;padding-bottom:8px;
        border-bottom:1px solid {LBR};">
        <div style="width:8px;height:8px;border-radius:50%;background:{BP};"></div>
        <span style="font-family:\'Space Grotesk\',sans-serif;font-size:11px;font-weight:700;
          letter-spacing:0.5px;color:{INK};">{app_label}</span>
      </div>
      {body_rows}
    </div>"""


PHOTO_BAND_H = 300  # px do slide (de 525) ocupados pela foto no slide 1


def _slide1_fullbleed(headline_lines, subtitle, tag_text, photo_path: Path, proof=None) -> str:
    """Slide 1: foto real ocupa a faixa de cima (sem texto sobreposto — evita cobrir o rosto,
    qualquer que seja o enquadramento da foto), texto fica na faixa escura sólida de baixo.
    Modelado nos posts virais analisados (castilho.ia, joaokepler, wendellcarvalho): a foto
    é a prova, o texto nunca compete com ela pelo mesmo espaço."""
    photo_uri = _img_data_uri(photo_path) if photo_path.exists() else None
    photo_html = (
        f'<img src="{photo_uri}" style="position:absolute;top:0;left:0;width:100%;height:{PHOTO_BAND_H}px;'
        f'object-fit:cover;object-position:center 15%;z-index:0;">'
        if photo_uri else f'<div style="position:absolute;top:0;left:0;width:100%;height:{PHOTO_BAND_H}px;background:{DBG};z-index:0;"></div>'
    )
    proof_html = ""
    if proof:
        if proof.get("type") == "stats":
            card = _proof_card_stats(proof["label"], proof["items"])
        else:
            card = _proof_card_checklist(proof["label"], proof["items"])
        # Sobrepõe a parte de baixo da FOTO (peito/jaqueta, nunca o rosto) — não invade a
        # faixa de texto abaixo.
        proof_html = f'<div style="position:absolute;top:{PHOTO_BAND_H - 150}px;left:0;right:0;z-index:2;">{card}</div>'

    text_top = PHOTO_BAND_H + 20
    return f"""<div class="slide" style="width:{W}px;height:{H}px;position:relative;overflow:hidden;background:{DBG};box-sizing:border-box;">
      {photo_html}
      <div style="position:absolute;left:0;right:0;top:{PHOTO_BAND_H - 60}px;height:60px;
        background:linear-gradient(180deg,rgba(18,16,13,0) 0%,rgba(18,16,13,1) 100%);z-index:1;"></div>
      {_slash_mark_light()}
      {proof_html}
      <div style="position:absolute;top:{text_top}px;left:26px;right:26px;z-index:5;">
        {_tag(tag_text, light=True)}
        {_h1(headline_lines[:2], size=32, light=True)}
        {_div()}
        {_body(subtitle, light=True)}
      </div>
    </div>"""


def _box_stat(items) -> str:
    """items: lista de (numero_grande, legenda) — card branco com números grandes em laranja.
    Pra reforçar autoridade/prova numérica na 'segunda capa'."""
    cols = "".join(
        f'<div style="flex:1;text-align:center;">'
        f'<div style="font-family:\'Bebas Neue\',Impact,sans-serif;font-size:32px;color:{BP};line-height:1;">{num}</div>'
        f'<div style="font-family:\'Space Grotesk\',sans-serif;font-size:10px;color:{MUT};margin-top:4px;line-height:1.3;">{leg}</div></div>'
        for num, leg in items
    )
    return (f'<div style="display:flex;gap:10px;background:#ffffff;border:1.5px solid {LBR};'
            f'border-radius:10px;padding:16px 10px;margin-top:16px;box-shadow:0 2px 12px rgba(26,22,17,0.04);">{cols}</div>')


def _slide_capa2(tag_text, headline_lines, body_text, stat_items) -> str:
    """Segunda capa (slide 2): fundo escuro, reforça o gancho do slide 1 com uma prova de
    autoridade/número concreto — modelado no padrão 'quem é essa pessoa / o que ela provou'
    encontrado nos posts virais analisados (@diegoalmeida.ia, @joelsonmadeira_)."""
    inner = (
        _tag(tag_text, light=True)
        + _h1(headline_lines, size=38, light=True)
        + _div()
        + _body(body_text, light=True)
        + _box_stat(stat_items)
    )
    return (f'<div class="slide" style="width:{W}px;height:{H}px;position:relative;overflow:hidden;'
            f'background:{DBG};box-sizing:border-box;">'
            f'<div style="position:relative;z-index:5;padding:56px 26px 44px;height:100%;box-sizing:border-box;'
            f'overflow:hidden;">{inner}</div>{_footer(light=True)}</div>')


def _slide_dor(tag_text, headline_lines, pain_lines) -> str:
    inner = _tag(tag_text) + _h1(headline_lines, size=42) + _div() + _body("Você sente isso quando:") + _box_pain(pain_lines)
    return _wrap_creme(inner)


def _slide_prompt(tag_text, headline_lines, body_text, prompt_text) -> str:
    inner = _tag(tag_text) + _h1(headline_lines, size=44) + _div() + _body(body_text) + _box_prompt(prompt_text)
    return _wrap_creme(inner)


def _slide_resultado(tag_text, headline_lines, body_text, items) -> str:
    inner = _tag(tag_text) + _h1(headline_lines, size=44) + _div() + _body(body_text) + _box_result(items)
    return _wrap_creme(inner)


def _slide_cta(cta_word: str, photo_path: Path) -> str:
    photo_uri = _img_data_uri(photo_path) if photo_path.exists() else None
    avatar = (
        f'<div style="display:flex;justify-content:center;margin-bottom:12px;margin-top:10px;">'
        f'<div style="width:68px;height:68px;border-radius:50%;overflow:hidden;border:3px solid {BP};'
        f'box-shadow:0 4px 20px rgba(255,140,0,0.25);">'
        f'<img src="{photo_uri}" style="width:100%;height:100%;object-fit:cover;object-position:center top;"></div></div>'
        if photo_uri else ""
    )
    inner = (
        avatar
        + f'<div style="text-align:center;font-family:\'Space Grotesk\',sans-serif;font-size:10px;font-weight:700;'
          f'letter-spacing:2px;color:{BP};text-transform:uppercase;margin-bottom:10px;">@THIAGORST.IA &middot; IA NA PR&Aacute;TICA</div>'
        + f'<div style="text-align:center;">{_h1(["ME SEGUE"], size=54)}</div>'
        + f'<div style="text-align:center;font-family:\'Bebas Neue\',Impact,sans-serif;font-size:24px;color:{INK};'
          f'line-height:1;margin-top:2px;">PRA N&Atilde;O PERDER OS PR&Oacute;XIMOS</div>'
        + f'<div style="background:{DBG};border-radius:10px;padding:12px 14px;margin-top:14px;">'
          f'<div style="font-family:\'Space Grotesk\',sans-serif;font-size:12.5px;font-weight:600;color:#fff;'
          f'line-height:1.45;text-align:center;">Todo dia eu mostro '
          f'<span style="color:{BP};font-weight:700;">1 jeito de usar IA</span> pra resolver uma dor real do seu dia. Sem enrola&ccedil;&atilde;o.</div></div>'
        + f'<div style="text-align:center;margin-top:12px;font-family:\'Space Grotesk\',sans-serif;font-size:12px;'
          f'color:{MUT};line-height:1.5;">E comenta <span style="color:{BP};font-weight:700;">{cta_word}</span> que eu te mando os prompts deste post &#128071;</div>'
    )
    return _wrap_creme(inner)


def build_slides_html(spec: dict) -> list:
    """Suporta carrossel de tamanho variável (5, 8, etc.) — cada item de spec['slides']
    tem um 'kind' que escolhe o renderer. kinds: capa, capa2, dor, prompt, resultado, cta."""
    photo_path = ROOT / spec.get("photo", "assets/thiago_perfil.jpg")
    slides_spec = spec["slides"]

    renderers = {
        "capa": lambda s: _slide1_fullbleed(s["headline"], s.get("subtitle", ""), s.get("tag", "IA NA PRÁTICA"), photo_path, proof=s.get("proof")),
        "capa2": lambda s: _slide_capa2(s.get("tag", "O CASO"), s["headline"], s.get("body", ""), s["stat_items"]),
        "dor": lambda s: _slide_dor(s.get("tag", "O PROBLEMA"), s["headline"], s["pain_lines"]),
        "prompt": lambda s: _slide_prompt(s.get("tag", "O PROMPT"), s["headline"], s.get("body", ""), s["prompt"]),
        "resultado": lambda s: _slide_resultado(s.get("tag", "O RESULTADO"), s["headline"], s.get("body", ""), s["items"]),
        "cta": lambda s: _slide_cta(s.get("cta_word", "CLAUDE"), photo_path),
    }
    return [renderers[s["kind"]](s) for s in slides_spec]


def build_html(spec: dict) -> str:
    slides = build_slides_html(spec)
    slides_wrapped = "".join(
        f'<div style="width:{W}px;height:{H}px;flex-shrink:0;">{s}</div>' for s in slides
    )
    return f"""<!doctype html>
<html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin:0; padding:40px; background:#ddd; display:flex; justify-content:center; }}
  .ig-frame {{ width:{W}px; background:#000; border-radius:16px; overflow:hidden; box-shadow:0 20px 60px rgba(0,0,0,0.3); }}
  .carousel-viewport {{ width:{W}px; height:{H}px; overflow:hidden; position:relative; }}
  .carousel-track {{ display:flex; transition: transform 0.3s ease; }}
</style>
</head>
<body>
  <div class="ig-frame">
    <div class="carousel-viewport">
      <div class="carousel-track">{slides_wrapped}</div>
    </div>
  </div>
</body></html>"""


async def export_slides(html: str, out_dir: Path, total: int):
    from playwright.async_api import async_playwright

    out_dir.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=SCALE)
        await page.set_content(html, wait_until="networkidle")
        await page.wait_for_timeout(2500)

        await page.evaluate(
            """() => {
                const frame = document.querySelector('.ig-frame');
                frame.style.cssText = 'width:%dpx;border-radius:0;box-shadow:none;margin:0;';
                document.body.style.cssText = 'padding:0;margin:0;background:#fff;';
            }""" % W
        )
        await page.wait_for_timeout(300)

        for i in range(total):
            await page.evaluate(
                """(idx) => {
                    const track = document.querySelector('.carousel-track');
                    track.style.transition = 'none';
                    track.style.transform = 'translateX(' + (-idx * %d) + 'px)';
                }""" % W,
                i,
            )
            await page.wait_for_timeout(200)
            await page.screenshot(
                path=str(out_dir / f"slide_{i + 1}.png"),
                clip={"x": 0, "y": 0, "width": W, "height": H},
            )
        await browser.close()


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 scripts/build_carousel.py <spec.json>")
        sys.exit(1)

    spec_path = Path(sys.argv[1])
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    slug = spec["slug"]

    html = build_html(spec)
    preview_dir = ROOT / "preview"
    preview_dir.mkdir(exist_ok=True)
    (preview_dir / f"{slug}.html").write_text(html, encoding="utf-8")
    print(f"Preview: {preview_dir / f'{slug}.html'}")

    out_dir = ROOT / "images" / slug
    asyncio.run(export_slides(html, out_dir, len(spec["slides"])))
    print(f"Slides exportados em: {out_dir}")


if __name__ == "__main__":
    main()
