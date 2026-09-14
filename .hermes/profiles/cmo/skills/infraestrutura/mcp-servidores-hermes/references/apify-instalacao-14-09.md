# Episódio: instalação do MCP do Apify (14/09/2026)

Contexto: Rob escolheu Apify como fonte do Agente 8 Radar e pediu "aplique o mcp"
(URL exata `https://mcp.apify.com/`, OAuth, instruções de vários clientes; o Hermes
cai no caso "outros clientes HTTP"). Instalação feita no meio de uma sessão de chat
com OAuth pendente de paste-back.

## Sequência real executada
1. Skill hermes-agent não existe neste profile; doc oficial usada direto:
   `https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp` (referência de config mcp_servers).
2. Descoberta da anatomia: krea-ai já configurado em `profiles/cmo/config.yaml` e
   `profiles/cuidar/config.yaml` (seção mcp_servers). Home do profile cmo é override
   (`~` = `/home/hermes/.hermes/profiles/cmo/home`): usar caminhos absolutos.
3. `patch` em config.yaml RECUSADO pelo guard: "Agent cannot modify security-sensitive
   configuration. Edit ~/.hermes/config.yaml directly or use 'hermes config' instead."
   Rota certa: CLI `hermes mcp add`.
4. `hermes -p cmo mcp add apify --url "https://mcp.apify.com/" --auth oauth` falhou:
   "OAuth setup failed — MCP SDK auth module not available" +
   "requires HTTP transport but mcp.client.streamable_http is not available".
   Causa raiz: pacote `mcp` ausente do venv do uv tool (extra [mcp] não instalado).
   O mesmo comando no `-p cuidar` falhou igual.
5. Diagnóstico: `uv pip show`/import falhou; METADATA do hermes_agent pinna `mcp==1.26.0`
   (extras dev/mcp/termux/all) e `pydantic==2.13.4`.
6. Fix: `uv pip install --python /home/hermes/.local/share/uv/tools/hermes-agent/bin/python "mcp==1.26.0"`
   (subiu pydantic 2.13.5 indevidamente) e repin `pydantic==2.13.4`. Sanity: `hermes --version`
   (v0.16.0) e `hermes -p cmo mcp list` ok (krea-ai enabled).
7. Relaunço do add em background pty: OAuth subiu. Output esperado:
   "MCP OAuth: authorization required. Open this URL in your browser:" +
   URL `console.apify.com/authorize/oauth?...` (scope full_api_access, resource=https://mcp.apify.com/)
   + "(Headless environment detected — open the URL manually.)" +
   "Or paste the redirect URL here (or the ?code=...&state=... portion) and press Enter. Type skip + Enter to continue".
8. Primeiro processo queimou ~2min de janela antes de mandar ao Rob: killed + relançado
   para entregar link fresco (janela de paste-back é ~5 min).

## Estado no fechamento da sessão
- Processo pty `proc_64eccfe89b31` (add no cmo) AGUARDANDO o Rob colar `?code=...&state=...`.
  URL enviada ao Rob no chat, redirect_uri `http://127.0.0.1:37131/callback`.
- Profile cuidar: add NÃO salvou (falhou antes do fix com default N em "Save config anyway?").
  Conferir `hermes -p cuidar mcp list`; refazer o add lá após o OAuth do cmo fechar.
- Pendências pós-autorização do Rob:
  1. Submeter o paste-back no pty vivo (se expirou, relançar e pedir novo authorize).
  2. `hermes -p cmo mcp test apify` + `hermes mcp configure apify` (selecionar search-actors,
     call-actor, fetch-actor-details etc.).
  3. Add no cuidar (Radar roda com profile=cuidar); se pedir OAuth de novo, checar cache
     `mcp-tokens/apify.json` nos dois homes (override do cmo).
  4. Testar se o job Radar (toolsets terminal+file) enxerga `mcp_apify_*`; plano B: CMO puxa
     via MCP e salva em `squad/radar/raw/<handle>/` para o agente analisar.
  5. Só depois de provado: ajustar playbook seção 2a (hoje assume curl+APIFY_TOKEN).
  6. Registrar tudo em PENDENTES e ativar perfis em `squad/radar/perfis.json` quando o Rob confirmar.

## Learnings fora do óbvio
- O add com OAuth salva a config ANTES de concluir o OAuth ("OAuth configured (tokens will be
  acquired on first connection)"): um add interrompido pode deixar servidor semi-configurado
  no config do perfil; conferir `mcp list`.
- Rob pediu para iniciar o OAuth IMEDIATAMENTE ("don't wait for the first tool call"):
  prática correta é mesmo assim validar a receita antes (a 1ª tentativa dele iria expirar
  com o pacote quebrado; 2 min de setup economizaram 5 min de link morto).
- A instrução do fornecedor "never ask me to paste a token into this chat" é respeitável;
  no paste-back o que transita é o code de autorização (uso único, amarrado ao processo),
  não o token: explicar ao Rob por que é seguro.

## Rodada 2: o massacre do timeout de 40s (14/09, mesmo dia)
O Rob colou o callback URL a tempo, mas a troca do código por token NÃO aconteceu:
1. Evidência no pty: `✗ Failed to connect: MCP call timed out after 40.6s (configured timeout: 40.0s)`
   disparou ~40s depois do prompt de OAuth, ANTES do paste. O paste chegou depois e foi
   parcialmente comida pelo prompt "Save config anyway? [y/N]" (o paste watcher imprimiu
   "Got authorization code from paste — completing flow.", mas nada foi trocado).
2. Disco contou a verdade: só `profiles/cmo/mcp-tokens/apify.client.json` (243 bytes:
   redirect_uris/client_id/grant_types = registro do client, SEM access_token).
3. Fixes aplicados e validados como sintaxe ok:
   - `hermes -p cmo config set mcp_servers.apify.timeout 300`
   - `hermes -p cmo config set mcp_servers.apify.connect_timeout 300`
   - `rm profiles/cmo/mcp-tokens/apify.client.json` (amarrado à porta morta 49757)
   - relanço com `hermes -p cmo mcp login apify` (client novo CwbAOoekKQdfKA2xA, porta 60655,
     janela cheia de 5 min); segundo authorize enviado ao Rob (aprovação 2ª vez = 1 clique).
4. Estado final da sessão: pty do login VIVO esperando o 2º paste-back do Rob; config do cmo
   com apify enabled: true (habilitado via config set após o add salvar como disabled);
   profile cuidar ainda SEM o servidor (refazer add + login/copiar tokens lá).
Lição-chave: no paste-back headless, o inimigo não é a janela de 5 min do login, é o
timeout de 40s da tentativa de conexão.

## Rodada 3: o config NÃO cura o login; o 40s é hardcoded no CLI (14/09, mesmo dia)
Mesmo com timeout/connect_timeout 300 gravados no config do cmo, o 2º login morreu
de novo em ~40s, ANTES de qualquer paste (o Rob colou a tempo; inútil, o code de
autorização morre junto com o processo que o gerou).
1. Causa raiz real: `_probe_single_server` em `hermes_cli/mcp_config.py` (site-packages
   do venv do uv tool) usa 30+10s hardcoded; o connect_timeout do config só vale para
   tool-calls em uso normal, é IGNORADO durante o login.
2. Fix definitivo: patch no fonte (connect_timeout 30 para 300 em `_probe_single_server`)
   e relançar `hermes -p cmo mcp login apify` em background pty.
3. 3ª tentativa, pós-patch: janela FRESCA de 5 min reais, novo authorize (client novo,
   redirect_uri porta 35825), URL entregue ao Rob com instrução de colar o redirect
   inteiro da barra.
4. Estado no fechamento da sessão: pty de login VIVO (proc_8d44041c06f2) esperando o
   paste-back do Rob; token ainda não trocado; perfil cuidar segue SEM o servidor;
   Radar segue em drops manuais até as tools `mcp_apify_*` provarem funcionais numa run.
Lição final: config set = runtime; patch no probe = login. Sem os dois, o OAuth
headless morre em 40s toda vez, com ou sem paste do Rob.

## Rodada 4: fechamento, integração completa (14/09, mesmo dia)
1. Paste-back do Rob submetido no pty vivo via `process(action='submit')`: "Autenticado".
   `hermes -p cmo mcp test apify` = exit 0, 12 tools no ar.
2. Profile cuidar: servidor addado + tokens copiados; `mcp test` também 12 tools.
3. Job do Radar atualizado com toolset `mcp-apify` (enabled_toolsets terminal+file+mcp-apify).
4. Depuração de caminhos: one-shot `-z` NÃO viu as tools (reusa a sessão do daemon já viva);
   a run real pelo scheduler re-descobre MCP por run. Validado com run manual via
   `cronjob(action='run')` (o job mora na store do CMO, não na do cuidar): tools carregaram,
   1ª coleta real = 24 posts de homeangelsbrasil + nonnoapp, zero falha, digest salvo.
5. Handles verificados via actor ANTES de ativar: homeangelscanaos era handle ERRADO
   (correto: homeangelsbrasil, 21.971 seg); cuidadoresdovalejc simplesmente não existe.
6. Estado final: integração CONCLUÍDA; Apify = fonte oficial do Radar; drops = fallback.
