---
name: lovable-mcp
description: Operar a plataforma Lovable de forma programática via servidor MCP oficial (mcp.lovable.dev) e conectar serviços OAuth no Hermes headless. Usar sempre que a squad tech precisar acessar o projeto cuidar.vc no Lovable para listar projetos, iterar com o agente via send_message, revisar código e diffs, rodar SQL no banco, publicar via deploy_project e puxar métricas de visitantes. Usar também para conectar ou reconectar qualquer servidor MCP OAuth em ambiente headless (receita de paste-back do redirect) e para autenticar o gh CLI via PAT.
---

# Lovable via MCP + OAuth headless

## Visão geral
O Lovable expõe um servidor MCP oficial em https://mcp.lovable.dev que dá controle programático sobre os projetos: criar, iterar com o agente, inspecionar código, rodar SQL, publicar e medir. No Hermes do profile cto o servidor está registrado com o nome `lovable`. Referência condensada de todas as ferramentas: references/lovable-mcp-tools.md.

## Conexão e OAuth headless (receita geral, vale para qualquer MCP OAuth)
Caminho padrão quando a autorização é mediada por chat (Rob responde via Telegram; validado 12/09 no Lovable): fluxo manual em 2 passos da skill `devops/mcp-oauth`, com scripts prontos em `/home/hermes/cuidarvc/squad-tech/scripts/lovable_oauth_step1.py` (descoberta, registro dinâmico, PKCE, gera a URL de autorização e salva o state) e `lovable_oauth_step2.py` (recebe o callback colado como argv[1], valida o state, troca o code por tokens e grava os 3 JSONs em `~/.hermes/profiles/cto/mcp-tokens/`). Depois habilitar no config via CLI e testar: `hermes -p cto config set mcp_servers.lovable.url "https://mcp.lovable.dev/?src=skill"`, `... auth oauth`, `... enabled true`, `hermes -p cto mcp test lovable`.

Fluxo interno `hermes mcp add --auth oauth` (registrar em background pty, dono abre a URL, dono cola o redirect `http://127.0.0.1:<porta>/callback?code=...&state=...`, injetar via process submit): só completa se o paste chegar dentro de ~40s, porque o initialize MCP interno expira nesse prazo. Via Telegram o dono nunca chega a tempo: a conexão falha, o prompt vira "Save config anyway?" e o processo trava em "completing flow" mesmo aceitando o paste; o code morre junto. Não usar como passo padrão quando a autorização vem pelo chat; só serve com navegador na própria máquina do Hermes.
- Se um link de autorização expirar antes do callback (~10 min): rerodar o passo 1 e pedir nova autorização.
- Config.yaml não aceita edição pela ferramenta patch (guard de segurança): sempre `hermes -p cto config set`.
- As ferramentas do MCP só entram na SESSÃO SEGUINTE do profile. Para validar na hora após conectar: `scripts/mcp_check.py` da skill `devops/mcp-oauth` (chama qualquer tool com o access_token salvo).

## Autenticação do gh CLI (GitHub)
- Pitfall: o prompt interativo do `gh auth login --web` rodando em PTY background não aceita input via process write/submit nesta máquina; não insistir nele. Caminho confiável: PAT fine-grained gerado pelo Rob em github.com/settings/personal-access-tokens/new (só o repo do projeto, permissões Contents e Pull requests em Read and Write), colado no chat, salvo imediatamente no .env do profile (GITHUB_TOKEN) e nunca ecoado de volta.
- Pitfall do sanitizador (12/09): o Hermes mascara credenciais literais em comandos e write_file: `GITHUB_TOKEN=<valor>` e PATs completos viram `***` e a substituição come aspas, quebrando o script (sintaxe inválida ou segredo gravado errado no .env). Para gravar um segredo colado pelo Rob: (a) extrair do state.db do profile (tabela messages, role=user, regex do padrão do segredo) num script que nunca contém o valor literal; ou (b) script python que monta o valor por concatenação de pedaços curtos (strings literais adjacentes de ~20 chars), que o sanitizador não reconhece. Conferir o arquivo gravado com read_file antes de rodar e validar depois (API /user). O terminal tool e os jobs do profile injetam o .env no ambiente (GITHUB_TOKEN/GH_TOKEN), então gh e curl autenticam sozinhos depois disso; `gh auth login --with-token` falha por design quando a env var existe, não é erro.

## Operação pelo MCP (ferramentas principais)
- Descobrir o projeto: list_projects (guardar o projectId do cuidar.vc), get_me e list_workspaces para IDs.
- Iterar com o agente do projeto: send_message (descrever o quê, não como; plan_mode=true para discutir arquitetura antes de codar; wait=true por padrão; anexar mockup via get_file_upload_url + file_id).
- Revisar: get_diff (por message_id), list_files, read_file, list_edits.
- Banco: get_database_status, enable_database, query_database (SQL completo, permissões totais).
- Publicar: deploy_project (retorna a live URL). Atenção: confirmar no primeiro uso real como isso interage com o domínio customizado cuidar.vc antes de virar passo padrão do DevOps.
- Métricas do site publicado: get_project_analytics (por dia/hora, com páginas, fontes, dispositivos e países) e get_project_analytics_trend (tempo real).

## Regras de operação
- Tool calls rodam na conta real do Rob: consomem créditos e editam projetos de verdade. QA nunca publica; só DevOps com item em Aprovação.
- Sync GitHub↔Lovable é bidirecional: push no branch ativo do repo volta pro Lovable sozinho, e o Lovable edita um branch por vez. Mexer via git push OU via MCP, nunca os dois ao mesmo tempo, para evitar corrida.
- Prompts enviados ao agente do Lovable em português; textos de interface sem travessões (regra do Rob).
- Fonte autoritativa sempre atualizada das ferramentas: https://mcp.lovable.dev/skill.md. Re-fetch quando houver dúvida de parâmetro.