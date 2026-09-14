---
name: gatilho-webhook-agentes
description: Disparar agentes cron do Hermes NA HORA via webhook externo (receiver HTTP + retrigger garantido + vigia), e depurar latência de resposta de agentes. Use quando um lead/usuário precisa de resposta em minutos e o intervalo do cron (15min+) é lento demais, quando for construir um gatilho instantâneo de evento (Zernio, GitHub, Stripe etc.) ou quando precisar investigar "por que o agente demora pra responder".
---

# Gatilho instantâneo de agentes cron via webhook

## Quando usar
- Lead esperando resposta em minutos (caso real: DM de lead no Instagram, Agente 7 Community do cuidar.vc). O cron periódico vira rede de segurança; o webhook vira o caminho principal.
- Depurar "demora pra responder": medir latência REAL no provedor antes de mexer em qualquer coisa.

## Arquitetura (validada em produção, cuidar.vc 13/09)
evento no provedor (ex.: Zernio `message.received`) → POST no receiver local (Caddy expõe `https://<dominio>/hook/<token>` → repassa pra `127.0.0.1:<port>`) → receiver dispara `hermes cron run <job_id>` na hora → agente roda e responde.

Receiver em Python puro (stdlib, zero dependência):
- `ThreadingHTTPServer`, bind SÓ em `127.0.0.1` (exposição pública apenas via Caddy).
- Token no path, validado com `secrets.compare_digest`; token NUNCA vai pro log.
- Set `GATILHOS` com os eventos que valem disparo. Eco das ações próprias do bot (ex.: `message.sent`, `post.published`, `webhook.test`) = logar e IGNORAR, senão o agente dispara pra resposta dele mesmo.
- Debounce curto (60s) só no disparo INICIAL: coalesce rajada de mensagens sem perder o gatilho.
- Log JSONL: `ts`, `evento`, `disparo` (sim/debounce/retrigger/ignorado) + contexto disponível no payload (conversationId, participantName, msg truncada em ~60 chars).

## Pitfalls (todos de caso real)
1. **`hermes cron run` disparado durante um run em curso NÃO roda quando o run termina**: ele cai no PRÓXIMO tick do scheduler (num job every 15m = até 15 min depois). E o run em curso pode já ter lido o inbox sem ver a mensagem nova que acabou de chegar. Caso real (13/09): resposta saiu 18 min depois da mensagem. **Fix: retrigger garantido** com `threading.Timer(~150s)` que chama `hermes cron run` de NOVO, fora do debounce; o dedupe do agente (arquivo de estado) evita resposta duplicada; run extra sem novidade = [SILENT], inofensivo e barato.
2. **Scheduler resolve scripts por profile**: cron watchdog que relança o receiver precisa do `profile:` igual à pasta onde o script mora (`~/.hermes/profiles/<p>/scripts/`). O job do agente pode morar em outro profile que o receiver (o `hermes cron run` sem `-p` usa o profile do processo que dispara).
3. **Relançar receiver = processo longevo**: terminal foreground com setsid/nohup é barrado pelo Hermes; usar `terminal(background=true)`. E criar um vigia cron (script-only, `no_agent=true`, a cada 15-30min): confere `GET /health` do receiver, relança se cair, silencioso quando saudável.
4. **Latência REAL nunca vem do autorrelato do agente**: medir `createdAt` de cada mensagem na API do provedor vs horário da resposta, cruzar com o JSONL do receiver e com os runs em `profiles/<p>/cron/output/<job_id>/`. Nome dos arquivos de run = hora de FINALIZAÇÃO, não de início.
5. Payload do provedor pode não trazer todos os campos: logar os que existirem; nome de usuário/conversa no log transforma diagnóstico futuro de "algum evento" em "esta conversa às HH:MM".

## Validação (receita, executada 13/09)
1. POST sintético de `message.received` no receiver (com o token real) → resposta imediata + run do agente em segundos (run extra responde [SILENT] se nada novo).
2. Esperar ~160s e confirmar no JSONL a linha `disparo: retrigger` (o Timer disparou).
3. Medir latência ponta a ponta no provedor: mensagem → resposta. Alvo: 1-3 min com agente livre.

## Instância em produção (cuidar.vc, Agente 7 Community)
- Receiver: `cuidarvc/squad/community/hook-zernio.py` (porta 8805), log `hook-log.jsonl`, job `b1c27fe585a1`, vigia cron `d58dd88fe8d5` (profile cmo, script `vigia-hook-zernio.sh`). Rota Caddy `/hook/*`.
- Assinatura na Zernio: `POST /v1/accounts/{accountId}/webhook-subscription` com body `name`/`url`/`secret`(HMAC-SHA256)/`events`. Eventos úteis: `message.received`, `conversation.started`, `comment.received`, `lead.received`, `review.new`, `referral.received`.
- Caso completo com timeline de evidências e números medidos: `references/receiver-zernio-13-09.md`.

## Sobre this skill vs community-cuidarvc
O guard de profile barra patch da skill `community-cuidarvc` (symlink do cuidar) a partir do cmo; esta skill nativa cobre a parte de gatilho. Na próxima passe de curadoria com file tools cross-profile: mover esta seção pra lá (ou vice-versa) e deixar um ponteiro.