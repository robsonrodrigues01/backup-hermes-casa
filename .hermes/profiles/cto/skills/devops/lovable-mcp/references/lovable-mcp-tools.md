# Lovable MCP: referência condensada de ferramentas

Fonte autoritativa sempre atualizada: https://mcp.lovable.dev/skill.md (re-fetch quando em dúvida; código aberto no repo lovablelabs/mcp).
Comandos Hermes: conectar `hermes -p cto mcp add lovable --url "https://mcp.lovable.dev/?src=skill" --auth oauth`; re-autenticar `hermes -p cto mcp login lovable`; testar `hermes -p cto mcp test lovable`.
Escopos OAuth pedidos: offline, projects:read, projects:write, workspaces:read, workspaces:write.
Atenção: tool calls rodam na conta real, consomem créditos, editam projetos de verdade e query_database usa permissões completas do banco.

## Identidade
- get_me: perfil autenticado e workspaces.
- list_workspaces: chamar primeiro para IDs de workspace; paginar com pagination.next_cursor.
- get_workspace: plano, créditos, configurações.

## Projetos
- list_projects: workspace_id é OBRIGATÓRIO (string; erro -32602 sem ele). Pegar o id antes em list_workspaces. Busca e filtros (query, visibility, publish_status, folder_id, viewed_by_me) com cursor; projetos vêm em data[].
- get_project: detalhes e screenshot do estado atual.
- create_project: workspace_id opcional, initial_message (vira a primeira mensagem do builder), files?, template_project_id?, design_systems?, wait?, timeout_seconds?.
- deploy_project: publica em produção, retorna live URL.
- set_project_visibility: draft, private ou public.
- move_projects_to_folder e set_folder_visibility: organização em pastas (até 30 por chamada).
- remix_project: fork de projeto para outro workspace.

## Iteração com o agente do projeto
- send_message: project_id, message (1 a 100k chars), wait (default true), timeout_seconds?, plan_mode? (true para discutir arquitetura antes de codar), files?.
- get_message: poll depois de send_message com wait=false ou timeout; passar message_id e thread_id retornados.
- list_messages: descobre message_ids quando só se tem o projeto; paginação por cursor.
- Dedup: create_project e send_message detectam retry idêntico (~2 min, estendido enquanto wait está em voo) e devolvem deduplicated=true com o resultado original. Se o original ainda está em voo, o erro manda pollar via list_messages + get_message em vez de reenviar.

## Inspeção de código
- get_diff: diff unificado por message_id ou entre commits (sha, base_sha).
- list_files: página de arquivos num git ref; paginar com next_cursor.
- read_file: conteúdo de um arquivo num ref.
- list_edits: histórico de edições com SHAs; cursor aceita before como timestamp ISO 8601.

## Knowledge (instruções persistentes do agente)
- get_workspace_knowledge / set_workspace_knowledge: valem para todos os projetos do workspace.
- get_project_knowledge / set_project_knowledge: valem para um projeto. Máx 10k chars; sempre ler antes de setar para não apagar conteúdo existente.
Exemplos úteis: identidade visual (cores da marca), convenções (Supabase para auth e banco), regras de texto (PT-BR, sem travessões, tom acolhedor).

## Banco (PostgreSQL via Supabase)
- get_database_status: verifica se há banco provisionado.
- enable_database: provisiona (30 a 60 segundos, único).
- query_database: SQL direto (SELECT, INSERT, UPDATE, DELETE, DDL).

## Upload de arquivos
- get_file_upload_url (file_name, content_type?) devolve upload_url e file_id; PUT do conteúdo no upload_url; passar file_id em files de send_message ou create_project. Usar para mockups, screenshots e wireframes.

## Analytics (projeto publicado)
- get_project_analytics: start_date e end_date em RFC 3339, granularity hourly ou daily; visitantes com quebra por página, fonte, dispositivo e país.
- get_project_analytics_trend: visitantes em tempo real e tendência de 30 minutos.

## Templates e design systems
- list_template_projects e list_design_systems (workspace_id).

## Mensagens eficazes para o agente do projeto
- Descrever o quê, não como ("adicionar página de configurações com edição de perfil e troca de senha" em vez de "criar src/pages/Settings.tsx").
- Ser específico sobre UI ("layout de cards com navegação lateral").
- Mencionar comportamento esperado ("ao salvar, mostrar toast de sucesso e redirecionar").
- plan_mode=true para features complexas; anexar mockup via file_id.

## Pagamentos nativos (Paddle ou Stripe)
Pedir ao agente que adicione pagamentos; ele cria contas, produtos, checkout e webhooks sozinho. Requer plano Pro+ e Lovable Cloud; auth recomendada. Um provider por projeto; testar com cartão 4242 4242 4242 4242; não criar webhooks manualmente (Lovable registra). Relevante quando o cuidar.vc ativar o pagamento seguro entre famílias e profissionais.