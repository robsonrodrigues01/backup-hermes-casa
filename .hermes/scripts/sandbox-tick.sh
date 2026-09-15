#!/bin/bash
# Trader sandbox — tick de 15 em 15 min via cron (no_agent).
# SILÊNCIO a menos que: compra, fechamento, freio diário ligado, ou erro 2x seguidas.
PY=/usr/bin/python3
SCRIPT=/home/hermes/.hermes/scripts/trader-sandbox.py
STATE=/home/hermes/trader-sandbox/state.json
FLAG=/home/hermes/trader-sandbox/.flags/halt_last

out=$($PY "$SCRIPT" tick 2>&1)
rc=$?

if [ $rc -ne 0 ]; then
  sleep 45  # falha transitória? tenta 1x mais
  out=$($PY "$SCRIPT" tick 2>&1)
  rc=$?
  if [ $rc -ne 0 ]; then
    echo "SANDBOX ERRO 2x seguidas: ${out:0:400}"
    exit 1
  fi
  out=""  # recuperou na 2a tentativa — fica em silêncio
fi

# 1) eventos de trade (compra/fechamento)
ev=$(printf '%s\n' "$out" | grep -E "COMPRA|FECHA")
[ -n "$ev" ] && printf '%s\n' "$ev"

# 2) freio diário: alerta UMA vez quando liga (estado muda pra data de hoje)
halt_on=$($PY -c "
import json
s = json.load(open('$STATE'))
print(s.get('halt_date') or '')
" 2>/dev/null)
mkdir -p "$(dirname "$FLAG")" 2>/dev/null
prev=$(cat "$FLAG" 2>/dev/null)
if [ -n "$halt_on" ] && [ "$halt_on" != "$prev" ]; then
  echo "FREIO DIARIO ATIVO (perdeu US\$ 150 no dia) — sandbox parado ate amanha"
  echo -n "$halt_on" > "$FLAG"
fi
exit 0
