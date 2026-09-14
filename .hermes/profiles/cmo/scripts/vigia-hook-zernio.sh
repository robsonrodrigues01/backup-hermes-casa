#!/bin/bash
# Vigia do receiver de webhooks da Zernio (gatilho de DMs/comentários do Agente 7).
# Silencioso quando saudável (padrão watchdog). Se o receiver cair: relança e avisa em 1 linha.
set -u
H="http://127.0.0.1:8805/health"
LOG=/home/hermes/cuidarvc/squad/community/hook-stdout.log

if curl -s -m 5 "$H" | grep -q "ok"; then
  exit 0
fi

# receiver fora do ar: relança
setsid nohup python3 /home/hermes/cuidarvc/squad/community/hook-zernio.py >>"$LOG" 2>&1 &
sleep 4
if curl -s -m 5 "$H" | grep -q "ok"; then
  echo "Gatilho de DMs (receiver Zernio) tinha caído e foi relançado agora. Saudável novamente."
  exit 0
fi
echo "ERRO: receiver de webhooks da Zernio caiu e o relance falhou. Health check continua sem resposta na porta 8805."
exit 1
