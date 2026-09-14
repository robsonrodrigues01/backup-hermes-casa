---
name: mcp-servidores-hermes
description: "Instalar, autenticar e manter servidores MCP remotos (HTTP/OAuth) no Hermes desta VM headless: Apify, Krea e futuros. Use quando o Rob pedir para adicionar/aplicar um MCP (ex.: 'aplique o mcp do Apify'), quando um mcp add falhar com 'streamable_http not available' ou 'MCP SDK auth module not available', quando um OAuth precisar ser completado sem navegador na VM (paste-back), ou para testar/auditar servidores MCP já configurados."
metadata:
  version: 1.0.0
---

# MCP remoto no Hermes (VM headless)

Receita para plugar servidores MCP externos (URL + OAuth) no Hermes que roda nesta VM.
Fatos do ambiente que mudam como se instala (verificar antes de improvisar):

## Anatomia da instalação local
- Hermes é um **uv tool**: venv em `/home/hermes/.local/share/uv/tools/hermes-agent/`, python `.../bin/python`, site-packages em `.../lib/python3.12/site-packages`.
- Por padrão o extra `[mcp]` NÃO vem instalado: sem o pacote `mcp`, o cliente Hermes degrada (stdio/SSE embutido funciona, mas sem `streamable_http` e sem OAuth). Sintoma: `mcp add` falha com "MCP SDK auth module not available" e "mcp.client.streamable_http is not available. Upgrade the mcp package".
- Fix (14/09/2026, validado): `uv pip install --python /home/hermes/.local/share/uv/tools/hermes-agent/bin/python "mcp==1.26.0"` e DEPOIS **repinar o pydantic do Hermes**: `uv pip install --python ... "pydantic==2.13.4"`. O uv sobe pydantic (2.13.5) quebrando o pin do hermes-agent; validar com `hermes --version` + `hermes mcp list`.
- Versão correta do `mcp`: conferir o pin no METADATA do hermes (`grep Requires-Dist.*mcp .../hermes_agent-*.dist-info/METADATA`), não instalar "latest" às cegas.

## Adicionar um servidor (por perfil!)
- **NUNCA editar config.yaml com patch/write_file**: o Hermes recusa ("Agent cannot modify security-sensitive configuration"). Rota certa: `hermes -p <perfil> mcp add <nome> --url "<URL exata>" --auth oauth`.
- A config de MCP é **por perfil** (`~/.hermes/profiles/<perfil>/config.yaml`, seção `mcp_servers`): um servidor usado por agentes de N perfis precisa de `mcp add` em CADA perfil (ex.: cmo e cuidar).
- Pegadinha de add sem TTY: em falha ele pergunta "Save config anyway? [y/N]" e o default N NÃO salva. Após qualquer add com erro, conferir com `hermes -p <perfil> mcp list` antes de presumir que salvou.
- Manter a URL exatamente como o fornecedor manda (query params selecionam tools/actors; ex. Apify: `https://mcp.apify.com/`).

## OAuth headless (paste-back), o fluxo completo
A VM não tem navegador; o dono (Rob) autoriza no navegador DELE e cola o resultado de volta no chat.
0. **ANTES de iniciar qualquer OAuth, dois fixes de timeout DIFERENTES**:
   - Config do perfil (sempre fazer): `hermes -p <perfil> config set mcp_servers.<nome>.timeout 300` e `hermes -p <perfil> config set mcp_servers.<nome>.connect_timeout 300`. Vale para tool-calls de uso normal.
   - Patch no probe do CLI (obrigatório para o login): o `hermes mcp login` NÃO lê esses valores. O probe interno (`_probe_single_server`, arquivo `hermes_cli/mcp_config.py` no site-packages do venv do uv tool, ver Anatomia) tem 40s HARDCODED (30+10) e é ele que mata o OAuth em ~40s com o Rob a caminho (evidência 14/09: 2ª tentativa morreu em 40.6s com config 300 já gravado; 3ª, após patch 30 para 300 no fonte, entregou janela cheia de 5 min).
   Para a rodada de autenticação usar `hermes -p <perfil> mcp login <nome>` (espera os 5 min inteiros); o `mcp add` serve para gravar a config.
1. Rodar o add/login em terminal background COM pty (`terminal background=true pty=true`), ex.: `hermes -p cmo mcp add apify --url "https://mcp.apify.com/" --auth oauth` seguido de `hermes -p cmo mcp login apify`.
2. `process(action='poll')` até aparecer "MCP OAuth: authorization required" com a URL de autorização.
3. A janela de espera do paste-back é curta (~5 min). Se o processo já queimou mais de ~2 min, **matar e relançar** para entregar link fresco, e mandar a URL ao Rob imediatamente com as instruções: autorizar, cair na página localhost que não carrega (esperado), copiar a URL inteira da barra (ou só `?code=...&state=...`) e colar no chat.
4. O que o Rob cola é o CÓDIGO de autorização (curto, uso único, amarrado ao PKCE do processo vivo), não um token: seguro pro chat. Enviar via `process(action='submit')` no pty que espera.
5. Sucesso = arquivo de TOKEN em disco (com access_token). ATENÇÃO: `<nome>.client.json` NÃO é token, é só o registro do OAuth client (redirect_uris, client_id, grant_types, ~250 bytes). Se um fluxo morrer no meio: rm o client.json velho ANTES de relançar, porque ele fica amarrado à callback port antiga e o fluxo novo registra redirect_uri diferente (risco de mismatch). Se o Rob demorar e a janela expirar, relançar e pedir novo authorize (aprovação 2ª vez é 1 clique).

## Token cache e segundo perfil
- Local CONFIRMADO (14/09): `~/.hermes/profiles/<perfil>/mcp-tokens/` (por perfil, direto na raiz do perfil, FORA do home/ override). Ex.: `/home/hermes/.hermes/profiles/cmo/mcp-tokens/apify.client.json`.
- Para o 2º perfil pode ser preciso novo login OU copiar os arquivos de mcp-tokens pro diretório do outro perfil; testar com `hermes -p <perfil2> mcp test <nome>` antes de conectar agentes.
- NUNCA logar/imprimir conteúdo do token file; se precisar citar, redact.

## Pós-instalação e verificação
- `hermes -p <perfil> mcp test <nome>`: conexão ok.
- `hermes mcp configure <nome>`: checklist interativo de seleção de tools (pty).
- Tools aparecem como `mcp_<server>_<tool>` (ex.: `mcp_apify_call-actor`).
- Sessão EM CURSO pode não registrar as tools novas de imediato (auto-reload de config ~30s, insuficiente pra OAuth: doc manda OAuth sempre em terminal novo). Descoberta de MCP POR CAMINHO (validado 14/09 com Apify + Radar): runs do scheduler (agendada ou `cron run`) re-descobrem MCP a cada run e PEGAM as tools; o one-shot `-z` reaproveita a sessão do daemon já viva e NÃO re-descobre (um teste `-z` sem tools MCP NÃO prova que o cron job não vai tê-las). Validar sempre com run real pelo cron + ler o output. Nunca afirmar "tools disponíveis" sem evidência de execução.
- SSO dashboard/CLI do hermes: `hermes -p <perfil> mcp list` mostra nome, transporte, tools e status por perfil.

## Pitfalls
- **Timeout de 40s é o assassino silencioso do paste-back**: o OAuth vai parecer que funcionou (client.json é gravado, o paste watcher até imprime "Got authorization code from paste — completing flow.") e AINDA ASSIM morre sem trocar o código por token. Na autenticação o 40s vem do probe HARDCODED do `mcp login`: config set NÃO cura, é preciso patchar `_probe_single_server` em `hermes_cli/mcp_config.py` (30 para 300). Qualquer `MCP call timed out` no pty = janela morta: colar depois disso não serve (o code morre com o processo), matar, confirmar o patch do probe e relançar com novo authorize.
- **Upgrade do hermes-agent (uv tool) reinstala o venv e APAGA o patch do probe**: após qualquer upgrade, conferir `_probe_single_server` no `hermes_cli/mcp_config.py` (ex.: grep -n connect_timeout) e reaplicar 30 para 300 antes de qualquer novo login.
- **`mcp add` cuja conexão falha salva o servidor como (disabled)**: após consertar, habilitar com `hermes -p <perfil> config set mcp_servers.<nome>.enabled true` e só então `mcp test`.
- A linha colada pelo Rob pode ser comida por um prompt pendente no pty ("Save config anyway? [y/N]") em vez de chegar ao paste watcher: depois de qualquer timeout, responder o prompt com y/n explícito e refazer o fluxo de login, não colar o código num processo moribundo.
- Repinar pydantic após instalar o `mcp` (o uv resolve para frente e fura o pin do hermes-agent; um patch release de pydantic pode quebrar o hermes inteiro).
- OAuth dentro de sessão Hermes rodante = corrida de reload (30s não basta); sempre `mcp add`/`mcp login` em processo separado (background pty).
- Servidor salvo só no cmo mas o agente que precisa roda em outro perfil (Radar roda com profile=cuidar): sem add no cuidar, o agente nunca vê as tools.
- Cron job só enxerga `mcp_<server>_*` se o toolset do servidor estiver no `enabled_toolsets` do job (ex.: `mcp-apify`): sem ele NÃO há tools, mesmo com o servidor instalado no perfil. Fix = adicionar o toolset ao job (cronjob update); só se o toolset não resolver, plano B = CMO puxa via MCP e salva em arquivo pro agente ler (padrão drop/raw). Validado 14/09: Radar com `mcp-apify` carregou as tools na run cron real.
- Não reinstalar/upgradar o `mcp` sem checar o pin do hermes-agent METADATA (versões futuras podem mudar o pin).

## Referências
- `references/apify-instalacao-14-09.md`: episódio completo do Apify MCP (erros, comandos, OAuth paste-back em 4 rodadas, add no 2º perfil e validação no Radar com a 1ª coleta real).
