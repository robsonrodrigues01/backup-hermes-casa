# Backup da casa Hermes (Rob)

Cofre PRIVADO. Atualizado automaticamente todo dia às 17h (horário de Brasília)
pelo Claudinho. Última foto completa em anexo: tag `migracao-2026-09-12`.

## O que tem aqui

- `.hermes/` — o cérebro dos 6 agentes (Claudinho, Claudete, Claudemir, cmo, cto, lab):
  memórias, skills, SOUL, cron, histórico, tokens dos bots do Telegram (`.env`)
- `cuidarvc/` — projetos do cuidar.vc (artes, marca, dashboard etc.)
- `tools/`, `headroom-test/`, `scrape-demo/` — ferramentas e experimentos
- `.config/`, `.local/` — configurações pessoais da máquina

O código de produção do cuidar.vc NÃO está aqui: ele já mora no repo
`robsoncoffy/cuidarvc` (é o mesmo, com histórico).

## Como restaurar num servidor novo

1. Instalar Python 3.12 + uv, o resto vem daqui.
2. `hermes import` com o zip da tag `migracao-2026-09-12` (contém tudo, inclusive plugins).
3. Como alternativa sem `hermes import`: clonar ESTE repo dentro de `/home/hermes`
   e copiar `.hermes/` sobrescrevendo, depois religar os gateways por perfil.
4. Religação dos bots: gateway por perfil (ver MAPA). Headroom: skill `local-proxy-headroom`.
5. ATENÇÃO: ligar os gateways da máquina velha ANTES de desligar — 1 token = 1 poller,
   se os dois estiverem no ar dá conflito.

## AVISO: contém segredos

Este repo tem tokens de bots e chaves de API (arquivos `.env`). Regra:
**repo permanece PRIVADO sempre.** Ative 2FA na conta GitHub.
