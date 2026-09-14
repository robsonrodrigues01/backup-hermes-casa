---
name: cron-cuidar-utc-e-jobs
description: Cron da squad cuidar.vc roda em UTC; CMO ativo é 8c20e6866ceb; Community não tem job; decisões do dono em squad/aprovacoes/
metadata: 
  node_type: memory
  type: project
  originSessionId: facabaf3-f4b0-48c0-8f9c-08456be1f502
  modified: 2026-09-12T21:49:22.482Z
---

Fatos conferidos em 12/09/2026 no servidor (relógio em UTC):
- Horários de cron/jobs.json são UTC (0 8,14,20 = 05h/11h/17h BRT). O dashboard.py antigo mostra esses horários como se fossem BRT.
- CMO ativo: job 8c20e6866ceb (0 10,21 UTC). O 9b7420a209aa (listado no dashboard.py antigo) está pausado.
- Agente Community (b1c27fe585a1) não existe no cron; a última atividade dele vem de community/estado.json.
- dashboard.py antigo NÃO tinha endpoint de decisão. O dashboard-novo.py criou squad/aprovacoes/decisoes.jsonl + aprovacoes-AAAA-MM-DD.md; a squad ainda precisa ser instruída a ler de lá.

**Why:** evita repetir horários errados e disparar jobs pausados ou inexistentes.
**How to apply:** ao mexer em painel, cron ou agentes da squad, converter horários de UTC para BRT e usar os ids acima. Ver [[dashboard-novo-cuidarvc]].
