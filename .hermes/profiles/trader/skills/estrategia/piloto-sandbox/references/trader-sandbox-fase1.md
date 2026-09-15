# Caso: AGENTE TRADER — FASE 1 SANDBOX (15/09/2026)

Primeiro piloto na forma desta skill. Registro pra reuso — tudo abaixo é do
dia 15/09; re-checar preços, 404s e portas se o assunto voltar depois disto.

## Decisão e gate
- Rob, 15/09: "por enquanto vamos de sandbox" → libera FASE 1 (papel), NÃO
  fase 2. Fase 2 (dinheiro real, carteira separada) = frase nova, com os
  resultados de 7 dias de prova na mesa — "SÓ com novo OK do Rob".

## Runner
- `~/.hermes/scripts/trader-sandbox.py` (~4.8KB) + estado JSON na mesma
  pasta do script.
- Carteira virtual: US$ 10.000. BTC via Kraken (leitura pública, sem chave).
- Regras de risco (constantes no código): 20% da carteira por operação,
  take profit +1,5%, stop loss -2%, freio diário se perder US$ 150 num dia.
- Prova antes do cron: 2 ticks e 1 relatório gerados à mão; BTC lido a
  US$ 77.702 no teste (15/09). Só depois disso os crons foram criados.

## Crons (ids da criação, 15/09)
- `trader-tick` — `*/15 * * * *`, silencioso (job c34c40e89140). Ticks fora
  do horário de relatório não mandam mensagem.
- `trader-relatorio-diario` — `0 12 * * *` UTC = 9h Bsb, no chat do Rob
  (job 9d17f88bd081).
- Prazo de prova: 15 → 22/09 (7 dias úteis). Dia 22, apresentar com números
  e pedir decisão de fase.

## Fontes de dados (estado no dia 15/09 — re-checar)
- Kraken: API pública de preço funcionou ✓ (escolhida).
- Binance: bloqueada/acessível não — não usar sem re-teste.
- Polymarket: 404 na rota testada; ficou pra "depois" no plano, condicional.

## Registro no quadro
- PENDENTES.md ganhou entrada "FASE 1 SANDBOX no ar" (regras + prazo);
  commit no repo `backup-hermes-casa` enviado (PUSH=0, 15/09).
- Plano de 3 fases foi apresentado ao Rob antes; ele só liberou a fase 1.
