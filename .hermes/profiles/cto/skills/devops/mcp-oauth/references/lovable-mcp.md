# Lovable MCP (instância mcp-oauth para o cuidar.vc)

## Endpoints OAuth (descobertos 12/09/2026)
- Servidor MCP: `https://mcp.lovable.dev` (referência viva e sempre atual das ferramentas: `https://mcp.lovable.dev/skill.md`)
- Issuer: `https://lovable.dev/oauth`
- Authorize: `https://lovable.dev/oauth/authorize`
- Token: `https://lovable.dev/oauth/token`
- Registro dinâmico: `https://lovable.dev/oauth/register` (aceita public clients com token_endpoint_auth_method none)
- Protected resource: `https://mcp.lovable.dev/.well-known/oauth-protected-resource`
- AS metadata: `https://lovable.dev/oauth/.well-known/oauth-authorization-server`
- Scopes suportados: offline, openid, email, profile, projects:create/read/write, workspaces:create/read/write. Pedir ao menos: offline projects:read projects:write workspaces:read
- Escopo do acesso: conta INTEIRA do dono no Lovable. Tool calls consomem créditos reais, editam projetos reais, deploy real e query_database roda SQL com permissão total do banco. Tratar com cuidado.

## Setup no profile cto (estado em 12/09/2026)
- Client registrado via dynamic registration: client_id `0d0ad5cff0b047caa1810d354b0bfb6e`, redirect `http://127.0.0.1:53123/callback`, client_name "Hermes Agent CTO cuidar.vc"
- Scripts: `/home/hermes/cuidarvc/squad-tech/scripts/lovable_oauth_step1.py` (descoberta + registro + URL de autorização; salva state em mcp-tokens/lovable-oauth-state.json) e `lovable_oauth_step2.py` (callback URL como argv[1]; valida state, troca code por tokens e grava os 3 JSONs em `~/.hermes/profiles/cto/mcp-tokens/`)
- Pendência imediata: o Rob autoriza e cola a URL de callback no chat; rodar o step2; se o code expirar, rerodar step1 e mandar link novo
- Config a adicionar no config.yaml do profile cto após o step2:
  ```yaml
  mcp_servers:
    lovable:
      url: https://mcp.lovable.dev/?src=skill
      auth: oauth
      enabled: true
  ```
- Teste: `hermes -p cto mcp test lovable` depois `hermes -p cto mcp list`

## Ferramentas MCP que importam para a squad tech
- `list_projects(workspace_id, query?)`: achar o projeto cuidar.vc e o project_id
- `deploy_project(project_id, name?)`: publica em produção e devolve a URL live (é o publish programático)
- `send_message(project_id, message, plan_mode?, wait?)`: manda prompt pro agente do Lovable (mexer no projeto por linguagem natural); plan_mode=true discute arquitetura antes de codar; mensagens de 1 a 100k chars
- `get_project(project_id)`: detalhes + screenshot do estado atual
- `get_diff(project_id, message_id?)`, `list_files`, `read_file(project_id, path, ref)`, `list_edits`: inspecionar código e histórico
- `get_database_status` / `enable_database` / `query_database(project_id, sql)`: SQL direto no Postgres (Supabase) do projeto
- `get_project_analytics(project_id, start_date, end_date, granularity)`: visitantes históricos do site publicado; `get_project_analytics_trend`: tempo real
- `get_project_knowledge` / `set_project_knowledge` (máx 10k chars): instruções persistentes do agente do projeto; SEMPRE ler antes de escrever (replace substitui tudo)
- Retry dedup: `send_message` e `create_project` deduplicam retries idênticos em ~2 min (retorno com `deduplicated: true` é o resultado original, não um novo)
- Mensagens eficazes: descrever o QUÊ (não o como); ser específico sobre UI; plan_mode para features complexas

## Git sync Lovable↔GitHub
- Bidirecional: push no branch ATIVO do repo conectado volta pro Lovable sozinho; o Lovable edita e sincroniza um branch por vez
- Site publicado (cuidar.vc): atualiza via deploy_project, ou botão Publish no painel
- Projeto sem repo conectado: painel do Lovable, Settings, Git sync (o dono conecta; a doc oficial é docs.lovable.dev, seção Git sync)
