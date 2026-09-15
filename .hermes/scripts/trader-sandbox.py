#!/usr/bin/env python3
"""Trader Sandbox — fase 1 (dinheiro IMAGINARIO).
Uso: trader-sandbox.py tick  |  trader-sandbox.py report
Estrategia v0 (conservadora, BTC/Kraken): comprar recuo de 1.5% vs media 6h,
realizar lucro +1.5%, cortar prejuizo -2%, freio diario se perda acumulada > $150.
Estado em state.json. nada disso toca dinheiro real.
"""
import json, sys, time, urllib.request
from datetime import datetime, timezone, timedelta

BASE = "/home/hermes/trader-sandbox"
STATE = f"{BASE}/state.json"
WALLET_USD = 10000.00   # carteira virtual
POS_USD = 2000.00       # 20% por operacao
STOP_LOSS = 0.98        # corta em -2%
TAKE_PROFIT = 1.015     # lucra em +1.5%
COMPRA_GATILHO = 0.985  # compra a -1.5% da media 6h
FREIO_DIA = -150.00     # perde $150 no dia = para

def agora():
    return datetime.now(timezone.utc)

def hoje():
    return agora().strftime("%Y-%m-%d")

def preco_btc():
    req = urllib.request.Request(
        "https://api.kraken.com/0/public/Ticker?pair=XBTUSD",
        headers={"User-Agent": "sandbox/0.1"})
    r = json.load(urllib.request.urlopen(req, timeout=20))
    return float(r["result"]["XXBTZUSD"]["c"][0])

def carregar():
    try:
        with open(STATE) as f:
            return json.load(f)
    except Exception:
        return {"history": [], "pos": None, "trades": [], "halt_date": None,
                "pnl_total": 0.0, "wl_usd": WALLET_USD}

def salvar(s):
    with open(STATE, "w") as f:
        json.dump(s, f, ensure_ascii=False)

def media(s, min_):
    h = [p for t, p in s["history"][-min_:]]
    return sum(h) / len(h) if h else None

def tick():
    s = carregar()
    p = preco_btc()
    if not p or p <= 0:
        return
    s["history"].append([int(time.time()), p])
    s["history"] = s["history"][-672:]  # 7 dias em ciclos de 15min
    m6 = media(s, 24)  # 6h = 24 ciclos de 15min
    t = agora()
    hh = t.hour * 60 + t.minute
    linha = f"| {t:%H:%M}Z BTC ${p:,.0f}"

    # freio diario ativo?
    perda_dia = sum(tr["pnl"] for tr in s["trades"] if tr["fechado"].startswith(hoje()))
    if s["halt_date"] == hoje() and hh >= 23 * 60:
        s["halt_date"] = None  # nova meia-noite libera

    if perda_dia <= FREIO_DIA:
        s["halt_date"] = hoje()
    print(f"tick {linha} pnl_dia {perda_dia:+.2f} halt {s['halt_date'] == hoje()}")

    if s["halt_date"] == hoje():
        salvar(s); return

    if s["pos"] is None and m6:
        if p < m6 * COMPRA_GATILHO:
            btc = POS_USD / p
            s["pos"] = {"aberto": t.isoformat(timespec="seconds"), "entrada": p,
                        "usd": POS_USD, "btc": round(btc, 8)}
            s["wl_usd"] -= POS_USD
            print(f"COMPRA (papel) ${POS_USD:.0f} @ {p:,.2f}")
    elif s["pos"]:
        e = s["pos"]["entrada"]
        if p >= e * TAKE_PROFIT or p <= e * STOP_LOSS:
            causa = "take_profit" if p >= e * TAKE_PROFIT else "stop_loss"
            lucro = s["pos"]["usd"] * (p / e - 1)
            s["wl_usd"] += s["pos"]["usd"] + lucro
            s["pnl_total"] += lucro
            s["trades"].append({"fechado": t.isoformat(timespec="seconds"),
                                "entrada": e, "saida": p, "pnl": round(lucro, 2),
                                "causa": causa})
            print(f"FECHA ({causa}) pnl {lucro:+.2f} | total {s['pnl_total']:+.2f} | carteira {s['wl_usd']:.2f}")
            s["pos"] = None
    salvar(s)

def report():
    s = carregar()
    p = preco_btc()
    t = datetime.now(timezone(timedelta(hours=-3)))  # Brasília
    aberto = 0.0
    if s["pos"]:
        aberto = s["pos"]["usd"] * (p / s["pos"]["entrada"] - 1)
    trades_dia = [tr for tr in s["trades"] if tr["fechado"].startswith(hoje())]
    perda_dia = sum(tr["pnl"] for tr in trades_dia)
    print(f"*TRADER SANDBOX ({t:%d/%m %H:%M} Bsb — dinheiro de papel)*")
    print(f"Carteira virtual: **US$ {s['wl_usd'] + s['pos']['usd'] if s['pos'] else s['wl_usd']:,.2f}** (inicial {WALLET_USD:,.0f})")
    print(f"Resultado total: {'**+' if s['pnl_total'] >= 0 else '**-'}US$ {abs(s['pnl_total']):,.2f}** em {len(s['trades'])} operações fechadas")
    if s["pos"]:
        print(f"Posição aberta: BTC comprado a {s['pos']['entrada']:,.2f} | no ar: {'+' if aberto >= 0 else '-'}US$ {abs(aberto):,.2f}")
    if trades_dia:
        print(f"Operações de hoje: {len(trades_dia)} | resultado do dia {perda_dia:+.2f}")
    if s["halt_date"] == hoje():
        print("Freio diário ATIVO (perdeu o limite do dia — parado até amanhã)")
    if not s["trades"] and not s["pos"]:
        print("Ainda sem operações — aguardando gatilho de preço.")

if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "tick"
    try:
        tick() if modo == "tick" else report()
    except Exception as e:
        print(f"ERRO sandbox: {e}", file=sys.stderr)
        sys.exit(1)
