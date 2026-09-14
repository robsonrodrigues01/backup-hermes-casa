---
name: ops-briefing-cuidarvc
description: Runbook do briefing operacional diário do cuidar.vc (cron "briefing-matinal" do profile cuidar, 12h UTC = 09h BRT) e de qualquer pedido de status tipo "como está a máquina?", "o que tá em aberto?", "prazos?". Saúde dos serviços Hermes do profile cuidar (gateway + Headroom), leitura da fila (PENDENTES.md + MAPA.md), checagem de estado dos jobs da squad, atualização do quadro e relatório máx. 12 linhas.
---

# Ops briefing cuidar.vc

Rotina diária de operações do mundo cuidar.vc (Claudete). Meta em cada passada: máquina sadia, fila em dia, Rob informado em ≤12 linhas, PENDENTES.md refletindo o estado real.

## Passos (ordem fixa)

1. **Saúde da máquina** (profile cuidar):
   ```
   export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus
   systemctl --user is-active hermes-gateway-cuidar.service
   curl -s -o /dev/null -w "%{http_code}" --max-time 10 http://127.0.0.1:8789/readyz
   ```
   - Gateway `active` + readyz `200` = ok, seguir.
   - Headroom morto → `systemctl --user restart hermes-headroom-cuidar.service` e re-testar (pode reiniciar sozinha).
   - Gateway morto → NÃO reiniciar sozinha: registrar PRECISA DO ROB no relatório.
   - Reparo falhar → `journalctl --user -u <unidade> -n 20` e anotar a causa no relatório.

2. **Fila**: ler `/home/hermes/cuidarvc/PENDENTES.md` e `/home/hermes/cuidarvc/MAPA.md` (NÃO ficam em ~; se moveram, `search_files` com pattern `PENDENTES.md`). Anotar prazos de hoje/amanhã no fuso `America/Sao_Paulo`.

3. **Estado dos jobs da squad**: verificar se os agentes que rodam antes do briefing (QC 11h UTC, etc.) rodaram e MUDARAM estado — é isso que faz o briefing ter valor. Mapa de job IDs, horários e o que checar em cada um: `references/cron-jobs-squad.md`. Ao ler um output de job, ver pegadinha "output de job é gordo" abaixo.

4. **Atualizar PENDENTES.md** se algo mudou de estado (QC aprovou/rejeitou, post agendado, serviço reparado): atualizar a linha `Atualizado:` do cabeçalho + o item correspondente. O arquivo é a fonte da verdade; memória falha.

5. **Relatório final** (máx. 12 linhas, PT-BR, sem preambulo/despedida):
   - `Máquina:` status ou causa+ação
   - `Prazos (BRT):` hoje/amanhã
   - `Fila:` máx. 3 itens
   - `Precisa do Rob:` ou "nada"
   - Última linha `Próximo:` 1 ação concreta do dia
   - Em cron: `[SILENT]` só se NADA de novo; nunca combinar [SILENT] com conteúdo.

## Pegadinhas (aprendidas em runs reais)

- **Tirith bloqueia subshell aninhado no terminal**: loop `for` com `$(ls ...)` dentro (ex.: achar o arquivo mais recente de um diretório) é bloqueado com "Nested executable body could not be resolved" e o comando INTEIRO morre. Não insistir no mesmo formato: listar com `search_files` (target=files, pattern `*` ou `2026-09-12*`) e ler o caminho direto com `read_file`, ou escrever comando flat sem substituição aninhada.
- **Output de job é GORDO**: o arquivo `cron/output/<job_id>/...md` embute a skill inteira + prompt (ex.: 36KB) e o veredito/resultado fica na seção `## Response` no FIM. Ler com `offset` alto, ou `search_files` no diretório por `APROVADO|REJEITADO|Response`, em vez de paginar o arquivo todo.
- **Jobs rodam em UTC, prazos são em BRT** (11h UTC = 08h BRT; 12h UTC = 09h BRT). Conferir `TZ=America/Sao_Paulo date` antes de afirmar "hoje/amanhã". Ausência de output no minuto exato do schedule (ex.: Agente 5 às 12h UTC, briefing às 12h UTC) = job em curso, NÃO é falha; checar de novo no próximo fechamento.
- **Gateway morto = PRECISA DO ROB** (nunca reiniciar sozinha); Headroom morto = pode reiniciar. Exato contrario seria destrutivo na hora errada.
- **CMO briefing 8c20e6866ceb dispara às 10h UTC mas demora ~2h**: o arquivo de output é nomeado no FIM do run (~12h08 UTC) e last_run_at só atualiza na conclusão. No briefing das 12h UTC o matinal ainda está em curso (ou acabou de fechar) — NÃO é falha; se precisar, confirme no journal do gateway-cuidar/cmo. Briefing-matinal (12h UTC) e Agente 5 (12h UTC) disparam juntos: o Agente 5 atualiza PENDENTES.md às ~12h04-12h05, o que dispara o aviso "modified by sibling" — reler o cabeçalho antes de gravar e prefixar seu segmento no topo da cadeia.
- PENDENTES.md e MAPA.md vivem em `/home/hermes/cuidarvc/`; outputs de jobs em `~/.hermes/profiles/cuidar/cron/output/`; jobs em `~/.hermes/profiles/cuidar/cron/jobs.json`. Jobs no profile cmo (vigias, Community) têm jobs.json PRÓPRIO em `~/.hermes/profiles/cmo/cron/jobs.json` e o campo de pausa é `state:"paused"`/`enabled:false` (não `paused:true`).

## Régua de decisão
- Nada mudou e tudo saudável → relatório curtíssimo ou [SILENT] (em cron).
- Estado mudou → relatório + PENDENTES.md atualizado no mesmo turno.
- Serviço morto que eu não posso tocar → PRECISA DO ROB, sem tentar "resolver".
