---
name: headroom-proxy-rollout
description: >-
  Runbook de operação do proxy Headroom (compressor de contexto) nos perfis
  Hermes desta máquina — 1 proxy por perfil, portas fixas, rollback e smoke
  tests. Use quando for ligar/desligar/diagnosticar o "economizador de
  memória" em qualquer perfil ou criar unidade para um perfil novo.
---

# Headroom proxy por perfil (openai-compatible)

## Arquitetura na casa (2026-09-09, deploy v2)
Unit systemd user `hermes-headroom-<perfil>.service` UNiCE por perfil
(`~/.config/systemd/user/`), todos 127.0.0.1 — se um morre, os outros seguem:

- lab: **8787** (cobaia; workspace default `~/.headroom`)
- default/Claudinho: **8788** (`HEADROOM_WORKSPACE_DIR=/home/hermes/.headroom-default`)
- cuidar/Claudete: **8789** (`.../.headroom-cuidar`)
- era4/Claudemir: **8790** (`.../.headroom-era4`)

Cada unit: `ExecStart=~/headroom-test/venv/bin/headroom proxy --port
<porta> --openai-api-url https://api.vultrinference.com/v1 --no-telemetry` +
`Environment=HEADROOM_WORKSPACE_DIR=...` (estado/stats por bot em
`proxy_savings.json` do próprio dir) + `Restart=always`.

Plumb: `model.base_url: http://127.0.0.1:<porta>/v1` no `config.yaml` do
perfil; backup pré-edição `config.yaml.bak-headroom` → rollback = restaurar +
`systemctl --user restart hermes-gateway-<perfil>`.

## Passo a passo liga-nova-em-perfil
1. `uv pip install --python ~/headroom-test/venv/bin/python "headroom-ai[proxy]"`
   (SÓ uma vez na máquina — sem fastapi o serviço morre com "No module named
   'fastapi'").
2. Escrever unit (veja molde acima) + `systemctl --user daemon-reload &&
   enable --now hermes-headroom-<perfil>`.
3. Bacaq health: `curl http://127.0.0.1:<porta>/readyz` → 200.
4. Editar `base_url` no `config.yaml` (SÓ dentro do bloco `model:` — o bloco
   `providers.vultr` mantém o URL real) + backup antes.
5. Reiniciar gateway: veja pitfalls de drain/restart em `hermes-profiles`
   (agendar o próprio em background; dormir em polling "deactivating").

## Diagnóstico (medidor leigo)
- `curl :<porta>/stats` → `api_requests` conta uso; `best_detail` pega a maior
  leitura comprimida (levard real: `20,541 → 16,072 tokens` ≈ 22%).
- requests curtinhas = `prefix_frozen`, 0% é esperado nelas — o ganho mora em
  payload grande (histórico longo, tool outputs).
- `/stats-history` = parcela durável; `/savings` CLI equivalente.
- Smoke headless: `hermes -p <perfil> chat -q 'ping' -Q --max-turns 2`.
- Molde reutilizável: QUALQUER outro proxy local segue este mesmo padrão
  (unit systemd + base_url localhost + smoke chat).
