# Máquina compartilhada — quem é quem e armadilhas de path (vultr)

Fonte: MAPA.md do perfil (2026-09). 4 agentes Hermes na mesma máquina:

| Agente | Home | Bot | Headroom |
|---|---|---|---|
| default (Claudinho) | ~/.hermes | @claudinhovc_bot | 8788 |
| cuidar (Claudete) | ~/.hermes/profiles/cuidar | @claudetezinhabot | 8789 |
| era4 (Claudemir) | ~/.hermes/profiles/era4 | @Claudemirera4bot | 8790 |
| lab | ~/.hermes/profiles/lab | @bottesteerabot | 8787 |

## Armadilhas de path
- `~/profiles/era4/` existe mas está VAZIO — os dados de verdade são em `~/.hermes/profiles/era4/`.
- `~/cuidarvc/PENDENTES.md` e `~/cuidarvc/MAPA.md` são do mundo cuidar.vc — não usar nos relatórios da era4.
- `~/.hermes/` na raiz = home do perfil default (Claudinho), não meu.
- Em search_files(target='files'), delimitar o `path` para não cair em arquivos de outro mundo.

## Serviços systemd do usuário (perfil era4)
- `hermes-gateway-era4.service` (não reiniciar sozinho em cron) · `hermes-headroom-era4.service` (restart permitido).
- Ativar session bus antes: `export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus`.
- Headroom era4: porta 8790 · `/readyz` esperado 200 · `/stats` e `/stats-history` p/ extrato.
- Plano B do headroom: cópias `config.yaml.bak-headroom` nos homes de cada perfil (voltar base_url e reiniciar).

## Inspecionar jobs agendados do Claudemir
```
python3 -c "
import json
d = json.load(open('/home/hermes/.hermes/profiles/era4/cron/jobs.json'))
jobs = d if isinstance(d, list) else d.get('jobs', d)
for j in jobs:
    print(j.get('id'), '|', j.get('name'), '|', j.get('schedule'), '| paused:', j.get('paused'))
"
```
Jobs ativos em 2026-09: `894915797be6` Caçada de leads semanal (seg 9:00 BRT) · `30d763c56a1b` briefing-matinal (12:00 UTC = 9:00 BRT).

## Credenciais
- TELEGRAM_BOT_TOKEN e chaves de provedor: `.env` de cada perfil — nunca citar valores em relatórios.
- Modelo/rota dos bots: `config.yaml` de cada perfil.
