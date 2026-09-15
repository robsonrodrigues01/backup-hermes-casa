#!/usr/bin/env python3
"""Vigia de lag READ-ONLY (24h): Kraken spot vs meio da Polymarket (Up/Down horario BTC).
Amostra cada 20s e appenda JSONL. Analise depois acha rajadas de spot (0.07%/tick)
e mede a latencia do midpoint da PM em ajustar. Custo: so leitura publica.
Env: WATCH_HOURS (default 24), VIGIA_TICK (default 20).
Saida: /home/hermes/trader-sandbox/lag_events.jsonl
"""
import json, os, subprocess, sys, time, urllib.request

OUT = "/home/hermes/trader-sandbox/lag_events.jsonl"
PM_PROBE = "/home/hermes/.hermes/scripts/pm_probe.py"
HOURS = float(os.environ.get("WATCH_HOURS", "24"))
TICK = int(float(os.environ.get("VIGIA_TICK", "20")))
DEADLINE = time.time() + HOURS * 3600

n = ok = 0
while time.time() < DEADLINE:
    t = int(time.time())
    spot = up = dn = slug = None
    try:
        req = urllib.request.Request(
            "https://api.kraken.com/0/public/Ticker?pair=XBTUSD",
            headers={"User-Agent": "trader-casa"})
        r = json.load(urllib.request.urlopen(req, timeout=15))
        spot = float(r["result"]["XXBTZUSD"]["c"][0])
        ok += 1
    except Exception:
        pass
    try:
        r2 = subprocess.run([sys.executable, PM_PROBE], capture_output=True,
                            text=True, timeout=40)
        if r2.returncode == 0 and r2.stdout.strip().startswith("{"):
            d = json.loads(r2.stdout)
            if d.get("found"):
                up, dn, slug = d.get("up"), d.get("down"), d.get("slug")
    except Exception:
        pass
    with open(OUT, "a") as f:
        f.write(json.dumps([t, spot, up, dn, slug]) + "\n")
    n += 1
    # recicla: dorme o tick menos o gasto nas chamadas
    time.sleep(max(1, TICK - (time.time() - t)))

print(json.dumps({"vigia_fim": {"ticks": n, "ok": ok, "horas": HOURS}}))
