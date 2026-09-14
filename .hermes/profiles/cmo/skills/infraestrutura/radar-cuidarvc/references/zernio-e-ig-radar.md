# Zernio e Instagram: achados do Radar (14/09/2026)

## Zernio: o que foi verificado
- openapi.json com 484 paths revisado em 14/09/2026: TODOS os endpoints de `analytics/instagram*`, `analytics/facebook*`, `inbox`, `posts`, `connect`, `accounts` operam SÓ as contas conectadas (insights, stories, inbox, publicação, limits).
- Existe `/v1/reddit/search` e `/v1/twitter/search` (busca de conteúdo de terceiros), mas NADA equivalente para Instagram ou Facebook de terceiros. Sem listening, sem competitor monitoring, sem perfil de terceiro.
- Conclusão: monitorar posts de perfis de concorrente no IG/FB pela Zernio não existe. Não procurar de novo; se o Rob questionar, este fato está datado aqui e no SKILL.md.

## Rotas IG testadas da VM (14/09/2026, todas barradas)
- API anônima `www.instagram.com/api/v1/users/web_profile_info/?username=X` com User-Agent de browser + header `x-ig-app-id: 936619743392459` → HTTP 401 `{"message":"Please wait a few minutes before you try again.","require_login":true}` (login wall para IP de datacenter).
- `r.jina.ai/https://www.instagram.com/<perfil>/` (proxy de leitura) → Cloudflare 403 "Just a moment".
- `picuki.com/profile/<handle>` (espelho público) → Cloudflare 403.
- Navegador do Hermes (`browser_navigate` em perfil público) → ERR_HTTP_RESPONSE_CODE_FAILURE.
- `publish.instagram.com/oembed/?url=<post>` → conexão nem abre (HTTP 000).
- Se revalidar no futuro, datar o resultado aqui; enquanto isso, partir direto para Apify, cookies ou drops.

## Receita Apify (rota MCP = a escolhida; curl = alternativa)
- **Rota MCP (decisão do Rob 14/09, "vamos pelo apify, aplique o mcp")**: server `apify` no Hermes via `https://mcp.apify.com/` com OAuth. Instalação, OAuth headless (paste-back) e pendências: skill `mcp-servidores-hermes` (`references/apify-instalacao-14-09.md`).
- **Rota curl (alternativa, se o Rob gerar um API token no console)**: `POST https://api.apify.com/v2/acts~apify~instagram-profile-scraper/run-sync-get-dataset-items?token=$APIFY_TOKEN`
- Body (curl): `{"usernames": ["handle1","handle2"], "resultsLimit": 12}`
- Token, quando existir, no env `APIFY_TOKEN` (nunca inline no comando, nunca logar); nunca expor em registro.
- Salvar a resposta bruta em `squad/radar/raw/<handle>/AAAA-MM-DD.json` ANTES de analisar.
- Custo: poucos centavos por perfil/varredura; orçamento 1 varredura/perfil/dia; crédito grátis (~US$ 5/mês) cobre ~8 perfis/dia.
- Dedupe contra `squad/radar/estado.json` (posts já vistos por id/caption curta).

## Opção cookies (só com escolha explícita do Rob)
- Funciona com sessionid da sessão de navegador dele; risco: automação sobre a conta principal pode ser flagrada pela Meta (a conta é o ativo principal do projeto).
- Não implementar sem OK explícito do Rob; na dúvida, oferecer Apify primeiro.

## Decisão RESOLVIDA (14/09)
Clarify enviado com as 3 opções; sem resposta em 10min ficou drops como padrão temporário. Logo depois o Rob respondeu: **Apify, via MCP** ("vamos pelo apify, aplique o mcp"). Integração em andamento (OAuth paste-back com o Rob na data). Drops seguem como intake/fallback permanente; cookies descartados por enquanto. Próximos passos pós-OAuth no SKILL.md do radar-cuidarvc e em `mcp-servidores-hermes`.
