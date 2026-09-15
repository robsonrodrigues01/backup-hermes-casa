# Caso: AGENTE TRADER — FASE 1 SANDBOX (início 15/09/2026)

Primeiro piloto na forma desta skill. Registro pra reuso — tudo abaixo é do
dia 15/09; re-checar preços, 404s e portas se o assunto voltar depois disto.

## Decisão e gate
- Rob, 15/09: "por enquanto vamos de sandbox" → libera FASE 1 (papel), NÃO
  fase 2. Fase 2 (dinheiro real, carteira separada) = frase nova, com os
  resultados de 7 dias de prova na mesa — "SÓ com novo OK do Rob".
- Trava presa também por produto: Rob mandou doc do Phantom MCP (wallet p/
  agente mover/trocar/perps c/ dinheiro real) → NÃO ativado: conflita c/
  travas (chave de saque, alavancagem, fase errada). Se a fase 2 vier,
  Phantom só como spot 1x/valor pequeno, capacidades de retirada fora.

## Runner
- `~/.hermes/scripts/trader-sandbox.py` + estado JSON junto
  (`/home/hermes/trader-sandbox/state.json`).
- Carteira virtual: US$ 10.000. BTC via Kraken (leitura pública, sem chave).
- Regras de risco (constantes no código): 20% da carteira por operação,
  take profit +1,5%, stop loss -2%, freio diário se perder US$ 150 num dia.
- Prova antes do cron: 2 ticks e 1 relatório gerados À MÃO antes de criar
  os crons (nunca agendar coisa não testada).

## Fontes de dados (estado no dia 15/09 — re-checar)
- Kraken: API pública de preço ✓ (spot efetivo do piloto: ~US$ 77.7k).
- Binance: bloqueada — não usar.
- Polymarket: **integrada por leitura READ-ONLY em 15/09** via SDK oficial
  (`polymarket-client` 0.10.0, venv do sandbox) conforme
  references/polymarket-sdk.md. Probe: `~/.hermes/scripts/pm_probe.py`
  (script filho que imprime JSON {found, title, slug, q, up, down}; o
  runner chama, parseia e grava `pm_history` no state — 24h de snapshots
  Up/Down do horário BTC). Zona livre: leitura, sem chave, sem ordem.

## Crons (derrubados e recriados no próprio dia 15/09)
- `tick 15min` — `*/15 * * * *`, no_agent script silencioso
  (job 961266b37ed7) → `sandbox-tick.sh`: roda tick, RETENTA 1x após 45s
  se falhar, e SÓ fala no chat em COMPRA/FECHA (grep da saída), freio
  diário ligando (alerta 1x por dia, flag em
  `/home/hermes/trader-sandbox/.flags/halt_last`) ou ERRO 2x seguidas;
  silêncio nos demais ticks.
- `relatorio-diario 19h Bsb` — job b15d6543f307, prompt sem agente externo
  que roda o report e entrega no chat: carteira, P&L, posição aberta,
  leitura Polymarket, freios.
- IDs anteriores do dia (c34c40e89140, 9d17f88bd081) ficaram mortos na
  reconfiguração; `cronjob list` clean antes de recriar.
- Prazo de prova: 15 → 22/09 (7 dias). Dia 22, apresentar COM NÚMEROS e
  pedir decisão de fase ao Rob.

## Fuso do cron (calibrado à tarde de 15/09)
A máquina roda UTC, mas o `next_run_at` devolvido pelo create/update do
cronjob é exibido com fuso Bsb (-03:00) e bate com a HORA ESPECIFICADA no
cron (ex.: spec `0 22 * * *` → next_run 22:00-03:00; `0 19` → 19:00-03:00).
REGRA: não converter fuso de cabeça — escolher o schedule e zerar olhando
o `next_run_at` da resposta do create/update: ele deve EXIBIR o horário de
Brasília pretendido. Relatório configurado em `0 19 * * *` = 19h Bsb ✓.

## Como o Rob acompanha (pergunta que ele fez)
1. Relatório diário automático no chat às 19h Bsb ✓
2. Alerta imediato: compra, fechamento com P&L, freio diário, falha 2x ✓
3. Sob demanda: "status" no chat → snapshot na hora.

## PITFALL do ambiente (mordeu o probe de tarde): HOME de sessão/cron
Nesta máquina o `HOME` em sessões do perfil aponta pro home do PERFIL
(`~/.hermes/profiles/trader/home`) → `expanduser('~')` e `~` em glob não
acham o que existe (pm_probe "não achava" o venv que estava lá). REGRA:
script rodando via cron/fallback usa CAMINHO ABSOLUTO
(`/home/hermes/trader-sandbox/...`), nunca `~`.

## Registro no quadro
- PENDENTES.md do perfil trader: fase 1 com feed Polymarket + automação
  marcados ✓ (15/09); relatório decisor 22/09 em aberto; Rob deve /start.
- Push no cofre `backup-hermes-casa` deve LEVAR runner + probe + state
  ANTES do dia 22 (não perder histórico se a máquina morrer no meio).
