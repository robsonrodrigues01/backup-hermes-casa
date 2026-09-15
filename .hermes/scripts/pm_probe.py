#!/usr/bin/env python3
"""Probe READ-ONLY do mercado horario de BTC na Polymarket.
Usa SDK oficial (polymarket-client) do venv do sandbox. Sem chave, sem ordem.
Sai JSON no stdout: {"found": true, title, slug, q, up, down} ou {"found": false}.
Bug conhecido do SDK 0.10.0: paginacao infinita no search() -> usar sempre .first_page().
"""
import sys, os, json, glob

for _sp in glob.glob("/home/hermes/trader-sandbox/.venv/lib/python3.*/site-packages"):
    sys.path.insert(0, _sp)


def main():
    from polymarket import PublicClient
    c = PublicClient()
    evs = c.list_events(tag_slug="crypto", order="volume24hr")
    ev = None
    for e in evs.first_page().items:
        if "Bitcoin Up or Down" in (getattr(e, "title", "") or ""):
            ev = e
            break
    out = {"found": False}
    if ev is not None:
        m = (getattr(ev, "markets", None) or [None])[0]
        if m is not None:
            oc = getattr(m, "outcomes", None)
            up = getattr(oc, "yes", None)
            dn = getattr(oc, "no", None)
            out = {
                "found": True,
                "title": (getattr(ev, "title", "") or "")[:48],
                "slug": getattr(ev, "slug", ""),
                "q": (getattr(m, "question", "") or "")[:80],
                "up": str(c.get_midpoint(token_id=up.token_id)) if up and up.token_id else None,
                "down": str(c.get_midpoint(token_id=dn.token_id)) if dn and dn.token_id else None,
            }
    json.dump(out, sys.stdout)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        json.dump({"found": False, "erro": str(e)[:200]}, sys.stdout)
        sys.exit(1)
