# Detalhes do login do Claude Code (sessão de 12/09/2026)

## O que aconteceu (transcrição resumida)
- Instalação: `npm install -g` falhou com EACCES. Instalador nativo `curl -fsSL https://claude.ai/install.sh | bash` funcionou: claude 2.1.270 em `/home/hermes/.local/bin/claude`.
- Fluxo 1, `claude setup-token` (PTY background): imprimiu URL de authorize com scope `user:inference`, esperou em "Paste code here if prompted >". O código do Rob colado via `process(action=submit)` FUNCIONOU (o CLI completou o exchange). Mas o token foi impresso no stdout do PTY e o sanitizador do Hermes o converteu em ~92 asterisks no log/poll. Nada em disco: `claude auth status` seguia `loggedIn: false`, o `.claude.json` sem oauthAccount, nenhum `.credentials.json` em lugar nenhum (busca em /home/hermes e ~/.hermes). Processo ficou pendurado até kill. Veredicto: perda total, refazer com outro fluxo.
- Fluxo 2, `claude auth login --claudeai` (PTY background): mesmo esquema de URL + paste, porém grava credenciais em `$HOME/.claude` (esse é o fluxo a usar). Scope estendido: `org:create_apiKey user:profile user:inference user:sessions:claude_code user:mcp_servers user:file_upload`.
- Lição transversal: log de PTY de processo background não existe como arquivo texto em disco no Hermes (busca por "Pastecodehere" em ~/.hermes não achou nada). Output de PTY só existe mascarado para o agente.

## Dados para OAuth manual (fallback, se um dia precisar do token em env var)
- client_id público do Claude Code: `9d1c250a-e61b-44d9-88ed-5944d1962f5e`
- authorize: `https://claude.com/cai/oauth/authorize?code=true&response_type=code&redirect_uri=https%3A%2F%2Fplatform.claude.com%2Foauth%2Fcode%2Fcallback&scope=user%3Ainference&code_challenge=<S256 do verifier>&code_challenge_method=S256&state=<state aleatório>`
- O código devolvido ao usuário vem no formato `CODIGO#STATE`: colar por inteiro.
- Exchange via script (padrão da skill mcp-oauth), gravar `CLAUDE_CODE_OAUTH_TOKEN` no .env sem printar o valor.

## Cuidar.vc: ambiente do repo
- Repo local: `/home/hermes/cuidarvc/repo` (clone de `robsoncoffy/cuidarvc`, privado, 12/09). Commit 596b43d = mesmo SHA do projeto no Lovable (sync bidirecional confirmado).
- CLAUDE.md na raiz do repo (~64k chars) é a fonte autoritativa de convenções: pull antes e push depois; commits do Lovable vêm como `gpt-engineer-app[bot]`; edge functions só publicam via agente Lovable (git push não publica); build é `npm run build` (tsc -b), nunca `npx tsc --noEmit` cru; testar build limpo com `env -i PATH="$PATH" HOME="$HOME" NODE_ENV=production npm run build`; padrões de segurança RLS/REVOKE detalhados lá.
- `.env` versionado é proposital: só `VITE_SUPABASE_PROJECT_ID`, `VITE_SUPABASE_PUBLISHABLE_KEY`, `VITE_SUPABASE_URL` (públicas, embutidas no bundle pelo Vite). A tarefa "remover .env do repo" que chegou a entrar no quadro é alarme falso: cancelar se ainda existir em TAREFAS.md.
- HOME do terminal no profile cto: `/home/hermes` (o home isolado do profile foi apagado em sessão anterior; se PATH/HOME mudarem de novo, conferir onde o `.claude`/`creds` cai antes de logar).
