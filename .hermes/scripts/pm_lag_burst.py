#!/usr/bin/env python3
"""Burst de lag READ-ONLY: Kraken spot vs meio da Polymarket (Up/Down horario BTC).
Amostra cada 20s por ~12min. Detecta movimento >=0.07% no spot (proxy do oracle)
e mede se/quando o meio da Polymarket ajusta. Custo: so leitura publica.
Saida: /home/hermes/trader-sandbox/lag_burst.json
"""
import json, subprocess, sys, time, urllib.request

OUT = "/home/hermes/trader-sandbox/lag_burst.json"
PM_PROBE = "/home/hermes/.hermes/scripts/pm_probe.py"

sample = []
for i in range(36):  # 36 x 20s ~ 12min
    t = int(time.time())
    kspot = None
    try:
        req = urllib.request.Request(
            "https://api.kraken.com/0/public/Ticker?pair=XBTUSD",
            headers={"User-Agent": "trader-casa"})
        r = json.load(urllib.request.urlopen(req, timeout=15))
        kspot = float(r["result"]["XXBTZUSD"]["c"][0])
    except Exception:
        pass
    up = dn = slug = None
    try:
        r2 = subprocess.run([sys.executable, PM_PROBE], capture_output=True,
                            text=True, timeout=40)
        if r2.returncode == 0 and r2.stdout.strip().startswith("{"):
            d = json.loads(r2.stdout)
            if d.get("found"):
                up, dn, slug = d.get("up"), d.get("down"), d.get("slug")
    except Exception:
        pass
    sample.append([t, kspot, up, dn, slug])
    if i < 35:
        time.sleep(20)

# analise: movimentos >= 0.07% no spot entre amostras consecutivas
moves = []
for i in range(1, len(sample)):
    p0, p1 = sample[i - 1][1], sample[i][1]
    if p0 and p1 and abs(p1 / p0 - 1) >= 0.0007:
        moves.append({
            "i": i, "move_pct": (p1 / p0 - 1) * 100,
            "pm_before": sample[i - 1][2], "pm_after": sample[i][2],
            "next_pm": sample[i + 1][2] if i + 1 < len(sample) else None,
        })

out = {
    "n_samples": len(sample),
    "slug_last": sample[-1][4] if sample else None,
    "kraken_first_last": [sample[0][1], sample[-1][1]] if sample else None,
    "pm_changes_detected": sum(
        1 for i in range(1, len(sample))
        if sample[i][2] and sample[i - 1][2] and abs(float(sample[i][2]) - float(sample[i - 1][2])) > 1e-9
    ),
    "spot_moves_ge_0.07pct": moves,
    "samples_tail": sample[-6:],
}
with open(OUT, "w") as f:
    json.dump(out, f)
print(json.dumps({
    "n": len(sample), "spot_moves": len(moves), "pm_mudou": out["pm_changes_detected"],
    "exemplos": moves[:4],
}))
