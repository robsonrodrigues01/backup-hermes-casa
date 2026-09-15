#!/usr/bin/env python3
"""Vigia das capas do blog do cuidar.vc.

As imagens de p_imagem_url hospedadas em litter.catbox.moe expiram em 72h.
Este vigia sobe a capa local de novo, atualiza o JSON do artigo e republica
via RPC, mantendo a imagem viva ate o dev entregar hospedagem definitiva.

Padrao watchdog: se der tudo certo imprime NADA (silencio). Se quebrar,
imprime a mensagem e sai com codigo 1 para o alerta do cron.
"""
import json
import subprocess
import sys
from pathlib import Path

BLOG = Path("/home/hermes/cuidarvc/squad/blog")
LITTER = "https://litter.catbox.moe/resources/internals/api.php"


def falha(msg: str):
    print("REFRESH_CAPA: " + msg)
    raise SystemExit(1)


def main() -> None:
    artigos = sorted((BLOG / "artigos").glob("*.json"))
    if not artigos:
        falha("nenhum artigo em squad/blog/artigos/*.json")
    tocado = 0
    for artigo_path in artigos:
        artigo = json.loads(artigo_path.read_text(encoding="utf-8"))
        url = artigo.get("p_imagem_url") or ""
        if not ("litter.catbox.moe" in url or "0x0.st" in url):
            continue
        slug = (artigo.get("p_slug") or "").strip()
        capa = None
        for ext in (".jpg", ".png"):
            candidato = BLOG / "capas" / (slug + ext)
            if candidato.exists():
                capa = candidato
                break
        if capa is None:
            falha("capa local nao encontrada para '" + slug + "' (procurei capas/" + slug + ".jpg/.png)")

        nova = ""
        for tentativa in range(2):
            upload = subprocess.run(
                ["curl", "-sS", "-m", "40",
                 "-A", "Mozilla/5.0 (X11; Linux x86_64) cuidar-vigia/1.0",
                 "-F", "reqtype=fileupload", "-F", "time=72h",
                 "-F", "fileToUpload=@" + str(capa), LITTER],
                capture_output=True, text=True, timeout=60,
            )
            saida_up = (upload.stdout or "").strip()
            if saida_up.startswith("https://"):
                nova = saida_up
                break
            if tentativa < 1:
                subprocess.run(["sleep", "65"], timeout=80)
        if not nova:
            fallback = subprocess.run(
                ["curl", "-sS", "-m", "40", "-F", "file=@" + str(capa), "https://0x0.st"],
                capture_output=True, text=True, timeout=60,
            )
            nova = (fallback.stdout or "").strip()
        if not nova.startswith("https://"):
            falha("upload da capa falhou para '" + slug + "': " + (nova or "")[:200])

        artigo["p_imagem_url"] = nova
        artigo_path.write_text(json.dumps(artigo, ensure_ascii=False, indent=1), encoding="utf-8")

        publicar = subprocess.run(
            [sys.executable, str(BLOG / "publicar.py"), str(artigo_path)],
            capture_output=True, text=True, timeout=180,
        )
        saida = (publicar.stdout or "").strip()
        try:
            resultado = json.loads(saida)
            if resultado.get("ok") is not True:
                falha("rpc nao confirmou ok para '" + slug + "': " + saida[:200])
        except ValueError:
            if publicar.returncode != 0:
                falha("publicar.py falhou para '" + slug + "': " + ((publicar.stderr or saida) or "")[:200])
        tocado += 1


if __name__ == "__main__":
    main()
