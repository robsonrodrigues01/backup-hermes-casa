cuidar.vc (set/2026): preparação p/ lançamento público urgente. Site no ar no Lovable, código no GitHub (robsoncoffy/cuidarvc). IG @cuidarvc.br. Público: cuidadores de idosos, babás e enfermeiros. Atuação: BRASIL TODO (11/09). Tom acolhedor e emocional. Claudete produz conteúdo p/ Rob publicar.
§
Squad 24/7 (set/2026): 1-2 posts/dia IG/FB via Zernio (key squad/zernio-key.txt); pipeline Planejador→Copy→Artes (z-image-turbo foto SEM texto + compose_card_glass.py glass oficial + canva_publish.py no Canva)→QC→Agendador→Métricas. CMO tem bot próprio t.me/cmocuidarvcbot (profile "cmo"); briefing 07h/18h BSB máx 12 linhas + 3 artes p/ aprovar; gosto em squad/gosto-do-rob.md; pipeline nunca espera resposta. Rob dorme 00h/acorda 07h: nada urgente 22h+.
§
Piapi (10/09): chave exige prefixo sk- (sem ele 401); base api.piapi.ai; só /v1/chat/completions confirmado; ler doc por provider antes de usar.
§
VPS (14/09): firewall externo só libera 22/80/443; browser_navigate do Hermes roda LOCAL, validar acesso externo via check-host.net. Caddy sem sudo, mas admin API 127.0.0.1:2019 aceita POST /load (vale até restart; backup /tmp/caddy-backup.json). Domínio ac836de9-2434-48c7-aa7b-69c1c7781d84.vultropenclaw.com: /dash → app 8800 (prefixo stripado), /hook → 8805, /painel → server.py 8643 (painel-escritório squad + embed dash CMO, key k injetada server-side, /home/hermes/painel-web). MCP krea ok (mcp==1.26.0 venv uv).
§
Canva conectado (10-11/09): app OC-AaCNd93weRRM (CANVA_* no .env), tokens+refresh em cuidarvc/squad/canva-tokens.json; canva_publish.py = entrega padrão de artes (compose_card → asset → design editável → export PNG).
§
Telegram DM do Rob = chat_id 8944451892 (usar send_message; TELEGRAM_HOME_CHANNEL no perfil cuidar).
§
Lovable MCP+GitHub cto: Lovable 42e995f4-4daf-4261-be2d-7a7472551277, repo robsoncoffy/cuidarvc (detalhes no skill dev-cuidarvc). Claude Code+Opus 5 = coder de TUDO (Rob 15/09: site E artefatos internos, painéis, scripts; agente não escreve código direto): claude -p --dangerously-skip-permissions; auth: claude auth login --claudeai PTY (nunca setup-token). dev-cuidarvc cto é symlink do cuidar: patch exige cross_profile.