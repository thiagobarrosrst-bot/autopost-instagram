"""
publish_instagram.py — Publica um carrossel (ou imagem única) no Instagram
via Meta Graph API.

Estratégia de URL pública (a Meta exige uma URL http(s) acessível, nunca um
caminho de arquivo local):
  1. Já é uma URL (http/https) -> usa direto.
  2. Caminho relativo ao repo + GITHUB_RAW_BASE configurado -> monta URL
     raw.githubusercontent.com (confiável, permanente, sem dependência de
     terceiros).
  3. Fallback: upload pra um host de imagem temporário (catbox -> uguu).
"""
import argparse
import os
import sys
import time
from pathlib import Path
from uuid import uuid4

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

IG_ID = os.getenv("INSTAGRAM_BUSINESS_ID")
ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
API_VERSION = os.getenv("META_API_VERSION", "v19.0")
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"
GITHUB_RAW_BASE = os.getenv("GITHUB_RAW_BASE", "").rstrip("/")

POLL_ATTEMPTS = 12
POLL_INTERVAL_S = 5


def get_public_url(image_path: str) -> str:
    if image_path.startswith("http://") or image_path.startswith("https://"):
        return image_path

    if GITHUB_RAW_BASE:
        try:
            rel = Path(image_path).resolve().relative_to(ROOT)
            # Cache-buster: a Meta guarda em cache uma tentativa de download
            # falha pra uma URL exata (ex: repo estava privado na 1a tentativa)
            # e continua rejeitando essa mesma URL depois, mesmo já pública.
            return f"{GITHUB_RAW_BASE}/{rel.as_posix()}?v={uuid4().hex[:8]}"
        except ValueError:
            pass  # imagem fora do repo — cai pro upload

    return _upload_to_temp_host(image_path)


def _upload_to_temp_host(image_path: str) -> str:
    providers = [("catbox", _try_catbox), ("uguu", _try_uguu)]
    last_err = None
    for name, fn in providers:
        try:
            print(f"  Upload [{name}]...")
            url = fn(image_path)
            print(f"  Hospedada: {url}")
            return url
        except Exception as e:
            print(f"  [{name}] falhou: {e}")
            last_err = e
            time.sleep(2)
    raise RuntimeError(f"Todos os hosts de fallback falharam. Último erro: {last_err}")


def _try_catbox(image_path: str) -> str:
    with open(image_path, "rb") as f:
        resp = requests.post(
            "https://catbox.moe/user/api.php",
            data={"reqtype": "fileupload", "userhash": ""},
            files={"fileToUpload": (Path(image_path).name, f, "image/png")},
            timeout=60,
        )
    url = resp.text.strip()
    if not url.startswith("https://"):
        raise RuntimeError(f"Catbox rejeitou: {url}")
    return url


def _try_uguu(image_path: str) -> str:
    with open(image_path, "rb") as f:
        resp = requests.post(
            "https://uguu.se/upload",
            files={"files[]": (Path(image_path).name, f, "image/png")},
            timeout=60,
        )
    data = resp.json()
    files = data.get("files", [])
    if not files or not files[0].get("url", "").startswith("https://"):
        raise RuntimeError(f"uguu rejeitou: {data}")
    return files[0]["url"]


def _wait_until_finished(container_id: str):
    for i in range(POLL_ATTEMPTS):
        r = requests.get(
            f"{BASE_URL}/{container_id}",
            params={"fields": "status_code", "access_token": ACCESS_TOKEN},
            timeout=15,
        )
        status = r.json().get("status_code", "")
        if status == "FINISHED":
            return
        if status == "ERROR":
            raise RuntimeError(f"Erro de processamento: {r.json()}")
        print(f"  Processando... {i * POLL_INTERVAL_S}s")
        time.sleep(POLL_INTERVAL_S)
    raise RuntimeError("Timeout esperando o container ficar pronto.")


def _create_carousel_item(image_path: str) -> str:
    resp = requests.post(
        f"{BASE_URL}/{IG_ID}/media",
        data={
            "access_token": ACCESS_TOKEN,
            "image_url": get_public_url(image_path),
            "is_carousel_item": "true",
        },
        timeout=60,
    )
    result = resp.json()
    if "id" not in result:
        raise RuntimeError(f"Erro ao criar item do carrossel: {result}")
    return result["id"]


def publish_carousel(images: list, caption: str) -> str:
    item_ids = []
    for img in images:
        item_ids.append(_create_carousel_item(img))
        time.sleep(2)

    resp = requests.post(
        f"{BASE_URL}/{IG_ID}/media",
        data={
            "access_token": ACCESS_TOKEN,
            "media_type": "CAROUSEL",
            "children": ",".join(item_ids),
            "caption": caption,
        },
        timeout=30,
    )
    result = resp.json()
    if "id" not in result:
        raise RuntimeError(f"Erro ao criar carrossel: {result}")
    carousel_id = result["id"]
    _wait_until_finished(carousel_id)

    resp2 = requests.post(
        f"{BASE_URL}/{IG_ID}/media_publish",
        data={"access_token": ACCESS_TOKEN, "creation_id": carousel_id},
        timeout=30,
    )
    result2 = resp2.json()
    if "id" not in result2:
        raise RuntimeError(f"Erro ao publicar: {result2}")
    return result2["id"]


def publish_single(image_path: str, caption: str) -> str:
    resp = requests.post(
        f"{BASE_URL}/{IG_ID}/media",
        data={
            "access_token": ACCESS_TOKEN,
            "image_url": get_public_url(image_path),
            "caption": caption,
        },
        timeout=60,
    )
    result = resp.json()
    if "id" not in result:
        raise RuntimeError(f"Erro ao criar container: {result}")
    container_id = result["id"]
    _wait_until_finished(container_id)

    resp2 = requests.post(
        f"{BASE_URL}/{IG_ID}/media_publish",
        data={"access_token": ACCESS_TOKEN, "creation_id": container_id},
        timeout=30,
    )
    result2 = resp2.json()
    if "id" not in result2:
        raise RuntimeError(f"Erro ao publicar: {result2}")
    return result2["id"]


def run(images: list, caption: str, dry_run: bool = False):
    if not IG_ID or not ACCESS_TOKEN:
        print("ERRO: INSTAGRAM_BUSINESS_ID / INSTAGRAM_ACCESS_TOKEN não configurados.")
        sys.exit(1)
    if not images:
        print("ERRO: nenhuma imagem fornecida.")
        sys.exit(1)
    for img in images:
        if not (img.startswith("http://") or img.startswith("https://")) and not Path(img).exists():
            print(f"ERRO: imagem não encontrada: {img}")
            sys.exit(1)

    if dry_run:
        print(f"[DRY RUN] {len(images)} imagem(ns), publicação não executada.")
        return

    if len(images) == 1:
        post_id = publish_single(images[0], caption)
    else:
        post_id = publish_carousel(images, caption)

    print(f"Publicado com sucesso! Post ID: {post_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", nargs="+", required=True)
    parser.add_argument("--caption", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(args.images, args.caption, args.dry_run)
