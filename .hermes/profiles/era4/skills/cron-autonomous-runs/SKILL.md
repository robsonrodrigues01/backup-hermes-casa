---
name: cron-autonomous-runs
description: Turnos autônomos agendados (cron) da ERA 4.0 — checagem de saúde (gateway/headroom), revisão da fila PENDENTES/MAPA, atualização de estado e relatório ≤12 linhas PT-BR ou [SILENT].
---

# Turnos autônomos (cron) — ERA 4.0

Dispara quando um cron me coloca sozinho fora de conversa (Rob não está no ar): health-check da máquina, leitura da fila, ajuste de estado e relatório curto.

## Regras de ouro
1. Nada destrutivo. Ação que depende do Rob → registrar "PRECISA DO ROB" e NÃO executar.
2. Sem perguntas: dúvida → padrão seguro + anotação no relatório.
3. Nada novo a relatar → responder exatamente `[SILENT]` (nunca combinar com conteúdo).
4. Mudou algo na fila → atualizar PENDENTES.md na hora (o arquivo é a fonte da verdade, não a memória).
5. Fuso do relatório: America/Sao_Paulo (`TZ=America/Sao_Paulo date`) — o host costuma estar em UTC.

## Procedimento
1. **Saúde** (uma chamada de terminal): `export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus && systemctl --user is-active hermes-gateway-era4.service; systemctl --user is-active hermes-headroom-era4.service`
2. **Readyz do Headroom** (esperado 200): `curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://127.0.0.1:8790/readyz`
3. **Reparo**: headroom morto → `systemctl --user restart hermes-headroom-era4.service` + re-teste do readyz. Gateway morto → NÃO reiniciar sozinho; registrar "PRECISA DO ROB". Reparo falhar → `journalctl --user -u <unidade> -n 20` e anotar a causa.
4. **Fila**: ler `~/.hermes/profiles/era4/PENDENTES.md` e `MAPA.md`. Extrair prazos de hoje/amanhã e itens aguardando o Rob.
5. **Jobs agendados**: conferir `~/.hermes/profiles/era4/cron/jobs.json` (id, nome, schedule, paused) — comando pronto em `references/maquina-compartilhada.md`.
6. **Relatório final** (entrega automática ao destino do cron): ≤12 linhas PT-BR — `Maquina / Prazos / Fila (≤3) / Precisa do Rob` + última linha `Proximo: 1 ação de hoje`. Sem preâmbulo nem despedida.

## Pitfalls (run real de 2026-09-13)
- Ferramentas que exigem aprovador ficam indisponíveis em run agendada: se uma chamada voltar bloqueada (ex.: execute_code sem moderador), refaça com ferramenta direta no mesmo turno (terminal/read_file/search_files) — nunca termine o turno sem produzir o relatório.
- Máquina compartilhada por 4 agentes Hermes: NÃO ler os PENDENTES/MAPA de outro mundo. Os meus dados vivem em `~/.hermes/profiles/era4/`; armadilhas de path e mapa por agente em `references/maquina-compartilhada.md`.
