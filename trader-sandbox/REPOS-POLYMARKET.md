# Repos Polymarket — digest (fonte: artigo Coding Nexus bloqueado na rede; absorção via GitHub API em 15/09/2026)

## Os 3 mandados pelo Rob
### 1. pmxt-dev/pmxt — ★2151 | TypeScript | MIT | ativo (push 2026-07)
- "CCXT para mercados de previsão": API unificada p/ Polymarket, Kalshi, Limitless, Opinion etc.
- 2 modos: (a) API hospedada deles → CUSTÓDIA NA MÃO DELES (linha vermelha da casa); (b) self-host → chaves ficam com a gente, mas continua sendo zona-dinheiro-real.
- ⚠️ 1.297 issues abertas (projeto jovem, jan/2026). Trading via SDK hoje: Polymarket/Opinion/Limitless.
- Uso pra casa: **leitura de mercado** (preços/orderbook Polymarket) = zona livre.

### 2. ent0n29/polybot — ★1011 | Java 21 | sem licença visível | parado desde 2026-02
- Infra completa de HFT p/ Polymarket: execução (paper e live), market making, ingestion p/ ClickHouse, análise e "replication scoring" (espelhar estratégia de traders reais).
- Stack pesada: microserviços Spring Boot + Docker + Redpanda + Grafana + Python p/ pesquisa.
- Valor pra casa: conceitos do `research/` (replicação, snapshots) — não rodar o peso todo no servidor.
- ⚠️ sem licença = não usar código sem checar; stale 6+ meses.

### 3. evan-kolberg/prediction-market-backtesting — ★1202 | Python 3.12 + Rust | mixed MIT/LGPL | push 2026-05
- Backtesting de estratégias de Polymarket sobre NautilusTrader. Adapters próprios da exchange.
- v4.1-alpha: plumbing LIVE sandbox p/ mercados BTC 5min da Polymarket (exatamente ciclo curto que interessa).
- Métricas de saída: equity, P&L, drawdown, Sharpe, **Brier advantage**.
- ⚠️ alpha, pesado (compila Rust), só Polymarket today. É o mais útil p/ validar estratégia ANTES de arriscar.

## Outros achados no scan topic:polymarket (resto provável da lista do artigo)
- Jon-Becker/prediction-market-analysis ★3832 — framework de coleta/análise de pred. markets
- alsk1992/CloddsBot ★2724 — agente de trading autônomo multi-market
- sterlingcrispin/nothing-ever-happens ★986 — bot que compra "No" em mercados não-esportivos
- kuestcom/prediction-market ★1095 — own-market (não útil pra gente)

## Fonte dos preços hoje (constraint da casa)
- Kraken: API pública de leitura OK (já usada no sandbox).
- Polymarket: leitura via CLOB API pública (clob.polymarket.com) — sem chave p/ dados; ordem = zona só Rob.
