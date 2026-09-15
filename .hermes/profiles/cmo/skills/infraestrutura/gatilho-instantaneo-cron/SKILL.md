---
name: gatilho-instantaneo-cron
description: Fazer agente cron do Hermes responder em minutos via webhook de gatilho (receiver HTTP + debounce + retrigger + vigia), em vez de esperar o ciclo do cron. Use quando um lead espera resposta rápida, quando o dono reclamar de demora de resposta de um agente da squad, ou ao montar ou auditar um gatilho instantâneo para qualquer agente cron.
category: infraestrutura
---

# Gatilho instantâneo para agentes cron

Problema de classe: agente cron (ex.: Agente 7 Community, every 15m) deixa um lead esperando até 15min ou mais. Solução: o provedor (ex.: Zernio para inbox de redes sociais) avisa por webhook na hora que chega entrada nova, e um receiver local dispara o job imediatamente. O cron recorrente vira rede de segurança, não caminho principal.

## Quando usar
- Lead/entrada do público precisa de resposta em minutos (DM, comentário, lead, review).
- O dono reclamar "demora muito pra responder": ANTES de mexer, auditar com dados reais (seção Auditoria); a demora reclamada pode ser de antes da cadeia existir.
- Estender o padrão para outro agente cron que precise reagir instantaneamente.

## Arquitetura (5 peças)
1. **Assinatura de webhook no provedor** (Zernio: `POST /v1/accounts/{accountId}/webhook-subscription` com `name`, `url`, `events`; `secret` HMAC opcional). Só eventos de ENTRADA valem gatilho (`message.received`, `comment.received`, `conversation.started`, `lead.received`, `review.new`, `referral.received`); eco das próprias ações (`message.sent`, `webhook.test`) NUNCA dispara.
2. **Receiver HTTP local**: bind 127.0.0.1 (ex.: 8805), token no path validado com `secrets.compare_digest`; exposto publicamente pela rota do Caddy `/hook/<token>` (ver skill `caddy-exposicao-publica`). O token funciona como senha: NUNCA expor o valor real em registro.
3. **Disparo**: receiver chama `hermes cron run <job_id>` em subprocess (`start_new_session=True`, stdout para log de disparo).
4. **Debounce**: máx 1 disparo INICIAL por janela de 60s (coalesce rajadas de mensagens).
5. **Vigia** (watchdog cron `no_agent`, a cada 15min): health check do receiver e relance se cair. Script deve morar no diretório `scripts/` do profile que roda o scheduler. Limitações medidas no vigia de capas do blog (15/09): teto de ~120s por execução (curl -m 90 dentro de retry estoura: dimensionar curl -m 40 + gap 65s, no máximo 2 tentativas + fallback) e stdout VAZIO = entrega silenciosa no chat (é o padrão desejado: o script só fala quando algo quebra); resultado real dos runs em `profiles/<profile>/cron/output/<job_id>/<timestamp>.md` (o `action='run'` retorna antes do fim). A mensagem de "Script not found" cita `~/.hermes/scripts/`, mas o resolvedor real é o `scripts/` DO PROFILE: copiar o arquivo pra lá.

## ⚠️ PITFALL central: cron run durante run em andamento NÃO roda na sequência
`hermes cron run <job>` disparado ENQUANTO um run está em andamento responde "It will run on the next scheduler tick" e, na prática, o job espera o próximo ciclo regular (até 15min). Pior: mensagem que chega NO MEIO de um run pode não ser vista por ele, porque o run já tinha lido o inbox. Caso real: lead esperou 18min por exatamente essa corrida (noite 12→13/09; detalhe em `references/caso-community-13-09.md`).

## ✅ Fix: retrigger garantido
- Todo gatilho agenda uma 2ª chamada do job ~150s depois (`threading.Timer`, `daemon=True`), FORA do debounce.
- Se a 1ª chamada viu tudo, a 2ª não acha novidade e o agente responde `[SILENT]` (barato). Se a mensagem caiu no meio de um run, a 2ª pega.
- Guard: só 1 retrigger pendente por vez (lock + flag), senão timers empilham.
- O caso debounced também agenda retrigger: a 2ª chamada cobre a mensagem que não gerou disparo.
- Resultado medido no cuidar.vc: 1min21s a 2min22s com agente livre; pior caso ~4min.

## Esqueleto do disparo (receita validada em produção)
```python
def _run_hermes():
    agora = time.time()
    with open(DISPARO_FILE, "w") as f: f.write(str(agora))  # atualiza relógio do debounce
    with open(out_log, "w") as fo:
        subprocess.Popen([HERMES, "cron", "run", JOB_ID],
                         stdout=fo, stderr=subprocess.STDOUT, start_new_session=True)

def agenda_retrigger(evento):  # threading.Timer(150, _go), 1 pendente por vez
    ...

def dispara_agente(evento, info):
    agenda_retrigger(evento)          # SEMPRE
    if not pode_disparar(): return "debounce"
    _run_hermes(); return "sim"
```

## Log e operação
- Log jsonl por evento: `ts`, `evento`, `disparo` (sim | debounce | retrigger | ignorado | token_invalido) + ids do payload (conversationId, participantName, trecho da msg) para diagnóstico futuro.
- Health: `GET /health` no receiver; vigia relança sozinho se cair.
- Fuso: logs do receiver são UTC (hora local da VM); BRT = UTC-3. Nunca misturar fusos na mesma análise de linha do tempo.

## Auditoria de latência (provar pro dono com dados reais)
1. Ler a conversa pela API do provedor: `createdAt` de cada mensagem + `direction` (incoming/outgoing).
2. Latência real = createdAt da resposta outgoing menos o da última incoming. Não confiar no relatório do agente: ler de volta a conversa.
3. Cruzar com o log do receiver (quando o gatilho chegou), os logs de disparo e o diretório de output do cron (quando o run rodou).
4. Arquivo de output do cron é nomeado pelo horário do run: reconstruir a linha do tempo pela API, não pelo mtime dos arquivos.

## Caso real cuidar.vc (Agente 7 Community)
Receiver `squad/community/hook-zernio.py` (porta 8805), job `b1c27fe585a1`, vigia cron `d58dd88fe8d5` (profile cmo, script `vigia-hook-zernio.sh`), assinatura Zernio `cuidar-gatilho-community`. Fonte técnica completa da operação do Community: `squad/community/playbook.md` (cabeçalho documenta a cadeia; playbook vence em divergência). Episódio completo da demora e do fix em `references/caso-community-13-09.md`.

## Fusão futura
Consolidar esta skill na `community-cuidarvc` (symlink do profile cuidar) quando a rota de file tools cross_profile abrir: hoje skill_manage do cmo é barrado pelo guard de perfil no edit de skills symlinkadas (12→13/09).
