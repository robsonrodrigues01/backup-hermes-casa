cuidar.vc (set/2026): em preparação para lançamento público (prazo: o quanto antes). Site no ar, código no GitHub, hospedado no Lovable, codado com Claude Code. Instagram @cuidarvc.br. Público-alvo: cuidadores e idosos + demais profissionais do hall (babás, enfermeiros). Atuação: BRASIL TODO (11/09), sem praça regional. Tom acolhedor e emocional. Claudete produz conteúdo para Rob publicar.
§
TECH (11/09): CTO bot t.me/CTOcuidarvcbot profile "cto" NO AR; jobs cto: Dev 12h UTC, QA 18h, DevOps 20h, status 07h15 BSB (IDs no PENDENTES.md); quadro squad-tech/TAREFAS.md; repo robsoncoffy/cuidarvc conectado 14/09 (token push ok). CRON (14/09): jobs do bot CMO vivem no scheduler do profile cmo (mesmo Profile: cuidar); rodar `hermes -p cmo cron list` antes de declarar job sumido.
§
Piapi auth (10/09): chave 64 hex exige prefixo sk- (sem ele: 401). Base https://api.piapi.ai; só /v1/chat/completions confirmado OpenAI-compat; /v1/task/* = 404.
§
MCP no Hermes: venv exige mcp==1.26.0 exato (novo renomeia streamablehttp_client; fix: uv pip install --python ~/.local/share/uv/tools/hermes-agent/bin/python mcp==1.26.0). krea-ai HABILITADO (34 ferramentas; key MCP_KREA_AI_API_KEY no .env; secrets via save_env_value).
§
Canva conectado (10-11/09): app OC-AaCNd93weRRM (CANVA_* no .env), OAuth+PKCE manual, redirect 127.0.0.1:3001/oauth-redirect, tokens+refresh em cuidarvc/squad/canva-tokens.json, 8 escopos OK; canva_publish.py operacional = entrega padrão de artes (compose_card → asset → design editável → export PNG).
§
Telegram DM do Rob = chat_id 8944451892 (TELEGRAM_HOME_CHANNEL setado no perfil cuidar 11/09; usar send_message com esse canal).
§
Apify MCP ok (14/09): server mcp.apify.com, OAuth token em profiles/cuidar/mcp-tokens/apify.json (scope full_api_access, expira ~1h com refresh automático do Hermes). Actor apify/instagram-profile-scraper: input exige resultsType:"posts" (default "details" devolve só perfil), waitSecs máx 45 no call-actor, datasetId vem aninhado em storages.datasets.default.id. @cuidadoresdovalejc não existe no Instagram (not_found em 2 runs 14/09).