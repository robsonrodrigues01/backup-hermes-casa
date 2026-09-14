#!/bin/bash
# Vigia do dashboard da squad (recriado 12/09 pelo CMO): se cair, relança dashboard-novo.py na 8800.
# Silencioso quando saudável (stdout vazio = não entrega nada). Fala só quando age ou quando falha.
if curl -sf -m 5 http://127.0.0.1:8800/api/health >/dev/null 2>&1; then
  exit 0
fi
cd /home/hermes/cuidarvc/squad/dashboard || { echo "VIGIA DASH: diretorio nao encontrado, nao consegui relancar"; exit 1; }
if pgrep -f "dashboard-novo.py" >/dev/null 2>&1; then
  echo "VIGIA DASH: health falhou mas o processo existe (possivel travamento), nao relancei: $(date '+%d/%m %H:%M')"
  exit 0
fi
DASH_PORT=8800 setsid nohup python3 dashboard-novo.py >>dash-novo.log 2>&1 &
sleep 4
if curl -sf -m 5 http://127.0.0.1:8800/api/health >/dev/null 2>&1; then
  echo "VIGIA DASH: servidor estava fora e foi RELANCADO na 8800 as $(date '+%d/%m %H:%M')"
else
  echo "VIGIA DASH: tentei relancar e o servidor continua fora na 8800 as $(date '+%d/%m %H:%M') - ver dash-novo.log"
fi
