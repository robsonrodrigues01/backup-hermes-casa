#!/usr/bin/env python3
"""Esqueleto de runner de piloto sandbox (dinheiro/conta de papel).

Copiar para ~/.hermes/scripts/<nome>/<nome>.py e adaptar as 3 funções.
Uso: ./runner.py tick   (calado; usado pelo cron */15)
     ./runner.py report (imprime resumo em texto; usado pelo cron diário)
"""
import json, os, sys
from datetime import datetime, timezone

# --- DOC_NAME(config) --- preencha os 5; são CONSTANTES, não config editável.
CARTEIRA_INICIAL = 10_000.00
DOCUMENTADORA = "sandbox"
NOME = "piloto-x"
FRACAO_POR_OP = 0.20      # 20% da carteira por operação
LUCRO_ALVO = 0.015        # sai com +1,5%
STOP_LOSS = 0.02          # corta com -2%
FREIO_DIA = 150.0         # trava o dia se acumular perda de US$ 150
FUSO_RELATORIO = "America/Sao_Paulo"  # relatório em fuso do Rob (Bsb)

DIR = os.path.dirname(os.path.abspath(__file__))
ESTADO = os.path.join(DIR, "estado.json")


def novo_estado():
    return {"saldo": CARTEIRA_INICIAL, "posicao": None, "ops": [],
            "perda_dia": 0.0, "freio_dia": False, "dia": _hoje()}


def _hoje():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def ler_mercado():
    """Leitura pública (sem chave). Retorne preço atual (float) ou None."""
    raise NotImplementedError  # ex.: requests.get(URL_PUBLICA).json()


def decidir(estado, preco):
    """Copie/adapte as regras. NUNCA quebre o freio: freio_dia=True => espera."""
    if estado["freio_dia"]:
        return "espera"
    if estado["posicao"] is None:
        return "comprar"          # regra de entrada do piloto
    pos = estado["posicao"]
    if preco >= pos["preco"] * (1 + LUCRO_ALVO) or preco <= pos["preco"] * (1 - STOP_LOSS):
        return "vender"
    return "espera"


def executar(estado, acao, preco):
    if acao == "comprar":
        estado["posicao"] = {"preco": preco, "qtd": (estado["saldo"] * FRACAO_POR_OP) / preco}
        estado["saldo"] -= estado["saldo"] * FRACAO_POR_OP
    elif acao == "vender":
        pos = estado["posicao"]
        valor_saida = pos["qtd"] * preco
        resultado = valor_saida - (pos["qtd"] * pos["preco"])
        estado["saldo"] += valor_saida
        estado["ops"].append({**pos, "saida": preco, "resultado": round(resultado, 2)})
        if resultado < 0:
            estado["perda_dia"] -= resultado
            if estado["perda_dia"] >= FREIO_DIA:
                estado["freio_dia"] = True   # freio o restante do dia
        estado["posicao"] = None
    return estado


def carregar():
    if os.path.exists(ESTADO):
        e = json.load(open(ESTADO))
        if e.get("dia") != _hoje():          # virada de dia: zera freio
            e.update(perda_dia=0.0, freio_dia=False, dia=_hoje())
        return e
    return novo_estado()


def main():
    acao_cli = sys.argv[1] if len(sys.argv) > 1 else "tick"
    estado = carregar()
    preco = ler_mercado()
    if acao_cli == "tick":
        acao = decidir(estado, preco)
        if acao in ("comprar", "vender"):
            estado = executar(estado, acao, preco)
        json.dump(estado, open(ESTADO, "w"), indent=1)  # tick CALADO: só estado
    elif acao_cli == "report":
        pnl = estado["saldo"] - CARTEIRA_INICIAL
        print(f"[{NOME}] saldo US$ {estado['saldo']:.2f} | P&L +/- US$ {pnl:+.2f} "
              f"| ops={len(estado['ops'])} | freio_dia={estado['freio_dia']} "
              f"| preco agora={preco}")
        # Cron: job com LLM le completa a mensagem humana a partir do stdout.

if __name__ == "__main__":
    main()
