# Auditoria de estratégia externa antes de integrar ao sandbox (caso oracle-lag-sniper, 15/09/2026)

Classe de coisa: Rob manda um repo de algoritmo de trading ("absorve" / "audita") e
quer saber se o padrão é real antes de qualquer coisa entrar no sandbox. Nunca
tratar "estrelas + READMEs de P&L" como verdade — AUDITAR.

## Fluxo de auditoria (o que funcionou)

1. **Absorver do repo, não do artigo.** Se a fonte é post/artigo bloqueado
   (Medium/Cloudflare), o substituto está na struct do artigo: buscar os repos
   citados via api.github.com (search por tópico `polymarket` etc.) e ler
   README/metadata direto. Ver escada completa em references/polymarket-sdk.md.
2. **Baixar os dados abertos e rodar REGRAS PRÓPRIAS.** No caso: `data/processed/
   btc.csv` (36.419 linhas: tick_ts, market_ts, outcome, volume, token_price,
   oracle_price; 2.219 mercados BTC; dados de FEVEREIRO). Implementar a estratégia
   descrita com código próprio, nunca rodar o deles blindado.
3. **Comparar conta independente vs claim.** Resultado: 1.537 sinais, win rate
   66,4% independente vs 61,5% claimado deles → padrão de lag EXISTIA no dataset.
   EV independente +0.257/entrada. Chamar é: existe ≠ vive hoje (dados 7 meses
   velhos; mercado adapta).
4. **Red flags de supply chain (anotar sempre):** instruções de install apontando
   .whl de OUTRA conta GitHub (Cóia de outra conta = risco de código embutido
   malicioso — se um dia usar, clonar FONTE e auditar, nunca instalar binário);
   0 estrelas com badges estáticos ("195 tests" de imagem = não prova CI);
   P&L printado sem dados abertos que batem.
5. **Veredito por camada:** (a) padrão existe nos dados? (b) vale HOJE? — exige
   prova ao vivo própria (item abaixo). Só depois de (b) sica qualquer conexão
   ao state.json do sandbox, e ainda assim READ-ONLY até OK do Rob.

## Prova ao vivo: rajada curta não fecha tribunal

- 36 amostras x 20s (~12min, detecta mov. ≥0,07% no spot Kraken) → deu 0 rajadas
  num mercado parado de madrugada: NEM CONFIRMA NEM NEGA. Mercado quieto não gera
  evento; piloto curto vira "sem dado", não "sem padrão".
- Ferramenta certa: **vigia silencioso de 24h** (JSONL append `[t, spot, up, dn,
  slug]` a cada tick) + análise por EVENTOS depois; ancora resultado no relatório
  diário. Scripts gerados: `pm_lag_burst.py` (descartável, cumpriu) e
  `pm_lag_watch.py` (vigia, /home/hermes/.hermes/scripts/).
- **Fumaçar o vigia ANTES da janela longa:** rodar com envs mínimos
  (`WATCH_HOURS=0.004 VIGIA_TICK=5` → 3 ticks) e conferir JSONL escrito, aí sim
  lançar o prof de 24h em background com timeout generoso. Generalização da regra
  "prova real antes do agendar": vale pra watcher, não só pro cron.
- Print honesto ao relatar combinação: dizer 0/0 SEM maquiar ("sem dado" ≠
  "padrão morto"), e deixar a decisão futura condicionada ao dado real.

## Ampliação de referência

- Regra virtual e trava de fase → SKILL.md deste grupo (regras da casa).
- Escada de fonte bloqueada → references/polymarket-sdk.md.
