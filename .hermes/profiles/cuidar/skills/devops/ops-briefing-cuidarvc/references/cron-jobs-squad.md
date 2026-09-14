# Cron jobs do mundo cuidar.vc (snapshot 14/09/2026)

⚠️ Existem DOIS schedulers: profile **cuidar** (`hermes -p cuidar cron list`) e profile **cmo** (`hermes -p cmo cron list`). Os jobs criados pelo bot do CMO (Community, vigias, Radar do CMO) vivem no scheduler **cmo** mesmo rodando com `Profile: cuidar` e NÃO aparecem na listagem do cuidar. Nunca declarar job "sumido" sem checar os dois (falso alarme real em 14/09). Perfis cmo/cto também têm jobs próprios (briefing do CMO, Dev/QA/DevOps do CTO) — não confundir. Antes de afirmar estado de job, reconfirmar contra o jobs.json real; este mapa serve de atalho, não de verdade eterna.

## Scheduler profile cuidar (deliver=local, exceto onde indicado)

| Job ID | Quem | Schedule UTC | BRT | O que checar no briefing |
|---|---|---|---|---|
| `9587d40be7e7` | Agente 1 Planejador | 0 8,14,20 | 05h/11h/17h | Pauta do dia gerada |
| `7bd73f39264b` | Agente 2 Copywriter | 0 9 | 06h | Copy do dia em `squad/copys/` |
| `7ab152d68c07` | Agente 3 Artes | 0 10 | 07h | Arte em `squad/artes/`, Canva |
| `9e68702df006` | Agente 4 QC | 0 11 | 08h | Veredito APROVADO/REJEITADO em `squad/qc/qc-AAAA-MM-DD.md` |
| `b9b585468254` | retrabalho-QC (gatilho, 14/09) | 30 11 | 08h30 | Se o QC rejeitou: redo do produtor disparado. Anti-duplicidade: comparar last_run_at do produtor vs 11h UTC (plantão do CMO pode já ter feito) |
| `d2fd43a7edcd` | Agente 5 Agendador | 0 12 | 09h | Post agendado no Zernio (multirede IG+FB); status `partial`/`failed` = reportar |
| `30b5228c9aea` | Agente 6 Métricas | 0 13 | 10h | Relatório de KPIs |
| `74a8ba3fcce7` | reacao-metricas (gatilho, 14/09) | 30 13 | 10h30 | `squad/metricas/aprendizados-AAAA-MM-DD.md` com seção PARA O PLANEJADOR (consumida pelo Planejador das 14h UTC); sugestão de impulsionamento vira SUGESTÃO no PENDENTES |
| `8c20e6866ceb` | CMO briefing 2x/dia (bot) | 0 10,21 | 07h/18h | Briefing entregue no bot (confirmar ok:true + message_id) |
| `bcb204d240b2` | Blog/SEO semanal | segundas 12h | segundas 09h | Artigo/post SEO |
| `3f2452a1b3fd` | Radar de tendências (14/09, deliver=origin) | segundas 12h30 | segundas 09h30 | Google Trends via Apify (12 termos-chave): top 5 buscas em alta + 3 pautas + alerta breakout; insumo p/ Planejador e Blog/SEO. 1º run 21/09 |
| `b66e74eee96a` | watchdog-site (14/09, no_agent script-only) | every 15m | — | Silêncio quando site OK; alerta no DM após 2 falhas seguidas + aviso de recuperação. Briefing NÃO duplica (ver `references/watchdog-site.md`) |
| `fb802f948cba` | briefing-matinal (Claudete) | 0 12 | 09h | É este runbook |

## Scheduler profile CMO (varredura 14/09; NÃO aparecem em `hermes -p cuidar cron list`)

- `b1c27fe585a1` Agente 7 Community, every 15m (desde 12/09): DMs/comentários IG+FB, deliver local; escalações em `squad/community/escalacoes.md`.
- `fbee0838b577` vigia do dashboard: relança o servidor do dashboard (porta 8800) se cair.
- `d58dd88fe8d5` vigia do webhook Zernio: monitora o receiver `community/hook-zernio.py`.
- `a15db537de2d` Radar do CMO (não confundir com o radar-trends `3f2452a1b3fd` do scheduler cuidar).

## Pausados (não reportar como falha)

- `be28f3036ccf` Pauta Diária IG (0 11 UTC): pausado 11/09 (duplicava a pauta da squad). Retomar: `hermes cron resume be28f3036ccf`.
- `9b7420a209aa` CMO orquestrador antigo (0 10,21 UTC): substituído pelo bot próprio. Retomar: `hermes cron resume 9b7420a209aa`.
- Snapshot 12/09 citava `42c6aa7c07c4` como vigia do dashboard no scheduler cuidar; não apareceu na varredura 14/09 dos dois schedulers (substituído pelo vigia `fbee0838b577` do cmo) — conferir antes de mexer.

## Outputs

Cada run grava em `~/.hermes/profiles/cuidar/cron/output/<job_id>/AAAA-MM-DD_HH-MM-SS.md`. O veredito/resultado fica na seção `## Response` no fim do arquivo (o começo embute skill+prompt, dezenas de KB).
