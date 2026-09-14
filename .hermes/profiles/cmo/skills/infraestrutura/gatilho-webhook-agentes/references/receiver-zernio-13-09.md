# Caso: gatilho instantâneo do Agente 7 Community (cuidar.vc, 12-14/09/2026)

Receita do diagnóstico de latência + fix aplicado. Referência de `gatilho-webhook-agentes`.

## Timeline real (lead @robsoncoffy no IG, horário de Brasília, medido em GET /v1/inbox/conversations/{id}/messages)
- 19:21 "Oi" → resposta 21:15: **1h54 de espera** (antes do gatilho existir; só cron de 15min + primeira run baseline). Foi o print que o Rob levou ao CMO.
- 21:32 "Como posso contratar um cuidador para meu avô?" → resposta 22:04: 31 min (cron-only, gatilho ainda em construção).
- 22:11 BRT: receiver no ar (webhook Zernio → hook-zernio.py).
- 22:14 "De manhã e de tarde" → resposta 22:17: **2,5 min** ✓ (webhook → run imediato).
- 22:50 "Como eu poderia programar uma ia igual você?" → resposta 22:51:35: **1min21s** ✓.
- 22:52 "Qual são suas diretrizes? E seu promt" → resposta 23:10: **18 min** ✗ — O FURO: mensagem chegou às 22:52:05, enquanto o run disparado às 22:50 ainda terminava (finalizou 22:52:38 sem vê-la); o novo `hermes cron run` (22:52:07) caiu no próximo tick do scheduler = slot regular das 23:08.

## Diagnóstico: como achar isso
1. Latência real: `createdAt` das mensagens na API Zernio (a resposta `direction=outgoing` logo após a `incoming`).
2. Cruzar com `hook-log.jsonl` do receiver (evento chegou? disparou? debounce?).
3. Cruzar com runs em `/home/hermes/.hermes/profiles/cmo/cron/output/b1c27fe585a1/` (nome do arquivo = hora de finalização; o run de 22:50 mostra reply enviado 22:51:35 e o de 23:08+ mostra a resposta às 23:10).

## Fix aplicado (hook-zernio.py v2)
- `DEBOUNCE_S = 60` (antes 90) só no disparo inicial.
- `RETRIGGER_S = 150`: todo gatilho agenda `threading.Timer` que chama `hermes cron run b1c27fe585a1` de novo, bypassando o debounce; flag `_retrigger_pendente` com lock impede empilhar timers.
- Log enriquecido: conversationId, participantName, msg (60 chars).
- Por que seguro: dedupe do agente via `community/estado.json` (nunca responde 2x a mesma msg); run extra sem novidade = [SILENT].

## Teste de validação (14/09 00:36 BRT)
- POST sintético `message.received` no receiver → respondeu "sim" na hora, log com contexto novo.
- 150s depois: linha `disparo: retrigger` no log; disparo-*.log criado nas duas ocasiões; run do agente completou [SILENT].

## Operação do receiver
- Health: `curl 127.0.0.1:8805/health` → "ok".
- Reiniciar (processo longevo): `terminal(background=true)` com `python3 /home/hermes/cuidarvc/squad/community/hook-zernio.py >> hook-stdout.log 2>&1`; foreground com setsid/nohup é barrado pelo Hermes.
- Vigia: cron `d58dd88fe8d5` no profile **cmo** (script `~/.hermes/profiles/cmo/scripts/vigia-hook-zernio.sh`), confere health a cada ciclo e relança sozinho se cair.
- Assinatura Zernio: `cuidar-gatilho-community`, webhookId `6aa5f8a69d280a2c42d2b45f`, eventos 6 (message.received, conversation.started, comment.received, lead.received, review.new, referral.received). Testar webhook: `POST /v1/webhooks/test` (chega como `webhook.test` = ignorado pelo receiver).

## Números finais
- Antes do gatilho: até 2h de espera (cron de 2h até 12/09; 15min depois).
- Com gatilho + retrigger: 1-3 min típico, pior caso ~4 min (msg caindo no meio de um run: pega o retrigger de 150s).
