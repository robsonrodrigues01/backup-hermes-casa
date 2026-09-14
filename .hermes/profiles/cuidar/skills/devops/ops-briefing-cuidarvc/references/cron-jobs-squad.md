# Cron jobs do profile cuidar (snapshot 12/09/2026)

Fonte: `~/.hermes/profiles/cuidar/cron/jobs.json`. Perfis `cmo` e `cto` têm os seus PRÓPRIOS jobs.json (briefing do CMO, Dev/QA/DevOps do CTO) — não confundir. Antes de afirmar estado de job, reconfirmar contra o jobs.json real; este mapa serve de atalho, não de verdade eterna.

## Ativos (todos deliver=local, exceto briefing-matinal)

| Job ID | Quem | Schedule UTC | BRT | O que checar no briefing |
|---|---|---|---|---|
| `9587d40be7e7` | Agente 1 Planejador | 0 8,14,20 | 05h/11h/17h | Pauta do dia gerada |
| `7bd73f39264b` | Agente 2 Copywriter | 0 9 | 06h | Copy do dia em `squad/copys/` |
| `7ab152d68c07` | Agente 3 Artes | 0 10 | 07h | Arte em `squad/artes/`, Canva |
| `9e68702df006` | Agente 4 QC | 0 11 | 08h | Veredito APROVADO/REJEITADO em `squad/qc/qc-AAAA-MM-DD.md` |
| `d2fd43a7edcd` | Agente 5 Agendador | 0 12 | 09h | Post agendado no Zernio (multirede IG+FB); status `partial`/`failed` = reportar |
| `30b5228c9aea` | Agente 6 Métricas | 0 13 | 10h | Relatório de KPIs |
| `8c20e6866ceb` | CMO briefing 2x/dia (bot) | 0 10,21 | 07h/18h | Briefing entregue no bot (confirmar ok:true + message_id) |
| `bcb204d240b2` | Blog/SEO semanal | segundas 12h UTC | segundas 09h | Artigo/post SEO |
| `fb802f948cba` | briefing-matinal (Claudete) | 0 12 | 09h | É este runbook |

## Pausados (não reportar como falha)

- `be28f3036ccf` Pauta Diária IG (0 11 UTC): pausado 11/09 (duplicava a pauta da squad). Retomar: `hermes cron resume be28f3036ccf`.
- `9b7420a209aa` CMO orquestrador antigo (0 10,21 UTC): substituído pelo bot próprio. Retomar: `hermes cron resume 9b7420a209aa`.

## Outros jobs citados no PENDENTES (fora do snapshot acima)

- `b1c27fe585a1` Agente 7 Community (a cada 2h, profile cuidar): escalacoes em `squad/community/escalacoes.md`.
- `42c6aa7c07c4` vigia do dashboard (cada 30min): relança o servidor do dashboard (porta 8800) se cair.

## Outputs

Cada run grava em `~/.hermes/profiles/cuidar/cron/output/<job_id>/AAAA-MM-DD_HH-MM-SS.md`. O veredito/resultado fica na seção `## Response` no fim do arquivo (o começo embute skill+prompt, dezenas de KB).
