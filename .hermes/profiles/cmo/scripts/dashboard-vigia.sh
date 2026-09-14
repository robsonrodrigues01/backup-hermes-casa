#!/bin/bash
# Vigia do dashboard da squad (cuidar.vc): relança o servidor se ele cair.
# Silencioso quando está tudo bem (stdout vazio = nada é enviado).
if ! curl -sf -m 8 http://127.0.0.1:8800/api/health >/dev/null 2>&1; then
  cd /home/hermes/cuidarvc/squad/dashboard
  nohup python3 dashboard.py >> dash.log 2>&1 &
  sleep 3
  if curl -sf -m 8 http://127.0.0.1:8800/api/health >/dev/null 2>&1; then
    echo "Vigia: o dashboard da squad caiu e foi relançado sozinho; já está no ar de novo."
  else
    echo "Vigia: o dashboard da squad está fora do ar e não subiu sozinho. Verificar /home/hermes/cuidarvc/squad/dashboard/dash.log"
  fi
fi
