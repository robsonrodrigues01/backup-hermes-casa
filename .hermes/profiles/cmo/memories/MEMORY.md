cuidar.vc (set/2026): pré-lançamento público; site no ar no Lovable, código no GitHub.
§
CTO código grande (12/09): NUNCA subagente (estoura ~20 calls, trunca). Receita completa na skill cmo "delegar-codigo-grande" (nativa): brief .md no projeto → claude -p bg+notify (HOME=/home/hermes, caminho absoluto, --add-dir p/ árvores fora do cwd) → verificação própria total (autorrelato não vale; texto de UI = DOM, não screenshot). Episódio dashboard-novo em references/dashboard-novo-12-09.md.
§
Piapi: chave 64 hex exige prefixo sk- (senão 401); base api.piapi.ai, só /v1/chat/completions confirmado.
§
Canva: tokens em squad/canva-tokens.json; canva_publish.py = entrega padrão de artes (detalhes na skill squad-postagens).
§
Telegram DM do Rob = chat_id 8944451892 (TELEGRAM_HOME_CHANNEL no perfil cuidar; send_message com esse canal).
§
Peça especial (14/09): brief → cron edit via python3 → mover artefato antigo ANTES do redo → conferir disco mesmo se run truncar. pypdf: uv run --with pypdf.
§
Padrões CMO: skills externas = destilar em PT-BR em references/ da skill da squad (copy-ig-fb.md e metricas-framework.md hookados no SKILL.md; Rob OK 11/09). Clarify sem resposta ~10min = seguir padrão de baixo risco e registrar em PENDENTES. Path.home() no profile cmo = profiles/cmo/home: usar caminhos absolutos p/ dados do cuidar. Mudar rota no Caddy (admin 127.0.0.1:2019) = barrado pelo security scan: exige OK do Rob.
§
Agente 7 Community = job b1c27fe585a1 (every 15m, scheduler cmo com profile=cuidar; playbook e escalacoes em squad/community/). Gatilho webhook: receiver hook-zernio.py na 8805 + retrigger 150s (13/09, cobre msg que chega durante run); vigia d58dd88fe8d5; latencia medida 1-3 min; detalhes no playbook.
§
Agente 8 Radar (13h UTC, cuidar, a15db537de2d): Apify MCP; painel squad/radar/perfis.json; skill radar-cuidarvc. § Agente 9 Redator Blog (16h UTC, cuidar, 10f502a4aa15): publica DIRETO no site via RPC Supabase, sem revisão; publicar.py injeta CVBLOG_KEY do .env cuidar (instalada 14/09; rotação via squad/blog/instala_cvblog.py stdin); falta SÓ a publishable key REAL (repo/bundle só placeholder mascarado).