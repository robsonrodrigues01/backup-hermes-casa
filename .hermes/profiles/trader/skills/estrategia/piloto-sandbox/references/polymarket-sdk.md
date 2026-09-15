# Polymarket read-only no sandbox — polymarket-client (estado: 15/09/2026)

## Pacote e onde vive
- `polymarket-client` 0.10.0 = SDK **OFICIAL** da Polymarket (github.com/Polymarket/py-sdk, PyPI desde 2026-07-22, MIT). No venv: `~/trader-sandbox/.venv` (python 3.12).
- Instalar/atualizar: `cd ~/trader-sandbox && .venv/bin/pip install polymarket-client`

## Padrão de leitura (zona livre, ZERO chave)
- `from polymarket import PublicClient; c = PublicClient()` — 58 métodos públicos. `SecureClient*` = ordem/conta → zona só-Rob; NÃO inicializar sem ele.
- Eventos ativos: `c.list_events(tag_slug="crypto", order="volume24hr").first_page().items` → `ev.title` / `ev.slug` / `ev.markets`.
- Outcome do mercado: `m.outcomes` é objeto `MarketOutcomes` com atributos `.yes` / `.no` (`label` Up/Down, `.token_id`, `.price`).
  - NÃO usar `m.tokens` (não existe) nem iterar `m.outcomes` como sequência.
- Preço/book: `c.get_midpoint(token_id=...)` → Decimal; `c.get_last_trade_price(token_id=...)`; `c.get_order_book(token_id=...)` → `.bids`/`.asks` (cada item `.price`/`.size`). Passar **token_id** (id longo ~78 dígitos), não condition_id.
- Hourly recém-aberta: book nasce ralo (bid 0.01 / ask 0.99) — não ler como ineficiência.

## PITFALL: paginação do `c.search()` (bug do SDK 0.10.0)
- `has_more` nunca cessa → itera até page 101 → `RequestRejectedError: query argument "page": must be less than or equal to 100`.
- Contorno: chamar `.first_page()` em `search` e tratar uma página por vez; nunca `list(paginator)` de search. Paginadores de `list_*` usam cursor (não página) — até agora OK.
- Ação pendente: abrir issue no Polymarket/py-sdk; re-testar quando sair versão nova.

## Spot paralelo
- Kraken: `https://api.kraken.com/0/public/Ticker?pair=XBTUSD` (público, sem chave) — foi a fonte efetiva de BTC/USD no piloto.

## Quando a fonte de estudo vem bloqueada (escada testada 15/09)
Desta rede: medium.com/Cloudflare bloqueou browser, curl, `/p/<id>?format=json`, freedium (DNS fail), DDG/Bing HTML, archive.ph; archive.org/save → HTTP 500; r.jina.ai → AuthenticationRequiredError (exige chave). O que FUNCIONOU:
1. RSS da publicação: `medium.com/feed/<publicação>` → slugs/IDs dos posts (e confirma que o post existe).
2. api.github.com: totalmente aberto — artigos de "repos pra X" têm a SUBSTÂNCIA no repositório: fetch README/metadata direto por API e absorver de lá.
3. pypi.org/pypi/<pkg>/json: metadados de pacote (autor oficial? versão? datas?) antes de qualquer install.
Lição: quando a fonte secundária trava, ir à fonte primária que ela aponta.
